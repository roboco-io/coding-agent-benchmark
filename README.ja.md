# Vibecoding Token Experiments

🌐 [English](README.md) · [한국어](README.ko.md) · **日本語** · [中文](README.zh-CN.md)

本プロジェクトは**Ralphループを使うモデル・ハーネスの組み合わせによるバックエンド実装性能**を比較する。課題・品質・予算に応じた実務上の選択が目的である。初期の戦略比較は研究履歴として保存する。

## 実験方法論

- 比較単位：**モデル × ハーネス × 推論設定 × 提供者・接続環境**。Claude CodeとCodexを含む。組み合わせの差をモデル単独の効果と断定しない。
- 基本課題：[RealWorldバックエンド](tasks/realworld-backend/)。既存コードのバグ修正・機能追加・DB移行へ拡張する計画。
- 主指標：**予算内合格率・失敗込みの費用・時間・人の介入量**。トークン代理指標と請求費用は区別する。
- [品質規則](docs/experiment-quality-rules.md)、[訂正記録](docs/2026-09-21-corrections.md)、[ロードマップ](ROADMAP.md)。
- 次のパイロット：Claude Code + Fable 5.1 対 Codex + Astra。[設計](experiments/024-practical-combinations/README.md)。

## 研究軸

優先はモデル・ハーネスと課題タイプの比較。戦略(S)・トークン習慣(H)・言語(L)は診断軸として[カタログ](hypotheses/catalog.md)に保存する。

## 実験結果

> 以下の表と実験別要約は [`scripts/update_readme_results.py`](scripts/update_readme_results.py) が各実験の `report.md` から自動生成する（英・日・中の README は [`scripts/readme_i18n.json`](scripts/readme_i18n.json) の翻訳を使用）。実験が終わり `report.md` がコミットされる際に pre-commit フックが自動実行する（手動実行: `python3 scripts/update_readme_results.py`）。

