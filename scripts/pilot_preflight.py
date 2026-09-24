#!/usr/bin/env python3
"""Offline smoke inspection and balanced pilot scheduling; never launches agents.

python3 scripts/pilot_preflight.py experiments/024-practical-combinations/manifest.json
Exit 2 means blocked/incomplete Phase 0, not failed benchmark performance.
"""
import json
import random
import sys
from pathlib import Path


def complete_counts(usage, fields):
    return isinstance(usage, dict) and all(
        type(usage.get(field)) is int and usage[field] >= 0 for field in fields
    )


def inspect_claude(events, requested_model):
    reasons = set()
    models = set()
    results = []
    for event in events:
        message = event.get('message') or {}
        if event.get('type') == 'assistant' and message.get('model'):
            models.add(message['model'])
        if 'fallback' in event.get('subtype', '') or any(
            part.get('type') == 'fallback' for part in message.get('content', [])
            if isinstance(part, dict)
        ):
            reasons.add('provider_model_fallback')
        if event.get('type') == 'rate_limit_event':
            rate = event.get('rate_limit_info', {})
            if rate.get('isUsingOverage'):
                reasons.add('subscription_overage')
            if rate.get('status') == 'rejected':
                reasons.add('subscription_limit')
        if event.get('type') == 'result':
            results.append(event)
            models.update(event.get('modelUsage', {}))
    if not models or models != {requested_model}:
        reasons.add('model_mismatch')
    if len(results) != 1 or results[0].get('is_error') is not False:
        reasons.add('missing_or_failed_result')
    elif not complete_counts(results[0].get('usage'), ('input_tokens', 'output_tokens')) or not complete_counts(
        results[0].get('modelUsage', {}).get(requested_model), ('inputTokens', 'outputTokens')
    ):
        reasons.add('missing_usage')
    return {'eligible': not reasons, 'observed_models': sorted(models),
            'reasons': sorted(reasons)}


def schedule(tasks, conditions, repetitions, seed):
    if len(conditions) != 2 or len(set(conditions)) != 2 or repetitions < 1:
        raise ValueError('Exactly two distinct conditions and positive repetitions required')
    rng = random.Random(seed)
    blocks = [(task, repeat) for repeat in range(1, repetitions + 1) for task in tasks]
    rng.shuffle(blocks)
    # Balanced first positions across blocks, while retaining paired task comparisons.
    firsts = [index % 2 for index in range(len(blocks))]
    rng.shuffle(firsts)
    runs = []
    for block, ((task, repeat), first) in enumerate(zip(blocks, firsts), 1):
        for condition in (conditions[first], conditions[1-first]):
            runs.append({'run_id': f'{task}-{condition}-{repeat}', 'block': block,
                         'task': task, 'condition': condition, 'repeat': repeat})
    return runs


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    manifest = json.loads(path.read_text())
    smoke = json.loads((path.parent / manifest['smoke_record']).read_text())
    checks = {}
    for condition in manifest['conditions']:
        entry = next((row for row in smoke['conditions'] if row['condition'] == condition['id']), None)
        if not entry or entry.get('exit_code') != 0:
            checks[condition['id']] = {'eligible': False, 'reasons': ['missing_or_failed_smoke']}
        elif condition['harness'] == 'claude':
            checks[condition['id']] = inspect_claude(json.loads(entry['stdout']), condition['model'])
        else:
            # CLI's compact stdout lacks served model identity. Do not call it verified.
            events = [json.loads(line) for line in entry['stdout'].splitlines() if line.strip()]
            complete = any(row.get('type') == 'turn.completed' and row.get('usage') for row in events)
            checks[condition['id']] = {'eligible': False, 'response_received': complete,
                                      'reasons': ['served_model_identity_unverified']}
    blockers = list(manifest['remaining_gates'])
    ready = all(check['eligible'] for check in checks.values()) and not blockers
    print(json.dumps({'ready': ready, 'conditions': checks, 'remaining_gates': blockers}, indent=2))
    return 0 if ready else 2


if __name__ == '__main__':
    raise SystemExit(main())
