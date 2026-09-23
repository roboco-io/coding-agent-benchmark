# Usage audit: 61 dashboard runs (2026-09-23)

Scripts: `agg_claude.py`, `agg_codex.py`, `build.py` (same folder). I matched each run to the dashboard `M` array by per-run output tokens. All 61 runs match the dashboard's rounded output values exactly.

## Per-experiment sources

| Exp | Raw source | Existing CSV | Method |
|---|---|---|---|
| 009, 010 | `experiments/0NN/runs/*/logs/*.jsonl` (archived in the repo) | none | reaggregated |
| 019 Opus | raw purged: `~/.claude/projects` is cleaned after 30 days | `runs/usage-opus.csv` | report_value |
| 023, 026 | `~/.claude/projects/-Users-dohyunjung-ralph-exp0NN-app-*` | usage.csv | csv_verified |
| 013/014/016/017 (qwen, kimi), 015, 025 | `~/ralph-exp0NN*/claude-config-projects-<run>` | per-run CSV | csv_verified, except qwen-ko-1 and qwen-ko-3 |
| 020 | `~/ralph-exp020/claude-config-projects-pro4-N` | none | reaggregated |
| 011/016/019/021 Codex | `~/ralph-exp0NN/codex-sessions-<run>` | per-run CSV | csv_verified, except sol-1 |

## Deduplication and conflicts

- **Existing CSVs**: the archived `parse_usage.py`/`usage0NN.py` scripts deduplicate by message.id and keep the last row for each ID. They do not check whether rows with the same ID carry different usage. I re-aggregated all raw logs with conflict detection.
- **Streaming conflicts (qwen, Solar)**: some IDs have two rows. The earlier row is preliminary: it has output=0, no `cache_creation` object, and an estimated input. The later row is complete. I kept the complete row only when this exact pattern held. No conflicts remained unresolved.
- **qwen-ko-1 and qwen-ko-3**: 1 and 2 IDs have only a preliminary row, so their final usage is unknown. I excluded them. Their input estimates are 20,886 and 46,621. The existing CSVs include these estimates, which inflates their uncached input about 8x and 14x.
- **gpt-5.6-sol sol-1**: the existing CSV includes a pre-run smoke session that returned "OK". I excluded it.

## Semantics

- **Claude-format rows**: `input_tokens` is uncached input. Cache read and cache write are separate fields.
  - EXP-009/010/023/026 wrote all cache at the 1h TTL.
  - qwen reported only 5m cache writes.
  - kimi, DeepSeek and Solar reported cache writes as 0. Solar also reported cache reads as 0. These zeros come from the provider and are not verified against billing.
- **Reasoning in output**:
  - Anthropic models: `output_tokens` includes thinking. `thinking_tokens` is a subset and appears in the notes.
  - Third-party models: I estimated tokens as characters/4. Output tokens roughly equal (thinking + visible)/4, not visible/4 alone. So I marked reasoning as included, based on this heuristic.
- **Codex**:
  - `total_token_usage` is cumulative per session. I verified that it equals the sum of `last_token_usage` and that no duplicate events exist.
  - `total = input + output`, so `cached_input_tokens` is a subset of input. Uncached input = input − cached.
  - `reasoning_output_tokens` is a subset of output.
  - gpt-5.6-sol rollouts have no cache-write field (null). astra reports 0.
- **Cache-write columns**: `cache_write_unsplit` is filled only when the 5m/1h split is missing. Never add it to the split columns.

## Scope decisions and gaps

- **Opus 4.8 48-1**: includes the iteration-2 re-verification session. This matches the dashboard's 37.1K output, but the dashboard time covers iteration 1 only.
- **Solar Open 2**: includes 2 subagent transcripts and the aborted iteration-3 session (17 requests).
- **Solar Pro 4**: includes all 12 sessions of pro4-1 (iterations 3–11 were false gate rejections) and the subagents of pro4-2.
- **EXP-019 Opus (6 runs)**: the 5m/1h split, request count and conflict handling cannot be verified.
- **Time**: `time_min` is copied from the dashboard.
