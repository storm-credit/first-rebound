# O-15G15AB — Detroit 1/23 원역사 전체 박스와 대체 명단 경계

- 시작점: `main` `1adeb18`; [G15AA 세 번째 이탈](O15G15AA_DETROIT_HAYES_THIRD_EXIT_AND_MEDICAL_BOUNDARY.md) 뒤에 남은 **원역사 Detroit 양수 분 전원** 확인.
- 판정: `OFFICIAL_ORIGINAL_BOX_RECONCILED / ALT_CONTRACT_MINUTES_OFFENSE_HOLD`. 원역사 박스의 관측값을 대체 Detroit 결과로 선택하지 않는다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; 신규 작가확정 0건, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.

## 1. 13개 박스 행 중 출전 10명

[NBA 공식 2022-01-23 DET@DEN 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)의 페이지 내장 `__NEXT_DATA__.props.pageProps.game.awayTeam`에서 [원역사 스냅샷](../simulation/NBA_2022_01_23_DET_ORIGINAL_BOX.json)을 추출했다. [검증기](../tools/check_o15g15ab_detroit_box.py)는 선수 행 합계를 공식 팀 `240:00 / 75 FGA / 19 FTA / 111점 / 22 TOV`와 대조했다. **10명 양수 분 + 3명 DNP**이며 선수 초 합도 정확히 `240:00`이다. 이 합계는 실제 역사 관측일 뿐 대체 경기의 포제션·점수 예산이 아니다.

| 원역사 양수 분 | 출전 | FGA | 점수 | TOV | 현재 분기 처리 |
|---|---:|---:|---:|---:|---|
| Saddiq Bey | `30:42` | 11 | 11 | 3 | 2020 **작가확정** DEN22 → 원역사 DET 행 이탈 |
| Killian Hayes | `24:42` | 5 | 8 | 3 | 2020 **작가확정** NOP13 → 원역사 DET 행 이탈 |
| Cade Cunningham | `36:14` | 15 | 18 | 6 | 2021 DB1 CHA1 **후보**에서만 DET 행 이탈 |
| Cory Joseph | `28:24` | 9 | 18 | 2 | 대체 Detroit의 계약·활동 재검증 |
| Hamidou Diallo | `20:25` | 7 | 9 | 1 | 동일 |
| Isaiah Stewart | `26:42` | 8 | 18 | 2 | 2020 정본 DET19지만 2022 계약·활동 별도 |
| Trey Lyles | `21:18` | 11 | 18 | 2 | 대체 팀 계약·활동 별도 |
| Josh Jackson | `17:18` | 2 | 3 | 1 | 동일 |
| Rodney McGruder | `23:38` | 4 | 6 | 2 | 동일 |
| Cassius Stanley | `10:37` | 3 | 2 | 0 | 당일 계약 형태·활동 별도 |

원역사 Luka Garza·Saben Lee·Jamorko Pickett은 최종 박스 `DNP - Coach's Decision` 0분이다. [19:30 ET NBA 부상 보고 4쪽](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf)은 **Garza Out / 복귀 준비**로 적으므로 최종 박스의 DNP 문구를 그날 사전 의료 허가로 바꾸지 않는다. 부상 보고에 이름이 없다는 것만으로 다른 선수의 건강·등록도 증명되지 않는다.

## 2. 두 단계의 제거 집합과 남아 있는 일곱 행

| 적용 조건 | 원역사 Detroit에서 사라지는 **선수 관측 행** | 나머지 원역사 양수 행의 산술 | 대체세계 의미 |
|---|---|---|---|
| 2020 작가확정 지명만 | Bey+Hayes `55:24 / 16 FGA / 19점 / 6 TOV` | 다른 8명 `184:36 / 59 FGA / 92점 / 16 TOV` | Cade의 2021 착지는 아직 선택되지 않음. 8명은 새 팀 보유가 확정된 집합이 아님 |
| 위 + 2021 DB1 조건부 | Bey+Hayes+Cade `91:38 / 31 FGA / 37점 / 12 TOV` | 다른 7명 `148:22 / 44 FGA / 74점 / 10 TOV` | Patrick7·Kira16·조건부 Suggs5의 서명/건강/역할을 새로 결정해야 함 |

`184:36`과 `148:22`는 **원역사 박스에서 지정한 행을 뺀 나머지의 합**이다. 대체 Detroit가 그 분을 그대로 보존할 수 있다는 예측이 아니다. 2020 정본의 Patrick7·Kira16·Stewart19는 지명 결과이며, 2021 DB1 Suggs5는 후속 드래프트 비교안이다. 지명권은 서명·2022-01-23 등록·당일 활동과 다르다. Joseph/Diallo/Lyles/Jackson/McGruder/Stanley의 계약 및 팀 잔류, Stewart의 출전도 날짜별로 확인해야 한다. 역사적 FGA/점수·TOV 잔차를 신인들에게 나누면 기존 선수의 공격 기회를 공짜로 가져온다.

