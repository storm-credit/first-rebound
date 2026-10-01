# O-15F14-L — 시즌 채택 전 실행 패킷

2026-10-02 [Orlando 35일 보조 증인](../research/D1_ORLANDO_DAILY_REGISTRATION_WITNESS_2026_10_02.md): 경기19+비경기16일의 조건부 자리 수와 구단 공표15행을 대조했다. 전체 법적 등록/비용 proof가 아니며 ORL_DATED_REGISTRATION complete_domain/source_verified=false, F0/5·A0/3·K0/4를 유지한다.

- 현행 기준(2026-09-30): [S2 작가 선택](../canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json)과 [운영 규칙](../control/CHICAGO_2020_21_D1_S2_PROTOCOL.md)을 적용한다. 아래 정확 필드는 원문 또는 전체 닫힌 법적 구간으로 판정하고, 반사실 건강·코칭은 개별 AUTHOR_MODELED 선택으로 따로 잠근다. R=null은 계속 HOLD, 법적 F0/5·A0/3·K0/4. S0 시기 EXACT_PASS와 S2의 LEGAL_BOUND_PASS를 혼합하지 않는다.
- 기준: PR #165 main `32a2b738c57981cf4892d61627827d0d1190f51d` 및 이번 실행 조항 후속.
- 판정: `PACKET_ASSEMBLED / FACT_BLOCKERS_OPEN / NOT_READY_FOR_FINAL_ADOPTION`.
- 이 문서는 현재 확보 범위와 잔여 의존을 연결하는 색인이다. 아래 분야별 문서·JSON이 사실과 산술의 권위를 가진다.
- `author_locked=false`, `season_selected=false`, `manuscript_allowed=false`. v0.30 PARTIAL·설계/원고 CLOSED.
- **2026-09-30 F5 선택 후속:** [C2 Varejão 영입·후속 계약 생략](../canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json)을 작가가 선택했다. [BD 8경기 명단 검문](../research/O15F14BD_CLEVELAND_C2_FINAL_ROSTER_WINDOW.md)은 나머지 계약 유지·McGee/Hartenstein 1대1 치환 조건에서 5/4~16 각 경기일 일반15+투웨이2를 확인했다. 아래 C1/C2 대기 표기는 선택 전 이력이다. 기존 5경기 분·승패 감도는 조건부이며 오프데이 등록·Cleveland 전체 건강/급여·Denver 새 플레이오프는 `HOLD`다. F 전체 PASS 0/5.

## 1. 시즌·사건 추천은 완성돼 있다

**Cleveland 비용 후속:** [C2 공개 목록](CLEVELAND_2020_21_C2_PAYROLL_SCREEN.md)의 $130,668,168·조건부 FA 하한 $130,711,287·두 감액 혜택0 시험 $132,059,577을 구분한다. 선수 보수/팀 차지, 이전9의무와 현재15명 자리, likely 포함 cap hit/추가 unlikely를 따로 검산했다. 전체 R_CLE와 실제 tax/apron·일자별 등록은 미확인으로 F5는 HOLD다.

K1 **원안**은 J1 Terry 후반 공백, Orlando Hall/Wagner 유지, LOW 분 정책, Porter ZERO, 라이벌 R1/28분, 피로 0.5, BPM 전체 경로다. Chicago 31승 41패·동부 10위, Minnesota 24승 48패·서부 13위로 연결된다. RAPTOR는 별도 전체 경로이며 경기마다 유리한 지표를 고르지 않는다. 원권위는 [K 추천](CHICAGO_2020_21_SEASON_RECOMMENDATION.md)이다. 선택된 Hall/McGee 생략의 30경기 국소 승자 방향 대조는 [후속 브리지](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md)에 있다.

L2는 Chicago가 Washington 원정에서 이긴 뒤 Indiana 원정에서 탈락하는 사건 추천이다. 동부 BOS의 IND전 승리, 서부 POR의 GSW전 승리와 MEM의 SAS·GSW전 승리까지 하나의 패킷이다. 정규시즌 산술로 플레이인 승패·점수·개인 박스까지 계산한 것은 아니다. [L 종료 사건](CHICAGO_2020_21_EXECUTION_CLOSEOUT.md)에 네 대안과 추천 근거가 있다.

