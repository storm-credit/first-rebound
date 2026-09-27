# O-15F14-P — Chicago 2020–21 D1 종료 묶음

- 기준: `main` `9ce3b21`; [채택 준비 색인](CHICAGO_2020_21_ADOPTION_READINESS.md), [CP2 통합 검토](../design/CP2_INTEGRATED_REVIEW_PACKET.md), [전체 7개 게이트](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md).
- 현재 판정: `D1_EXACT_EXECUTION_OPEN / CP2_CONDITIONAL_CONTINUATION_ALLOWED`.
- 목적: 이미 회수한 세부 사실을 반복 수집하지 않고 **D1을 닫는 데 필요한 최소 증거와 그 증거가 없을 때의 다음 실행**을 한곳에서 관리한다. 여기서 새 거래·부상·계약·시즌을 채택하지 않는다.

## 1. 확정 가능한 현재 위치

K1의 Chicago 31–41·Minnesota 24–48 정규시즌 **추천**, L2의 Chicago WAS 원정 승리→IND 원정 탈락 **사건 추천**, CP2의 사전 기록된 **잠정 추첨·픽 결산**은 이미 있다. 이는 완료된 조건부 산출물이며 이번 묶음에서 재계산하지 않는다. [K1](CHICAGO_2020_21_SEASON_RECOMMENDATION.md) · [L2](CHICAGO_2020_21_EXECUTION_CLOSEOUT.md) · [잠정 추첨](NBA_2021_PROVISIONAL_DRAFT.md).

정확 실행에 필요한 F1~F5의 **전체 PASS는 0/5**, A1~A3의 **최종 채택은 0/3**, K_HEALTH·K_REGISTRATION·K_TRANSACTIONS·K_METHOD_EVENTS의 **종료는 0/4**다. 이는 증거 행 수나 완료된 조건부 계산 수가 아니라 **게이트 판정**이다. 전체 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다. 완료율로 환산하지 않는다.

이 패킷에서 `PASS`는 해당 경로가 요구한 근거·산술·승인된 선택을 충족한 상태, `HOLD`는 **열린 채로 증거/결정을 기다리는 상태**, `FAIL`은 특정 실행 경로가 반증되어 대안 경로와 파급 재계산이 필요한 상태다. `HOLD`는 PASS·종료·면제가 아니다. F의 증거가 없어도 A의 비교안은 준비할 수 있지만 A의 **최종 채택과 K 종료는 하지 않는다**. F는 사실/계약 경로를 검증하는 관문이고, A는 그 통과 경로 중 대체 세계 사건을 선택하는 별도 관문이므로 순환하지 않는다.

## 2. F1~F5를 한 묶음으로 닫는 증거 기준