두 줄은 **중첩된 시나리오**다. `91:38` 안에 Bey+Hayes의 `55:24`가 들어 있으므로 둘을 더하지 않는다. DB1 줄에서는 `91:38 + 148:22 = 240:00`이다. 정본의 New Orleans Hayes13과 Detroit Kira16도 동일 순번 중복이 아니라, 원역사 New Orleans Kira13이 2020 드래프트 연쇄에서 다른 팀·순번으로 이동한 결과다.

## 3. 10/20 시험 조합을 1/23에 복사하지 않는다

[G14의 2021-10-20 Detroit 조건부 5인 조합](../simulation/CHICAGO_2021_22_PAIRED_REVIEW.md)은 Patrick·Kira·Suggs와 Joseph/Grant/Olynyk/Plumlee 등을 사용한 **개막 경기**의 수학 증명이다. G14의 원역사 DET `88점 / 90 FGA / 13 FTA / 선수 TOV16`과 이번 1/23 원역사 DET `111점 / 75 FGA / 19 FTA / TOV22`는 날짜·상대·명단이 다른 관측값이다. 어느 값도 대체 1/23의 고정 공격 예산이 아니다.

원역사 1/23 부상 보고에서 Jerami Grant·Kelly Olynyk은 `Out`이다. 이 원역사 의료상태를 대체 Detroit에 자동 적용하지 않지만, **G14의 Grant30·Olynyk18을 사유 없이 그대로 이월할 수 없다는 경고**다. 원역사 [Charlotte의 2021-08-06 공식 발표](https://www.nba.com/hornets/press-releases/charlotte-hornets-acquire-mason-plumlee-and-draft-rights-jt-thor)는 Detroit에서 Plumlee와 37순위 Thor 지명권을 받았다고 한다. 대체세계 G14가 Plumlee를 쓰려면 그 거래를 미실행하는 분기의 자산·계약 비용이 필요하다. 해당 거래 선택은 아직 `HOLD`다.

## 4. 사실·추론·후보·작가확정

| 구분 | 이번 결론 |
|---|---|
| 사실 | NBA 공식 원역사 박스 13행·팀240분/75 FGA/19 FTA/111점/22 TOV, 당시 부상 보고의 원역사 상태, 정본의 2020 지명 경로 |
| 추론 | 2020 정본 두 지명만으로도 원역사 Detroit의 Bey/Hayes 행을 대체 DET 기록으로 보존할 수 없다. DB1을 넣으면 Cade 행도 별도 제거된다 |
| 후보 | 대체 Patrick/Kira 및 조건부 Suggs의 날짜별 5인·볼 권한, Grant/Olynyk 의료 경로, Plumlee 거래 실행 여부 |
| 작가확정 | 이번 0건. 2022-01-23 대체 Detroit 계약·등록·의료·분·FGA/FTA·승패 `HOLD` |

다음은 **대체 Detroit의 2020/2021 신인 서명과 기존 7명 계약·거래의 날짜별 소유 원장**, 그리고 그 이후에만 조건부 1/23 240분·공격 기회 증명이다. Chicago 2020–21 정확 시즌, G14 DET `PRIOR_HOLD`·ORL `ROLE_HOLD`, G16/G17은 그대로다. 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다.

[이번 CLI·제한 source-blind 검토](../reviews/R01_O15G15AB_CLI_AND_SOURCE_BLIND.md)는 NotebookLM의 공식 부상 보고 한정 확인, Antigravity 시간 초과·본문 0건, Claude의 유효한 미해결 게이트와 잘못된 이중계산/드래프트 충돌을 분리했다. 어떤 검토도 G16/G17 완료가 아니다.

### 후속 — G15AC Plumlee 거래의 드래프트 자산 비용

[G15AC](O15G15AC_PLUMLEE_2021_DRAFT_ASSET_COLLISION.md)는 G14의 Plumlee 조건부 잔류와 원역사 2021-08-06 Charlotte 거래가 DB1의 30·37·57·58순위 제안과 **동일하게 실행될 수 없음**을 확인했다. 원역사 DET 1/23에 Plumlee가 없다는 관측만으로 대체 DET Plumlee를 지우거나, G14 C24를 1/23에 무료 추가하지 않는다. 날짜별 계약·거래·활동과 Charlotte 상대 비용은 `HOLD`다.
