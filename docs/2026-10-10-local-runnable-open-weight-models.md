# 로컬 실행 가능 오픈 웨이트 모델 조사 (2026-10-10)

## 목적과 범위

이 문서는 다음 벤치마크 후보를 고르기 위한 조사 기록이다. 대상은 **가중치가 공개되어 로컬 장비 한 대에서 실행할 수 있는 모델**이다. 실험 자체는 기존 실험과 같이 제공자의 클라우드 API로 실행한다. 로컬 서빙(Ollama·llama.cpp·vLLM·MLX)으로 실험하는 것은 이 조사의 범위가 아니다.

기준 장비는 세 가지다.

| 장비 | 메모리 | 메모리 대역폭 |
|---|---|---|
| NVIDIA DGX Spark (GB10) 1대 | 통합 128GB | 약 273 GB/s |
| Mac Studio 256GB | 통합 256GB | M3 Ultra 819 GB/s, M5 Ultra 약 1.2 TB/s |
| Mac Studio 512GB | 통합 512GB | 같음 |

M5 Ultra Mac Studio는 2026-08-25 발표되었고 512GB 구성은 2026-10월 말 출하 예정이다([Macworld](https://www.macworld.com/article/3220024/apple-announces-the-m5-ultra-mac-studio-with-up-to-512gb-of-ram.html)).

## 근거 수준

- **직접 확인(2026-10-10)**: 제공자 모델 목록 조회(`GET /v1/models`), DashScope Anthropic 호환 엔드포인트 응답, Hugging Face 모델 API의 라이선스·파라미터 수. 아래 표에 "확인"으로 표시한다.
- **웹 조사(2차 자료 포함)**: 양자화 크기, 디코드 속도, 벤치마크 점수, 가격. 대부분 제조사 발표나 커뮤니티 측정이며 서로 비교 가능한 조건이 아니다. 이 리포에서 측정한 값이 아니다.
- "128K 컨텍스트를 포함해 탑재 가능" 판정은 가중치 크기와 KV 캐시 추정에서 계산한 추정이다. 실측하지 않았다.

## 장비별 후보

| 모델 (HF ID) | 전체 / 활성 파라미터 | 라이선스 | 양자화와 가중치 크기 | 탑재 가능 장비 (추정) |
|---|---|---|---|---|
| `Qwen/Qwen3.8-Flash-Next` | 125B / 6B (+51B n-gram 임베딩, safetensors 합계 약 180B 확인) | other (Qwen Community 1.0) 확인 | NVFP4 약 99GiB + 임베딩 27GiB(디스크 mmap) | Spark(빠듯함)·256·512 |
| `Qwen/Qwen3-Coder-Next` | 약 80B / 3B (79.7B 확인) | Apache-2.0 확인 | Q4_K_M 약 48GB | 세 장비 모두 |
| `Qwen/Qwen3.8-27B` | 27.8B dense 확인 | Apache-2.0 확인 | 4비트 약 16GB, FP8 약 28GB | 세 장비 모두 |
| `openai/gpt-oss-120b` | 117B / 5B 확인 | Apache-2.0 확인 | MXFP4 약 65GB | 세 장비 모두 |
| `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B` | 31.6B / 3B 확인 | other 확인 | BF16 약 63GB, 4비트 약 18GB | 세 장비 모두 |
| `Qwen/Qwen3.6-35B-A3B` | 36B / 3B 확인 | Apache-2.0 확인 | NVFP4 약 20GB | 세 장비 모두 |
| `zai-org/GLM-5.3-Flash` | 320B / 18B | MIT | 4비트 MLX 177.6GB | 256·512 |
| `deepseek-ai/DeepSeek-V4-Flash` | 284B / 13B | MIT | 4비트 MLX 151GB | 256·512 (Spark는 약 2비트에서만) |
| `MiniMaxAI/MiniMax-M3` | 약 428B / 23B | MiniMax Community | 4비트 약 240GB | 512 |
| GLM-5.3 (전체) | 약 743B / 40B | 미확인 | Q3 343GB | 512 (3비트) |
| `moonshotai/Kimi-K2.7-Code` | 1T / 32B | Modified MIT (2차 자료) | 2비트 339GB | 512 (2비트) |

512GB에도 올라가지 않는 모델: DeepSeek-V4-Pro(1.6T), Kimi K3(2.8T), Qwen3.8-Max. 크기 출처는 [Pinggy](https://pinggy.io/blog/self_hosting_llms_on_512gb_m5_ultra_mac_studio/)와 각 HF 모델 카드다.

### 보고된 디코드 속도 (단일 스트림, 2차 자료)

| 장비 | 모델·양자화·스택 | tok/s | 출처 |
|---|---|---|---|
| Spark | Qwen3.8-Flash-Next NVFP4, vLLM, MTP | 48.7 | [ThreatFrontier](https://threatfrontier.com/articles/best-local-ai-models-to-run-on-your-dgx-sparks) |
| Spark | Qwen3-Coder-Next Q4_K_M, Ollama | 47.0 | [ai-muninn](https://ai-muninn.com/en/blog/dgx-spark-ollama-benchmark-8-models) |
| Spark | gpt-oss-120b MXFP4, Ollama | 42.4 | 같음 |
| Spark | Qwen3.6-35B-A3B NVFP4 | 약 106 | [noze.it](https://www.noze.it/en/insights/dgx-spark-local-models-august-2026/) |
| M5 Ultra | Qwen3.8-Flash-Next, MLX | 90.7 (4K) / 60.6 (128K) | [Context Studios](https://www.contextstudios.ai/blog/mac-studio-m5-ultra-local-ai-guide) |
| M5 Ultra | GLM-5.3-Flash, MLX | 41 | [MacStories](https://www.macstories.net/stories/m5-ultra-mac-studio-review-the-dream-mac-for-local-ai-agents/) |
| M3 Ultra 512GB | GLM-5.2 4비트 | 17.7 | Pinggy |

### 제조사 발표 코딩 점수

서로 다른 조건과 하네스에서 낸 값이라 직접 비교할 수 없다.

| 모델 | SWE-bench Verified | SWE-bench Pro | Terminal-Bench |
|---|---|---|---|
| MiniMax-M3 | 80.5 | 59.0 | 66.0 |
| DeepSeek-V4-Flash | 79.0 | 52.6 | 56.9 (2.0) |
| GLM-5.3-Flash | 미공개 | 미공개 | 84.3 (2.1, Claude Code) |
| Qwen3.8-Flash-Next | 미공개 | 62.5 | 미공개 |
| Qwen3-Coder-Next | 70.6 | – | – |

## 클라우드 API 연결 경로

이 리포의 하네스 규칙(CLAUDE.md)은 제공자의 Anthropic 호환 엔드포인트 직결(`claude-direct`)을 기본으로 하고, 없으면 pi 하네스로 OpenAI 호환 엔드포인트에 직결한다. ccr·OpenRouter의 Anthropic 변환처럼 요청 형식을 바꾸는 계층은 쓰지 않는다.

| 모델 | 제공자 모델 ID | 경로 | 상태 (2026-10-10) |
|---|---|---|---|
| Qwen3.8-Flash-Next | `qwen3.8-flash` | DashScope `/apps/anthropic` → `claude-direct` | 응답 확인. API 모델이 HF 공개 가중치와 같은지는 공식 확인 안 됨 |
| Qwen3-Coder-Next | `qwen3-coder-next` | DashScope `/apps/anthropic` → `claude-direct` | 응답 확인 |
| Qwen3.8-27B | `qwen3.8-27b` | DashScope `/apps/anthropic` → `claude-direct` | 응답 확인 |
| Qwen3.6-35B-A3B | `qwen3.6-35b-a3b` | DashScope `/apps/anthropic` | 정상 응답 없음. 같은 계열 최신 세대(3.8)를 포함하므로 제외 |
| gpt-oss-120b | `openai/gpt-oss-120b` | Hugging Face 라우터(OpenAI 호환) → `pi` | 목록에 있음(하위 제공자 10곳, 모두 tools 지원). 계정 크레딧 부족으로 호출 실패 |
| Nemotron-3.5-Lightning | `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16` | Hugging Face 라우터(fireworks-ai) → `pi` | 계정에서 해당 하위 제공자가 비활성이라 호출 실패 |
| GLM-5.3-Flash / GLM-5.3 | `glm-5.3-flash` / `glm-5.3` | Z.ai `/api/anthropic` | 미확인. 공식 문서는 Coding Plan 기준. 키 없음 |
| MiniMax-M3 | `MiniMax-M3` | MiniMax `/anthropic` (공식 문서) | 미확인. 키 없음 |
| Kimi-K2.7-Code | `kimi-k2.7-code` | Moonshot `/anthropic` (EXP-014 검증 제공자) | 미확인 |

가격(100만 토큰당 입력/출력, 2차 자료 포함): qwen3.8-flash 약 $0.16/$0.47, GLM-5.3-Flash $0.15/$0.50, MiniMax-M3 $0.30/$1.20, GLM-5.3 $1.40/$4.40, Kimi-K2.7-Code $0.95/$4.00, gpt-oss-120b는 HF 하위 제공자별 $0.04-0.35/$0.17-0.75.

## 결정 (2026-10-10 사용자 지시)

- 첫 단계는 **DGX Spark 1대에 올릴 수 있는 모델**을 벤치마크한다.
- Anthropic 호환 엔드포인트가 있으면 `claude-direct`, 없으면 `pi`로 실행한다.
- 256GB·512GB 등급(GLM-5.3-Flash, MiniMax-M3 등)은 후속 단계로 둔다. 해당 제공자 키 확보와 엔드포인트 스모크가 선행 조건이다.

## 확인하지 않은 것

- DashScope `qwen3.8-flash`가 HF `Qwen3.8-Flash-Next`와 같은 가중치인지.
- Qwen3.8-Flash-Next가 Spark에서 128K 컨텍스트로 실제 동작하는지(임베딩 mmap 포함 빠듯함).
- GLM-5.2/5.3 라이선스, Kimi-K2.7-Code 공식 모델 카드.
- Devstral, Gemma, Llama 계열은 조사하지 않았다.
