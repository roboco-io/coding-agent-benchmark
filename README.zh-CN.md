# Vibecoding Token Experiments

🌐 [English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · **中文**

随着氛围编程（vibe coding）成为标准做法，许多组织正遭遇严重的 token 短缺。
本仓库用于管理关于 token 使用的假设，并通过受控实验验证实际的节省效果。

## 实验方法论

- **共同任务**：实现 [RealWorld App](https://github.com/gothinkster/realworld) 后端——用于条件间比较的固定基准任务。规范见 [`tasks/realworld-backend/`](tasks/realworld-backend/)。
- **固定模型**：所有实验均使用 **Claude Opus 单一模型**（消除模型差异带来的干扰）。
- **测量工具**：使用现有工具——[tokenhabit](https://github.com/epoko77-ai/tokenhabit)（`habit_scan.py`）、[ccusage](https://github.com/ryoppippi/ccusage)。`scripts/` 中只放用于提取实验区间·比较汇总的最小封装。
- **首要对象工具**：Claude Code。与其他工具的比较见 [`ROADMAP.md`](ROADMAP.md)。

## 假设的维度

1. **工作流策略（S 轴）**：同一任务采用不同策略时的 token 差异
   - Ralph 循环：指定目标后由 Ralph 循环自主推进
   - Plan-then-execute：制定计划 → 拆分任务 → 各任务并行实现
2. **token 习惯（H 轴）**：tokenhabit 的 H1–H8 习惯模式纠正前后的 token 差异
3. **语言（L 轴）**：提示词·产出文档的语言（韩文/英文）带来的 token 差异

完整的假设列表与实验状态在 [`hypotheses/catalog.md`](hypotheses/catalog.md) 中管理。

## 实验结果

> 下表与各实验摘要由 [`scripts/update_readme_results.py`](scripts/update_readme_results.py) 根据各实验的 `report.md` 自动生成（英·日·中 README 使用 [`scripts/readme_i18n.json`](scripts/readme_i18n.json) 中的翻译）。实验结束提交 `report.md` 时，pre-commit 钩子会自动执行（手动执行：`python3 scripts/update_readme_results.py`）。

**📊 实时仪表板**：[Ralph 循环各模型完成率对比](https://claude.ai/code/artifact/137de971-ded4-4fc6-ac5e-79bc96a09237) —— 最新实验：EXP-025（2026-09-21）

<!-- RESULTS:BEGIN -->
<!-- 此区块由 scripts/update_readme_results.py 根据 experiments/*/report.md 自动生成（翻译来自 scripts/readme_i18n.json）。请勿手动编辑。 -->

| 实验 | 假设 | 判定 |
|------|------|------|
| [EXP-001](experiments/001-ralph-vs-plan-then-execute/report.md) Ralph 循环 vs Plan-then-execute | S-01: Plan-then-execute 在同一任务上比 Ralph 循环使用更少 token | **否定（反证）** |
| [EXP-002](experiments/002-korean-vs-english/report.md) 韩文 vs 英文流水线 token 比较 | L-01: 全流程用英文进行可比韩文显著减少 billable token | **保留** |
| [EXP-003](experiments/003-pte-skills/report.md) PTE + 技能式渐进披露 | S-02: 按技能官方建议（文档不超过 200 行、通过技能只加载所需内容）组织上下文，可比 EXP-001 的 PTE 减少 30% 以上 billable | **验证** |
| [EXP-004](experiments/004-ralph-skills/report.md) Ralph 循环 + 技能结构 | S-03: 为单会话 ralph 提供领域契约技能可减少 billable | **保留（实际上无效果）** |
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

**EXP-001 — Ralph 循环 vs Plan-then-execute** (否定（反证）)  
plan-then-execute 按 billable 计使用了**约 8.7 倍**的 token → [报告](experiments/001-ralph-vs-plan-then-execute/report.md)

**EXP-002 — 韩文 vs 英文流水线 token 比较** (保留)  
未满足预先登记的判定规则（|KO 均值−EN 均值| > 条件内 run 间波动幅度）。语言效应（均值差 29K）被 run 间轨迹波动（最大 138K）淹没 → [报告](experiments/002-korean-vs-english/report.md)

**EXP-003 — PTE + 技能式渐进披露** (验证)  
**减少 39.3%**（2,839,815 → 1,723,575）。工作流相同，只改变了上下文结构。 → [报告](experiments/003-pte-skills/report.md)

**EXP-004 — Ralph 循环 + 技能结构** (保留（实际上无效果）)  
均值差 +3.5%（方向与假设相反）被条件内波动幅度（200K）完全淹没 → [报告](experiments/004-ralph-skills/report.md)

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

<!-- RESULTS:END -->

### 综合洞察（随实验积累更新）

贯穿各实验（RealWorld 后端，Opus 固定）的结论：

1. **token 成本的主导变量是上下文（缓存）复用。** 单会话 ralph（约 290K）把一次建立的上下文复用到底——技术背景（基于前缀的 prompt caching、0.1 倍的 cache read、美元折算重算）见 [docs/context-reuse-mechanism.md](docs/context-reuse-mechanism.md)。一旦拆分会话，启动固定成本（每会话约 20.6K）与上下文重建成本累积，同一任务变贵 6–9 倍（EXP-001）。
2. **渐进披露（技能）是多会话专用处方。** 当会话只需要完整上下文的子集时（PTE 任务会话），它消除了重复读取和修正循环：−39.3%（EXP-003）。而需要全部内容的单会话会把技能全部预加载，没有效果（EXP-004）。
3. **智能体工作轨迹的波动是 ± 数十万 token 的常量噪声。** 同一条件的 run 可相差 2 倍（EXP-002 EN 191K–329K，EXP-004 199K–400K）。约 10% 量级的效应（如语言）在 n=2 下无法判别。
4. **实用指南**：任务放得进单会话就用单会话跑。若不得不拆分，就用技能把上下文结构化以减少损失。文档语言（韩/英）是远小于这两项决策的变量。
5. **“模型无法完成”的主导因素是实验环境污染（M 轴，EXP-005–008）。** Solar 后端四部曲的叙事：EXP-005（缺乏自主性而未完成）→ EXP-006（建立了 TDD 但 3/13 未完成）→ EXP-007（剖析：usage 高估 3.07 倍的错觉 + superpowers 钩子·全局 CLAUDE.md 污染侵蚀 23% 的 iteration + 模型缺陷）→ **EXP-008（去除污染的干净 run 仅用 10 个 iteration 就 13/13·154/154 完成，并完成 4 次提交）**。同一模型·同一 PROMPT·同一 env，仅靠隔离就翻转了判定，且完成点在 EXP-006 上限之内，因此提高上限没有贡献。三条教训：(a) **自主循环实验中，隔离实验者本地环境（钩子·全局设置）是前提条件**——否则“模型能力”的测量就变成了“污染顺应度”的测量。(b) 未经日志剖析不要把完成失败归咎于模型——可能是转换层缺陷（CCR 多 delta bug）·计量错误（usage 行累加，必须按 message.id 去重）·环境污染，以及**评分门控本身的误判**（EXP-010 48-1 评分文件未复制、EXP-015 iter 2 端口探测缺陷——在 measure v4 中修复）。(c) 模型内在缺陷（等待许可 1 次、thinking 94%、回合边界的不可执行状态）即使残留，Ralph 循环的重复结构也能吸收。成本优势的判定因单价未公开仍无法做出。
6. **Ralph 循环协议可跨框架移植，完成由模型决定、轨迹由框架决定（EXP-011/012 配对）。** 同一 PROMPT·门控·模型（gpt-5.6-sol，effort medium）只更换框架的配对实验中两者都无人干预完成——Codex CLI 为 iteration 1·5 分 46 秒·单文件 436 行·提交 3 次，Claude Code（经 ccr）为 iteration 11·58 分钟·模块化 11 个文件·提交 11 次。“最重要的一块”这一指令，Codex 理解为做到完成，Claude Code 一侧则按字面理解为一块，小型 iteration 由 Ralph 循环吸收。隔离原则（专用 CODEX_HOME/CLAUDE_CONFIG_DIR）和逐 iteration 的外部评分门控不分工具均成立。工具间的 token 效率比较需先标准化计量方式（rollout 累计 vs ccr 标签页 vs ccusage）。Codex 框架在模型换代时也可原样移植——GPT-6 首个模型 gpt-6-astra（因无 Anthropic 兼容端点，Codex 路径是唯一一致的路径）仅替换模型 ID 一项即接入并 3/3 在 iter 1 完成（EXP-021，会话 7 分钟级·误判 0 起）。但会话时间比 sol 多 +23–32%，官方“快 1.9 倍”的数字在此框架中未复现——速度叙事保留判断。
7. **第三方模型的接入，通过 Anthropic 兼容端点直连在结构上优于转换层（ccr），且直连模板可跨提供商复用（EXP-013/014）。** 用 `ANTHROPIC_BASE_URL` 直连 qwen3.8-max（DashScope）和 kimi-k3（Moonshot）后，ccr 栈中反复出现的失败模式（usage 丢失→另建标签页、transformer 链调整、流停滞）全部消失——两个实验均未经调整通过 Phase 0·在 iteration 1 完成（15 分 5 秒 / 21 分 18 秒）·会话 jsonl usage 正常。EXP-014 在 EXP-013 框架上仅替换 3 个 env 值（端点/密钥/模型 ID）即可运行——方法与提供商无关。直连也把计量回归到 Claude 标准路径（jsonl + message.id 去重），部分解决了第 6 条的标准化前置课题，但缓存计量方式因提供商而异（Moonshot 将 cache_create 计为 0）。与 ccr 的比较因模型不同而存在栈·模型效应混淆——若提供商提供 Anthropic 兼容端点则以直连为默认选项，但栈间定量比较需要同一模型实验。**可复现性以 n=3 确定（EXP-016）**：Codex×gpt-5.6-sol·qwen 直连·kimi 直连三个条件各 3/3 完成（合计 9/9，8/9 为 iter 1）——但完成以外的指标（时间·提交·output）在同一条件下也波动至 3 倍（kimi 21 分钟→7 分钟级），S 轴“轨迹波动是常量噪声”的结论在 M 轴同样成立。只有完成率是稳定指标。**韩文条件也不损害完成率（EXP-017/019）**：在韩文标准版（要求全部产出为韩文）下 qwen·kimi·Opus 4.8·Opus 5·Codex×gpt-5.6-sol 五个条件各 3/3，**累计 15/15 在 iter 1 完成**，提交·README 全部韩文·语言偏离 0——连英语系模型（gpt-5.6-sol）也遵从，说明韩文执行是指令遵从问题而非模型谱系问题。时间·提交·output 在 EXP-019 三个条件下也全部与 EN 分布重叠——qwen 在 ko 下 +48% 的时间（EXP-017）是例外案例，仅作方向性记录（L-01 原则）。模型特征（4.8 单次提交 vs 5 细分提交）在语言翻转后依然保持。**但直连的可复现性依赖于提供商（EXP-018）**：EXP-015 完成次日，Upstage 无预告下线了 Anthropic 兼容端点和 solar-open2 托管 API（需申请的测试版结束），复现窗口关闭——第三方基准中标明实验时点界定了可复现性主张的边界，复用框架前的提供商冒烟测试必不可少。两周后端点以 solar-pro4 恢复，确认直连 3/3 完成（EXP-020）——完成能力与直连上游相当，但有效时间 119–258 分钟（qwen 的 8–17 倍）为最长特征，原因是不支持缓存（所有调用 cache 为 0，每次重新预填约 8 万 token）·往返 37 秒·thinking 88% 的乘积。**注意：solar-open2·solar-pro4 端点并非商用正式版（GA）API，而是预览（需申请的测试版）状态**，基础设施约束（不支持 prompt caching、往返延迟长、无预告下线端点）始终存在，Solar 系列的时间·usage 特征是模型能力与预览基础设施特性相混淆的值——不要当作商用基础设施上的性能来解读。门控误判第 3 例（全局 npm 污染遮蔽了 hurl 二进制）新增了**固定评分二进制绝对路径**的教训。
8. **输出量扩大特征是模型固有特性而非世代特征（EXP-023）。** Claude 5 世代的高阶模型 Fable 5.1 在同一框架·EN 标准版下 3/3 在 iter 1 完成，output 28.7–35.8K·6.2–7.8 分钟，与 Opus 4.8 分布（29.6–37.1K·7.8–8.7 分钟）重叠，而与 Opus 5（41.1–48.4K·8.9–17.6 分钟）不重叠。EXP-010 确定为“世代特征”的 Opus 5 output·提交扩大在同世代的高阶模型中未复现，因此重新解释为 Opus 5 独有的特征（n=3·时点差 7 周，方向性记录）。

9. **DeepSeek V4.1-Flash 无需调整即通过直连标准，并显示出全部条件中最快一档·最低成本的特征（EXP-025）。** 仅替换 3 个 env 值，Flash·V4-Pro 在 EN·KO 各 3/3，共 12/12 在 iter 1 完成（响应 model 字段全部保持）。Flash EN 4.6–6.0 分钟·每 run 折算约 $0.1（缓存命中输入 $0.006/M），低于 Codex×sol（5.3–10.0 分钟）一档；Pro 12–16 分钟·约 $0.5，output 为 1.5 倍。因时点·框架混淆，不确定速度·成本优势；作为直连可复用案例（第 4 家）和特征记录保留。

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
