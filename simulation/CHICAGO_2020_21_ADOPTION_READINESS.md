# O-15F14-L — 시즌 채택 전 실행 패킷

- 기준: PR #165 main `32a2b738c57981cf4892d61627827d0d1190f51d` 및 이번 실행 조항 후속.
- 판정: `PACKET_ASSEMBLED / FACT_BLOCKERS_OPEN / NOT_READY_FOR_FINAL_ADOPTION`.
- 이 문서는 현재 확보 범위와 잔여 의존을 연결하는 색인이다. 아래 분야별 문서·JSON이 사실과 산술의 권위를 가진다.
- `author_locked=false`, `season_selected=false`, `manuscript_allowed=false`. v0.30 PARTIAL·설계/원고 CLOSED.

## 1. 시즌·사건 추천은 완성돼 있다

K1 **원안**은 J1 Terry 후반 공백, Orlando Hall/Wagner 유지, LOW 분 정책, Porter ZERO, 라이벌 R1/28분, 피로 0.5, BPM 전체 경로다. Chicago 31승 41패·동부 10위, Minnesota 24승 48패·서부 13위로 연결된다. RAPTOR는 별도 전체 경로이며 경기마다 유리한 지표를 고르지 않는다. 원권위는 [K 추천](CHICAGO_2020_21_SEASON_RECOMMENDATION.md)이다. 선택된 Hall/McGee 생략의 30경기 국소 승자 방향 대조는 [후속 브리지](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md)에 있다.

L2는 Chicago가 Washington 원정에서 이긴 뒤 Indiana 원정에서 탈락하는 사건 추천이다. 동부 BOS의 IND전 승리, 서부 POR의 GSW전 승리와 MEM의 SAS·GSW전 승리까지 하나의 패킷이다. 정규시즌 산술로 플레이인 승패·점수·개인 박스까지 계산한 것은 아니다. [L 종료 사건](CHICAGO_2020_21_EXECUTION_CLOSEOUT.md)에 네 대안과 추천 근거가 있다.

| 선택 ID | 구체적인 추천 | 보존할 제한 |
|---|---|---|
| A1 가용성 | K의 1,079행 조건부 달력과 J1 Terry 후반 27경기 공백 | 실제 진단·발병일·건강 인증이 아니다. Carter/Porter의 기존 겨울 공백을 다시 빼지 않는다. |
| A2 등록 사건 | 작가가 **Hall 5/9 재계약 생략**을 선택했다. [선택 브리지](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md)의 15+2 경로에는 Hall hardship 신청·허가가 발생하지 않는다 | 추가 작가 선택은 필요 없다. 대체 분·건강·등록/비용이 F4에서 닫히기 전까지 최종 게이트는 `HOLD`다. |
| A3 방법·시즌 사건 | K1/BPM 전체 정규시즌과 L2 동서부 플레이인 패킷 | 정확 점수·개인 박스·추첨 결과 미포함. R1/T1~T4 방향 재승인이 아니다. |

A2의 **행정 비발생 방향**은 작가 선택으로 기록됐다. A1의 대체 건강·분과 A3의 단일 시즌/플레이인, A2를 포함한 최종 실행 게이트는 아직 채택되지 않았다. 사용자의 ‘자동으로 끝까지 계속’에 따라 조사·구현·PR 병합을 계속했으며, 새로운 최종 시즌 승인으로 확대하지 않았다.

## 2. 잔여 사실 F1~F5 — 최신 통합 상태

기존 다섯 묶음을 그대로 사용하며 새 경기 목록을 추가하지 않는다. 이전 문서의 ‘금액 미확보’와 ‘Gordon 종료 미확보’는 아래 회수 범위에서 이력으로 읽는다. 모든 원계약만을 유일한 근거로 요구하지는 않지만, 공개 보도·규정 해석·조건부 계산을 실제 장부 인증으로 올리지 않는다.