| 선택 ID | 구체적인 추천 | 보존할 제한 |
|---|---|---|
| A1 가용성 | K의 1,079행 조건부 달력과 J1 Terry 후반 27경기 공백 | 실제 진단·발병일·건강 인증이 아니다. Carter/Porter의 기존 겨울 공백을 다시 빼지 않는다. |
| A2 등록 사건 | 작가가 **Hall 5/9 재계약 생략**을 선택했다. [선택 브리지](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md)의 15+2 경로에는 Hall hardship 신청·허가가 발생하지 않는다 | 추가 작가 선택은 필요 없다. 대체 분·건강·등록/비용이 F4에서 닫히기 전까지 최종 게이트는 `HOLD`다. |
| A3 방법·시즌 사건 | K1/BPM 전체 정규시즌과 L2 동서부 플레이인 패킷 | 정확 점수·개인 박스·추첨 결과 미포함. R1/T1~T4 방향 재승인이 아니다. |

A2의 **행정 비발생 방향**은 작가 선택으로 기록됐다. A1의 대체 건강·분과 A3의 단일 시즌/플레이인, A2를 포함한 최종 실행 게이트는 아직 채택되지 않았다. 사용자의 ‘자동으로 끝까지 계속’에 따라 조사·구현·PR 병합을 계속했으며, 새로운 최종 시즌 승인으로 확대하지 않았다.

[A1 Lakers 건강 하위 선택 패킷](../design/CHICAGO_2020_21_A1_LAKERS_HEALTH_DECISION_PACKET.md)은 Davis 2/14 사건+30결장과 LeBron 3/20 부분 경기+20/2/6/2 창의 재검문 날짜 45개를 연결한다. H00 원역사 두 달력 유지/H10 Davis 변경/H01 LeBron 변경/H11 둘 다 변경은 전부 후보이며, H00 권고도 A1 전체 채택이나 F5 대진 종료가 아니다. 종료 증거 기준은 작가가 S2를 선택했고 [Cleveland C2](../canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json)는 선택됐으나 실제 실행 검증이 남아 있다.

## 2. 잔여 사실 F1~F5 — 최신 통합 상태

기존 다섯 묶음을 그대로 사용하며 새 경기 목록을 추가하지 않는다. 이전 문서의 ‘금액 미확보’와 ‘Gordon 종료 미확보’는 아래 회수 범위에서 이력으로 읽는다. 모든 원계약만을 유일한 근거로 요구하지는 않지만, 공개 보도·규정 해석·조건부 계산을 실제 장부 인증으로 올리지 않는다.

