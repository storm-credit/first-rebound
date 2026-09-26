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

[G15I 샐러리캡 비용 분기](../research/O15G15I_AMINU_WAIVER_CAP_COST.md)에서는 명단 한 자리와 방출 뒤 팀 샐러리를 구분했다. NotebookLM CLI는 NBA CBA PDF와 2021–22 캡 발표를 지정 출처로 인용했다. Anti-Gravity CLI는 NBA CBA PDF 판독에 실패했지만 별도 캡 발표 URL은 `read_url_content`→`view_file`로 본문을 실제 읽었다. 상태는 **해당 NBA 기사 1건의 직접 판독 PASS**, CBA PDF와 Aminu 계약액은 `HOLD`다. 같은 기사에 대한 Codex·NotebookLM·Anti-Gravity 확인을 세 독립 출처로 세지 않는다.

[G15I Claude 반증](../reviews/R01_O15G15I_CLAUDE_CBA_REVIEW.md)은 48시간 waiver·Moritz FA 지위·9월1일 stretch에 오류 가능성을 제기했으나 NBA CBA 전체본과 구단/리그 자료에 대조해 모델의 잘못된 전제를 기각했다. [G15I 결과물 단독 검수](../reviews/R02_O15G15I_SOURCE_BLIND_REVIEW.md)는 상대 팀 수용·픽/현금 보상과 8월 Chicago 거래→10월 Orlando 시장의 순서를 보강했다. 별도 조사로 드러난 Aminu 선수 옵션 선행 게이트는 모델의 성과로 오인하지 않는다. 둘 다 제한적 실행이며 G16 전체 독립 검수 PASS가 아니다.

[G15J 계약 입력 원장](../research/O15G15J_ORLANDO_2021_22_CONTRACT_INPUT_LEDGER.md)은 비공식 계약 추적 자료의 Vučević $24m와 Aminu 옵션 $10.1838m를 **원역사 기본급 후보**로만 넣었다. NotebookLM CLI의 공식 CBA/캡 두 출처 지정 질의는 보호급여가 Team Salary에 남는 규칙과 선수별 급여 부재를 확인했고, 구단 영입 기사 두 URL의 새 출처 추가는 실패했다. Anti-Gravity CLI는 두 구단 URL을 직접 요청했지만 JavaScript만 회수해 본문 판독은 실패했다. Claude CLI 반증 두 시도도 응답 없이 중단해 이번 독립 반증과 source-blind는 `NOT_RUN`이다. 실패를 성공한 Evidence Pack이나 검수로 세지 않고, 동일 공식 문서에 대한 NotebookLM 재질의를 독립 출처로 늘리지 않는다. `G15J`도 G16/G17 완료가 아니다.

[G15K 옵션 통지 재검사](../research/O15G15K_AMINU_OPTION_NOTICE_AND_PREFERENCE.md)는 G15J의 5/18 행사일 단정을 **5/18 행사 계획 보도일 / 공식 통지일 미확보**로 고쳤다. NotebookLM CLI는 NBC Sports 기사를 새 출처로 수집하고 그 출처만 지정해 계획·완료 표현을 분석했다. Anti-Gravity CLI의 같은 URL 읽기는 60초 시간 초과로 본문 0건이다. 원역사 행동과 분기 전 무릎 이력에 기댄 행사 `WORKING_PRIOR`는 대체 Orlando의 선수 결정이나 작가확정이 아니다. [Claude 제한 반증](../reviews/R01_O15G15K_CLAUDE_OPTION_REVIEW.md)과 [결과물 단독 맹점 검수](../reviews/R02_O15G15K_SOURCE_BLIND_REVIEW.md)를 실행해 승인 범위·명단 산술 설명을 보강하고 잘못된 계약/지명 구단 전제는 기각했다. 두 검수는 사실 출처의 독립 검증이나 G16/G17 통과가 아니다.

