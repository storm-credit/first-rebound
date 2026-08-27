# Design Orchestrator Workflow

이 문서는 `control/MASTER_WORKFLOW.md`를 실제 작업 단위로 실행하는 runbook이다. 단계의 정의가 충돌하면 Master Workflow가 우선한다.

## 총괄 원칙

- Root Orchestrator 한 명이 현재 게이트·정본·브랜치·승인을 소유한다.
- 필요한 역할만 좁게 호출하고 상시 에이전트 군단을 만들지 않는다.
- 사용자 승인 없이 하위 에이전트를 생성하지 않는다.
- 조사 역할은 정본을 바꾸지 못하고, 설계 역할은 미검증 사실을 확정하지 못한다.
- 독립 비평자는 설계자의 장황한 의도를 받지 않고 산출물·요구·제약만 검토한다.
- 모든 단계는 별도 브랜치→검증→PR→병합→상태 갱신으로 닫는다.
- `DESIGN_GATE=CLOSED` 동안 원고 파일은 0개를 유지한다.

## 역할

| 역할 | 책임 | 입력 | 출력 | 금지 |
|---|---|---|---|---|
| Root/Gate Owner | 범위·순서·승인·상태·PR | 정본과 사용자 결정 | 현재 게이트 판정 | 조사값 임의 창작 |
| Evidence Lane | 공식 규정·기록·시대 자료 | 연구 질문 | 출처 원장 | 소설 사건 결정 |
| Reference Lane | 합법적 참고작 본문 기능 분석 | 접근 가능한 표본 | KEEP/ADOPT/AVOID/RANGE | 문장·장면 모사 |
| World/Character Lane | 제도·몸·문화·관계 모델 | 검증 연구 | 분야별 정본 초안 | 실존 사생활 창작 |
| Historical Simulation Lane | 접촉·파급 사건 계산 | 원역사 원장과 Act | 대안 결과 원장 | 유명 결과 강제 복원 |
| Narrative Design Lane | 결말→Act→Sub-Act→회차 기능 | 잠긴 정본 | 구조 설계 | 원고 작성 |
| Independent Critic | 모순·맹점·반복·현실성 | 산출물·요구·제약 | PASS/HOLD/BLOCKER | 설계 의도에 편승 |

## 실행 순서

| Run | 현재 질문 | 핵심 산출물 | 다음 단계로 가는 조건 |
|---|---|---|---|
| R00 | 저장소 상태가 무엇인가? | State/Freeze/Gate 복구 | 충돌 목록 작성 |
| R01 | 어느 NBA 시대인가? | `ERA_SELECTION.md` | 사용자 E0 LOCK |
| R02 | 연표가 제도적으로 가능한가? | 출생→고교→프렙→NCAA→드래프트 역산 | 날짜·나이·자격 PASS |
| R03 | 세계는 어떻게 작동하는가? | 한국/프렙/NCAA/NBA/문화/경제 원장 | 핵심 규칙 VERIFIED |
| R04 | 누구의 이야기인가? | 인물·관계·신체·기술 성장 정본 | 욕망·결핍·비용 연결 |
| R05 | 무엇으로 끝나는가? | Ending/Theme v1 | 시작과 결말 대응 PASS |
| R06 | 실제 역사는 어디까지 유지되는가? | Baseline/Causality Ledger | 접촉·파급 분류 PASS |
| R07 | 어떻게 읽히게 할 것인가? | 참고작 딥리드와 House Style | 실제 본문 표본과 합성 완료 |
| R08 | 커리어 전체가 어떻게 변하는가? | Master Architecture | 시즌별 역할·비용·보상 |
| R09 | 큰 덩어리가 작동하는가? | Act Map | 모든 Act 상태 변화 |
| R10 | 중간 덩어리가 작동하는가? | Sub-Act Map | 주 장치 1개와 종료 상태 |
| R11 | 연재가 끊기지 않는가? | Episode Function Map | 삭제 가능한 회차 0 |
| R12 | 회차 입력이 안전한가? | Context Packs | 출처·버전·연속성 PASS |
| R13 | 전체가 한 작품인가? | Unity/Traction Review | 중복·혼합·정체성 충돌 0 |
| R14 | 설계자가 놓친 것은 무엇인가? | Independent Review | HOLD/BLOCKER 0 |
| R15 | 집필을 열어도 되는가? | 사용자 승인 PR | Gate OPEN |

## 매 Run 화면에 보여 줄 진행표

```markdown
현재 Run:
목표:
읽은 정본:
조사 중:
완료 산출물:
검증 결과:
HOLD/BLOCKER:
다음 Run:
원고 게이트: CLOSED
```

## 단계 내부 루프

1. 현재 정본을 읽는다.
2. 다음 결정을 막는 질문만 추린다.
3. 중요한 선택이면 4개 시안을 비교한다.
4. 맹점·함정·복제 위험을 검사한다.
5. 공식/1차 자료를 우선해 조사한다.
6. 권위 문서 한 곳에만 반영한다.
7. 별도 관점으로 수용 기준을 검사한다.
8. `PROJECT_STATE.md`와 결정 로그를 갱신한다.
9. PR을 병합한 뒤 다음 Run으로 이동한다.

## 중단 조건

- 사용자 선택이 필요한 E0/중심 정본 결정
- 공식 자료가 충돌하거나 해당 연도 규정을 확보하지 못함
- 참고작 실제 본문 접근이 필요한데 로그인·구매가 필요함
- 기존 정본과 새 조사 결과가 충돌함
- 원고 작성 요청이 들어왔지만 Design Gate가 CLOSED임

중단은 실패가 아니다. 필요한 결정 또는 증거만 정확히 요청한다.
