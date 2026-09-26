# Research/Verification Layer v2 — 기존 워크플로의 조사·검증 부속 절차

- 상태: `READY_FOR_TRIAL / NOT_A_CANON_OR_GATE_REPLACEMENT`.
- 적용 위치: `control/MASTER_WORKFLOW.md`의 조사와 변경 후 검증, `control/ORCHESTRATOR_WORKFLOW.md` R09–R16 사이. 기존 PR→main, 단일 권위, 사용자 확정, `DESIGN_GATE`의 G16/G17 순서를 유지한다.
- 현재 시험 대상: O-15G15 Suggs 개막 이전 prior와 Orlando 12분. 과거 완료 원장을 전량 반복하지 않는다.
- [2026-09-26 CLI 시범과 후속 재시험](../reviews/O15G15_V2_CLI_PILOT_20260926.md): NotebookLM 출처 연결 분석과 Anti-Gravity → NotebookLM MCP 호출은 실행됐다. Anti-Gravity의 독립 NBA 출처 팩은 아직 0건이며 Claude 실행 결과는 없다. 도구 출력이나 인포그래픽은 단독으로 정본의 근거가 되지 않는다.

## 현재 실행 연결

- **Codex → Anti-Gravity:** 설치된 `C:\Users\Storm Credit\AppData\Local\agy\bin\agy.exe`를 절대 경로로 호출한다. 2026-09-26 로컬 확인에서 `--version`은 `1.2.11`, `models`는 서비스의 모델 목록을 정상 반환했다. `agy`가 셸 검색 경로에 없다는 사실만으로 연결 실패라고 판정하지 않는다.
- **Anti-Gravity → 외부 MCP:** 이 CLI는 MCP 클라이언트다. 사용자 확인 기준으로 Codex·NotebookLM·프로젝트별 Obsidian 서버가 설정돼 있다. 이 시범에서 실제 도구 호출까지 확인한 서버는 **NotebookLM**뿐이다. 다른 서버의 설정·활성 표시는 통신 성공의 증거가 아니다. Codex가 Anti-Gravity를 사용하기 위해 Anti-Gravity를 MCP 서버로 등록할 필요는 없다.
- **분석·검증:** Anti-Gravity의 원자료와 NotebookLM의 출처 연결 분석을 총괄이 후보 판정에 사용하고, Codex는 저장소 검증, Claude는 독립 반증, source-blind 검수는 결과물 자체의 맹점을 맡는다. 마지막 연구 판정도 G16 독립 검수와 G17 작가 승인을 대신하지 않는다.

## 단계·전용 책임·인수 기준

| 단계 | 받는 입력 | 전용 질문·산출물 | 다음 단계에 넘길 조건 |
|---|---|---|---|
| 0. 총괄 프롬프트 잠금 | 최신 main SHA, State/Freeze/Gate, 해당 권위, 정확 연구 질문 | 사실/추론/후보/작가확정 및 시간 방화벽을 먼저 명시한 작업 지시 | 선행 승인 재질문·원고 요청·과거 권위 덮어쓰기 없음 |
| 1. Anti-Gravity Evidence Lane | 필요한 원역사 사건·규정·시즌 | 원문 링크, 작성/게시/사건일, 팀·선수·경기 ID, 접근 상태, 정확 인용 위치를 가진 Evidence Pack | 공식 1차 자료 우선, 서로 다른 출처의 실제 독립성 기록, 접근 불가 null |
| 2. NotebookLM Analysis Lane | 읽기 전용 Evidence Pack + 현재 설정집 사본 | 연표/관계/출전시간/계약·픽/충돌의 **출처 연결 분석**; 인포그래픽은 탐색용 | 각 노드에 출처·시점·불확실성, 근거 없는 합성은 HOLD |
| 3. 총괄 판정 | 1·2단계와 활성 권위 | 상호 배타적 4안, 농구/개연성/관계/웹소설 흥미/나비효과 비용 비교 | 추천과 작가확정 분리, 정본 변경 범위 명시 |
| 4. Codex 저장소 감사 | 승인된 범위의 후보 변경 | 권위 충돌·연표·분/로스터/급여 보존·해시/JSON/링크/중복·회귀 검사 | 브랜치·검사 로그·PR diff, 재현 불가 값 HOLD |
| 5. Claude 독립 반증 | 정본 불변값과 PR diff, 원자료 위치. 총괄의 장황한 설득문 제외 | ‘이 설계가 틀렸다’는 가설 아래 반례·누락된 실제 선수 비용·규정·캐릭터 붕괴를 찾음 | 각 지적을 재현 절차·심각도·원자료로 제시. 도구 사용 불가 시 `NOT_RUN` |
| 6. Source-blind 맹점 | 결론·추천·검토 이력·선행 점수 제거한 결과물과 불변 제약 | 처음 보는 편집자 시각의 미심쩍은 인과, 초점 이탈, 실존 스타 편의, 독자 흥미 빈자리 | 독립성 한계·새로운 반례만 판정. 근거가 필요한 주장은 다시 1단계로 환류 |
| 7. 총괄 수렴 | 4–6의 지적과 새 증거 | 수용/기각/HOLD를 증거별 기록, State/Decision Log·권위 정렬 | G16 전체 독립 검수·G17 작가 승인 대체 금지; 검증 PR→main 뒤 다음 Run |