| ID | 이미 재사용할 결과 | 정확 종료에 필요한 최소 판정 | 못 얻으면 |
|---|---|---|---|
| F1 Chicago 거래 | [비납세 범위](CHICAGO_2020_21_TAX_BOUND.md)에서 알려진 상단 $127,017,028·미포함 순증 `R_CHI≤$5,609,972` 조건, [R 구성](CHICAGO_2020_21_RESIDUAL_COMPONENTS.md)의 타팀 계약/빈자리 분류 | **3/25 거래 당시** 적용되는 R의 전체 상한 또는 실제 구성과 양측 incoming/outgoing charge를 결합해 비납세 자격·matching을 같은 사건에서 판정 | 기본급 matching 여유만으로 Theis/Green 정확 거래 PASS 불가; 승인된 선수 이동 방향을 폐기하지 않고 `K_TRANSACTIONS=HOLD` |
| F2 Boston Fournier | [자산 연쇄](NBA_2021_ASSET_CHAIN.md)의 MEM2025 출처·TPE 사용 보도/후대 잔액, [BOS 급여](BOSTON_DENVER_2020_21_PAYROLL.md)의 조건부 apron 여유 $5,381,195 | 수취일 Fournier **전체 charge**에 쓴 TPE 당일 가용액/다른 사용, 두 2R의 보호·우선권·가용성과 미포함 팀 부담을 연결 | 후대 $11.05m 잔액 역산을 당일 허가서로 승격하지 않고 거래/픽 소유 `HOLD` |
| F3 Denver Gordon | [실행 조항](CHICAGO_2020_21_EXECUTION_TERMS.md)의 공개 bonus matching, [후속](NBA_2021_EXECUTION_RESOLUTION.md)의 후행 보호 종료 보도, [DEN 급여](BOSTON_DENVER_2020_21_PAYROLL.md)의 조건부 apron 여유 $6,684,733 | **선행 1R이 실제 전달되는 분기와 2R로 전환되는 분기를 각각** 후행 1R 연결·소멸 조건과 대체 Denver의 자산 우선권/가용성·거래일 charge에 결합 | 선행 2R 전환을 후행 1R 전달로 가정하지 않고 Gordon 거래 정확 실행 `HOLD` |
| F4 Orlando Hall 재계약 **생략** | [작가 선택](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)·[선택 브리지](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md): 5/9 이후 일반 15+투웨이 2, Hall 새 계약/추가 자리/신청 불필요, 5경기 분 재배정과 조건부 apron 여유 $14,809,543 | 선택된 대체 건강·분/체력과 다른 후속 등록을 대조하고, Hall 4월 두 계약을 보존한 전체 Orlando 비용 및 미포함 부담을 닫는다 | 원안의 §6.08 추가 자리 허가와 5/9 Hall charge는 **미발생**. 선택 경로의 건강·팀 비용·후속 사건이 남아 `K_REGISTRATION=HOLD` |
| F5 Denver–Cleveland McGee 거래 **생략** | [작가 선택](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)·[선택 브리지](CHICAGO_2020_21_F4_F5_SELECTED_BRIDGE.md): McGee CLE/Hartenstein DEN 잔류, DEN 11·CLE 14경기 국소 분, Denver 조건부 apron 여유 $9,264,169. [Cleveland 5월 검문](../research/O15F14U_CLEVELAND_VAREJAO_HARDSHIP_F5.md): 원역사 Varejão 뒤 16+2. [C2 분 검문](../research/O15F14V_CLEVELAND_VAREJAO_OMISSION_MINUTE_SCREEN.md): 5경기 35:56. [Denver 원역사 비교](../research/O15F14Z_DENVER_2021_PLAYOFF_NONTRADE_SCREEN.md): 10경기 McGee 4출전 33:49, 6 DNP. [K1+L2 대진](CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md): Denver–Lakers 1라운드 | Cleveland의 C1 Varejão hardship 유지 또는 C2 영입 생략을 날짜별 등록·급여/건강/분에 연결한다. Denver는 **Lakers 상대의 새 1라운드** 건강·등록·5인조·가용성·승패를 만들고, 이후 대진·계약·픽 파급과 미포함 부담을 닫는다. 원역사 6/13 Jokić 퇴장·McGee 19:40은 역사 비교이며 K1+L2 입력이 아니다 | 원안의 Grant TPE·McGee 대가 2023/2027 2R 의무는 **미발생**. 1대1 치환·25경기 국소 승패 불변만으로 Cleveland 5월 추가 자리나 전체 F5·`K_TRANSACTIONS` PASS 불가 |

위 금액은 각 문서가 정한 **서로 다른 시점·정의의 조건부 여유**다. Chicago의 6(j) 비납세 검사를 다른 세 팀의 apron 검사와 합산하지 않는다. 공개 보도·2차 계약표·산술 시험은 분야별 문서의 출처 등급대로만 사용한다. 실재하지 않는 리그 원장이나 미공개 계약 문구를 만들어 빈칸을 닫지 않는다.

### F4·F5의 대체 사건 선별 — O-15F14-Q