| ID / K 조건 | 지금 확보한 결과와 권위 | 여전히 필요한 정확 필드 |
|---|---|---|
| F1 / 거래 | [CHI tax bound](CHICAGO_2020_21_TAX_BOUND.md): 알려진 급여 상단 $127,017,028·R 한도 $5,609,972. [R 구성](CHICAGO_2020_21_RESIDUAL_COMPONENTS.md): 타팀 계약·빈자리 처리. [이번 후속](NBA_2021_EXECUTION_RESOLUTION.md): 과거 Asik 비용의 시즌 구분·캠프 FA 해석 | 적용 방출잔액·기타 권리·미서명 1R·6(m)(2) 예외·기타 조정의 실제 합계 또는 근거 있는 전체 상한. 거래 수취/송출 charge도 별도. 전체 R은 null이며 캠프 3명 연간 전액 시험은 그 전체 상한이 아님 |
| F2 / 거래 | [Boston 자산](NBA_2021_ASSET_CHAIN.md): Bane발 MEM2025 출처, Fournier TPE 원역사 사용과 후대 잔액 대조. [Orlando 3/25 등록 연결](../research/O15F14S_ORLANDO_MARCH25_REGISTRATION_BRIDGE.md): 선택 거래의 일반 15+투웨이 2 자리 산술 PASS. [BOS/DEN 급여](BOSTON_DENVER_2020_21_PAYROLL.md): Boston 조건부 apron 여유 $5,381,195 | 거래 시점 TPE 정확 가용액·수취 charge·다른 사용, BOS/MEM2025 및 BOS2027의 보호/우선권, Teague/Orlando 거래일 비용과 미포함 순증 부담 |
| F3 / 거래 | [실행 조항](CHICAGO_2020_21_EXECUTION_TERMS.md): Gordon 공개 보너스 포함 matching. [이번 후속](NBA_2021_EXECUTION_RESOLUTION.md): 후행 보호 종료 보도 회수. [DEN 급여](BOSTON_DENVER_2020_21_PAYROLL.md): 조건부 apron 여유 $6,684,733 | 선행 1R이 2R로 전환될 때 후행의 연결, 해당 미래 자산의 전체 가용성·우선권, 정확 charge/미포함 부담. 후행의 일반 종료 문구 자체를 다시 찾을 필요는 없음 |
| F4 / 등록 | [작가 선택·국소 검산](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md): Hall 5/9 새 계약을 생략해 다섯 경기 일반 15+투웨이 2, 4월 두 계약은 보존. 조건부 ORL apron 여유 $14,809,543. [사전 보고](../research/O15F14N_HALL_MAY9_16_FOUR_PLAYER_STATUS.md)·[최종 미출전](../research/O15F14O_HALL_FIVE_FINAL_BOX_ABSENCE.md)은 원역사 비교 이력 | 5경기 대체 분·건강/체력, 전체 Orlando 계약 비용·미포함 부담, 후속 등록. **Hall 신규 hardship 허가는 선택 경로의 조건이 아님** |
| F5 / 등록·거래 | [작가 선택·국소 검산](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md): McGee–Hartenstein 거래 생략, 두 선수 원소속 잔류, DEN 11·CLE 14경기 국소 승패 불변. 조건부 DEN apron 여유 $9,264,169. [Cleveland 5/4 공식 등록](../research/O15F14U_CLEVELAND_VAREJAO_HARDSHIP_F5.md): 원역사 Varejão 영입 뒤 일반 16+투웨이 2. [C2 5경기 화면](../research/O15F14V_CLEVELAND_VAREJAO_OMISSION_MINUTE_SCREEN.md): 35:56 재배정, 조건부 5인조 5/5·국소 및 F14F 상대팀 구간 합 두 방법 각 10/10 방향 유지. [Denver 플레이오프](../research/O15F14Z_DENVER_2021_PLAYOFF_NONTRADE_SCREEN.md): 원역사 McGee 4경기 33:49·6경기 DNP, 6/13 Jokic 퇴장 경기 19:40 | C1 Varejão hardship 유지 또는 C2 영입 생략의 전체 등록·급여/건강/새 나비효과와 DEN 플레이오프 4경기 로테이션·승패/후속 사건. **원거래 Grant TPE·두 2R 이전은 선택 경로에서 미발생** |

등록 대조는 기존 범위에서 ORL 19경기 및 BOS/DEN 양수 선수·날짜 267+266에 충돌이 없었다. 이는 리그 전체 등록·건강의 인증이 아니다. **ORL 5/9 이후 5경기의 추가 일반계약 1자리는 Hall 재계약을 유지한 원안에서만 필요했고, 선택된 생략 경로에서는 필요하지 않다.** 출전 분이 0인 선수를 급여·등록 원장에서 삭제하지 않는다.

각 팀의 여유는 서로 다른 시점·정의의 값이다. CHI는 거래 직후 6(j) 비납세 판정, ORL/BOS/DEN은 각 문서 범위의 apron 예산 시험이다. 값들을 합치거나 모두 시즌말 사치세 여유로 부르지 않는다. 이 범위 검사만으로 네 K 묶음 전체를 닫지 않는다. 종료 수는 여전히 0이다.

