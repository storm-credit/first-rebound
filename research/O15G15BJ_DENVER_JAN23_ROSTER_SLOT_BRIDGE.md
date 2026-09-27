# O-15G15BJ — Denver 2022-01-23 정규 15인·투웨이 2인 자리 다리

- 선행: [G15BI 쿼터 교대 후보](O15G15BI_DENVER_QUARTER_ROTATION_WITNESS.md). [조건부 명단 JSON](../simulation/O15G15BJ_DENVER_JAN23_ROSTER_SWAP.json)과 [검사기](../tools/check_o15g15bj_denver_roster.py)는 **자리 수와 교대 선수의 명단 포함만** 확인한다.
- 판정: `ROSTER_SLOT_PARITY_CONDITIONAL_PASS / SIGNING_TRANSACTION_SALARY_MEDICAL_HOLD`. 정본/최종 경기 승패 변경 0건.

## 1. 공식 1/23 원역사 명단과 날짜

[Denver의 DET전 경기 노트 2쪽](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/01/nuggetsPistons.pdf)는 아래 17명을 싣고 Howard·Reed에 투웨이 별표를 붙인다. **정규계약 15명 + 투웨이 2명**은 그날 원역사 자료의 직접 계수다. 이 명단만으로 대체세계 계약/출전 자격을 보증하지 않는다.

| 구분 | 원역사 선수 |
|---|---|
| 정규계약 15 | Barton, Campazzo, Čančar, Cousins, Forbes, Gordon, JaMychal Green, Jeff Green, Hyland, Jokić, Morris, Murray, **Nnaji**, Porter Jr., Rivers |
| 투웨이 2 | Markus Howard, **Davon Reed** |