[F4 Hall 5월 재계약 생략](../research/O15F14Q_ORLANDO_HALL_NO_RESIGN_F4_SCREEN.md)과 [F5 McGee 거래 생략](../research/O15F14Q_DENVER_MCGEE_NONTRADE_F5_SCREEN.md)을 대체 경로로 추가했고, **작가가 두 생략 방향을 선택**했다. 권위는 [F4/F5 결정 기록](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)이다. F4는 5경기 분·등록 수와 10개 평점 비교를, F5는 Denver/Cleveland 25경기 국소 분 치환과 50개 평점 비교를 기록한다. 위 표는 이제 **선택 경로**를 나타낸다. 원안의 Hall hardship/5월 계약 및 McGee TPE/픽 조항은 각 선별 문서에서 비교 이력으로만 보존한다. 기존 승인 T1~T4는 그대로다. 실행 재검증이 남아 있어 F1~F5 전체 PASS `0/5`, A1~A3 최종 채택 `0/3`, K 종료 `0/4` 판정은 아직 바뀌지 않는다.

[F5 Denver 플레이오프 명단 충돌](../research/O15F14AN_DENVER_2021_PLAYOFF_ROSTER_COLLISION.md)은 원역사 McGee 분의 `11:17`에 Nnaji가 동시 출전한 것을 드러냈다. 선택된 Gordon A 아래 Nnaji는 Orlando로 갔으므로 McGee→Hartenstein 단일 치환이 그 구간에서 무효다. Hartenstein·Bey 이중 치환의 조건부 5인조/역할 검사는 통과했으나, 다른 Nnaji `6:22`와 의료·등록·승패는 F5와 K를 계속 묶는다.

[K1+L2 대진 재현](CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)에서는 Denver 3번–Lakers 6번이 첫 라운드다. 위 Portland→Phoenix 10경기 교대 검사는 원역사 비교 및 **동일 대진을 가정한 별도 민감도 시험**으로만 보존한다. 선택 후보 K1+L2의 F5 종료 증거로 승격할 수 없으며 Lakers 상대 분·결과가 새 빈칸이다.

[DEN–LAL 5/3 맞대결 및 5/22·23 개막 경기 대조](../research/O15F14AU_DENVER_LAKERS_PLAYOFF_COMPARATOR.md)는 국소 F5 744초 치환의 공식 분 근거와 James·Schröder의 날짜별 결장/출전 차이를 확인했다. 5/3 정규시즌 승자 방향을 1라운드 승패로 고정하지 않는다. F5/K_METHOD_EVENTS 종료를 위해 건강·등록·양 팀 경기별 분/전술·시리즈 결과가 여전히 필요하다.

[DEN–LAL 개막 분 검문](../research/O15F14AV_DEN_LAL_OPENING_MINUTE_TEMPLATES.md)은 서로 다른 원역사 상대와 치른 Denver 홈 5/22와 Lakers 원정 5/23의 **각 팀 240:00**을 분리해 회수했다. AU의 Lakers `Gasol 7:05`는 `Horton-Tucker 7:05`/Gasol 감독 선택 DNP로 정정했다. Hartenstein·Bey의 대체 분은 선택하지 않았고, 새 상대의 코치 선택·5인조·득점·시리즈 승자는 여전히 미검증이다.

[2월 DEN–LAL 동일 상대 경기책](../research/O15F14AW_DEN_LAL_HARTENSTEIN_HEAD_TO_HEAD_PRECEDENT.md)은 Hartenstein의 원역사 Lakers 상대 출전 `10:11`·`3:04`를 전술 선례로 추가했다. 원역사 Denver의 Hampton 분은 대체 Draft에서 Dallas #31로 이동했으므로 2월부터 복사 불가다. 2/14 Davis의 선행 아킬레스건 상태와 경기 중 재악화도 A1에서 분리해야 한다. 이 선례만으로 F5/A1·시리즈 승패를 닫지 않는다.