## 3. 최종 정본 게이트와 승인된 CP2 예외

최종 정본 추첨은 건강·등록·거래 사실 조건과 A1~A3 최종 채택을 요구한다. 다만 사용자 CP2 승인에 따라 K1·L2 조건부 작업에서는 잠정 2021 동률/상위4 추첨과 후속 설계를 허용한다. 실제 조건이 미해소된 결과를 최종 정본으로 승격하지 않는다. 먼저 결과를 본 뒤 시즌안이나 seed를 바꾸는 역선택을 막기 위해서다. [드래프트 인과 규약](DRAFT_CAUSALITY_PROTOCOL.md)의 고정 seed를 유지하며 새 seed 후보를 만들지 않는다.

L2의 Chicago 9~10위/NOP 동률군·Minnesota 6위는 추첨 전 순서다. 최종 지명 순번·보호픽 소유권 결산이 아니다. Gordon의 먼 미래 의무와 2021 추첨 산술은 구분하되, 정확 거래 실행의 HOLD를 지우지 않는다.

I의 Washington HIGH/RAPTOR 반례, F의 비상 역할 비용 반례, K의 4경기 잔여 빅맨 중복을 보존한다. 이번 자료가 이 비용을 자동 합산하거나 없앤 것은 아니다.

## 4. 추가 조회의 실제 한계

PR #161 이후 급여·등록·픽 본문을 추가 확보해 F1~F5의 여러 금액과 보고 필드를 회수했다. 당시 ‘신규 사실 0’은 그 작업의 이력이며 현재 상태가 아니다. 이번 출처 원장은 성공 경로와 HTTP 실패 경로를 함께 기록한다.

Chicago 상세 cap 페이지, ProsportsTransactions의 Denver/Boston 목록, RealGM 상세 픽 페이지는 이번 직접 요청에서 403이었다. 검색 요약·현재 홈페이지·미기재 문구를 정확 잔액이나 보호 없음의 증거로 사용하지 않았다. CBS Gordon은 직접 요청 실패 뒤 웹 본문 회수에 성공했다. 공개 자료로 아직 확보하지 못한 것을 ‘반드시 비공개’라고 단정하지도 않는다.

같은 급여를 재수집하거나 새 경기 전량 검사를 늘려도 위 정확 필드가 자동 해소되지는 않는다. 다음 조사에는 해당 날짜 원장·새 조항 출처 등 새로운 입력이 필요하다.

## 5. 다음 실행 순서와 검토 가능한 진행 선택

최종 정본 순서는 **사실 조건 통과 → A1~A3 최종 채택 → 추첨/결산 검증 → 2020–21 최종 종료**다. CP2 작업 순서는 **입력/알고리즘 사전 게시 → 잠정 추첨·픽 결산 → 조건부 2021–23 이후 설계**로 병행한다. 이미 승인한 팀·드래프트·Theis/Green·R1/T1~T4는 재질문하지 않는다.

[조건부 결산 CP2](../design/O15F14_CONDITIONAL_CONTINUATION_PROPOSAL.md)는 직전 전환 질문에 대한 사용자의 ‘이어서’로 승인됐다. 승인 범위는 작업 절차이며 정확 비용/조항이나 최종 시즌 승인이 아니다. 사전 기록과 실행 로그는 `NBA_2021_DRAW_PREREGISTRATION.md`와 후속 잠정 결과에서 관리한다. 같은 승인을 다시 묻지 않는다.

이번 수용 기준은 최신 사실/산술의 단일 색인, 잔여 정확 필드, 작가 선택과 현행 게이트, 자동 후속을 위한 구체안 연결이다. 이 기준은 충족했지만 시즌 최종 완료 기준은 미충족이다. 자체 검토 `NOT_INDEPENDENT`, 전체 7묶음 중 1완료·1진행·5대기, 진행 중 포함 남은 큰 작업 6개다.

## O-15F14-M / O-15G1 — 승인된 조건부 후속 실행

CP2 절차 승인 후 [2021 잠정 추첨·픽 결산](NBA_2021_PROVISIONAL_DRAFT.md)을 실행했다. CHI10·39, MIN7→GSW/36→OKC 조건부 경로다. [2021–23 거래·계약 작업안](CHICAGO_2021_23_CONTINUATION.md)의 G1A/E2와 예산/역할 검산을 시작했다. 네 K 묶음의 정확 사실/최종 채택 HOLD는 그대로다. 과거 ‘추첨 미실행’은 CP2 승인 전 상태이며 현행 조건부 결과를 막지 않는다.
