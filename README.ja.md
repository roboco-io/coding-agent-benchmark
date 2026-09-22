# Vibecoding Token Experiments

🌐 [English](README.md) · [한국어](README.ko.md) · **日本語** · [中文](README.zh-CN.md)

バイブコーディングが標準として導入されるにつれ、多くの組織が深刻なトークン不足に直面している。
このリポジトリはトークン使用に関する仮説を立て、統制された実験で実際の節約効果を検証するための実験管理リポジトリである。

## 実験方法論

- **共通課題**: [RealWorld App](https://github.com/gothinkster/realworld) バックエンドの実装——条件間比較のための固定ベンチマーク課題。仕様は [`tasks/realworld-backend/`](tasks/realworld-backend/) を参照。
- **モデル固定**: 全ての実験は **Claude Opus 単一モデル** で行う（モデル差による攪乱を除去）。
- **測定ツール**: 既存ツールを活用する——[tokenhabit](https://github.com/epoko77-ai/tokenhabit)（`habit_scan.py`）、[ccusage](https://github.com/ryoppippi/ccusage)。`scripts/` には実験区間の抽出・比較集計用の最小ラッパーのみ置く。
- **一次対象ツール**: Claude Code。他ツールとの比較は [`ROADMAP.md`](ROADMAP.md) を参照。

## 仮説の軸

1. **ワークフロー戦略（S軸）**: 同じ課題をどの戦略で遂行するかによるトークン差
   - Ralphループ: ゴールを指定した後、Ralphループで自律進行
   - Plan-then-execute: 計画策定 → タスク分割 → 個別タスクの並列実装
2. **トークン習慣（H軸）**: tokenhabit の H1–H8 習慣パターン矯正前後のトークン差
3. **言語（L軸）**: プロンプト・成果物文書の言語（韓国語/英語）によるトークン差

全ての仮説一覧と実験状態は [`hypotheses/catalog.md`](hypotheses/catalog.md) で管理する。

## 実験結果

> 以下の表と実験別要約は [`scripts/update_readme_results.py`](scripts/update_readme_results.py) が各実験の `report.md` から自動生成する（英・日・中の README は [`scripts/readme_i18n.json`](scripts/readme_i18n.json) の翻訳を使用）。実験が終わり `report.md` がコミットされる際に pre-commit フックが自動実行する（手動実行: `python3 scripts/update_readme_results.py`）。

**📊 ライブダッシュボード**: [Ralphループ モデル別完走比較](https://roboco-io.github.io/coding-agent-benchmark/) —— 最新実験反映: EXP-026（2026-09-23）

<!-- RESULTS:BEGIN -->
<!-- このブロックは scripts/update_readme_results.py が experiments/*/report.md から自動生成する（翻訳は scripts/readme_i18n.json）。直接編集禁止。 -->

| 実験 | 仮説 | 判定 |
|------|------|------|
| [EXP-001](experiments/001-ralph-vs-plan-then-execute/report.md) Ralphループ vs Plan-then-execute | S-01: Plan-then-executeはRalphループより同一課題でトークンを少なく使う | **棄却（反証）** |
| [EXP-002](experiments/002-korean-vs-english/report.md) 韓国語 vs 英語パイプラインのトークン比較 | L-01: 全パイプラインを英語で進めると韓国語比でbillableトークンが有意に減る | **保留** |
| [EXP-003](experiments/003-pte-skills/report.md) PTE + スキル式の段階的開示 | S-02: コンテキストをスキル公式推奨（文書200行以下、スキルで必要なものだけロード）で構造化すればEXP-001のPTE比でbillableが30%以上減る | **検証** |
| [EXP-004](experiments/004-ralph-skills/report.md) Ralphループ + スキル構造 | S-03: 単一セッションのralphにドメイン契約スキルを与えるとbillableが減る | **保留（事実上効果なし）** |
| [EXP-005](experiments/005-solar-pro3-backend/report.md) Claude Code × Upstage Solar Pro 3 バックエンド | M-01: Claude CodeのバックエンドをSolar Pro 3に置き換えると同一課題（RealWorldバックエンド）を無介入で完走でき、完走時の総費用がOpus比で有意に低い。 | **保留** |
| [EXP-006](experiments/006-solar-open2-backend/report.md) Claude Code × Upstage Solar Open 2 バックエンド | M-02: Claude CodeのバックエンドをSolar Open 2に置き換えると同一課題（RealWorldバックエンド）を無介入で完走でき、完走時の総費用がOpus比で有意に低い。 | **保留** |
| [EXP-007](experiments/007-solar-open2-autopsy/report.md) Solar Open 2 未完走原因の検死 | M-03: EXP-006（Solar Open 2）の未完走は収束速度という単一ボトルネックではなく、複数の失敗要因（モデル行動欠陥・実験環境汚染・計測歪み）の重なりである。 | **検証** |
| [EXP-008](experiments/008-solar-open2-clean-run/report.md) Solar Open 2 無汚染クリーンrun——完走検証 | M-04: 汚染除去（隔離設定）・無攪乱・上限30 iterの条件でsolar-open2はRalphループでRealWorldバックエンド（Hurl 154/154）を無介入で完走できる（課金は除外、完走可否の単一判定）。 | **検証** |
| [EXP-009](experiments/009-opus5-ralph-en/report.md) Opus 5 Ralphループ（EXP-002 en条件、n=3） | M-05: Opus 5はEXP-002 en条件のRalphループで単一セッション完走を再現し、Opus 4.x基準線（en 6–7分・API 38–54回）比で同等以上の効率を示す。 | **部分検証（n=3）** |
| [EXP-010](experiments/010-opus48-vs-opus5/report.md) Opus 4.8 vs Opus 5 純粋A/B（同時点、各n=3） | M-06: 完全同一条件でOpus 5の出力量拡大プロファイル（output・コミット↑）がOpus 4.8比で再現され、両モデルとも単一セッション完走を維持する。 | **検証** |
| [EXP-011](experiments/011-codex-gpt56-sol/report.md) Codex CLI × gpt-5.6-sol RealWorldバックエンド完走検証 | M-07: Codex CLI（`codex exec`）ハーネスでgpt-5.6-sol（effort medium）は隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる。 | **検証** |
| [EXP-012](experiments/012-ccr-gpt56-sol/report.md) Claude Code × gpt-5.6-sol バックエンド（ccr）RealWorldバックエンド完走検証 | M-08: Claude Codeのバックエンドをccrでgpt-5.6-solに接続すると（reasoning effort medium）、隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる。 | **検証** |
| [EXP-013](experiments/013-qwen38max-direct/report.md) Claude Code × qwen3.8-max 直結（ANTHROPIC_BASE_URL）RealWorldバックエンド完走検証 | M-09: Claude CodeをDashScopeのAnthropic互換エンドポイントでqwen3.8-maxに直結すると（thinkingデフォルト）、隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる。 | **検証** |
| [EXP-014](experiments/014-kimi-k3-direct/report.md) Claude Code × kimi-k3 直結（ANTHROPIC_BASE_URL）RealWorldバックエンド完走検証 | M-10: Claude CodeをMoonshotのAnthropic互換エンドポイントでkimi-k3に直結すると（thinkingデフォルト）、隔離・無介入のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる。 | **検証** |
| [EXP-015](experiments/015-solar-open2-direct/report.md) Claude Code × solar-open2 直結（ANTHROPIC_BASE_URL）RealWorldバックエンド完走検証 | M-11: Claude CodeをUpstageのAnthropic互換エンドポイントでsolar-open2に直結すると（thinkingデフォルト）、隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる。 | **検証** |
| [EXP-016](experiments/016-n3-replication/report.md) n=1完走条件3種の再現性拡充（各n=3） | M-12: EXP-011/013/014の3条件（Codex CLI × gpt-5.6-sol、qwen3.8-max直結、kimi-k3直結）の無介入完走は再現される：各条件の追加2 run（計n=3）が全て上限30 iteration以内にゲート+独立再検証一致で完走する。 | **検証** |
| [EXP-017](experiments/017-ko-condition/report.md) qwen3.8-max・kimi-k3 韓国語条件Ralphループ完走検証（各n=3） | L-02: qwen3.8-max・kimi-k3（直結、thinkingデフォルト）は韓国語正本プロンプト（全成果物の韓国語指示を含む）条件でも隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる。 | **検証** |
| [EXP-018](experiments/018-solar-n3-replication/report.md) solar-open2直結の再現性拡充——プロバイダのエンドポイント終了により再現不可 | M-13: EXP-015のsolar-open2直結の無介入完走は再現される：追加2 run（計n=3）が全て30 iteration以内にゲート（measure v4）+再検証で完走できる。 | **保留** |
| [EXP-019](experiments/019-ko-native-codex/report.md) ネイティブOpus 4.8・Opus 5・Codex×gpt-5.6-sol 韓国語条件完走検証（各n=3） | L-03: ネイティブOpus 4.8・Opus 5（Claude Code）とgpt-5.6-sol（Codex CLI）は韓国語正本プロンプト（全成果物の韓国語指示を含む）条件でも隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限iteration以内に無介入で完走できる。 | **検証** |
| [EXP-020](experiments/020-solar-pro4-direct/report.md) Claude Code × solar-pro4 直結完走検証（n=3） | M-14: Claude CodeをUpstageのAnthropic互換エンドポイントでsolar-pro4に直結すると（thinkingデフォルト）、隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる（n=3、完走率判定・課金除外）。 | **検証** |
| [EXP-021](experiments/021-gpt6-astra-codex/report.md) Codex CLI × gpt-6-astra Ralphループ完走検証（n=3） | M-15: Codex CLI（`codex exec`）ハーネスでgpt-6-astra（effort medium）は隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration以内に無介入で完走できる（n=3、完走率判定・課金除外）。 | **検証** |
| [EXP-023](experiments/023-fable51-ralph/report.md) Claude Code × Fable 5.1 ネイティブRalphループ完走検証（n=3） | M-17: Claude CodeネイティブハーネスでFable 5.1（`claude-fable-5-1`、thinkingデフォルト）はEN正本のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限10 iteration以内に無介入で完走できる（n=3、完走率判定・課金除外）。 | **検証** |
| [EXP-025](experiments/025-deepseek-direct/report.md) Claude Code × DeepSeek V4.1-Flash・V4-Pro 直結Ralphループ完走検証（EN・KO各n=3） | M-18: Claude CodeをDeepSeekのAnthropic互換エンドポイントで`deepseek-flash`（DeepSeek-V4.1-Flash）・`deepseek-v4-pro`（DeepSeek-V4-Pro-0813）に直結すると（thinkingデフォルト）、隔離・無攪乱のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration・4時間以内に無介入で完走できる（EN・KO正本各n=3、完走率判定・課金除外）。 | **検証** |
| [EXP-026](experiments/026-opus55-ralph/report.md) Claude Code × Opus 5.5 ネイティブRalphループ完走検証（EN・KO各n=3） | M-19: Claude Codeネイティブハーネスで、Opus 5.5（`claude-opus-5-5`、thinkingデフォルト）はEN正本・KO正本のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限10 iteration・4時間以内に無介入で完走できる（EN・KO各n=3、完走率判定・課金除外）。 | **検証** |

**EXP-001 — Ralphループ vs Plan-then-execute** (棄却（反証）)  
plan-then-executeがbillable基準で**約8.7倍多い**トークンを使用 → [レポート](experiments/001-ralph-vs-plan-then-execute/report.md)

**EXP-002 — 韓国語 vs 英語パイプラインのトークン比較** (保留)  
事前登録した判定規則（|KO平均−EN平均| > 条件内run間変動幅）を満たさず。言語効果（平均差29K）がrun間の軌跡変動（最大138K）に埋もれる → [レポート](experiments/002-korean-vs-english/report.md)

**EXP-003 — PTE + スキル式の段階的開示** (検証)  
**39.3%減少**（2,839,815 → 1,723,575）。ワークフローは同一でコンテキスト構造だけを変えた。 → [レポート](experiments/003-pte-skills/report.md)

**EXP-004 — Ralphループ + スキル構造** (保留（事実上効果なし）)  
平均差+3.5%（方向は仮説と逆）が条件内変動幅（200K）に完全に埋もれる → [レポート](experiments/004-ralph-skills/report.md)

**EXP-005 — Claude Code × Upstage Solar Pro 3 バックエンド** (保留)  
solar-1未完走（テスト実行0回・コミット0回、6/15 iteration時点で早期中断）：連携スタックは検証されたが、headless自律ループで許可待ち・コンテキスト超過の失敗モードが繰り返され完走軌道に乗らなかった。 → [レポート](experiments/005-solar-pro3-backend/report.md)

**EXP-006 — Claude Code × Upstage Solar Open 2 バックエンド** (保留)  
0/2完走だが完全プロトコルのrunは1回のみ（open2-1は1 iterで虚偽の完了申告により自己終了）：open2-2は15 iterationを使い切っても独立検証3/13ファイル（94/154リクエスト）に留まったが、solar-pro3に欠けていた自律TDDループを確立し単調収束したことで「行動層」のボトルネックが自律性から収束速度へ移った。 → [レポート](experiments/006-solar-open2-backend/report.md)

**EXP-007 — Solar Open 2 未完走原因の検死** (検証)  
3層を実証：①計測歪み（usage 3.07倍の過大計上——実際は483リクエスト・23.3M input、推定約$3.8でOpusの$6.41より低い）、②環境汚染（superpowersフック・グローバルCLAUDE.md注入で最低3 iterationを浸食）、③モデル行動欠陥（宣言のみで実行しないためコミット0回、thinking-only切断25回、課題逸脱の幻覚2件）。 → [レポート](experiments/007-solar-open2-autopsy/report.md)

**EXP-008 — Solar Open 2 無汚染クリーンrun——完走検証** (検証)  
**iteration 10/30で完走**：`.ralph-done`生成→ハーネスゲート13/13ファイル・154/154リクエスト通過→実験者の独立再検証2回一致。wall-clock約2時間53分、無介入・無中断、gitコミット4回（韓国語）まで履行。完走時点がEXP-006の上限（15）の内側なので、決定変数は上限増加ではなく**環境汚染の除去・無攪乱**だった。 → [レポート](experiments/008-solar-open2-clean-run/report.md)

**EXP-009 — Opus 5 Ralphループ（EXP-002 en条件、n=3）** (部分検証（n=3）)  
完走条項は検証：**3/3 run全てがiteration 1で単一セッション完走**（9分03秒–12分22秒、ゲート13/13・154/154 + 独立再検証各2回、コミット6–7個）。効率条項は未達で確定：時間分布（8.9–12.2分）が4.x（5.8–6.9分）と重ならない——ただし原因はサービング速度ではなく**一貫した出力量増加（+62%）を伴う行動プロファイルの変化**と判別。 → [レポート](experiments/009-opus5-ralph-en/report.md)

**EXP-010 — Opus 4.8 vs Opus 5 純粋A/B（同時点、各n=3）** (検証)  
完走6/6（全runがiteration 1、ゲート13/13・154/154）。事前登録指標を全て充足：**outputトークン分布の非重複**（4.8：29.6–37.1K vs 5：41.1–47.9K、平均+37%）・**gitコミット分布の非重複**（1–2個 vs 4–8個）、方向はEXP-009と同一（5 > 4.8）。世代差は時点・計測アーティファクトではなく実在するプロファイルと確定。 → [レポート](experiments/010-opus48-vs-opus5/report.md)

**EXP-011 — Codex CLI × gpt-5.6-sol RealWorldバックエンド完走検証** (検証)  
**iteration 1で完走**（ゲート13/13・154/154 + 独立再検証2回一致、codex exec 5分46秒・セッション1個・コミット3回、無介入）。 → [レポート](experiments/011-codex-gpt56-sol/report.md)

**EXP-012 — Claude Code × gpt-5.6-sol バックエンド（ccr）RealWorldバックエンド完走検証** (検証)  
**iteration 11/30で完走**（ゲート13/13・154/154 + 独立再検証2回一致、計58分・コミット11回）。ただしiteration 2でストリームのストール1件にハーネスレベルの介入（プロセス終了でiteration境界を復旧、モデル成果物には不介入）があった——下記のプロトコル課題を参照。 → [レポート](experiments/012-ccr-gpt56-sol/report.md)

**EXP-013 — Claude Code × qwen3.8-max 直結（ANTHROPIC_BASE_URL）RealWorldバックエンド完走検証** (検証)  
**iteration 1で完走**（ゲート13/13・154/154 + 独立再検証2回一致、15分5秒・コミット4回・介入0、直結スタックのトラブルシューティング0件）。 → [レポート](experiments/013-qwen38max-direct/report.md)

**EXP-014 — Claude Code × kimi-k3 直結（ANTHROPIC_BASE_URL）RealWorldバックエンド完走検証** (検証)  
**iteration 1で完走**（ゲート13/13・154/154 + 独立再検証2回一致、21分18秒・コミット4回・介入0、直結スタックのトラブルシューティング0件）。 → [レポート](experiments/014-kimi-k3-direct/report.md)

**EXP-015 — Claude Code × solar-open2 直結（ANTHROPIC_BASE_URL）RealWorldバックエンド完走検証** (検証)  
**iteration 2で完走**（成果物の直接再採点2回とも13/13・154/154一致、58分15秒・コミット2回。脚注：ゲート誤棄却1件——measure v3のポート検出欠陥で正当な完走を棄却、EXP-010 48-1の先例を適用）。 → [レポート](experiments/015-solar-open2-direct/report.md)

**EXP-016 — n=1完走条件3種の再現性拡充（各n=3）** (検証)  
**追加6 run全て完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0）。元のrunを含め3条件の完走率は**各3/3、合算9/9**。 → [レポート](experiments/016-n3-replication/report.md)

**EXP-017 — qwen3.8-max・kimi-k3 韓国語条件Ralphループ完走検証（各n=3）** (検証)  
**6/6 run全てiteration 1で完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0）。言語遵守も成立：全runのコミットメッセージ・READMEが韓国語。 → [レポート](experiments/017-ko-condition/report.md)

**EXP-018 — solar-open2直結の再現性拡充——プロバイダのエンドポイント終了により再現不可** (保留)  
モデル外的障害（事前登録基準）：実験開始時点でUpstageがAnthropic互換エンドポイント（`/v1/messages`）とsolar-open2 hosted APIを終了し、run自体が不可能。仮説は棄却ではなく**検証不可**。 → [レポート](experiments/018-solar-n3-replication/report.md)

**EXP-019 — ネイティブOpus 4.8・Opus 5・Codex×gpt-5.6-sol 韓国語条件完走検証（各n=3）** (検証)  
**9/9 run全てiteration 1で完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0）。言語遵守も全数成立：9 run全てコミットメッセージ・READMEが韓国語（英語圏モデルgpt-5.6-solを含む）。 → [レポート](experiments/019-ko-native-codex/report.md)

**EXP-020 — Claude Code × solar-pro4 直結完走検証（n=3）** (検証)  
**3/3完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、モデル介入0）。ただしpro4-1はゲート誤棄却（ハーネス起因）でループが延長——遡及再採点で有効完走iter 3を確定。 → [レポート](experiments/020-solar-pro4-direct/report.md)

**EXP-021 — Codex CLI × gpt-6-astra Ralphループ完走検証（n=3）** (検証)  
**3/3 run全てiteration 1で完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0、セッション7分台・コミット3–4回）。 → [レポート](experiments/021-gpt6-astra-codex/report.md)

**EXP-023 — Claude Code × Fable 5.1 ネイティブRalphループ完走検証（n=3）** (検証)  
**3/3 run全てiteration 1で完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0、セッション6–8分・コミット2–4回）。補助指標はOpus 5（EXP-009/010）比で**時間・output分布が重ならず下方へ**（6.2–7.8分 vs 8.9–17.6分、28.7–35.8K vs 41.1–48.4K）——Opus 5の出力量拡大プロファイルはFable 5.1では4.8水準に戻った。 → [レポート](experiments/023-fable51-ralph/report.md)

**EXP-025 — Claude Code × DeepSeek V4.1-Flash・V4-Pro 直結Ralphループ完走検証（EN・KO各n=3）** (検証)  
**12/12 run全てiteration 1で完走**（4条件各3/3、ゲートpass + 独立再検証各2回13/13・154/154一致、介入0、応答modelフィールド全件一致）。FlashはEN 4.6–6.0分で全条件最速帯・公開単価でrunあたり約$0.1、Proは12–16分・約$0.5。観測値であり一般的成功率・効率優位の証明ではない。 → [レポート](experiments/025-deepseek-direct/report.md)

**EXP-026 — Claude Code × Opus 5.5 ネイティブRalphループ完走検証（EN・KO各n=3）** (検証)  
**6/6 run全てiteration 1で完走**（EN 3/3・KO 3/3、ゲートpass + 独立再検証各2回13/13・154/154一致、介入0、応答modelフィールド全件`claude-opus-5-5`）。セッション4.0–8.4分（6 run中5 runが4.0–4.2分）・output 18.6–28.2Kでネイティブ Claude条件中最短・最低帯、Opus 5（8.9–17.6分・39–49K）とFable 5.1（6.2–7.8分・28.7–35.8K）の分布より下。観測値であり優位の確定ではない。 → [レポート](experiments/026-opus55-ralph/report.md)

<!-- RESULTS:END -->

### 総合インサイト（実験が積み重なるたびに更新）

実験群（RealWorldバックエンド、Opus固定）を貫く結論：

1. **トークンコストの支配変数はコンテキスト（キャッシュ）の再利用である。** 単一セッションのralph（約290K）は一度作ったコンテキストを最後まで再活用する——技術的背景（prefixベースのプロンプトキャッシング、0.1倍のcache read、ドル換算の再計算）は [docs/context-reuse-mechanism.md](docs/context-reuse-mechanism.md) を参照。セッションを分けた瞬間、起動固定費（セッションあたり約20.6K）とコンテキスト再構築コストが累積し、同じ課題が6–9倍高くなる（EXP-001）。
2. **段階的開示（スキル）はマルチセッション専用の処方である。** セッションが全コンテキストの部分集合だけを必要とする場合（PTEタスクセッション）、繰り返し読みと修正ループをなくして −39.3%（EXP-003）。一方、全体が必要な単一セッションはスキルを全量プリロードするため効果がない（EXP-004）。
3. **エージェントの作業軌跡の変動は±数十万トークンの定常ノイズである。** 同一条件のrunが2倍まで開く（EXP-002 EN 191K–329K、EXP-004 199K–400K）。約10%程度の効果（例：言語）はn=2では判別不能。
4. **実用指針**: 課題が単一セッションに収まるなら単一セッションで回せ。分割が避けられないならコンテキストをスキルで構造化して損失を減らせ。文書言語（韓/英）はこの2つの決定よりはるかに小さい変数である。
5. **「モデルが完走できない」の支配要因は実験環境の汚染だった（M軸、EXP-005–008）。** Solarバックエンド4部作の叙述：EXP-005（自律性欠如で未完走）→ EXP-006（TDDは確立したが3/13で未完走）→ EXP-007（検死：usage 3.07倍過大計上の錯覚 + superpowersフック・グローバルCLAUDE.md汚染がiterationの23%を浸食 + モデル欠陥）→ **EXP-008（汚染除去クリーンrunでiteration 10のうちに13/13・154/154完走、コミット4回まで履行）**。同一モデル・同一PROMPT・同一envで隔離ひとつで判定が覆り、完走時点がEXP-006の上限内だったため上限増加は寄与しなかった。教訓3つ：(a) **自律ループ実験では実験者のローカル環境（フック・グローバル設定）の隔離が前提条件**——これを破ると「モデル能力」の測定が「汚染順応度」の測定になる。(b) 完走失敗の原因をログ検死なしにモデル起因と断定するな——変換層の欠陥（CCRマルチデルタバグ）・計測誤り（usage行の合算、message.id dedup必須）・環境汚染、そして**採点ゲート自体の誤棄却**（EXP-010 48-1採点ファイル未コピー、EXP-015 iter 2ポート検出欠陥——measure v4で修正）でありうる。(c) モデル内在の欠陥（許可待ち1回、thinking 94%、ターン境界での実行不能状態）は残存してもRalphループの反復構造が吸収可能。コスト優位の判定は依然として単価未公開のため不能。
6. **Ralphループのプロトコルはハーネス非依存に移植され、完走はモデルが・軌跡はハーネスが決めた（EXP-011/012ペア）。** 同一PROMPT・ゲート・モデル（gpt-5.6-sol、effort medium）でハーネスだけを変えたペア実験で両方とも無介入完走——Codex CLIはiteration 1・5分46秒・単一ファイル436行・コミット3回、Claude Code（ccr経由）はiteration 11・58分・モジュール型11ファイル・コミット11回。「最も重要な一片」の指示をCodexは完走までと解釈し、Claude Code側は文字通り一片と解釈して小型iterationをRalphループが吸収した。隔離原則（専用CODEX_HOME/CLAUDE_CONFIG_DIR）とiterationごとの外部採点ゲートはツールを問わず成立。ツール間のトークン効率比較は計測方式（rollout累計 vs ccrタブ vs ccusage）の標準化が先行課題。Codexハーネスはモデル世代交代にもそのまま移植される——GPT-6初のモデルgpt-6-astra（Anthropic互換エンドポイント不在のためCodex経路が唯一の整合）をモデルID 1要素の差し替えだけで接続し3/3 iter 1完走（EXP-021、セッション7分台・誤棄却0件）。ただしsol比でセッション時間+23–32%で公式の「1.9倍高速」はこのハーネスでは再現せず——速度の叙述は判断保留。
7. **サードパーティモデルの接続は変換層（ccr）よりAnthropic互換エンドポイントへの直結が構造的に優れ、直結テンプレートはプロバイダを越えて再利用される（EXP-013/014）。** qwen3.8-max（DashScope）とkimi-k3（Moonshot）を`ANTHROPIC_BASE_URL`直結で接続すると、ccrスタックで繰り返された失敗モード（usage欠落→別タブ構築、transformerチェーン調整、ストリームのストール）が全て消滅——両実験ともPhase 0を無調整で通過・iteration 1完走（15分5秒 / 21分18秒）・セッションjsonlのusage正常。EXP-014はEXP-013のハーネスでenv 3要素（エンドポイント/キー/モデルID）だけを差し替えてそのまま動作——方法がプロバイダ非依存。直結は計測もClaude標準経路（jsonl + message.id dedup）に回帰させ、6番の標準化先行課題を部分的に解消するが、キャッシュ計上方式はプロバイダごとに異なる（Moonshotはcache_create 0計上）。ccr比の比較はモデルが異なるためスタック・モデル効果が交絡——プロバイダがAnthropic互換エンドポイントを提供するなら直結を既定の選択肢とするが、スタック間の定量比較には同一モデル実験が必要。**再現性はn=3で確定（EXP-016）**：Codex×gpt-5.6-sol・qwen直結・kimi直結の3条件それぞれ3/3完走（合算9/9、8/9がiter 1）——ただし完走以外の指標（時間・コミット・output）は同条件でも最大3倍変動し（kimi 21分→7分台）、S軸の「軌跡変動は定常ノイズ」という結論がM軸でも成立。完走率だけが安定した指標である。**韓国語条件も完走率を損なわない（EXP-017/019）**：韓国語正本（全成果物の韓国語指示）でqwen・kimi・Opus 4.8・Opus 5・Codex×gpt-5.6-solの5条件それぞれ3/3、**累計15/15 iter 1完走**、コミット・README全て韓国語・言語逸脱0——英語圏モデル（gpt-5.6-sol）まで遵守し、韓国語の履行はモデル系統ではなく指示遵守の問題と判明。時間・コミット・outputもEXP-019の3条件全てEN分布と重なる——qwenのko +48%時間（EXP-017）は例外事例で、方向性の記録としてのみ残す（L-01原則）。モデルプロファイル（4.8単一コミット vs 5細かく刻む）は言語反転後も維持。**ただし直結の再現性はプロバイダに従属する（EXP-018）**：EXP-015完走の翌日、UpstageがAnthropic互換エンドポイントとsolar-open2 hosted APIを予告なく終了（申請制ベータ終了）し再現の窓が閉じた——サードパーティのベンチマークは実験時点の明記が再現性主張の限界を規定し、ハーネス再利用前のプロバイダスモークが必須。2週間後にエンドポイントがsolar-pro4として復旧し直結3/3完走を確認（EXP-020）——完走能力は直結上位と同等だが有効時間119–258分（qwenの8–17倍）の最長プロファイルで、原因はキャッシュ非対応（全呼び出しcache 0、毎回約8万トークンを再プリフィル）・往復37秒・thinking 88%の積。**注意：solar-open2・solar-pro4のエンドポイントは商用提供（GA）APIではなくプレビュー（申請制ベータ）状態**で、基盤制約（prompt caching非対応、長い往復遅延、予告なしのエンドポイント終了）が常時かかっており、Solar系の時間・usageプロファイルはモデル能力とプレビュー基盤特性が交絡した値——商用基盤基準の性能として読まないこと。ゲート誤棄却の3例目（グローバルnpm汚染がhurlバイナリを隠した）により**採点バイナリの絶対パス固定**の教訓を追加。
8. **出力量拡大プロファイルは世代ではなくモデル固有の特性である（EXP-023）。** Claude 5世代の上位モデルFable 5.1は同一ハーネス・EN正本で3/3 iter 1完走しつつ、output 28.7–35.8K・6.2–7.8分でOpus 4.8の分布（29.6–37.1K・7.8–8.7分）と重なり、Opus 5（41.1–48.4K・8.9–17.6分）とは重ならなかった。EXP-010が「世代特性」と確定したOpus 5のoutput・コミット拡大は同世代の上位モデルで再現しないため、Opus 5固有のプロファイルとして再解釈する（n=3・時点差7週、方向性の記録）。

9. **DeepSeek V4.1-Flashは直結標準を無調整で通過し、全条件最速帯・最低コストのプロファイルを示した（EXP-025）。** env 3要素の差し替えだけでFlash・V4-ProともEN・KO各3/3、計12/12 iter 1完走（応答modelフィールド全件維持）。Flash EN 4.6–6.0分・runあたり換算約$0.1（キャッシュヒット入力$0.006/M）でCodex×sol（5.3–10.0分）より下の帯、Proは12–16分・約$0.5でoutputが1.5倍。時点・ハーネスの交絡により速度・コスト優位は確定せず、直結再利用性の事例（4社目）とプロファイル記録として残す。
10. **Opus 5.5はモデルIDの差し替えだけでネイティブハーネスを通過し、ネイティブClaude条件中で最短・最低出力のプロファイルを示した（EXP-026）。** EN・KO各3/3、計6/6 iter 1完走（再検証各2回一致）。6 run中5 runが4.0–4.2分・output約20KでFable 5.1（6.2–7.8分・28.7–35.8K）とOpus 5（8.9–17.6分・39–49K）の分布より下にあり、KOでも同じ帯を維持した。第8項の解釈（出力量拡大はOpus 5固有の特性）と整合する。ただし時点・CLIバージョンが異なる基準線との並置かつn=3の観測であり、速度優位は同時期の交差再測定まで確定しない。

## 実験ライフサイクル

1. `templates/experiment-readme.md` をコピーして `experiments/NNN-名前/README.md` に実験設計を書く（仮説、条件、測定方法、成功基準）
2. 条件ごとにセッションを実行し、セッションログ・測定結果を `runs/<条件名>/` に保存
3. `report.md` にトークン差の分析と結論を書く——ヘッダーに `- 가설: [코드](...) — ...` と `- **판정: ...** — <要約一文>` の形式を守る（README自動生成がこの2行をパースする）
4. `hypotheses/catalog.md` の状態を更新（未実験 → 進行中 → 検証/棄却）
5. `scripts/readme_i18n.json` に新実験の英・日・中翻訳（タイトル・仮説・判定・要約）を追加する——欠落時は該当言語のREADMEに韓国語原文が入り、スクリプトが警告する
6. `report.md` のコミット時にpre-commitフックが4つのREADME（ko/en/ja/zh-CN）の実験結果セクションを自動更新する。新規クローンしたら最初に1回 `git config core.hooksPath hooks` を実行（手動更新: `python3 scripts/update_readme_results.py`）

## ディレクトリ構成

```
├── ideation.md            # 最初のアイデーション（原本維持）
├── ROADMAP.md             # 段階別ロードマップ
├── hypotheses/catalog.md  # 仮説カタログ + 実験状態表
├── experiments/           # 実験単位ディレクトリ（NNN-名前/）
│   └── 001-ralph-vs-plan-then-execute/
├── tasks/                 # 共通課題仕様（条件間で再利用）
│   └── realworld-backend/
├── templates/             # 実験設計・報告書テンプレート
├── scripts/               # 測定・集計ラッパースクリプト
└── docs/specs/            # 設計文書
```