F4의 [후속 5경기 부하 상한](../research/O15F14AM_ORLANDO_HALL_FIVE_GAME_OBSERVED_LOAD.md)은 Bamba의 원경기 출전분 초과 없이 5인조·240분·10개 평점 방향을 통과했다. 5/11·13 Wagner의 최소 추가 `3:03`·`6:40`과 Vučević/Nnaji 상한 부하, 전체 계약·후속 등록은 열려 있어 F4/A1/K 판정은 올리지 않는다.

F5 Cleveland의 별도 [Varejão C1/C2 결정 패킷](../research/O15F14AA_CLEVELAND_VAREJAO_C1_C2_DECISION_PACKET.md)은 5/4 첫 10일 계약과 5/14 **형식 미인증 후속**, 조건부 개인 charge 합 $144,297, C2 35:56 재배분 및 추가 자리/2021–22 권리 파급을 비교한다. C2를 추천하지만 **작가 선택 전 후보**다. “10일 계약 2건”은 정확 F5 종료 요건이 아니다.

F2의 BOS/MEM 2025 2R 중 뒤 순번·BOS 2027 2R 규칙은 [Orlando 구단의 2021년 6월 자산 설명](https://www.nba.com/magic/news/orlando-magic-have-great-opportunity-add-several-quality-players-through-draft-next-few-years-20210610)의 검색 색인 문장으로 기존 2차 거래 장부와 대조했다. 이번 접근에서 본문 HTTP 403이므로 **구단 본문 직접 회수로 등급을 올리지 않는다**. 이 대조는 F2의 당일 TPE 사용 가능액·Fournier 전체 charge·다른 자산 의무를 닫지 않는다.

[F2 원거래 동일성 경로](../research/O15F14R_BOSTON_FOURNIER_PRIMARY_EQUIVALENCE.md)에서는 NBA의 거래일 기사로 Hayward 예외의 **원역사 사용**과 Boston/Orlando 구단의 같은 선수·두 2R 거래를 공식 자료에 연결했다. 비공개 센트 원장을 만들어 채우기 전에, Boston 예외/픽·Orlando 3/25~27 Teague 임시 등록과 Vučević 잔류 장부가 원거래의 합법 입력과 동일한지 검증한다. 이름 붙은 Boston 거래 네 선수의 일치만으로 F2 PASS는 아니다. F2·K_TRANSACTIONS `HOLD`와 전체 `0/5`는 유지한다.

[F2 Orlando 당일 순서 화면](../research/O15F14AJ_ORLANDO_TRADE_DAY_ORDER_SCREEN.md)은 기존 급여 입력으로 Gordon 먼저/Fournier 먼저 중간 부담을 분리했다. 0보장 캠프 4명의 연간 기본급 전액을 추가한 Gordon 먼저 스트레스만 apron `$76,411` 초과하지만 실제 charge·hard-cap 트리거·리그 승인 순서 미확정이므로 위반 판정이나 F2 PASS가 아니다. 같은 날 거래라는 말로 중간 급여/세금선 변화를 생략하지 않는다.

[F2 Orlando MLE 전환 규칙](../research/O15F14AK_ORLANDO_2020_MLE_RECLASSIFICATION_GATE.md)은 Ennis/Clark의 2020-12 공개 합계 `$5.3m`·보고 계약 기간이 2017 CBA VII §6(f)(5)의 납세 MLE `$5.718m` 이월 조건에 들어갈 **가능성**을 검문한다. 추가 MLE·BAE·수취 S&T·보너스·2020 수정 규칙이 미확인이고 `$418,000`은 Team Salary 초과분 상쇄액이 아니다. 실제 hard-cap 발생/전환은 계속 HOLD이며 AJ 스트레스 음수를 위반으로 사용하지 않는다.

[F2 Orlando 등록 후속](../research/O15F14S_ORLANDO_MARCH25_REGISTRATION_BRIDGE.md)은 3/24 NBA 공식 경기책의 일반 15+투웨이 2 재관측과 구단 공식 거래 연혁의 3/25 전 공백, 3/27 Teague 방출을 결합했다. 승인 방향의 Gordon/Clark 2:2와 Fournier/Teague 1:1 실행에서 **3/25~26 일반 15+투웨이 2, 3/27 방출 뒤 일반 14+투웨이 2**의 공개 자리 산술은 통과했다. Teague 비용과 Vučević 잔류·Nnaji 수취의 정확 한도/예외, Boston TPE·픽 우선권은 아직 F2 `HOLD`; 이를 다시 자리 수 미검수로 설명하지 않는다.

## 3. 사실 통과 뒤의 최종 채택

| 선택 | 이미 있는 검토안 | 최종 채택 전에 필요한 것 |
|---|---|---|
| A1 건강/분 | K의 1,079행 조건부 가용성·J1 Terry 후반 공백 | 대체 세계의 건강 달력 선택과 F4 등록 자격에 미치는 영향. 실존 선수의 새 진단·의료 예후 창작 금지 |
| A2 Hall 행정 사건 | **작가가 5/9 재계약 생략을 선택**. 선택 명단은 15+2라 Hall 신규 계약·hardship 신청·허가 사건 없음 | 새로운 선택 질문은 불필요. F4의 5경기 대체 분/건강·등록·팀 비용이 닫히면 이 **행정 비발생 사건**을 최종 경로에 반영. 그 전까지 A2 최종 게이트는 `HOLD` |
| A3 시즌/사건 | K1/BPM 전체 경로·L2 동서부 플레이인 추천 | F1~F5·A1/A2와 모순 없는 단일 정규시즌/사건의 최종 작가 채택, 이후 추첨·픽 소유 재검증 |

A1~A3는 기존 Chicago 원클럽, 2020 지명 연쇄, Theis/Green 선수 이동 A, R1/T1~T4 방향을 **재승인받는 질문이 아니다**. 이 단계 전에는 `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`다. `G17` 전체 설계 승인과도 별개다.

A1의 세부 달력과 A3의 시즌/플레이인 대안은 [채택 준비 색인](CHICAGO_2020_21_ADOPTION_READINESS.md) 및 [L1~L4 비교](CHICAGO_2020_21_EXECUTION_CLOSEOUT.md)에서 가져온다. A2의 작가 선택은 이미 [F4/F5 결정](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)에 있다. 이전 Hall hardship 경로는 비교 이력이고, 지금 검증할 것은 5/9 이후 **재계약·신청 없는 15+2 등록**과 그 분/비용이다. A2 최종 게이트 수를 조기 올리지는 않는다.

## 4. 반복 조사 중지선과 다음 실행

1. F1~F5를 **한 번의 거래일 실행 묶음**으로 다룬다. 새 자료가 나올 때 해당 필드·시각·팀·출처 등급과 판정에 미치는 효과를 위 표에 반영한다. 이미 확인된 1080경기, K1/L2, Hall 5경기, 기존 급여 기본표를 새 PR마다 다시 계산하지 않는다.
2. 특정 정확 필드를 공개 자료에서 더 확인하지 못하면 `미확인/0 아님`, 해당 F와 연결된 K를 **열린 `HOLD`**로 남기고 **같은 검색·같은 대체 자료로 재시도하는 작업을 중단**한다. 새로운 원계약/당일 장부/리그 판단/신뢰할 만한 동시대 출처가 발견되거나 명시적 실패 경로의 대안이 제시됐을 때 재개한다. 이 중지선은 게이트 면제가 아니다.
3. 정확 F1~F5가 닫히기 전까지 최종 시즌·2021 실제 순번·계약을 정본화하지 않는다. 이미 승인된 CP2에 따라 [D2 2021 선수·계약](../design/CP2_INTEGRATED_REVIEW_PACKET.md)의 **조건부 후속**을 계속한다. 기존 [60픽 비교](NBA_2021_FULL_DRAFT_COMPARISON.md)와 [G1A/E2 예산](CHICAGO_2021_23_CONTINUATION.md)은 완료 입력으로 재사용한다. 이 ID는 일곱 매크로 게이트의 추가 번호가 아니다. 다음 실행은 `CHI 잠정 #10/#39·백업 C 실명 취득·Caruso 예외 순서`의 한 경로를 거래일/등록일로 연결하는 것이다. 이 역시 정확 계약 채택이 아니다. F 경로가 실패하면 CP2 산출물은 **계속 잠정**이며 영향을 받은 입력과 후손만 다시 계산한다. 실패한 사실 위에 최종 픽을 고정하지 않는다.
4. 새로운 F 증거 또는 비용이 재계산된 대안 경로로 다섯 묶음의 정확 실행이 성립하면 A1~A3를 한 검토 패킷에서 판정한다. 그런 다음 단일 시즌/플레이인→추첨/픽 소유 재검증→네 K 묶음 PASS→D1 종료를 순서대로 수행한다. 특정 경로 `FAIL`이면 이유와 후속 자리·분·자산 비용을 남긴 뒤 영향을 받은 갈래만 다시 계산한다. `HOLD`가 하나라도 최종 사건에 남으면 D1을 종료하지 않는다.

**완료 시점은 달력 날짜가 아니라 4단계의 실제 통과로 결정한다.** 이 패킷 자체는 D1 종료가 아니다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `manuscript_allowed=false`를 유지한다.

문서 단독 반증에서 발견한 HOLD·CP2·F4 승인 표현의 빈틈과 처리 범위는 [R01 검토 기록](../reviews/R01_O15F14P_D1_CLOSEOUT_BLIND.md)에 둔다.

[F5 Denver Nnaji 잔여 구간](../research/O15F14AO_DENVER_NNAJI_OTHER_PLAYOFF_STINTS.md)은 기존 McGee 겹침 11:17 밖의 5/24·6/7·6/11 **6:22**를 세 NBA 박스·FOX 2차 교대로 시간 분리했다. 확정된 Nnaji 이탈과 McGee 거래 생략 아래 Hartenstein/Bey 조건부 배분의 총 18개 양수 구간이 K1 역할·5인 검사에 통과한다. NBA 박스 분과 FOX 교대의 출처 등급, 원역사 대 대체 감독 선택을 구분한다. 이것은 F5·A1·K·시즌 종료가 아니며 표의 `HOLD` 수를 바꾸지 않는다.

[F5 Hartenstein 건강 인과 검문](../research/O15F14AP_DENVER_HARTENSTEIN_HEALTH_CAUSALITY.md)은 원역사 Cleveland의 뇌진탕 보고를 선택된 Denver 경로로 이식하지 못하게 한다. Denver의 새 건강·등록·실제 출전은 미확정이므로 위 18/18은 계속 **가용성 조건부**이고 F5/A1/K 판정은 `HOLD`다.

[F1 Chicago 방출잔액 후속](../research/O15F14AR_CHICAGO_DEAD_MONEY_DATED_SCREEN.md)은 4/16 원역사 팀 총액 `$97,261`을 동시대 2차 보도로 확인했다. 이를 선택된 3/25 정확 장부로 승격하지 않고, 동일 부담이 유지될 때의 잔여 R 여유 `$5,512,711`만 별도 계산한다. F1과 전체 F·A·K 게이트 수는 바뀌지 않는다.

[F1 공개 15인 급여 차액](../research/O15F14AS_CHICAGO_PUBLIC_ROSTER_DELTA.md)은 원역사 보관 15인 기본급과 선택 경로의 같은 자리 입력을 비교한다. Young bonus를 양쪽에서 같게 두면 선택 경로는 주인공 급여 상한에서도 **$1,951,061 낮다**. 이는 알려진 선수 부분의 조건부 비교이며 원역사 보관 표를 거래일 공식 Team Salary로 쓰거나 선택 경로의 명단 밖 `R`이 같다고 가정하지 않는다. F1 정확 실행은 계속 `HOLD`다.