[G15N 공통 계약 비용](../research/O15G15N_ORLANDO_COMMON_2021_22_CONTRACT_CHARGES.md)은 G15L의 조건부 8명을 원역사 계약표의 cap hit에 연결했다. NotebookLM CLI에 Harris·Cole 계약표 두 URL을 새로 수집해 **그 두 자료만** 지정한 질의로 기본급과 likely incentive를 분리했다. Anti-Gravity CLI는 NBA 공식 cap 기사 판독 요청이 35초 time-out으로 본문 0건이어서 이번의 직접 원자료는 없다. Codex는 나머지 선수 계약표·NBA 드래프트 프로필·2020 #24 신인 스케일을 대조하고 부분합을 별도 재계산했다. Claude의 제한 산술 반증은 합산 오류를 찾지 못했지만 **대체 #24가 원역사 #22 Nnaji의 계약을 그대로 부담해야 한다는 전제**는 대체 드래프트 조건과 충돌하여 기각했다. [이번 검토 기록](../reviews/R01_O15G15N_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)은 도구 실행 범위를 명시한다. 이 작업은 G16/G17 완료가 아니다.

[G15O 2021 FA 세 건](../research/O15G15O_ORLANDO_2021_FA_SIGNINGS_AND_HOLDS.md)은 NBA 구단 서명일, 비공식 계약표의 base/charge, 2017 CBA의 1년 최저급 환급 규칙을 연결했다. NotebookLM CLI는 Lopez·Moritz·Moore 계약표 세 URL을 추가하고 그 세 소스만 질의해 선행 FA hold의 소유 팀을 분리했다. Anti-Gravity CLI의 Moritz 구단 발표 판독은 35초 time-out·본문 0건이었다. Codex는 NBA의 Moritz UFA 분류와 SalarySwish의 RFA 표기 충돌을 `HOLD`로 남기고 Lopez/Washington·Moore/Phoenix hold를 Orlando 비용으로 복사하지 않았다. [제한 Claude 검토](../reviews/R01_O15G15O_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)는 원자료 독립 감사나 G16 PASS로 세지 않는다.

[G15P 2라운드 지명권 경계](../research/O15G15P_HERBERT_33_SECOND_ROUND_TENDER.md)에서는 Antigravity CLI의 NBA 드래프트 URL 요청이 25초 time-out·본문 0건으로 끝났다. NotebookLM CLI는 NBA 공식 드래프트 결과와 비공식 Herbert 원역사 계약표를 출처 제한 분석했으나, 기존 CBA 소스가 전체본이 아닌 요약본이어서 Required Tender 세부 규칙을 반환하지 못했다. Codex가 2017 NBA–NBPA CBA **전체본**을 직접 읽어 2라운드 tender의 1시즌·최저급·수락기한, 미서명 1라운드 120% hold 및 incomplete roster charge를 분리했다. [Claude 제한 반증·결과물 단독 검수](../reviews/R01_O15G15P_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)에서는 반증 모델의 2라운드 제도 오독을 원문으로 기각했다. 같은 URL의 두 도구 판독은 독립 출처 두 건이 아니며, G16/G17 PASS도 아니다.

[G15Q Antigravity 인증 복구](../reviews/O15G15Q_ANTIGRAVITY_AUTH_RECOVERY.md)에서 `agy models` 성공과 실제 agent turn 성공을 분리했다. 실패 당시 로그의 `You are not logged into Antigravity`를 확인하고 대화형 CLI로 재로그인한 뒤, headless `READY` 1턴 응답과 NBA 드래프트 URL의 `read_url_content`→`view_file` 실제 도구 단계, 저장 본문의 33·35번 항목을 확인했다. 현재는 `AGY_AUTH_RECOVERED / NBA_PAGE_BODY_VERIFIED`다. G15P 당시 타임아웃 기록은 삭제하지 않고, 같은 NBA 원문을 새 독립 출처로 중복 계수하지 않는다. `SUCCESS`라도 응답이 비고 `num_turns=0`이면 회수 성공이 아니다.

[G15R 최저급/MLE 분기](../research/O15G15R_ORLANDO_HERBERT_MINIMUM_MLE_AND_MORITZ_UFA.md)는 Antigravity에서 NBA QO 기사와 Orlando 프로필의 URL 읽기·파일 보기까지 수행했다. QO 기사 저장 본문에서 Moritz 명단 부재는 확인했으나 Orlando 프로필은 선수 본문 없는 HTML이어서 `UFA` 표기를 AG 단독 증거로 세지 않았다. 최종 AG 답변은 추가 `run_command` headless 권한 거절로 비었고 해당 호출은 **부분 성공/agent 답변 실패**다. NotebookLM CLI는 QO 기사를 추가했지만 세 차례 출처 제한 질의가 무응답, RealGM 추가는 실패했다. Codex가 CBA 전체본과 NBA 두 해 cap/MLE 원문을 사용해 최저급·예외 한도를 재현했고, [Claude 제한 검토](../reviews/R01_O15G15R_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)의 ‘MLE는 한 계약만 가능’ 주장은 CBA 명문과 충돌해 기각했다. 도구 실패를 우회하면서 출처·검증 횟수를 부풀리지 않는다.