같은 원문이나 같은 모델 결론을 여러 도구에 전달한 것만으로 독립 검증 횟수를 늘리지 않는다. Codex의 재현 검사는 **내부 일관성**, Claude는 **반증**, source-blind는 **편집상 의심**을 맡는다. 둘 이상이 동일한 원문 오류를 공유할 수 있으므로 출처 계보를 보존한다. 단계가 실행되지 않았으면 `NOT_RUN`, 직접 확인되지 않았으면 `HOLD`로 기록한다.

## 복사 가능한 전용 지시

### Anti-Gravity — 원자료 수집

> 질문: [정확한 시즌·경기·선수·규정·거래]. [main SHA] 이후의 기존 Evidence Pack은 반복 수집하지 말고 빈칸만 채워라. 각 주장에 원문 URL, 발행/사건일, 원문 위치, 공식/2차 분류, 접근 여부, 원역사와 대체세계 적용 차이를 기록하라. 추정치를 사실처럼 쓰지 말고 미확보는 null/HOLD로 반환하라. 작품의 선택이나 정본 확정은 하지 마라.

### NotebookLM — 연결 분석

> 제공된 고정 Evidence Pack과 설정집 사본만 사용하라. 각 연표·관계·로스터·분·계약/픽 노드에 자료 식별자와 날짜를 붙이고 서로 충돌하는 노드를 출력하라. 인포그래픽에는 사실/추론/후보 범례와 불확실한 연결을 표시하라. 새로운 출처나 임의 숫자를 만들지 말고, 불일치는 질문으로 반환하라.

### 총괄 — 후보 판정

> 최신 정본을 유지하면서 현재 막힌 질문 하나에 상호 배타적 네 후보를 비교하라. 각 후보의 원역사 접촉, 실존 선수 분·권리·수상 비용, 후속 시즌 나비효과, 인물 성장, 독자 흥미를 적고 사실·추론·후보·작가확정을 표시하라. 추천은 작가확정으로 쓰지 말고 HOLD와 다음 증거를 지정하라.

### Codex — 저장소 감사

> PR diff를 권위 지도와 대조하고 기존 완료 작업 중복, 연표·등록·분/포제션·계약/CBA·픽 자산 보존, JSON 재현성·링크·해시·게이트 플래그를 검사하라. 숫자 표와 본문이 다른 곳을 파일·행·재현 명령으로 보고하라. 통과 범위와 미검증 범위를 분리하고 State를 갱신하라.

### Claude — 독립 반증

> 이 변경이 틀렸다고 가정하라. 정본 불변값과 결과 diff, 원자료만 보고 NBA 역사/CBA/인과/실존 선수 출전 비용/주인공 성격·성장/장기 웹소설 구조의 반례를 찾아라. 총괄 추천의 의도에 기대지 말고 가장 이른 반례부터 제시하라. 각 지적은 심각도, 원문 링크, 재현 조건, 수정 가능한 최소 범위를 기록하라. 증거가 없으면 의심으로 표시하라.

### Source-blind — 마지막 맹점 검수

> 이전 분석·추천·승인 논리를 보지 않은 편집자로서 결과물과 작품의 고정 제약만 읽어라. ‘왜 이런 일이 일어나나’, ‘누가 분·돈·권한을 잃나’, ‘실존 역사를 편의상 복구했나’, ‘조용한 주인공의 책임 성장과 NBA 중심성이 보이나’, ‘장기 독자가 계속 읽을 이유가 있나’를 물어라. 원문 검증이 필요한 의심과 결과물 자체의 논리 결함을 구별하라. 앞 검토자의 결론을 맞히려 하지 마라.

## 시범 적용 기록 양식

| 필드 | 필수값 |
|---|---|
| 시작점 | main SHA, 활성 권위, 이번에 닫으려는 HOLD |
| 자료 계보 | 자료 ID/URL/발행일/접근일/원역사 적용 범위 |
| 출력 상태 | `VERIFIED`, `INFERENCE`, `CANDIDATE`, `AUTHOR_LOCKED`, `HOLD`, `NOT_RUN` |
| 검증 독립성 | 독립 원자료·독립 검토자 여부, 공유 전제 |
| 파급 | 접촉 경기→분/등록/계약/픽/플레이오프→다음 시즌 |
| 종료 | 테스트·PR·State, 남은 HOLD, 게이트 플래그 |

