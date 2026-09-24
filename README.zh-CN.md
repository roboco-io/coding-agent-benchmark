# Vibecoding Token Experiments

🌐 [English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · **中文**

本项目比较**使用 Ralph 循环的模型与执行框架组合的后端实现性能**，目标是根据任务、质量和预算选择实用组合。最初的策略对比保留为研究历史。

## 实验方法论

- 比较单位：**模型 × 执行框架 × 推理设置 × 提供方与连接环境**，涵盖 Claude Code 和 Codex。组合差异不等于模型的独立效果。
- 基本任务：[RealWorld 后端](tasks/realworld-backend/)。计划扩展至现有代码的缺陷修复、功能添加和数据库迁移。
- 主要指标：**预算内通过率、含失败的成本、时间及人工介入量**。token 是诊断指标，不等于计费成本。
- [质量规则](docs/experiment-quality-rules.md)、[更正记录](docs/2026-09-21-corrections.md)、[路线图](ROADMAP.md)。
- 下一轮试验：Claude Code + Fable 5.1 对比 Codex + Astra。[设计](experiments/024-practical-combinations/README.md)。

## 研究维度

优先比较模型与框架组合以及任务类型。策略(S)、token 习惯(H)、语言(L)作为诊断维度保留在[目录](hypotheses/catalog.md)中。

## 实验结果

> 下表与各实验摘要由 [`scripts/update_readme_results.py`](scripts/update_readme_results.py) 根据各实验的 `report.md` 自动生成（英·日·中 README 使用 [`scripts/readme_i18n.json`](scripts/readme_i18n.json) 中的翻译）。实验结束提交 `report.md` 时，pre-commit 钩子会自动执行（手动执行：`python3 scripts/update_readme_results.py`）。

**📊 实时仪表板**：[Ralph 循环各模型完成率对比](https://roboco.io/coding-agent-benchmark/) —— 最新实验：EXP-029（2026-09-24）

> 外部仪表板尚未反映2026-09-21更正。数值判断请参考下方报告及更正记录。

<!-- RESULTS:BEGIN -->
<!-- 此区块由 scripts/update_readme_results.py 根据 experiments/*/report.md 自动生成（翻译来自 scripts/readme_i18n.json）。请勿手动编辑。 -->

| 实验 | 假设 | 判定 |
|------|------|------|
| [EXP-001](experiments/001-ralph-vs-plan-then-execute/report.md) Ralph 循环 vs Plan-then-execute | S-01: Plan-then-execute 在同一任务上比 Ralph 循环使用更少 token | **在观测范围内否定** |
| [EXP-002](experiments/002-korean-vs-english/report.md) 韩文 vs 英文流水线 token 比较 | L-01: 全流程用英文进行可比韩文显著减少 token proxy token | **保留** |
| [EXP-003](experiments/003-pte-skills/report.md) PTE + 技能式渐进披露 | S-02: 按技能官方建议（文档不超过 200 行、通过技能只加载所需内容）组织上下文，可比 EXP-001 的 PTE 减少 30% 以上 token proxy | **未达标准（更正）** |
| [EXP-004](experiments/004-ralph-skills/report.md) Ralph 循环 + 技能结构 | S-03: 为单会话 ralph 提供领域契约技能可减少 token proxy | **保留** |
| [EXP-005](experiments/005-solar-pro3-backend/report.md) Claude Code × Upstage Solar Pro 3 后端 | M-01: 将 Claude Code 后端替换为 Solar Pro 3 后可无人干预完成同一任务（RealWorld 后端），且完成时总成本显著低于 Opus。 | **保留** |
| [EXP-006](experiments/006-solar-open2-backend/report.md) Claude Code × Upstage Solar Open 2 后端 | M-02: 将 Claude Code 后端替换为 Solar Open 2 后可无人干预完成同一任务（RealWorld 后端），且完成时总成本显著低于 Opus。 | **保留** |
| [EXP-007](experiments/007-solar-open2-autopsy/report.md) Solar Open 2 未完成原因剖析 | M-03: EXP-006（Solar Open 2）未完成不是收敛速度这一单一瓶颈，而是多重失败因素（模型行为缺陷·实验环境污染·计量失真）的叠加。 | **验证** |
| [EXP-008](experiments/008-solar-open2-clean-run/report.md) Solar Open 2 无污染干净 run——完成验证 | M-04: 在去除污染（隔离配置）·无干扰·上限 30 iter 的条件下，solar-open2 能以 Ralph 循环无人干预完成 RealWorld 后端（Hurl 154/154）（排除计费，仅判定是否完成）。 | **验证** |
| [EXP-009](experiments/009-opus5-ralph-en/report.md) Opus 5 Ralph 循环（EXP-002 en 条件，n=3） | M-05: Opus 5 在 EXP-002 en 条件的 Ralph 循环中复现单会话完成，且效率不低于 Opus 4.x 基线（en 6–7 分钟·API 38–54 次）。 | **部分验证（n=3）** |
| [EXP-010](experiments/010-opus48-vs-opus5/report.md) Opus 4.8 vs Opus 5 纯 A/B（同时点，各 n=3） | M-06: 在完全相同条件下，Opus 5 的输出量扩大特征（output·提交 ↑）相对 Opus 4.8 可复现，且两模型均保持单会话完成。 | **验证** |
| [EXP-011](experiments/011-codex-gpt56-sol/report.md) Codex CLI × gpt-5.6-sol RealWorld 后端完成验证 | M-07: 在 Codex CLI（`codex exec`）框架中，gpt-5.6-sol（effort medium）能在隔离·无干扰的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）。 | **验证** |
| [EXP-012](experiments/012-ccr-gpt56-sol/report.md) Claude Code × gpt-5.6-sol 后端（ccr）RealWorld 后端完成验证 | M-08: 通过 ccr 将 Claude Code 后端连接到 gpt-5.6-sol（reasoning effort medium）后，能在隔离·无干扰的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）。 | **验证** |
| [EXP-013](experiments/013-qwen38max-direct/report.md) Claude Code × qwen3.8-max 直连（ANTHROPIC_BASE_URL）RealWorld 后端完成验证 | M-09: 通过 DashScope 的 Anthropic 兼容端点将 Claude Code 直连到 qwen3.8-max（thinking 默认）后，能在隔离·无干扰的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）。 | **验证** |
| [EXP-014](experiments/014-kimi-k3-direct/report.md) Claude Code × kimi-k3 直连（ANTHROPIC_BASE_URL）RealWorld 后端完成验证 | M-10: 通过 Moonshot 的 Anthropic 兼容端点将 Claude Code 直连到 kimi-k3（thinking 默认）后，能在隔离·无干预的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）。 | **验证** |
| [EXP-015](experiments/015-solar-open2-direct/report.md) Claude Code × solar-open2 直连（ANTHROPIC_BASE_URL）RealWorld 后端完成验证 | M-11: 通过 Upstage 的 Anthropic 兼容端点将 Claude Code 直连到 solar-open2（thinking 默认）后，能在隔离·无干扰的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）。 | **验证** |
| [EXP-016](experiments/016-n3-replication/report.md) 3 种 n=1 完成条件的可复现性扩充（各 n=3） | M-12: EXP-011/013/014 三个条件（Codex CLI × gpt-5.6-sol、qwen3.8-max 直连、kimi-k3 直连）的无人干预完成可复现：每个条件追加 2 个 run（共 n=3）均在上限 30 iteration 内以门控+独立复验一致完成。 | **验证** |
| [EXP-017](experiments/017-ko-condition/report.md) qwen3.8-max·kimi-k3 韩文条件 Ralph 循环完成验证（各 n=3） | L-02: qwen3.8-max·kimi-k3（直连，thinking 默认）在韩文标准提示词（含全部产出用韩文的指示）条件下也能在隔离·无干扰的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）。 | **验证** |
| [EXP-018](experiments/018-solar-n3-replication/report.md) solar-open2 直连可复现性扩充——提供商端点下线导致无法复现 | M-13: EXP-015 的 solar-open2 直连无人干预完成可复现：追加 2 个 run（共 n=3）均在 30 iteration 内通过门控（measure v4）+复验完成。 | **保留** |
| [EXP-019](experiments/019-ko-native-codex/report.md) 原生 Opus 4.8·Opus 5·Codex×gpt-5.6-sol 韩文条件完成验证（各 n=3） | L-03: 原生 Opus 4.8·Opus 5（Claude Code）与 gpt-5.6-sol（Codex CLI）在韩文标准提示词（含全部产出用韩文的指示）条件下也能在隔离·无干扰的 Ralph 循环中于上限 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）。 | **验证** |
| [EXP-020](experiments/020-solar-pro4-direct/report.md) Claude Code × solar-pro4 直连完成验证（n=3） | M-14: 通过 Upstage 的 Anthropic 兼容端点将 Claude Code 直连到 solar-pro4（thinking 默认）后，能在隔离·无干扰的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）（n=3，完成率判定·排除计费）。 | **验证** |
| [EXP-021](experiments/021-gpt6-astra-codex/report.md) Codex CLI × gpt-6-astra Ralph 循环完成验证（n=3） | M-15: 在 Codex CLI（`codex exec`）框架中，gpt-6-astra（effort medium）能在隔离·无干扰的 Ralph 循环中于上限 30 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）（n=3，完成率判定·排除计费）。 | **验证** |
| [EXP-023](experiments/023-fable51-ralph/report.md) Claude Code × Fable 5.1 原生 Ralph 循环完成验证（n=3） | M-17: 在 Claude Code 原生框架中，Fable 5.1（`claude-fable-5-1`，thinking 默认）能以 EN 标准 Ralph 循环在上限 10 iteration 内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）（n=3，完成率判定·排除计费）。 | **验证** |
| [EXP-025](experiments/025-deepseek-direct/report.md) Claude Code × DeepSeek V4.1-Flash·V4-Pro 直连 Ralph 循环完成验证（EN·KO 各 n=3） | M-18: 通过 DeepSeek 的 Anthropic 兼容端点将 Claude Code 直连到 `deepseek-flash`（DeepSeek-V4.1-Flash）和 `deepseek-v4-pro`（DeepSeek-V4-Pro-0813）（thinking 默认）后，能在隔离·无干扰的 Ralph 循环中于上限 30 iteration·4 小时内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）（EN·KO 标准版各 n=3，完成率判定·排除计费）。 | **验证** |
| [EXP-026](experiments/026-opus55-ralph/report.md) Claude Code × Opus 5.5 原生 Ralph 循环完成验证（EN·KO 各 n=3） | M-19: 在 Claude Code 原生框架中，Opus 5.5（`claude-opus-5-5`，thinking 默认）使用 EN 与 KO 标准版提示的 Ralph 循环，能在上限 10 iteration·4 小时内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）（EN·KO 各 n=3，完成率判定·排除计费）。 | **验证** |
| [EXP-027](experiments/027-gpt6-sol-luna-codex/report.md) Codex CLI × gpt-6-sol·gpt-6-luna Ralph 循环完成验证（各 n=3） | M-20: 在 Codex CLI（`codex exec`）框架中，gpt-6-sol 与 gpt-6-luna（effort medium）各自能在隔离、无人干预的 Ralph 循环中于上限 30 iteration·4 小时内完成 RealWorld 后端（Hurl 13/13·154/154）（各 n=3）。 | **验证** |
| [EXP-028](experiments/028-sonnet5-ralph/report.md) Claude Code × Sonnet 5 原生 Ralph 循环完成验证（EN·KO 各 n=3） | M-21: 在 Claude Code 原生框架中，Sonnet 5（`claude-sonnet-5`，默认 thinking）能以 EN·KO 正本 Ralph 循环提示在上限 10 iteration·4 小时内无人干预完成 RealWorld 后端（Hurl 13/13·154/154）（EN·KO 各 n=3）。 | **验证** |
| [EXP-029](experiments/029-pi-openweight/report.md) pi coding agent × kimi-k3·qwen3.8-max·deepseek-flash Ralph 循环完成验证（EN 各 n=3） | M-22: 将 pi coding agent（`pi -p` v0.87.1）直连各提供方的 OpenAI 兼容端点运行 `kimi-k3`·`qwen3.8-max`·`deepseek-flash`（thinking 为 pi 默认值），能在隔离·无人干预的 Ralph 循环中于上限 30 iteration·4 小时内完成 RealWorld 后端（Hurl 13/13·154/154）（EN 各 n=3，按完成率判定，不含计费）。 | **验证** |

**EXP-001 — Ralph 循环 vs Plan-then-execute** (在观测范围内否定)  
去重后的 token 代理指标：PTE 1,128,420，Ralph 136,506（8.27倍）。评分集不同，不能作为同等质量的成本比较。 → [报告](experiments/001-ralph-vs-plan-then-execute/report.md)

**EXP-002 — 韩文 vs 英文流水线 token 比较** (保留)  
KO均值114,605.5，EN均值112,463.5。均值差2,142低于条件内最大范围23,033。 → [报告](experiments/002-korean-vs-english/report.md)

**EXP-003 — PTE + 技能式渐进披露** (未达标准（更正）)  
token 代理指标下降22.45%（1,128,420 → 875,083），未达预设30%标准，撤回已验证判定。 → [报告](experiments/003-pte-skills/report.md)

**EXP-004 — Ralph 循环 + 技能结构** (保留)  
技能run为117,352 / 118,311，相对KO基线均值+2.81%。范围为959，撤回无效果及两倍波动的结论。 → [报告](experiments/004-ralph-skills/report.md)

**EXP-005 — Claude Code × Upstage Solar Pro 3 后端** (保留)  
solar-1 未完成（测试执行 0 次·提交 0 次，在 iteration 6/15 时提前中止）：集成栈已验证，但在 headless 自主循环中反复出现等待许可·上下文超限的失败模式，未能进入完成轨道。 → [报告](experiments/005-solar-pro3-backend/report.md)

**EXP-006 — Claude Code × Upstage Solar Open 2 后端** (保留)  
0/2 完成，但完整协议的 run 只有 1 次（open2-1 在 1 个 iteration 后以虚假完成申报自行终止）：open2-2 用尽 15 个 iteration 仍只达到独立验证 3/13 文件（94/154 请求），但建立了 solar-pro3 所缺的自主 TDD 循环并单调收敛，“行为层”瓶颈从自主性转移到收敛速度。 → [报告](experiments/006-solar-open2-backend/report.md)

**EXP-007 — Solar Open 2 未完成原因剖析** (验证)  
证实三层：① 计量失真（usage 高估 3.07 倍——实际 483 个请求·23.3M input，估算约 $3.8，低于 Opus 的 $6.41），② 环境污染（superpowers 钩子·全局 CLAUDE.md 注入至少侵蚀 3 个 iteration），③ 模型行为缺陷（只声明不执行导致提交 0 次、thinking-only 截断 25 次、偏离任务的幻觉 2 起）。 → [报告](experiments/007-solar-open2-autopsy/report.md)

**EXP-008 — Solar Open 2 无污染干净 run——完成验证** (验证)  
**在 iteration 10/30 完成**：生成 `.ralph-done` → 通过框架门控 13/13 文件·154/154 请求 → 实验者 2 次独立复验一致。wall-clock 约 2 小时 53 分，无干预·无中断，完成 git 提交 4 次（韩文）。完成点在 EXP-006 的上限（15）之内，因此决定变量是**去除环境污染·无干扰**而非提高上限。 → [报告](experiments/008-solar-open2-clean-run/report.md)

**EXP-009 — Opus 5 Ralph 循环（EXP-002 en 条件，n=3）** (部分验证（n=3）)  
完成条款已验证：**3/3 run 均在 iteration 1 单会话完成**（9 分 03 秒–12 分 22 秒，门控 13/13·154/154 + 各 2 次独立复验，提交 6–7 次）。效率条款确认未达成：时间分布（8.9–12.2 分钟）与 4.x（5.8–6.9 分钟）不重叠——但原因不是服务速度，而是**伴随一致输出量增加（+62%）的行为特征变化**。 → [报告](experiments/009-opus5-ralph-en/report.md)

**EXP-010 — Opus 4.8 vs Opus 5 纯 A/B（同时点，各 n=3）** (验证)  
完成 6/6（所有 run 均在 iteration 1，门控 13/13·154/154）。预先登记指标全部满足：**output token 分布不重叠**（4.8：29.6–37.1K vs 5：41.1–47.9K，均值 +37%）·**git 提交分布不重叠**（1–2 次 vs 4–8 次），方向与 EXP-009 相同（5 > 4.8）。世代差异是真实存在的特征，而非时点·计量伪影。 → [报告](experiments/010-opus48-vs-opus5/report.md)

**EXP-011 — Codex CLI × gpt-5.6-sol RealWorld 后端完成验证** (验证)  
**在 iteration 1 完成**（门控 13/13·154/154 + 2 次独立复验一致，codex exec 5 分 46 秒·1 个会话·提交 3 次，无干预）。 → [报告](experiments/011-codex-gpt56-sol/report.md)

**EXP-012 — Claude Code × gpt-5.6-sol 后端（ccr）RealWorld 后端完成验证** (验证)  
**在 iteration 11/30 完成**（门控 13/13·154/154 + 2 次独立复验一致，共 58 分钟·提交 11 次）。但 iteration 2 出现 1 次流停滞并进行了框架级干预（终止进程以恢复 iteration 边界，未干预模型产出）——见下文协议问题。 → [报告](experiments/012-ccr-gpt56-sol/report.md)

**EXP-013 — Claude Code × qwen3.8-max 直连（ANTHROPIC_BASE_URL）RealWorld 后端完成验证** (验证)  
**在 iteration 1 完成**（门控 13/13·154/154 + 2 次独立复验一致，15 分 5 秒·提交 4 次·干预 0，直连栈故障排查 0 起）。 → [报告](experiments/013-qwen38max-direct/report.md)

**EXP-014 — Claude Code × kimi-k3 直连（ANTHROPIC_BASE_URL）RealWorld 后端完成验证** (验证)  
**在 iteration 1 完成**（门控 13/13·154/154 + 2 次独立复验一致，21 分 18 秒·提交 4 次·干预 0，直连栈故障排查 0 起）。 → [报告](experiments/014-kimi-k3-direct/report.md)

**EXP-015 — Claude Code × solar-open2 直连（ANTHROPIC_BASE_URL）RealWorld 后端完成验证** (验证)  
**在 iteration 2 完成**（对产出直接重评 2 次均为 13/13·154/154，58 分 15 秒·提交 2 次。脚注：门控误判 1 起——measure v3 端口探测缺陷拒绝了合法完成，适用 EXP-010 48-1 先例）。 → [报告](experiments/015-solar-open2-direct/report.md)

**EXP-016 — 3 种 n=1 完成条件的可复现性扩充（各 n=3）** (验证)  
**追加的 6 个 run 全部完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，干预 0）。含原 run 在内三个条件完成率**各 3/3，合计 9/9**。 → [报告](experiments/016-n3-replication/report.md)

**EXP-017 — qwen3.8-max·kimi-k3 韩文条件 Ralph 循环完成验证（各 n=3）** (验证)  
**6/6 run 全部在 iteration 1 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，干预 0）。语言遵从也成立：所有 run 的提交信息·README 均为韩文。 → [报告](experiments/017-ko-condition/report.md)

**EXP-018 — solar-open2 直连可复现性扩充——提供商端点下线导致无法复现** (保留)  
模型外部故障（预先登记标准）：实验开始时 Upstage 下线了 Anthropic 兼容端点（`/v1/messages`）和 solar-open2 托管 API，run 本身无法进行。假设并非被否定，而是**无法验证**。 → [报告](experiments/018-solar-n3-replication/report.md)

**EXP-019 — 原生 Opus 4.8·Opus 5·Codex×gpt-5.6-sol 韩文条件完成验证（各 n=3）** (验证)  
**9/9 run 全部在 iteration 1 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，干预 0）。语言遵从全部成立：9 个 run 的提交信息·README 均为韩文（含英语系模型 gpt-5.6-sol）。 → [报告](experiments/019-ko-native-codex/report.md)

**EXP-020 — Claude Code × solar-pro4 直连完成验证（n=3）** (验证)  
**3/3 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，模型干预 0）。但 pro4-1 因门控误判（框架责任）延长了循环——追溯重评确认有效完成为 iter 3。 → [报告](experiments/020-solar-pro4-direct/report.md)

**EXP-021 — Codex CLI × gpt-6-astra Ralph 循环完成验证（n=3）** (验证)  
**3/3 run 全部在 iteration 1 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，干预 0，会话 7 分钟级·提交 3–4 次）。 → [报告](experiments/021-gpt6-astra-codex/report.md)

**EXP-023 — Claude Code × Fable 5.1 原生 Ralph 循环完成验证（n=3）** (验证)  
**3/3 run 全部在 iteration 1 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，干预 0，会话 6–8 分钟·提交 2–4 次）。辅助指标相对 Opus 5（EXP-009/010）**时间·output 分布不重叠地下移**（6.2–7.8 分钟 vs 8.9–17.6 分钟，28.7–35.8K vs 41.1–48.4K）——Opus 5 的输出量扩大特征在 Fable 5.1 中回到 4.8 水平。 → [报告](experiments/023-fable51-ralph/report.md)

**EXP-025 — Claude Code × DeepSeek V4.1-Flash·V4-Pro 直连 Ralph 循环完成验证（EN·KO 各 n=3）** (验证)  
**12/12 run 全部在 iteration 1 完成**（四个条件各 3/3，门控通过 + 各 2 次独立复验 13/13·154/154 一致，干预 0，响应 model 字段全部一致）。Flash：EN 4.6–6.0 分钟，为全部条件中最快一档，按公开单价每 run 约 $0.1；Pro：12–16 分钟，约 $0.5。为观测值，不证明普遍成功率或效率优势。 → [报告](experiments/025-deepseek-direct/report.md)

**EXP-026 — Claude Code × Opus 5.5 原生 Ralph 循环完成验证（EN·KO 各 n=3）** (验证)  
**6/6 run 全部在 iteration 1 完成**（EN 3/3·KO 3/3，门控通过 + 各 2 次独立复验 13/13·154/154 一致，干预 0，响应 model 字段全部为 `claude-opus-5-5`）。会话 4.0–8.4 分钟（6 个 run 中 5 个为 4.0–4.2 分钟），output 18.6–28.2K，为原生 Claude 条件中最短·最低一档，低于 Opus 5（8.9–17.6 分钟·39–49K）和 Fable 5.1（6.2–7.8 分钟·28.7–35.8K）。为观测值，并非确定的优势。 → [报告](experiments/026-opus55-ralph/report.md)

**EXP-027 — Codex CLI × gpt-6-sol·gpt-6-luna Ralph 循环完成验证（各 n=3）** (验证)  
**sol 3/3·luna 3/3 全部在 iteration 1 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，响应 model 字段全部一致）。会话：sol 4.8–5.2 分钟·output 10.4–11.0K；luna 5.4–10.0 分钟·output 13.4–21.5K。评分基础设施挂起 1 次（D-1）在未干预代理的情况下处理，不影响判定。首个使用 `ralph-model-benchmark` 技能执行的实验。为观测值，并非确定的排名。 → [报告](experiments/027-gpt6-sol-luna-codex/report.md)

**EXP-028 — Claude Code × Sonnet 5 原生 Ralph 循环完成验证（EN·KO 各 n=3）** (验证)  
**EN 3/3·KO 3/3 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，零干预，所有消息的响应 model 字段均为 `claude-sonnet-5`）。5 个 run 在 iteration 1 完成；en-1 由代理自行把工作拆成 3 个 iteration，在 iteration 3 完成（无 rejected）。会话 11.2–16.8 分钟·output 57.6–73.7K，高于同一框架下 Opus 5.5（EXP-026）与 Fable 5.1（EXP-023）的观测范围。为观测值，并非确定的排名。 → [报告](experiments/028-sonnet5-ralph/report.md)

**EXP-029 — pi coding agent × kimi-k3·qwen3.8-max·deepseek-flash Ralph 循环完成验证（EN 各 n=3）** (验证)  
**三个条件均 3/3 完成**（门控通过 + 各 2 次独立复验 13/13·154/154 一致，零干预，响应 model 字段全部一致）。8 个 run 在 iteration 1 完成；qwen-en-1 因评分端口被外部进程占用而记录为 iteration 5 完成（其 iteration 1 代码复评也通过）。会话时长：flash 1.9–7.7 分钟，kimi 9.5–9.9 分钟，qwen 15.6–29.0 分钟。这是本仓库首次使用第三种框架（pi）；与此前 Claude Code 直连 run 的比较同时混杂了框架与 API 格式。为观测值，并非确定的排名。 → [报告](experiments/029-pi-openweight/report.md)

<!-- RESULTS:END -->

### 综合洞察（2026-09-21更正）

- EXP-001更正后的PTE/Ralph代理指标比为8.27倍；评分集不同，不能视为同等质量的成本比较。
- EXP-003下降22.45%，未达预设30%标准。撤回EXP-004两倍波动及无效果的结论。
- 首轮成功仅支持相应条件下的实现可行性。循环恢复贡献与维护性能需要单独评估。
- 3次成功或不同时期的耗时不足以确定通用排名或因果效果。订阅成本未测量不意味着免费。

9. **DeepSeek V4.1-Flash 无需调整即通过直连标准，并显示出全部条件中最快一档·最低成本的特征（EXP-025）。** 仅替换 3 个 env 值，Flash·V4-Pro 在 EN·KO 各 3/3，共 12/12 在 iter 1 完成（响应 model 字段全部保持）。Flash EN 4.6–6.0 分钟·每 run 折算约 $0.1（缓存命中输入 $0.006/M），低于 Codex×sol（5.3–10.0 分钟）一档；Pro 12–16 分钟·约 $0.5，output 为 1.5 倍。因时点·框架混淆，不确定速度·成本优势；作为直连可复用案例（第 4 家）和特征记录保留。
10. **Opus 5.5 仅替换模型 ID 即通过原生框架，并显示出原生 Claude 条件中最短·最低输出的特征（EXP-026）。** EN·KO 各 3/3，共 6/6 在 iter 1 完成（各 2 次复验一致）。6 个 run 中 5 个为 4.0–4.2 分钟·output 约 20K，低于 Fable 5.1（6.2–7.8 分钟·28.7–35.8K）和 Opus 5（8.9–17.6 分钟·39–49K）的分布，KO 下也保持同一档。这与第 8 条的解释（输出量扩大是 Opus 5 特有特征）一致。但这是与时点·CLI 版本不同的基准并置，且为 n=3 观测，在同期交叉重测之前不确定速度优势。
11. **GPT-6 系列 3 个模型（astra·sol·luna）在 Codex 框架中仅替换模型 ID 即全部完成（EXP-021·027）。** sol·luna 各 3/3 在 iter 1 完成（响应 model 字段全部一致）。sol 3 个 run 均为 4.8–5.2 分钟·output 约 11K，离散度小；luna 为 5.4–10.0 分钟·output 13.4–21.5K，与其 "fast" 定位不同，在此任务中没有比 sol 更短的 run。与 astra（EXP-021，7 分钟左右）的差异受时点·CLI 版本混杂影响，不归因于模型。EXP-027 是封装新模型基准流程的 `ralph-model-benchmark` 技能的首次应用。
12. **Sonnet 5 在原生框架中 EN·KO 也都完成了，但比同一框架中的上位模型更慢、输出更多（EXP-028）。** EN 3/3·KO 3/3 完成（所有消息的响应 model 字段均为 `claude-sonnet-5`）。5 个 run 在 iteration 1 完成；en-1 由代理把脚手架、测试准备和实现拆成 3 个 iteration，在 iteration 3 完成（无 rejected）。会话 11.2–16.8 分钟·output 57.6–73.7K，高于 Opus 5.5（EXP-026，4.0–8.4 分钟·18.6–28.2K）与 Fable 5.1（EXP-023）的观测范围。测量日期与 Claude Code 版本不同，不归因于模型本身。
13. **第三种框架 pi 也在无转换层的情况下用 3 个开放权重系模型完成（EXP-029）。** 将 pi coding agent 直连各提供方的 OpenAI 兼容端点，kimi-k3·qwen3.8-max·deepseek-flash 各 EN 3/3，共 9/9 完成（响应 model 字段全部一致，框架故障排查 0 次）。8 个 run 在 iteration 1 完成；qwen-en-1 因评分端口被外部进程占用而记录为 iteration 5（其 iteration 1 代码复评也通过）。会话时长：flash 1.9–7.7 分钟，kimi 9.5–9.9 分钟，qwen 15.6–29.0 分钟。与同一模型此前的 Claude Code 直连 run（EXP-013·014·025）相比，框架与 API 格式（Anthropic 兼容 vs OpenAI 兼容）同时不同，因此不把差异归因于 pi。至此 Ralph 循环基准可在 Claude Code·Codex·pi 三种框架上按同一流程复现。

## 实验生命周期

1. 复制 `templates/experiment-readme.md` 到 `experiments/NNN-名称/README.md` 并撰写实验设计（假设、条件、测量方法、成功标准）
2. 按条件运行会话，将会话日志·测量结果保存到 `runs/<条件名>/`
3. 在 `report.md` 中撰写 token 差异分析与结论——头部保持 `- 가설: [코드](...) — ...` 与 `- **판정: ...** — <一句话摘要>` 的格式（README 自动生成解析这两行）
4. 更新 `hypotheses/catalog.md` 的状态（未实验 → 进行中 → 验证/否定）
5. 在 `scripts/readme_i18n.json` 中添加新实验的英·日·中翻译（标题·假设·判定·摘要）——缺失时该语言 README 会填入韩文原文并由脚本给出警告
6. 提交 `report.md` 时，pre-commit 钩子会自动更新 4 个 README（ko/en/ja/zh-CN）的实验结果部分。新克隆的仓库需先执行一次 `git config core.hooksPath hooks`（手动更新：`python3 scripts/update_readme_results.py`）

## 目录结构

```
├── ideation.md            # 最初的构思（保留原样）
├── ROADMAP.md             # 分阶段路线图
├── hypotheses/catalog.md  # 假设目录 + 实验状态表
├── experiments/           # 实验目录（NNN-名称/）
│   └── 001-ralph-vs-plan-then-execute/
├── tasks/                 # 共同任务规范（跨条件复用）
│   └── realworld-backend/
├── templates/             # 实验设计·报告模板
├── scripts/               # 测量·汇总封装脚本
└── docs/specs/            # 设计文档
```