[G15S 날짜별 charge 시험](../research/O15G15S_ORLANDO_2021_22_DATED_CHARGE_WITNESS.md)은 이미 출처가 붙은 선수별 금액을 8/3 cap 발효 이후의 이름 있는 부분합으로만 연결했다. Antigravity CLI의 공식 cap 기사 재시험은 최종 1턴 답변에서 8/3 발효와 $136.606m 세금선을 반환했지만 해당 호출의 원문 도구 단계·저장 본문은 확인하지 못해 신규 Evidence Pack 0건이다. NotebookLM CLI의 cap/Bacon 두 출처 지정 질의는 또 무응답이어서 이번 출처 연결 분석 0건이다. [Claude 제한 반증·source-blind 기록](../reviews/R01_O15G15S_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)의 8명 집계 오독·hold 중복합산·Gordon 1대2 거래 오독은 기존 선수 원장과 충돌해 기각했고, Codex는 8/8 waiver 요청과 실제 이탈 완료의 시간 차이를 수정했다. 이름 있는 비용 부분합을 완전 Team Salary·apron·G16 PASS로 승격하지 않는다.

[G15T Moritz 계약 인과](../research/O15G15T_MORITZ_2021_AGREEMENT_SIGNING_AND_HOLD_BRANCH.md)는 NBA 8/4 **합의 보도**와 Orlando 8/23 **재계약 발표**를 나누었다. Antigravity CLI가 NBA 8/4 기사 저장 본문을 회수했고 Codex가 Source URL/기사 본문을 직접 대조했다. NotebookLM CLI는 같은 NBA URL 추가에 성공했으나 단일 출처 질의는 무응답이라 분석 0건이다. 원역사 8/4 보도 속 Franz 동팀 사유는 G15E/F의 Franz GSW 대체 분기와 충돌하므로 Moritz 재계약을 자동 복사하지 않는다. 비재계약 시 15표준 자리 시험과 FA hold 유지/제거 비용을 **조건부**로 계산한다. [Claude 제한 검토](../reviews/R01_O15G15T_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)는 계약/hold $60,039 차이와 역할 비용을 지적했으며 오류로 오인한 부분과 근거 없는 경험/할인 추정은 기각했다. QO 실제 사건·권리 포기일·다음 팀/분·완전 Team Salary는 `HOLD`다.

[G15U 8/6 Moritz 중간 비용](../research/O15G15U_MORITZ_FA_HOLD_INTERIM_CAP_AND_ROLE_GATE.md)은 **FA hold 유지 H / 적법 제거 R / NBA에 통지된 예상 급여 D**를 분리했다. Codex가 2017 CBA Article II §13·Article VII §4의 UFA amount, renounce/QO 제한, 통지된 합의 예상 급여 규칙을 직접 대조했다. NotebookLM CLI는 기존 NBA CBA 요약 **한 소스** 지정 질의 `0573ed95-5398-4c61-bb8f-c6835229e396`에서 FA amount 포함·renounce 제거를 인용해 답했으나, 원문 규칙의 독립 출처는 아니다. Antigravity CLI의 8/23 구단 URL 요청은 1턴·`SUCCESS`에도 최종 응답이 비고 저장 HTML에 기사 본문이 없어 직접 증거 0건이다. [Claude 제한 반증·source-blind](../reviews/R01_O15G15U_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)는 실제 통지 서류 부재를 지적했지만 **정식 서명 계약만** 급여에 영향이 있다는 오독은 CBA에 대조해 기각했다. 공개 8/4 보도와 리그 통지 사건을 동일시하지 않고, H/R/D의 실제 발생 여부와 완전 Team Salary·apron은 `HOLD`다.