[같은 경기 노트 1쪽](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/01/nuggetsPistons.pdf)은 2021-08-18 JaMychal 재계약, 2021-08-31 Rivers 계약, 2022-01-19 **Bol Bol·PJ Dozier 이탈과 Forbes 취득**, 같은 날 Ennis III 방출, 2022-01-21 **Cousins 10일 계약**을 적는다. [NBA 공식 거래 추적기](https://www.nba.com/news/2021-22-nba-trade-tracker)는 Forbes 거래에서 San Antonio가 Hernangómez와 미래 2라운드 픽·현금을 받았다고 적지만, 그 표는 **픽의 연도/원소유 팀과 현금액을 적지 않는다**. 이 비용을 새 확정 Denver 자산으로 자동 차감하지 않는다.

## 2. 대체세계 한 자리 교체가 성립하는 정확한 조건

[2020 정본](../canon/PROJECT_FREEZE.md)의 Denver **Bey22·Nnaji24**, [승인된 Gordon A 선수/자산 방향](../simulation/ORLANDO_DENVER_2021_GORDON_BOARD.md)의 **Nnaji 이탈**을 연결한다. [NBA 공식 2020 지명 결과](https://www.nba.com/news/2020-nba-draft-results-picks-1-60)에서 원역사는 **Bey19·Nnaji22·Hampton24**다. 역사적 Denver는 Nnaji22·Hampton24를 보유했고 실제 Gordon 거래에서 Hampton24가 떠났다. 따라서 다른 계약·거래가 모두 살아남는다는 **비교 조건**에서 1/23 원역사 정규 15명의 **Nnaji 한 자리만 Bey로 바꾸면** 여전히 정규 15·투웨이 2다. X1의 Bey는 명단에 남되 0분, X2의 JaMychal은 명단에 남되 0분이다. 한 분기에서 둘 다 내보내거나, 0분 선수를 명단에서 지우지 않는다.

2022-01-19 거래 뒤 Cousins가 아직 오기 전의 **단순 역산**은 정규 14명, 2022-01-21 계약을 조건부로 적용한 1/23은 15명이다. 이는 1/19 실제 접수 시각·Ennis 계약의 예외·다른 일자별 이동을 재구성한 증명이 아니다. 역사적 Forbes·Cousins 거래가 대체세계에서도 같은 자산·상대 동의·급여로 가능하다는 가정이 필요하다. Forbes 거래가 불성립이면 G15BI의 Forbes20분은 즉시 무효가 되어 교대를 다시 계산한다. Reed의 투웨이 12분도 계약·당일 활동/투웨이 자격이 이어져야 한다.

## 3. 신인 계약과 급여의 제한

[NBA CBA 101 2018–19판](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)의 신인 예외와 rookie scale 설명에 따르면 1라운드 신인이 **서명한 경우** 첫 두 시즌은 보장이고 3·4년차는 별도 팀 옵션이다. Bey가 Denver에서 2020 #22 계약에 서명하고 거래/방출 없이 남았다면 2022-01-23은 계약 **두 번째 시즌**이다. 3년차 옵션 행사는 그날 출전의 선행 조건이 아니다. 지명권 확정이나 2020–21 급여 **가정**만으로 Bey의 실제 서명과 2021–22 보유를 확정하지 않는다.

동일 2020 #22 자리의 Bey 대 원역사 Nnaji는 **같은 연도·순번·서명 비율**이라면 rookie scale 기본급이 같다. 비율을 각각 `r_B`, `r_N`, #22의 2년차 scale을 `S22,2`로 두면 기본급 차이는 `(r_B − r_N) × S22,2`; `r_B = r_N`일 때만 0이다. 이 조건부 **한 항목의 중립성**은 보너스·실제 계약서·2021 Gordon 거래의 급여 매칭·Denver 전체 팀급여/세금·Forbes 거래·픽/현금 비용을 PASS로 바꾸지 않는다. 정확 2020 #22 2년차 금액과 두 계약의 서명 비율은 이 문서에서 채우지 않는다.

## 4. 당일 의료·역할과 다음 연결

[경기 전 Denver 노트](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/01/nuggetsPistons.pdf)는 JaMychal을 `Questionable`로 적고, 더 늦은 [NBA 19:30 ET 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf)는 `Available`로 갱신한다. 뒤 보고서가 원역사의 최신 행이다. 이는 X1의 **대체세계** 건강과 16분 PF 기용 허가가 아니다. X2 Bey의 Denver 당일 활동과 PF 적합성도 별도다.

| 분류 | 이번 판정 |
|---|---|
| 사실 | 원역사 Denver 공식 15+2 명단, 1/19 Forbes·Bol·Dozier 및 1/21 Cousins 사건, 투웨이 Reed, 늦은 보고서의 JaMychal `Available`. 2020 Denver Bey22/Nnaji24 및 Gordon A **선수/자산 방향**은 프로젝트 작가확정. |
| 추론 | Bey 서명·잔류와 모든 다른 계약/거래 지속이 성립하면 Nnaji↔Bey의 **자리 수**는 15+2를 유지한다. 같은 rookie-scale 비율이면 #22 2년차 기본급 차이는 0이다. |
| 후보 | X1 JaMychal PF16/Bey0 또는 X2 Bey PF16/JaMychal0, Forbes 거래와 Cousins 계약을 유지한 교대. |
| 작가확정 | 이번 0건. Gordon **정확 실행**, Bey 서명/급여/당일 등록, Forbes 거래의 미래 픽·현금·상대 동의, Cousins·Reed 조건, 두 수신자 의료/역할, 시즌 결과 모두 `HOLD`. |

다음은 Denver 2021-03-25→2022-01-23의 **실제 계약액·자산·거래 순서 원장**과 Detroit Bey/Hayes 이탈·DB1 Cade 조건 및 Patrick/Kira/Suggs 대체 등록·기회 비용을 함께 검산한다. Chicago 2020–21 D1 F1~F5 `0/5`·A1~A3 `0/3`·K `0/4`, G14 DET `PRIOR_HOLD`/ORL `ROLE_HOLD`, G16/G17은 그대로다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; 전체 7묶음 1완료·1진행·5대기, 진행 중 포함 6묶음 남음.

### 후속 — G15BK Bol 소유의 선행 조건

[G15BK](O15G15BK_DET_DEN_BOL_MCGRUDER_FORBES_DEPENDENCY.md)는 원역사 1/10 Detroit행 Bol–McGruder 거래 **발표**가 1/13 의료 사유로 취소되어, 1/19 Denver가 Bol을 Boston에 보낼 수 있었음을 연결했다. 대체세계에서 1/10 거래가 완료되면 Denver의 Bol 보유가 없어 원형 Forbes 거래가 막힌다. 따라서 이 문서의 Forbes 포함 15+2와 G15BI의 Forbes20분은 **취소 유지 또는 검증된 대체 거래**를 선행 조건으로 추가한다. 두 경로 모두 후보이며 신규 작가확정 0건이다.