**📊 ライブダッシュボード**: [Ralphループ モデル別完走比較](https://roboco.io/coding-agent-benchmark/) —— 最新実験反映: EXP-030（2026-09-24）

> 外部ダッシュボードには2026-09-21の訂正が未反映。数値の判断は以下の報告書と訂正記録を参照。

<!-- RESULTS:BEGIN -->
<!-- このブロックは scripts/update_readme_results.py が experiments/*/report.md から自動生成する（翻訳は scripts/readme_i18n.json）。直接編集禁止。 -->

| 実験 | 仮説 | 判定 |
|------|------|------|
| [EXP-001](experiments/001-ralph-vs-plan-then-execute/report.md) Ralphループ vs Plan-then-execute | S-01: Plan-then-executeはRalphループより同一課題でトークンを少なく使う | **観測範囲で棄却** |
| [EXP-002](experiments/002-korean-vs-english/report.md) 韓国語 vs 英語パイプラインのトークン比較 | L-01: 全パイプラインを英語で進めると韓国語比でtoken proxyトークンが有意に減る | **保留** |
| [EXP-003](experiments/003-pte-skills/report.md) PTE + スキル式の段階的開示 | S-02: コンテキストをスキル公式推奨（文書200行以下、スキルで必要なものだけロード）で構造化すればEXP-001のPTE比でtoken proxyが30%以上減る | **基準未達（訂正）** |
| [EXP-004](experiments/004-ralph-skills/report.md) Ralphループ + スキル構造 | S-03: 単一セッションのralphにドメイン契約スキルを与えるとtoken proxyが減る | **保留** |
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
| [EXP-027](experiments/027-gpt6-sol-luna-codex/report.md) Codex CLI × gpt-6-sol・gpt-6-luna Ralphループ完走検証（各n=3） | M-20: Codex CLI（`codex exec`）ハーネスで、gpt-6-sol・gpt-6-luna（effort medium）はそれぞれ隔離・無介入のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration・4時間以内に完走できる（各n=3）。 | **検証** |
| [EXP-028](experiments/028-sonnet5-ralph/report.md) Claude Code × Sonnet 5 ネイティブRalphループ完走検証（EN・KO各n=3） | M-21: Claude Codeネイティブハーネスで、Sonnet 5（`claude-sonnet-5`、thinkingデフォルト）はEN・KO正本のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限10 iteration・4時間以内に無介入で完走できる（EN・KO各n=3）。 | **検証** |
| [EXP-029](experiments/029-pi-openweight/report.md) pi coding agent × kimi-k3・qwen3.8-max・deepseek-flash Ralphループ完走検証（EN各n=3） | M-22: pi coding agent（`pi -p` v0.87.1）を各提供者のOpenAI互換エンドポイントに直結して`kimi-k3`・`qwen3.8-max`・`deepseek-flash`（thinkingはpiデフォルト）を動かすと、隔離・無介入のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration・4時間以内に完走できる（EN各n=3、完走率で判定・課金は対象外）。 | **検証** |
| [EXP-030](experiments/030-pi-frontier/report.md) pi coding agent × Opus 5.5・gpt-6-sol Ralphループ完走検証（EN各n=3） | M-23: pi coding agent（`pi -p` v0.87.1）で`anthropic/claude-opus-5-5`（Anthropic APIキー直結）と`openai-codex/gpt-6-sol`（ChatGPT OAuth）をpiデフォルトのthinkingで動かすと、隔離・無介入のRalphループでRealWorldバックエンド（Hurl 13/13・154/154）を上限30 iteration・4時間以内に完走できる（EN各n=3、完走率で判定・課金は対象外）。 | **検証** |

**EXP-001 — Ralphループ vs Plan-then-execute** (観測範囲で棄却)  
重複除去後のトークン代理指標はPTE 1,128,420、Ralph 136,506（8.27倍）。採点セットが異なるため同品質の費用比較ではない。 → [レポート](experiments/001-ralph-vs-plan-then-execute/report.md)

**EXP-002 — 韓国語 vs 英語パイプラインのトークン比較** (保留)  
KO平均114,605.5、EN平均112,463.5。平均差2,142は条件内の最大範囲23,033を下回る。 → [レポート](experiments/002-korean-vs-english/report.md)

**EXP-003 — PTE + スキル式の段階的開示** (基準未達（訂正）)  
トークン代理指標は22.45%減少（1,128,420 → 875,083）。事前基準30%未達のため検証判定を撤回。 → [レポート](experiments/003-pte-skills/report.md)

**EXP-004 — Ralphループ + スキル構造** (保留)  
スキルrunは117,352 / 118,311、KO基準比平均+2.81%。範囲は959で、無効果・2倍の変動という解釈を撤回。 → [レポート](experiments/004-ralph-skills/report.md)

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

**EXP-027 — Codex CLI × gpt-6-sol・gpt-6-luna Ralphループ完走検証（各n=3）** (検証)  
**sol 3/3・luna 3/3 全てiteration 1で完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、応答modelフィールド全件一致）。セッション: sol 4.8–5.2分・output 10.4–11.0K、luna 5.4–10.0分・output 13.4–21.5K。採点インフラのハング1件（D-1）はエージェントに介入せず処理し判定に影響なし。`ralph-model-benchmark`スキルで実施した最初の実験。観測値であり順位の確定ではない。 → [レポート](experiments/027-gpt6-sol-luna-codex/report.md)

**EXP-028 — Claude Code × Sonnet 5 ネイティブRalphループ完走検証（EN・KO各n=3）** (検証)  
**EN 3/3・KO 3/3 完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0、応答modelフィールドは全メッセージ`claude-sonnet-5`）。5 runはiteration 1で完走し、en-1はエージェント自身が作業を3 iterationに分けてiteration 3で完走（rejectedなし）。セッション11.2–16.8分・output 57.6–73.7Kで、同じハーネスのOpus 5.5（EXP-026）・Fable 5.1（EXP-023）の観測範囲より上。観測値であり順位の確定ではない。 → [レポート](experiments/028-sonnet5-ralph/report.md)

**EXP-029 — pi coding agent × kimi-k3・qwen3.8-max・deepseek-flash Ralphループ完走検証（EN各n=3）** (検証)  
**3条件すべて3/3完走**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0、応答modelフィールドは全件一致）。8 runはiteration 1で完走し、qwen-en-1は採点ポートを外部プロセスが占有していたためiteration 5で完走と記録された（iteration 1のコードも再採点で通過）。セッションはflash 1.9–4.1分（D-3再実行を反映）、kimi 9.5–9.9分、qwen 15.6–29.0分。このリポで初めての第3のハーネス（pi）であり、過去のClaude Code直結runとの比較はハーネスとAPI形式が交絡する。観測値であり順位の確定ではない。 → [レポート](experiments/029-pi-openweight/report.md)

**EXP-030 — pi coding agent × Opus 5.5・gpt-6-sol Ralphループ完走検証（EN各n=3）** (検証)  
**2条件とも3/3完走、6 runすべてiteration 1**（ゲートpass + 独立再検証各2回13/13・154/154一致、介入0、応答modelフィールドは全件一致）。セッションはOpus 5.5が3.1–4.9分、gpt-6-solが4.2–5.6分で、ネイティブエージェントの基準線（EXP-026 Opus 5.5 4.0–8.4分、EXP-027 gpt-6-sol 4.8–5.2分）と範囲が重なる。観測値であり順位の確定ではない。 → [レポート](experiments/030-pi-frontier/report.md)

<!-- RESULTS:END -->

### 総合インサイト（2026-09-21訂正反映）

- EXP-001の訂正後のPTE/Ralph比率は8.27倍。採点セットが異なり同品質の費用比較ではない。
- EXP-003は22.45%減で事前基準30%未達。EXP-004の2倍変動・無効果の解釈は撤回。
- 初回iterationの成功は当該条件での実装可能性を示す。反復による回復と保守性能は別途評価が必要。
- 3回の成功や異なる時点の時間から一般順位や因果関係を断定しない。サブスクリプション費用の未測定は無料を意味しない。

9. **DeepSeek V4.1-Flashは直結標準を無調整で通過し、全条件最速帯・最低コストのプロファイルを示した（EXP-025）。** env 3要素の差し替えだけでFlash・V4-ProともEN・KO各3/3、計12/12 iter 1完走（応答modelフィールド全件維持）。Flash EN 4.6–6.0分・runあたり換算約$0.1（キャッシュヒット入力$0.006/M）でCodex×sol（5.3–10.0分）より下の帯、Proは12–16分・約$0.5でoutputが1.5倍。時点・ハーネスの交絡により速度・コスト優位は確定せず、直結再利用性の事例（4社目）とプロファイル記録として残す。
10. **Opus 5.5はモデルIDの差し替えだけでネイティブハーネスを通過し、ネイティブClaude条件中で最短・最低出力のプロファイルを示した（EXP-026）。** EN・KO各3/3、計6/6 iter 1完走（再検証各2回一致）。6 run中5 runが4.0–4.2分・output約20KでFable 5.1（6.2–7.8分・28.7–35.8K）とOpus 5（8.9–17.6分・39–49K）の分布より下にあり、KOでも同じ帯を維持した。第8項の解釈（出力量拡大はOpus 5固有の特性）と整合する。ただし時点・CLIバージョンが異なる基準線との並置かつn=3の観測であり、速度優位は同時期の交差再測定まで確定しない。
11. **GPT-6系3モデル（astra・sol・luna）はいずれもCodexハーネスでモデルIDの差し替えだけで完走した（EXP-021・027）。** sol・luna各3/3 iter 1完走（応答modelフィールド全件一致）。solは3 run全て4.8–5.2分・output約11Kでばらつきが小さく、lunaは5.4–10.0分・output 13.4–21.5Kで、「fast」の位置付けに反しこの課題ではsolより短いrunはなかった。astra（EXP-021、7分台）とは時点・CLIバージョンが異なるためモデル差とは断定しない。EXP-027は新モデルのベンチマーク手順をまとめた`ralph-model-benchmark`スキルの初適用である。
12. **Sonnet 5もネイティブハーネスでEN・KOともに完走したが、同じハーネスの上位モデルより遅く出力が多かった（EXP-028）。** EN 3/3・KO 3/3完走（応答modelフィールドは全メッセージ`claude-sonnet-5`）。5 runはiteration 1で終わり、en-1はエージェントがスキャフォールド・テスト準備・実装を3 iterationに分けてiteration 3で完走した（rejectedなし）。セッション11.2–16.8分・output 57.6–73.7Kで、Opus 5.5（EXP-026、4.0–8.4分・18.6–28.2K）・Fable 5.1（EXP-023）の観測範囲より上。測定日・Claude Codeバージョンが異なるためモデル単独の差とは断定しない。
13. **第3のハーネスpiも変換レイヤーなしでオープンウェイト系3モデルで完走した（EXP-029）。** pi coding agentを各提供者のOpenAI互換エンドポイントに直結し、kimi-k3・qwen3.8-max・deepseek-flashが各EN 3/3、計9/9完走した（応答modelフィールド全件一致、ハーネスのトラブルシューティング0件）。8 runはiteration 1で終わり、qwen-en-1は採点ポートを外部プロセスが占有していたためiteration 5と記録された（iteration 1のコードも再採点で通過）。セッションはflash 1.9–4.1分（D-3再実行を反映）、kimi 9.5–9.9分、qwen 15.6–29.0分。同じモデルの過去のClaude Code直結run（EXP-013・014・025）とはハーネスとAPI形式（Anthropic互換とOpenAI互換）が同時に異なるため、差をpiの効果として分離しない。これによりRalphループベンチマークはClaude Code・Codex・piの3ハーネスで同じ手順で再現できる。
14. **piはベンダーの基準モデルでも完走した（EXP-030）。** piでOpus 5.5（Anthropic APIキー直結）とgpt-6-sol（ChatGPT OAuth）を動かし、各EN 3/3、6 runすべてiteration 1で完走した。セッションはOpus 5.5が3.1–4.9分、gpt-6-solが4.2–5.6分で、ネイティブエージェントの基準線（EXP-026 Claude Code 4.0–8.4分、EXP-027 Codex 4.8–5.2分）と範囲が重なり、outputはpi側が少なかった（Opus 5.5 16.6–19.8K対18.6–28.2K、gpt-6-sol 7.0–8.6K対10.4–11.0K）。エージェントとAPI経路（システムプロンプト・ツール・thinkingの渡し方・キャッシュTTL）が同時に異なるため、この差は組み合わせ全体の差であり、piの効果とは断定しない。

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