[G15V 빅맨 기회 부채](../research/O15G15V_2021_22_FRONTCOURT_OPPORTUNITY_DEBT.md)는 Chicago/Cleveland/Denver/Orlando 구단·NBA 공식 회고 자료의 **원역사 총분**을 같은 Orlando C/PF 예산에 무리하게 복사할 때의 압박을 진단한다. Codex는 세 구단 이탈 비용과 G15B 한 경기 조건부 배정을 연결했다. NotebookLM CLI는 Orlando 구단 가이드 한 소스에서 네 선수의 행을 출처 제한 질의로 인용했고, 같은 출처의 재판독임을 명시했다. Antigravity CLI는 PDF 직접 접근이 headless `command` 거절로 실패했으나 **별도 도구 없는** 산술 반증은 반환했다. [Claude source-blind 제한 검토](../reviews/R01_O15G15V_CLAUDE_SOURCE_BLIND.md)는 원역사 거래 방향과 가상 배정을 혼동한 잘못된 반증을 내어 공식 2021-03-25 거래 발표로 기각했다. 도구별 성공 범위가 달라도 이 분석은 기회 비용 `HOLD`이며 G16/G17을 통과하지 않는다.

[G15W 1/23 두 경기 연결](../research/O15G15W_2022_01_23_TWO_GAME_OPPORTUNITY_GATE.md)은 G14 Chicago 센터 분이 **이미 48분 채워진 사실**을 재사용해 중복 차감을 피하고, 같은 날 Denver Nnaji16:45 손실·Detroit 상대 변경·Orlando Moritz25:08 원역사 역할을 열었다. Cleveland는 현지 1/23 경기가 없어 Mobley의 기회 비용을 같은 날짜에 가짜 경기로 쓰지 않는다. Antigravity NBA 박스 직접 요청은 제한 시간 뒤 빈 답변, NotebookLM URL 추가는 성공했으나 웹 소스가 메뉴만 포함해 선수 표 질의가 실패했다. Codex의 NBA 검색 가능 공식 박스와 저장소 JSON 대조만 사실·산술 근거다. [Claude 무도구 제한 검토](../reviews/R01_O15G15W_CLAUDE_SOURCE_BLIND.md)는 Denver 수신자 `HOLD`와 별도 Mobley3 드래프트 계보를 짚었다. 두 경기의 새 생산성·승패, 전체 G16/G17은 계속 `HOLD`다.

[G15Z Denver 5인 수학 증명](../research/O15G15Z_DENVER_FIVE_MAN_AND_BEY_CONTRACT_BRIDGE.md)에서는 Antigravity CLI가 NBA 자유계약 설명 기사 본문을 직접 읽고, NotebookLM CLI는 **이미 있던** NBA CBA 101 한 출처만으로 신인 계약 2+1+1을 반환했다. Codex는 같은 공식 규칙과 5인 JSON을 직접 대조했고 Claude의 Monte Morris 신원 의심은 공식 Denver 경기 노트로 기각했다. [실행·맹점 기록](../reviews/R01_O15G15Z_CLI_AND_LIMITED_BLIND_REVIEW.md)은 각 성공 범위와 공유 근거를 분리한다. NBA 기사 직접 판독 1건은 성공이지만 실전 로테이션·Bey의 당일 계약/등록·G16/G17 완료는 아니다.

[G15AA Detroit 세 번째 이탈](../research/O15G15AA_DETROIT_HAYES_THIRD_EXIT_AND_MEDICAL_BOUNDARY.md)은 Codex가 정본 Hayes NOP13과 공식 원역사 Detroit Hayes24:42를 직접 연결해 G15Y의 누락을 고쳤다. NotebookLM은 기존 공식 부상 보고 **한 출처**로 Hayes 사전 상태만 확인했고, Antigravity의 박스 요청은 headless `RunCommand` 거부로 본문 0건이었다. Claude 제한 검토는 원역사 Bey·Hayes의 팀을 잘못 바꾸고 2020/2021 조건부 연쇄를 오해해 해당 주장을 기각했다. [검토 기록](../reviews/R01_O15G15AA_THIRD_EXIT_CLI_AND_SOURCE_BLIND.md)처럼 도구 실패·모델 오류를 PASS로 세지 않는다. G16/G17은 여전히 미완료다.