| ID / K 조건 | 지금 확보한 결과와 권위 | 여전히 필요한 정확 필드 |
|---|---|---|
| F1 / 거래 | [CHI tax bound](CHICAGO_2020_21_TAX_BOUND.md): 알려진 급여 상단 $127,017,028·R 한도 $5,609,972. [R 구성](CHICAGO_2020_21_RESIDUAL_COMPONENTS.md): 타팀 계약·빈자리 처리. [실행 후속](NBA_2021_EXECUTION_RESOLUTION.md): 과거 Asik 비용의 시즌 구분·캠프 FA 해석. [AD 감소일 위험](../research/O15F14AD_CHICAGO_EXCEPTION_PRORATION_BOUND.md)은 양쪽 예외가 산입될 때의 스트레스. [AE 급여 하한·예외 시작 시점](../research/O15F14AE_CHICAGO_OVER_CAP_EXCEPTION_TRIGGER.md)은 드래프트 뒤~거래 직전 캡 초과 최소 $2,838,148, 2차 일정의 11/21 새 리그 연도 시작, 기존 CBA의 MLE/BAE 첫날 발생·정규시즌 말 소멸을 연결한다. [AF 구단 거래 연혁](../research/O15F14AF_CHICAGO_PREDEADLINE_EXCEPTION_ORIGIN.md)은 2019 마지막 선수 송출·2020 무거래·2021 3/25 첫 거래를 대조해 승인 경로의 **거래 직전 기존 Chicago TPE 조건부 0**을 보인다. 수정 규칙·급여 하한 유지 시 미사용 예외의 신규 6(m)(2) 산입도 조건부 0 | 적용 방출잔액·기타 권리·미서명 1R·DPE 실제 허가/사용·기타 조정의 실제 합계 또는 근거 있는 전체 상한. 코로나 수정 CBA의 날짜/조항 원문, 1차 Chicago 계약 장부, 대체 선행 거래 전수, 거래 수취/송출 charge도 별도. 전체 R은 null이며 캠프 3명 연간 전액 시험이나 AD 위험 분기는 그 전체 상한이 아님 |
| F2 / 거래 | [Boston 자산](NBA_2021_ASSET_CHAIN.md): Bane발 MEM2025 출처, Fournier TPE 원역사 사용과 후대 잔액 대조. [Orlando 3/25 등록 연결](../research/O15F14S_ORLANDO_MARCH25_REGISTRATION_BRIDGE.md): 선택 거래의 일반 15+투웨이 2 자리 산술 PASS. [BOS/DEN 급여](BOSTON_DENVER_2020_21_PAYROLL.md): Boston 조건부 apron 여유 $5,381,195 | 거래 시점 TPE 정확 가용액·수취 charge·다른 사용, BOS/MEM2025 및 BOS2027의 보호/우선권, Teague/Orlando 거래일 비용과 미포함 순증 부담 |
| F3 / 거래 | [실행 조항](CHICAGO_2020_21_EXECUTION_TERMS.md): Gordon 공개 보너스 포함 matching. [이번 후속](NBA_2021_EXECUTION_RESOLUTION.md): 후행 보호 종료 보도 회수. [DEN 급여](BOSTON_DENVER_2020_21_PAYROLL.md): 조건부 apron 여유 $6,684,733 | 선행 1R이 2R로 전환될 때 후행의 연결, 해당 미래 자산의 전체 가용성·우선권, 정확 charge/미포함 부담. 후행의 일반 종료 문구 자체를 다시 찾을 필요는 없음 |
| F4 / 등록 | [작가 선택·국소 검산](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md): Hall 5/9 새 계약을 생략해 다섯 경기 일반 15+투웨이 2, 4월 두 계약은 보존. 조건부 ORL apron 여유 $14,809,543. [5경기 Bamba 상태·대체 부하 대조](../research/O15F14Q_ORLANDO_HALL_NO_RESIGN_F4_SCREEN.md#5월-원역사-건강출전-대조-후속-검문)에서 5/11 원역사 `Out`에는 Bamba 0분, 5/14·16 원역사 복귀/출전과 선택 분을 분리했다. [5/16 부하 민감도](../research/O15F14AL_ORLANDO_HALL_FINAL_GAME_LOAD_BOUND.md)는 Bamba·Wagner를 원경기 출전분 이하로 두는 240분/5인조 증인을 확보했다. [사전 보고](../research/O15F14N_HALL_MAY9_16_FOUR_PLAYER_STATUS.md)·[최종 미출전](../research/O15F14O_HALL_FIVE_FINAL_BOX_ABSENCE.md)은 원역사 비교 이력 | 5경기 대체 분·건강/체력, 전체 Orlando 계약 비용·미포함 부담, 후속 등록. **Hall 신규 hardship 허가는 선택 경로의 조건이 아님** |
| F5 / 등록·거래 | [작가 선택·국소 검산](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md): McGee–Hartenstein 거래 생략, 두 선수 원소속 잔류, DEN 11·CLE 14경기 국소 승패 불변. 조건부 DEN apron 여유 $9,264,169. [Cleveland 5/4 공식 등록](../research/O15F14U_CLEVELAND_VAREJAO_HARDSHIP_F5.md): 원역사 Varejão 영입 뒤 일반 16+투웨이 2. [C1/C2 비용·선택](../research/O15F14AA_CLEVELAND_VAREJAO_C1_C2_DECISION_PACKET.md): 5/4 10일+5/14 형식 미인증 후속, 조건부 팀 charge $144,297 대 생략 $0. [C2 5경기 화면](../research/O15F14V_CLEVELAND_VAREJAO_OMISSION_MINUTE_SCREEN.md): 35:56 재배정, 조건부 5인조 5/5·국소 및 F14F 상대팀 구간 합 두 방법 각 10/10 방향 유지. [Denver 원역사 비교](../research/O15F14Z_DENVER_2021_PLAYOFF_NONTRADE_SCREEN.md): McGee 4경기 33:49·6경기 DNP. [K1+L2 대진](CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md): Denver–Lakers 1라운드 | 작가가 선택한 C2 경로의 Cleveland 전체 등록·급여/건강/새 나비효과와 DEN–LAL 새 1라운드의 건강·등록·로테이션·승패/후속 대진. 원역사 6/13 퇴장·19:40은 비교치. **원거래 Grant TPE·두 2R 이전은 선택 경로에서 미발생** |

[F2/F3 픽 원역사 1차 스냅샷](NBA_2021_ASSET_CHAIN.md)은 Orlando 구단의 2021년 6월 기사에서 BOS/MEM 2025 뒤 2R·BOS 2027 2R·DEN 2025 top5 1R을 직접 확인했다. 이 구단 기사에는 전체 픽 원계약의 2027 BOS 우선권/보호나 DEN 2026–27 연결/종료가 없어 위 F2/F3 정확 필드는 계속 `HOLD`다.

[F1 2020 CBA 발표 범위](../research/O15F14BC_2020_CBA_AMENDMENT_PUBLIC_SOURCE_BOUNDARY.md)는 공식 11/09·11/10 발표가 캡·일정과 수정 승인 사실을 확인하지만 수정 조항 전문·Chicago 개별 장부를 제공하지 않음을 분리했다. 발표 수치를 정확 §6(m)(2) 적용이나 전체 `R`의 대용으로 쓰지 않는다. F1은 `HOLD`다.

[F5 Denver 플레이오프 구간 검문](../research/O15F14AC_DENVER_PLAYOFF_NONTRADE_STINT_WITNESS.md)은 원역사 McGee 4경기의 공식 교대 시계를 `33:49`와 맞췄고, 6/13 `19:40` 가운데 퇴장 후 `15:49.3`을 분리했다. 이 초 단위 증인은 M1 동일 슬롯 치환의 비용을 특정하지만 Hartenstein의 건강·실제 5인조·승패 또는 추가 경기의 최종 증거가 아니다.

[F5 Denver 원역사 5인조 겹침 후속](../research/O15F14AN_DENVER_2021_PLAYOFF_ROSTER_COLLISION.md)은 McGee와 선택 경로에서 Orlando로 간 Nnaji의 동시 출전 `11:17`을 확인했다. McGee→Hartenstein 한 명 치환만으로는 그 두 경기 구간의 Denver 명단이 성립하지 않는다. Bey까지 치환한 14개 McGee 시간 구간의 수량·K1 역할 검사는 조건부 통과했으나, McGee와 겹치지 않은 Nnaji 최소 `6:22`와 전체 등록·건강·플레이오프 승패는 `HOLD`다.

[F5 Nnaji 단독 구간 후속](../research/O15F14AO_DENVER_NNAJI_OTHER_PLAYOFF_STINTS.md)은 위 `6:22`의 세 NBA 공식 박스와 FOX 2차 교대 표기를 결합해 4개 시간 구간을 분리했다. Hartenstein 조건부 배분의 4/4 K1 역할·인원 검사와 앞선 14개 McGee 구간을 합친 18/18 검사는 통과했다. Bey 단독 치환은 5/24 첫 26초에서 K1 센터 태그가 없고, 원역사 Nnaji도 그 모델에서는 센터 태그가 없다. 이것은 모델의 보수적 경계이며 출전 가능·감독 선택·점수·시리즈를 인증하지 않는다. F5와 시즌 게이트는 `HOLD`다.

[F5 건강 인과 경계](../research/O15F14AP_DENVER_HARTENSTEIN_HEALTH_CAUSALITY.md)는 NBA 공식 부상 보고의 Hartenstein 뇌진탕·결장 표기가 원역사 **Cleveland 경로**에 속함을 확인했다. 거래 생략 뒤 Denver 건강 장부에 이 결장을 복사할 수 없고, Denver에서 건강했다는 증명도 아니다. 위 18/18 조건부 5인조는 A1 날짜별 가용성을 아직 통과하지 않았다.

[K1+L2 플레이오프 대진 연결](CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)을 원입력에서 재현하면 Denver 3번–Lakers 6번, Phoenix 2번–Portland 7번이다. 위 McGee `33:49`·Nnaji `17:39`·18/18은 **원역사 Portland→Phoenix 경로**의 비교·동일 대진 민감도다. K1+L2 F5를 닫으려면 Denver–Lakers 새 시리즈부터 검문해야 하며, 원역사 6/13 퇴장이나 Phoenix 4차전 결과를 대체 일정으로 상속하지 않는다. F5·A3·K_METHOD_EVENTS `HOLD`는 그대로다.

[Denver–Lakers 원역사 맞대결/개막 비교](../research/O15F14AU_DENVER_LAKERS_PLAYOFF_COMPARATOR.md)는 5/3 McGee `12:24=744초`가 F5 국소 치환 입력과 맞지만, 당시 James·Schröder는 결장했고 원역사 5/23 Lakers 첫 플레이오프 경기에는 둘 다 출전했음을 공식 경기책으로 확인했다. Denver 5/22 Portland 상대 출전도 다른 시리즈의 기록이다. 5/3의 두 방법 Lakers 승리 방향은 새 시리즈 4~7경기의 건강·점수 증명이 아니다. F5/A1/A3와 K_METHOD_EVENTS는 계속 `HOLD`다.

[2월 DEN–LAL 동일 상대 선례](../research/O15F14AW_DEN_LAL_HARTENSTEIN_HEAD_TO_HEAD_PRECEDENT.md)에서 Hartenstein 원역사 `10:11`·`3:04` 출전을 확인했다. 하지만 두 경기의 Hampton Denver 출전분은 대체 Draft의 Dallas행으로 무효이며 2/14 Davis 재부상도 A1 인과 분기다. 이 자료를 5월 Hartenstein 분·Davis 건강·시리즈 승패의 확정값으로 쓰지 않는다.

[F038/L2 대진 민감도](../research/O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)는 4/15 Boston–Lakers 반전 한 건만으로 Denver 3–Dallas 6이 되고, 2/14 Lakers–Denver 반전 한 건은 Denver 4–Lakers 5로 같은 상대라도 다음 라운드 갈래를 바꿈을 검산했다. 건강·코칭·경기 결과는 미선택이다. F5/K_METHOD_EVENTS를 닫기 전에 A1 선행 사건과 최종 시드를 함께 재산출해야 한다.

AX 후속은 두 사건의 `홈_원정` ID를 기준 원경기와 직접 맞추고, Davis 원역사 결장 30경기 14–16과 3/20 LeBron 별도 발목 사건을 재집계했다. F038은 이 30경기의 승패를 바꾼 적이 없다. A1이 건강 경로를 달리 택하면 변경된 날짜만이 아니라 Lakers 순위·상대 승수·Denver의 첫 대진을 다시 산출한다. [AX 근거·16패 원장](../research/O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)은 가용성이나 경기 반전을 확정하지 않는다.

[F1 이름 있는 FA 보류액 후속](../research/O15F14AG_CHICAGO_2020_FA_HOLD_FOLLOWUP.md)은 Valentine·Mokoka 재계약과 Strus의 Miami 영입을 공식 연혁에 연결했다. 이 계약 경로에서 세 명의 종전 보류액은 별도 추가하지 않지만, 전체 과거 권리·방출액·미서명 1R·예외/기타 조정과 R은 계속 미확정이다. F1 통과나 `$5,609,972` 한도 증가로 읽지 않는다.

[F1 미서명 1R·출처 한계](../research/O15F14AH_CHICAGO_UNSIGNED_FIRST_RIGHTS_SOURCE_SCOPE.md)는 구단 가이드의 일부 지명/권리 계약을 확인하고, 2019-01-22 Diebler 2R 권리 누락을 당시 구단 공식 공지와 대조했다. 가이드 무기재는 2021-03-25 **모든** 미서명 1R/거래 예외 0의 증명이 아니다. `UNSIGNED_FIRSTS`, R과 F1은 HOLD다.

[F1 방출잔액 날짜 검문](../research/O15F14AR_CHICAGO_DEAD_MONEY_DATED_SCREEN.md)은 동시대 2차 보도에서 **4/16 원역사 Chicago dead money $97,261**을 회수했다. 대체세계 3/25 charge로 앞당겨 확정하지 않는다. 같은 값이 적용된다는 조건의 다른 R 여유는 `$5,512,711`이지만 `WAIVED_PAY`·R·F1은 `HOLD`다.

[F2 Boston Hayward TPE 용량](../research/O15F14AI_BOSTON_FOURNIER_TPE_CAPACITY_BOUND.md)은 NBA 3/16 약 `$28.5m` 기사와 공식 시즌 거래표를 연결했다. 거래표에 3/16~24 Boston 거래가 없고 3/25에는 Fournier·Theis 3팀 거래 두 건이 있다. 2차 계약액으로 Kornet·Wagner를 같은 Hayward 예외에 먼저 모두 차감하는 스트레스에서 `$28m−$4.41192m−$17.45m=$6.13808m`이다. 이것은 **공개 입력의 조건부 명목 용량**이며 리그의 정확 예외 잔액·수취 charge, Boston/Orlando 전체 급여와 픽 가용성은 HOLD다. [도구·반증 기록](../reviews/R01_O15F14AI_BOSTON_TPE_CAPACITY_REVIEW.md)은 AG/NLM의 공유 출처와 문서 단독 Claude 검수를 분리한다.

[F2 Orlando 거래일 순서 화면](../research/O15F14AJ_ORLANDO_TRADE_DAY_ORDER_SCREEN.md)은 두 거래 뒤 동일한 후반 장부에 도달해도 중간 apron 여유가 Gordon 먼저 `$4,064,216`, Fournier 먼저 `$22,644,815`로 갈라짐을 재현했다. Gordon 먼저에서 캠프 4명 연간 전액을 추가한 가혹한 시험은 `$76,411` 초과다. 실제 캠프 charge·hard-cap 트리거·리그 처리 순서가 미확정이므로 거래 실패나 위반을 선언하지 않는다. 등록 15+2 검산과 별도로 `F2=HOLD`를 유지한다.

[F2 Orlando MLE 재분류 조건](../research/O15F14AK_ORLANDO_2020_MLE_RECLASSIFICATION_GATE.md)은 공개된 Ennis/Clark 첫해 `$5.3m`과 보고된 1·2년 기간이 2017 CBA VII §6(f)(5)의 납세 MLE 전환 숫자 조건에 들어갈 수 있음을 보인다. 이는 정확 계약·추가 예외·2020 수정 조항이 같을 때의 **조건부 후보**이며 AJ의 `$76,411` 스트레스를 법적 실패로 승격하지 않는다. hard-cap 발생 여부와 F2는 계속 `HOLD`다.

등록 대조는 기존 범위에서 ORL 19경기 및 BOS/DEN 양수 선수·날짜 267+266에 충돌이 없었다. 이는 리그 전체 등록·건강의 인증이 아니다. **ORL 5/9 이후 5경기의 추가 일반계약 1자리는 Hall 재계약을 유지한 원안에서만 필요했고, 선택된 생략 경로에서는 필요하지 않다.** 출전 분이 0인 선수를 급여·등록 원장에서 삭제하지 않는다.

F4 분 부담의 최신 [5경기 상한 화면](../research/O15F14AM_ORLANDO_HALL_FIVE_GAME_OBSERVED_LOAD.md)은 Bamba의 원경기 출전분 초과를 0으로, Wagner의 원경기 초과를 5/11·13 합계 `9:43`으로 낮춘다. 이는 K1의 다른 선수 분을 고정하고 Vučević 36분·Nnaji 16분 상한을 쓴 **국소 후보**이며 대체 건강·전시즌 실행의 PASS가 아니다.

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