G15F까지의 시범 상태는 로그인 복구 후 Anti-Gravity `RUN / NO_VERIFIED_EVIDENCE_PACK`, NotebookLM `RUN / SOURCE_LINKAGE_ONLY_WITH_CORRECTIONS`, Claude `NOT_RUN`; Codex 조사/저장소 감사와 총괄의 후보 분리는 `IN_PROGRESS`; source-blind 독립 검수는 `NOT_RUN`이었다. [실행 기록](../reviews/O15G15_V2_CLI_PILOT_20260926.md)과 [원자료 대조](../research/O15G15C_ORLANDO_CONTRACT_CHRONOLOGY.md) 참조. 뒤의 G15H 제한 검토와 결과물 단독 검수는 아래에 시간순으로 기록한다. 이 표시는 검수 횟수나 G16 PASS를 부풀리지 않는다.

후속 O-15G15D에서 [NBA의 2021–22 공식 로스터 규칙과 투웨이 자리 조건](../research/O15G15D_ORLANDO_TWO_WAY_SLOT_GATE.md)을 대조했다. NotebookLM 작업실은 공식 규칙을 네 번째 출처로 추가하고 두 출처 한정 질문으로 2/2 자리 산술을 반환했다. Anti-Gravity의 같은 URL 요청은 headless 명령 권한 거부로 증거 0건 유지. 이전 세 출처 분석의 오류 교정과 G16/G17 구분은 그대로다.

후속 O-15G15E에서 [10/16 명단을 대체세계 표준 자리와 대조](../research/O15G15E_ORLANDO_STANDARD_SLOT_BRIDGE.md)했다. Anti-Gravity의 구단 URL 읽기는 `ACCESS_FAILED`, NotebookLM의 같은 URL 소스 추가도 실패했다. NotebookLM에 **Codex 작성 G15E 문서 사본**을 다섯 번째 출처로 올려 NBA 공식 규칙과의 16/17명 산술만 재현했다. 공유 입력이므로 구단 명단의 독립 검증이나 Evidence Pack 증가로 표시하지 않는다.

[MCP/URL 재시험](../reviews/O15G15_V2_CLI_PILOT_20260926.md)에서 Anti-Gravity → NotebookLM MCP 호출은 실제 성공했다. 공식 Google 제품 페이지는 `read_url_content`가 저장한 파일을 `view_file`로 잇자 읽혔다. Orlando NBA 기사는 자바스크립트 HTML만 회수되어 명단 본문을 읽지 못했다. NotebookLM에서 이미 수집한 NBA 규칙의 MCP 재조회는 **연결 시험**이며 별도 독립 Evidence Pack이 아니다. 현 단계는 `AG_MCP_CONNECTED / NBA_DIRECT_SOURCE_HOLD`다.

[G15G 후속](../research/O15G15G_AMINU_DEROZAN_CAUSAL_LEDGER.md)에서는 Anti-Gravity의 공식 PDF 읽기가 headless `command` 권한 거부, Bulls 기사 본문 읽기가 `ACCESS_FAILED`였다. NotebookLM CLI에는 NBA 공식 오프시즌 거래 원장 URL을 새로 추가해 8/11 DeRozan 거래의 선수·픽을 출처 제한 질의로 분석했다. 도구들이 같은 원문을 읽은 결과를 독립 원자료로 중복 계수하지 않으며 Anti-Gravity 직접 NBA Evidence Pack은 여전히 0건이다.

[G15H 자리 증명](../research/O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md)은 G15B JSON의 양수 분 집합을 이름별 표준/투웨이 가정과 대조한다. NotebookLM은 로스터 규칙과 부상 보고서 두 지정 출처를 분석했지만 시간 표기를 한 번 잘못 병기해 원문으로 교정했다. Anti-Gravity는 NBA 거래 원장의 출처 위치와 자산을 반환했으나 로스터 규칙 페이지는 `read_url_content`→`view_file` 후에도 본문을 판독하지 못했다. 결과가 성공한 URL 하나를 다른 NBA URL 전체의 접근 보장으로 확대하지 않는다.

[Claude 제한 검토](../reviews/R01_O15G15H_CLAUDE_LIMITED_REVIEW.md)는 넓은 반증 요청이 시간 초과로 미완료였고, 좁은 G15H 산술 검토만 종료했다. 지적을 수용해 계약 자리·의료 분기를 분리했으며 최소 명단 14/15 적용은 HOLD다. 이 시점은 `CLAUDE_LIMITED_RUN`이고 source-blind는 아직 `NOT_RUN`이었다. G16/G17 PASS가 아니다.

[결과물 단독 맹점 검수](../reviews/R02_O15G15H_SOURCE_BLIND_REVIEW.md)도 실행했다. 의료 이월 편의, Lopez/Moritz 실존 선수 비용, Orlando 리그 인과를 지적했고 문서에 선택 전 조건을 보강했다. Hampton 삭제 의심은 Dallas 31번 정본으로 기각했다. 상태는 `SOURCE_BLIND_EDITORIAL_RUN`이며 원문을 독립 검증한 G16 PASS가 아니다.