[G15AB Detroit 1/23 전체 박스](../research/O15G15AB_DETROIT_JAN23_ORIGINAL_BOX_AND_BRANCH_BOUNDARY.md)는 Codex가 NBA 페이지 내장 13행을 직접 추출해 팀 합계와 두 분기 합계를 기계 대조했다. NotebookLM은 기존 공식 부상 보고 한 출처만 확인했고 Antigravity의 박스 요청은 40초 시간 초과·본문 0건이었다. Claude 제한 반증의 Plumlee 거래·Grant/Olynyk 의료 게이트는 유지하되 중첩 분을 이중 합산한 `295:24` 주장과 원역사/정본 Kira·Hayes 순번 혼동은 기각했다. [검토 기록](../reviews/R01_O15G15AB_CLI_AND_SOURCE_BLIND.md)은 각 도구의 성공 범위를 분리한다. G14 원본·G16/G17·설계/원고 게이트를 바꾸지 않는다.

[G15AC Plumlee 자산 충돌](../research/O15G15AC_PLUMLEE_2021_DRAFT_ASSET_COLLISION.md)은 NBA 구단 발표/드래프트 결과와 DB1~DB4의 30·37·57·58 제안을 분리했다. Antigravity의 구단 URL 요청은 40초 시간 초과·본문 0건, NotebookLM의 구단 URL 추가도 실패했지만 기존 NBA 드래프트 결과 한 출처 한정 질의는 성공했다. Claude 제한 검토는 권리 충돌 자체를 짚었으나 Plumlee 거래 방향과 DB1 37번 선수/소유를 뒤집어 해당 주장을 기각했다. [검토 기록](../reviews/R01_O15G15AC_TRADE_CLI_AND_SOURCE_BLIND.md)처럼 도구별 원문 접근과 논리 감사의 성공을 따로 기록한다. G16/G17 및 정본/게이트는 변하지 않는다.

[G15AD Plumlee/Olynyk cap 연결](../research/O15G15AD_PLUMLEE_OLYNYK_CAP_AND_DATE_BRIDGE.md)은 거래 미실행 P0만으로 원역사 Olynyk 영입을 보존할 수 없다는 동시 보유 게이트다. NBA/Detroit 구단의 계약 기간·거래·영입·cap 목적을 구분했다. Antigravity는 구단 URL 도구 1턴이 실행됐지만 본문 대신 셸만 읽었고, NotebookLM은 구단 URL 추가 실패 뒤 기존 공식 거래/CBA 두 출처만 질의했다. NLM의 원역사 37 Thor 권리를 DB1 Detroit에 이식한 답변은 기각했다. Claude는 초안 텍스트만 본 제한 source-blind 의심이며 cap·명단 미증명은 그대로 `HOLD`다. [검토 기록](../reviews/R01_O15G15AD_CAP_CLI_AND_SOURCE_BLIND.md)에 따라 실패/반증/자료 접근을 분리한다. G16/G17 및 정본/게이트는 변하지 않는다.

[G15AE Detroit 8월 자리/9월 Nets 거래](../research/O15G15AE_DETROIT_AUGUST15_AND_SEPTEMBER_ASSET_BRIDGE.md)는 원역사 15표준 관측과 `same-other-events` 조건부 16명 스트레스, 9월 Doumbouya·Okafor 송출/ Jordan·네 2R·현금 수취를 날짜별로 분리했다. Antigravity는 NBA 거래 원문 본문을 실제 읽었고 NotebookLM은 같은 공식 출처를 제한 질의해 방향을 재확인했으므로 독립 출처 두 건이 아니다. Claude는 초안만 보고 출발 15명에 Plumlee 포함 여부와 개막 실명 경로를 의심했고, 전자는 8/6 Charlotte 거래로 교정·후자는 `HOLD` 유지했다. [검토 기록](../reviews/R01_O15G15AE_ROSTER_CLI_AND_SOURCE_BLIND.md)과 같이 실제 접근/논리 의심을 구분한다. G16/G17 및 정본/게이트는 변하지 않는다.

