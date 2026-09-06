# Chicago 2019-20 Impact Crosscheck v0.1

- 상태: `EXTERNAL_METHOD_CROSSCHECK_PASS / CENTRAL_SEED7_ROBUST / TAIL_ENVELOPE_OPEN`
- 기준일: 2026-09-06
- 적용 범위: O-15C6C historical RAPTOR·regularizer sensitivity·2020 lottery decision boundary
- 원고 게이트: `CLOSED`

## 결론

FiveThirtyEight의 historical modern RAPTOR를 제3계열로 적용했다. 2019-20 modern RAPTOR는 box estimate와 on/off plus-minus를 결합하고 tracking-era 데이터를 사용하므로 Basketball-Reference BPM이나 NBA raw on-court NET과 계산 계열이 같지 않다.

RAPTOR_EB-1000의 LOW/BASE/HIGH는 무피로 **20/21/22승**, second-night stress 포함 **20~22승**이다. 500~2,000분 regularizer 전체 stress에서는 19승 꼬리가 생긴다. 따라서 전체 tail envelope는 기존 21~24승에서 **19~24승**으로 넓어진다.

그러나 정본 중심값인 BASE끼리만 비교하면 BPM 21~22, NET_EB 22, RAPTOR_EB 21로 모두 **21~22승**이다. 두 기록 모두 Chicago lottery seed 7을 유지한다. exact 승수를 고르지 않고도 `central seed 7`은 견고하다.

## 1. 주인공 RAPTOR prior

O-15C1에서 고정한 2018 윙 9명을 2019-20 RAPTOR로 다시 추적했다. 다팀 선수는 possession 가중 평균이다.

| anchor | 관측값 | 적용 prior |
|---|---:|---:|
| Q1 | -2.709 | LOW -2.7 |
| median | -1.804 | BASE -1.8 |
| Q3 | -0.953 | HIGH -1.0 |

성과를 본 뒤 비교군을 바꾸지 않았다. 이 prior는 주인공의 확정 RAPTOR가 아니라 O-15C6A box range와 같은 종단 비교군 stress다.

## 2. donor RAPTOR regularization

RAPTOR total도 6분의 Max Strus가 +29.41처럼 작은 표본에 흔들린다. 모든 donor를 league-average 0으로 같은 분량만큼 수축한다.

\[
R_i^{EB}=\frac{MIN_i R_i}{MIN_i+M_0}
\]

primary는 `M0=1,000분`, sensitivity는 500·1,500·2,000분이다. 결과를 보고 선수별 수축 강도를 다르게 고르지 않는다.

## 3. primary RAPTOR_EB-1000 결과

| fatigue | LOW | BASE | HIGH |
|---|---:|---:|---:|
| 0 | 20 | 21 | 22 |
| -0.5 / 48분 | 20 | 21 | 21 |
| -1.0 / 48분 | 20 | 21 | 21 |

무피로 LOW에서는 실제 1점 차 G017 Charlotte전과 실제 2점 차 G061 Dallas전이 패배로 바뀐다. BASE는 G017만 바뀐다. 실제 3점 차 이상 반전은 없다.

## 4. regularizer sensitivity

| M0 | 가능한 승수 |
|---:|---|
| 500 | 19·21·22 |
| 1,000 | 20·21·22 |
| 1,500 | 21·22 |
| 2,000 | 21·22 |

500분 LOW의 19승은 G017·G030 Washington·G061을 잃는 stress tail이다. raw RAPTOR 무수축은 작은 표본이 지배하므로 정본 후보에서 제외하지만, 500분 결과는 모델 민감도 경고로 보존한다.

## 5. 세 계열 통합

### 중심 BASE

| proxy | fatigue 0 | -0.5 | -1.0 |
|---|---:|---:|---:|
| BPM | 22 | 21 | 21 |
| NET_EB | 22 | 22 | 22 |
| RAPTOR_EB | 21 | 21 | 21 |

중심 집합은 `{21,22}`이며 둘 다 seed 7이다. G017 반전으로 Charlotte가 24-41이 되어도 Charlotte는 seed 8, Chicago는 seed 7을 유지한다.

### 전체 stress tail

| Chicago 결과 | lottery 위치 | 의미 |
|---:|---|---|
| 19-46 | Cleveland와 seed 2/3 동률 | 14% 조합군·공식 동률 처리 필요 |
| 20-45 | seed 6 | 1순위 9.0% |
| 21-44 | seed 7 | 1순위 7.5% |
| 22-43 | seed 7 | 실제 입력 |
| 24-41 | seed 8 | 1순위 6.0%, Charlotte와 교환 |

tail은 모형 위험 범위이지 동일 가중 정본 후보가 아니다. `19~24의 중간인 21~22`를 평균으로 고른 것도 아니다. 중심 prior와 stress prior의 권위를 분리한다.

## 6. 정본 후보

총괄 추천은 **정확 승수 21~22 HOLD + lottery seed 7 및 실제 4순위 추첨 사건 유지**다.

근거는 세 가지다.

1. 세 외부 계열의 BASE와 fatigue가 전부 21~22승에 있다.
2. 21·22승 모두 Chicago 7·Charlotte 8의 lottery 입력과 조합을 유지한다.
3. exact 승수를 서사 편의로 고르지 않아도 Draft Causality Protocol에 따라 실제 4순위 외부 확률 사건을 유지할 수 있다.

이는 아직 `AUTHOR_APPROVAL_REQUIRED`다. 승인돼도 Patrick Williams 지명은 자동 유지하지 않는다. 4순위 팀보드는 주인공과의 SF/PF 성장시간 중복을 반영해 별도로 연다.

## 7. 남는 한계

- RAPTOR도 실제 변경 전 선수와 lineup 결과를 사용하므로 counterfactual causal estimator는 아니다.
- RAPTOR와 BPM은 모두 box-score 정보를 일부 공유한다. 완전 독립 데이터는 아니다.
- 19승 꼬리는 regularizer 선택에 민감하고 중심 모델보다 권위가 낮다.
- G017은 거의 모든 하방 모델에서 임계 경기다. exact 승수를 잠글 때 possession-level stress가 필요하다.

## 출처

- [FiveThirtyEight — NBA RAPTOR data·변수 설명](https://github.com/fivethirtyeight/data/tree/master/nba-raptor)
- [FiveThirtyEight — modern RAPTOR by team](https://github.com/fivethirtyeight/data/blob/master/nba-raptor/modern_RAPTOR_by_team.csv)
- [NBA Communications — 2020 lottery 공식 records·odds](https://pr.nba.com/2020-nba-draft-tiebreakers/)
- [NBA — 2020 Draft 결과](https://www.nba.com/news/2020-nba-draft-results-picks-1-60)
