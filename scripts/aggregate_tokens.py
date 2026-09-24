#!/usr/bin/env python3
"""Aggregate archived Claude message usage, deduplicated within each run.

Usage: python3 scripts/aggregate_tokens.py [--json] <run-log-dir> [...]
Each directory is ONE run. Only top-level *.jsonl files are included.
Codex cumulative usage and conflicting streaming snapshots are rejected.
The token proxy is input + output + cache creation, NOT billed cost.
"""
import argparse
import json
from pathlib import Path

FIELDS = ['input_tokens', 'output_tokens', 'cache_creation_input_tokens',
          'cache_read_input_tokens']
VERSION = 2


def aggregate(log_dir: Path) -> dict:
    files = sorted(log_dir.glob('*.jsonl'))
    if not files:
        raise ValueError(f'No JSONL files: {log_dir}')
    seen = {}
    missing = set()
    duplicates = rows = 0
    for path in files:
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f'{path}:{number}: invalid JSON') from error
            if not isinstance(record, dict):
                raise ValueError(f'{path}:{number}: expected object')
            payload = record.get('payload')
            if (record.get('type') in ('event_msg', 'response_item', 'session_meta')
                    or isinstance(payload, dict) and payload.get('type') == 'token_count'):
                raise ValueError(f'{path}:{number}: unsupported cumulative/Codex format')
            if record.get('type') != 'assistant':
                continue
            message = record.get('message')
            if not isinstance(message, dict) or not isinstance(message.get('id'), str) or not message['id']:
                raise ValueError(f'{path}:{number}: assistant message ID missing')
            mid = message['id']
            usage = message.get('usage')
            if usage is None or usage == {}:
                missing.add(mid)
                continue
            if not isinstance(usage, dict):
                raise ValueError(f'{path}:{number}: invalid usage')
            for field in FIELDS:
                value = usage.get(field)
                if value is not None and (type(value) is not int or value < 0):
                    raise ValueError(f'{path}:{number}: invalid {field}')
            rows += 1
            if mid in seen:
                if seen[mid] != usage:
                    raise ValueError(f'{path}:{number}: conflicting usage for {mid}; resolve provider semantics first')
                duplicates += 1
            else:
                seen[mid] = usage
    missing -= seen.keys()
    if not seen and not missing:
        raise ValueError(f'No assistant usage/messages: {log_dir}')
    totals = {}
    for field in FIELDS:
        values = [usage.get(field) for usage in seen.values()]
        totals[field] = (sum(values) if values and not missing
                         and all(value is not None for value in values) else None)
    proxy = [totals[field] for field in FIELDS[:3]]
    totals.update(
        token_proxy=sum(proxy) if all(value is not None for value in proxy) else None,
        sessions=len(files), messages=len(seen), usage_rows=rows,
        duplicates=duplicates, missing_usage=len(missing),
        missing_fields={field: sum(usage.get(field) is None for usage in seen.values())
                        for field in FIELDS},
    )
    return totals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='machine-readable output')
    parser.add_argument('directories', nargs='+', type=Path)
    args = parser.parse_args()
    results = {}
    try:
        for directory in args.directories:
            if not directory.is_dir():
                raise ValueError(f'Not a directory: {directory}')
            results[str(directory)] = aggregate(directory)
    except ValueError as error:
        parser.exit(2, f'error: {error}\n')
    if args.json:
        print(json.dumps({'aggregator_version': VERSION, 'format': 'claude-message-usage',
                          'scope': 'one directory per run; top-level JSONL only',
                          'results': results}, ensure_ascii=False, indent=2))
    else:
        for name, result in results.items():
            print(name)
            for key in ['sessions', 'messages', 'usage_rows', 'duplicates', 'missing_usage', *FIELDS, 'token_proxy']:
                value = result[key]
                print(f'  {key}: {value:,}' if value is not None else f'  {key}: unmeasured')
        print('token_proxy = input + output + cache creation; not billed cost')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
