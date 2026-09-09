# 후반 상대 접촉·생산성 입력 — O-15F7

- 상태: `OBSERVATION_AND_CHICAGO_BOX_INPUT_PASS / OPPONENT_ALLOCATION_AND_IMPACT_HOLD`
- 기준 main: `0665795e4c2a91c6b3301874f4254b7b7c99c1a4` (PR #137)
- 전체 위치: 설정집 매크로 2/7, Chicago 2020–21 후반 입력
- 원고 게이트: `CLOSED / manuscript_allowed: false`

## 1. 이번에 닫은 범위

후반 29경기의 양 팀 실제 박스 **815행**, 관련 실존 선수 **300명의 3월 24일 cutoff 관측 원장**, Chicago 조건부 분 2가지×생산성 LOW/BASE/HIGH×29경기의 **174개 박스 귀속 입력**을 작성했다. 상대의 변경된 분과 causal impact는 아직 계산하지 않았다.

공개 NBA V3 미러의 2020-21 시즌 28,859행·1,080경기·30개 팀에서 필요한 관측만 추출했다. 기존 Chicago 전반 625,202초와 후반 417,603초를 대조했고, 후반의 선수·분·득점·선발·코멘트·plus-minus가 기존 원장과 전부 일치한다. 양 팀별 선발5명·팀 총분·득점과 선수 plus-minus 합도 대조했다. 원래 경기별 초 표시 잔차는 실제 표에 보존한다.

출처: [NBA V3 공개 미러](https://github.com/NocturneBear/NBA-Data-2010-2024). 공식 [04-14 Orlando–Chicago 경기 페이지](https://www.nba.com/game/orl-vs-chi-0022000833/box-score)와 [04-11 Chicago–Minnesota 경기 페이지](https://www.nba.com/game/chi-vs-min-0022000812/box-score)의 경기 식별은 확인했으나 HTML에서 숫자 박스를 전부 추출하지 못했다. 미러의 숫자를 새로 공식 endpoint와 전수 대조했다고 주장하지 않는다. 미러 커밋·입력 해시·수집 범위는 `CHICAGO_2020_21_POSTDEADLINE_INPUT_PROVENANCE.json`에 보존한다.

## 2. 상대 변화: 7팀·10경기를 우선 재계산

| 상대 | 직접 경기 수 | 이번에 특정한 변경 | 다음 수치 입력 |
|---|---:|---|---|
| GSW | 1 | 2018 Hutchison/Evans 후보가 Russell–Wiggins 거래 보조 자산에 접촉 | 후보 가치·거래 조건; 당일 옛 선수 분0이 무변경 증명은 아님 |
| MIN | 1 | Edwards 대신 가상 라이벌, 위 2018 거래 조건 연결 | 라이벌 신인 역할·생산성, 실제 Edwards 분의 적절한 donor 범위 |
| CHA | 2 | LaMelo·Riller 대신 Edwards·Terry; Carey/Richards 픽 슬롯 변경 | 가드 창출·분 분배. LaMelo 손목 사건을 Edwards에게 이식 금지 |
| DET | 1 | Hayes·Bey 대신 Patrick·Kira; Stewart는 팀 유지 | 가드/윙 역할별 donor, 실제 선수의 분·성과 일대일 복사 금지 |
| TOR | 2 | Portland에 Trent가 없어 Powell 원거래가 그대로 성립하지 않음 | Powell·Trent·Hood 행선지 조건, Toronto 분 분기 |
| ORL | 1 | Carter·Porter Chicago 보존, Hampton Dallas; Vučević·Gordon·Fournier 미정 | 정확 거래 가지별 로스터·분, 현재 실제 박스 재사용 금지 |
| BOS | 2 | Theis·Green 출발은 승인 경로와 부합; Fournier/Wagner 후속 연결 미정 | 당일 가용성과 Fournier·후속 자리 분기 |

나머지 **12팀·19경기**는 검토한 드래프트/마감일 경로에서 새 직접 변경을 특정하지 못한 기준선 후보다. 리그 전체 파급이 없다는 증명이나 상대 로스터 FINAL이 아니다. 해당 팀은 SAS·PHX·UTA·BKN·IND·ATL·MEM·CLE·MIA·NYK·MIL·PHI다. 폐기된 Atlanta 주인공 분기의 Spellman/Metu/Spalding 이적을 활성 Chicago 세계선에 끌어오지 않았다.

`CHICAGO_2020_21_POSTDEADLINE_OPPONENT_QUEUE.csv`는 29행마다 정본 근거, 검토한 변화, 실제 접촉 선수의 초, 상대 분 미배정 및 outcome HOLD를 기록한다. 예를 들어 TOR 05-13의 명시한 접촉 선수 실제 분이 0이어도 다른 가지의 Powell 등 새로운 분은 0으로 확정되지 않는다. 접촉 선수 초는 영향도나 변화 크기의 추정치가 아니다.

## 3. Chicago 생산성 입력 정책

실존 선수는 **2020-12-23~2021-03-24 실제 리그 관측치의 합계/36분**을 사용한다. 여러 팀에서 뛴 선수는 같은 cutoff까지의 팀들을 합산하고 팀 코드를 기록한다. Theis/Green의 Boston 표본과 Carter/Porter의 Chicago 표본을 사용할 수 있지만 이후 새 팀에서의 성과를 미리 가져오지 않는다.

주인공과 Chicago LaMelo는 기존 `CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv`의 LOW/BASE/HIGH를 그대로 이어 쓴다. 시즌 후반이라는 이유만으로 새 성장 보너스를 주지 않는다. LaMelo의 실존 관측 행이 있어도 Chicago 계산에는 잠긴 역할 prior가 우선한다. 주인공은 제1옵션·전업 PG가 되지 않는다.

분은 O-15F6B의 PORTER_ZERO/PORTER_CAPPED 최소 변경 5인 조합 후보다. 두 가지 모두 아직 가용성 가정이다. 새 결장 스트레스와 섞어 한 시즌 기록으로 합산하지 않는다. 각 날짜의 기존 +1초 잔차를 실제 기대분과 대체 기대분 양쪽에서 동일하게 보정하므로 비교되는 팀 분은 양쪽 모두 240분이다. 원본 실제 CSV는 수정하지 않는다.

실존 선수 양쪽 기대 귀속은 `같은 cutoff rate × 해당 분/36`으로 계산한다. 대체 기대 귀속에서 같은 rate를 쓴 실제분 기대 귀속을 뺀다. **실제 관측 팀 박스에 새 선수 박스를 더하는 계산이 아니다.** 이는 분 이전의 귀속 감사이며 사용률·슈팅 기회·동료 패스 귀속·수비를 재생성하지 않는다. 기존 전반 prior보다 방법이 우수하다는 선언도 아니다.

## 4. BASE 참고선과 대가

두 가용성 가정에서 주인공은 29경기 870분, LaMelo는 812분이다. 다음은 해당 분과 기존 per-36 prior를 곱한 참고 평균이다. 실제 GP·성장 성과·정수 경기 박스로 LOCK하지 않는다.

| 선수 | 가정 분/경기 | PTS | REB | AST |
|---|---:|---:|---:|---:|
| 주인공 | 30.0 | 12.08 | 8.17 | 2.67 |
| LaMelo | 28.0 | 14.00 | 5.29 | 5.60 |

29경기의 대체 기대 귀속 − 실제분 기대 귀속:

| 가용성 가정 | PTS | REB | AST | STL | BLK | TOV | PF |
|---|---:|---:|---:|---:|---:|---:|---:|
| PORTER_ZERO | -69.41 | +56.19 | +86.72 | +33.98 | +8.82 | +54.93 | +78.73 |
| PORTER_CAPPED | -44.04 | +91.11 | +70.88 | +32.59 | +8.29 | +51.74 | +76.89 |

이 표는 Vučević 미영입을 포함한 전체 분·선수 변화의 조건부 귀속 효과다. 특정 선수 한 명의 인과 효과가 아니며 **득점 차이 -44/-69를 팀 점수차에 직접 더하지 않는다.** 리바운드·어시스트 증가도 팀 총량 보상이 아니다. 턴오버·파울 비용을 남겨 두고 impact 단계에서 중복 산입을 차단한다.

### 표본의 한계

120분 미만은 표본 주의 표식이며 통계적 유의성 기준이 아니다. Dotson 9:32, Mokoka 46:41, Felicio 39:44 등의 원시 rate를 안정된 NBA 역할 예측치로 사용하지 않는다. 특히 Felicio 비상18분의 효율 비용은 이 all-active BASE에 포함되지 않았다.

300명 중 14명은 cutoff까지 양수 NBA 분이 없다: Anthony Tolliver, Cam Reynolds, Dewayne Dedmon, Donta Hall, Elijah Bryant, Freddie Gillespie, Grant Riller, Kris Dunn, Matthew Dellavedova, Mike James, Oshae Brissett, Robert Franks, Romeo Langford, Udonis Haslem. 이들은 rate 칸을 비우고 `NO_PREDEADLINE_SAMPLE`로 남겼다. 0능력·0impact로 대체하지 않는다. 다음 상대 입력에서 이전 NBA 시즌 또는 적합한 하위리그 표본과 역할 범위를 검토하며 이후 NBA 성과를 cutoff 정보로 넣지 않는다. 이번 Chicago 분 계산의 모든 실존 선수에는 양수 cutoff 표본이 있다.

## 5. LaMelo 잔여 세 조건 종료

| 날짜 | 기존 실패 원인 | 대안 | 결과 |
|---|---|---|---|
| 03-31 | 외곽 분 상한 부족 | Coach's Decision DNP인 Green/Mokoka/Dotson 중 조건부 벤치 후보를 각 최대12분 범위로 열기 | PASS |
| 04-04 | 외곽 분 상한 부족 | 동일 조건부 벤치 후보 정책 | PASS |
| 05-15 | 볼 운반자 분 상한 부족 | 기존 배분에서0이 된 Arcidiacono의 실제13:36 상한 복원 | PASS |

이는 두 정책×실패3날짜의 **6개 시험**이다. 원래 통과한26조건은 보존한다. 위 대안을 더하면 LaMelo 단독 공백29조건의 분 존재 증명이 갖춰지지만, 실제 부상 일정이나 상대 대응까지 확정한 것은 아니다. 주인공·Carter·Porter·LaVine 분과 선발 조합은 고정했고 주인공을 PG로 새로 분류하지 않았다. 각각의 순서 없는 조합 증명은 `CHICAGO_2020_21_LAMELO_RESPONSES.json`에 있다. 벤치 후보 모두를 반드시12분 쓰는 정책이 아니며 실제 등록·건강은 여전히 조건이다.

## 6. 다음 종료 조건

**O-15F8: 상대 변경 분·생산성과 양 팀 impact 입력.** 7팀10경기의 가지별 분을 배정하고, 나머지19경기의 기준선 적용 범위를 확인한다. 무표본14명 중 실제 계산에 쓰이는 선수만 과거 표본을 보충한다. 그 뒤 Chicago 변화와 상대 변화를 함께 반영한 outcome을 계산한다. 최종 72경기 결합 전에는 전반19~21승 모델의 상대 고정 한계도 같은 접촉 목록으로 회수한다. 후반만 양 팀을 고쳐 전반을 완전한 정본으로 간주하지 않는다.

다시 만들지 않을 것: 2020 드래프트 팀보드, Carter 단독 공백 전체 감사, 기존 전반 prior, 이번815행 실측 수집. 새 증거·입력 변경이 있는 부분만 재개한다. 원고와 정확 거래·시즌 기록은 계속 닫혀 있다.

검증: `python tools/build_chicago_2020_21_postdeadline_inputs.py`, `python tools/audit_chicago_2020_21_lamelo_responses.py`.