[G15AF Detroit 실명 명단→개막 자리](../research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md)는 NBA 드래프트 프로필의 11 계약자와 구단의 8/12 표준 15명 관측을 혼동하지 않고 여름 출입으로 15명의 이름을 재구성했다. Antigravity CLI는 해당 드래프트 URL에서 도구 `SUCCESS` 뒤에도 선수 본문 없는 HTML 셸만 얻어 증거 0건; NotebookLM CLI는 같은 NBA URL의 11 계약자/5 FA를 제한 질의로 반환했지만 8월/10월 명단의 독립 증거가 아니다. Codex는 구단 거래·계약·방출·Garza 전환을 날짜별로 연결했고 집합 검사기는 원역사 `15→16→15→14→15`, 엄격한 P0-B 반사실 `16→17→16→15→16`을 검산했다. [Claude 제한 source-blind](../reviews/R01_O15G15AF_NAMED_ROSTER_CLI_AND_BLIND.md)는 세 1라운더 서명·Aldama 미서명 가정과 Jordan 사건 순서를 더 명확히 하게 했고, Jordan이 8월에 Detroit를 떠났다는 식의 시간 오류는 기각했다. 원역사 10/20 독립 명부·대체 Nets 거래·Olynyk cap 경로·실명 이탈은 `HOLD`; 검수 횟수를 G16/G17 PASS로 세지 않는다.

[G15AG 공식 개막 FINAL BOX 대조](../research/O15G15AG_DETROIT_2021_OPENING_GAMEBOOK_WITNESS.md)는 NBA PDF 첫 페이지에서 Detroit 17명(선발5·교체5·DNP4·inactive3)을 직접 회수해 G15AF 사건 재구성의 개막 이름을 대조했다. Antigravity CLI의 동일 PDF 요청은 45초 time-out·빈 응답으로 이번 직접 증거 0건; NotebookLM CLI는 **같은 PDF**를 소스로 추가해 17명을 제한 질의했으므로 새로운 독립 원자료가 아니다. 구단 10/5 Smith·10/13 Pickett 투웨이 설명을 결합해 나머지 15명 이름이 G15AF와 정확히 일치하지만, 경기 기록 자체에는 계약 유형이 없어 이는 교차 출처 추론이다. [Claude 문서 단독 검수](../reviews/R01_O15G15AG_GAMEBOOK_CLI_AND_BLIND.md)의 9/29→10/20 이월 경고는 근접 날짜 구단 근거로 좁혔고 PDF의 부상 사유 누락 의심은 원문으로 기각했다. P0-B의 실제 대체 명단·8/6 Olynyk cap 경로·추가 이탈은 `HOLD`; G16/G17 통과로 세지 않는다.

[G15AH 8/6 급여·개막 자리](../research/O15G15AH_DETROIT_AUG6_CAP_AND_OPENING_SLOT_SCREEN.md)는 공식 리그 캡/MLE 발표와 **2차** 선수 계약액을 분리해 P0-B Plumlee 미이적 기본급 후보·원역사 Charlotte 이적 보너스 포함 표시를 혼동하지 않았다. Antigravity CLI는 NBA 공식 발표의 수치를 최종 답변으로 반환했지만 저장 원문을 별도로 확인하지 않아 독립 Evidence Pack을 추가하지 않았다. NotebookLM CLI는 기존 공식 발표/규칙 해설과 새 2차 계약표 두 건의 지정 출처 분석을 수행했으며 전체 Detroit Team Salary는 없다고 답했다. Claude CLI는 무도구 문서 단독 검수에서 급여액 구분 문구와 실명 이탈 경로 부재를 지적했다. [검토 기록](../reviews/R01_O15G15AH_CAP_SLOT_CLI_AND_BLIND.md)에 수용/기각을 남겼다. 8월 cap 경로·10월 한 자리 실행은 `HOLD`; G16/G17 및 정본/게이트를 바꾸지 않는다.

[G15AI Joseph room MLE 연결](../research/O15G15AI_JOSEPH_ROOM_EXCEPTION_SEQUENCE_GATE.md)은 원역사의 7/31 방출 잔여급여와 8/10 새 계약을 나눠 8/6 Olynyk cap room 뒤 Joseph의 예외 자격까지 확인하도록 했다. Antigravity CLI가 NBA 자유계약 설명의 규칙 본문을 인용했지만 저장본 독립 확인은 없고, NotebookLM CLI도 **같은 공식 한 출처**의 `any time during that Salary Cap Year` 조건만 한정 분석했다. Detroit Joseph URL 추가 실패는 별도로 남겼다. Claude의 `계약 당시 under-cap 필수` 주장은 원문과 충돌해 기각했고, 날짜·계약 표현의 두 모호점은 고쳤다. [검토 기록](../reviews/R01_O15G15AI_JOSEPH_CLI_AND_BLIND.md)대로 정확한 전체 Team Salary와 P0-B의 두 선수 계약·등록은 `HOLD`; G16/G17 및 정본/게이트는 변하지 않는다.
