# Atlanta 2018-19 Player Production & Impact Priors v1.0

- 상태: `PRIOR_METHOD_HOLD / OUTCOME_INPUTS_HOLD`
- 정본성: `PROVISIONAL_METHOD`
- 적용 범위: Atlanta에서 제거된 Omari Spellman 805.0분과 주인공·실명 수취자에게 재배분된 같은 805.0분
- 데이터 마감: `2026-09-02`
- 원고 게이트: `CLOSED`
- 계산 권위: `simulation/ATLANTA_2018_19_CAUSALITY_LEDGER.xlsx`의 `ATL Priors` 시트

## 결론

이 단계에서는 개인 박스스코어나 대체 승패를 만들지 않는다. 독립 검토에서 수치 교정 근거가 부족하다고 판정했으므로, 결과 실행 전에 다음 네 방화벽만 고정한다.

1. 수취자의 실제 2018-19 시즌 평균을 그대로 복사하지 않고, 교정 완료 전에는 수축 후보값으로만 보관한다.
2. 주인공의 박스 생산성·경기 영향 수치는 최종 시즌 기록이나 확정 prior가 아니라 비교·교정용 후보값이다.
3. 모든 경기 영향은 새 선수의 절대 기여가 아니라 같은 날짜에 제거된 Spellman 기여와의 차이만 계산한다.
4. 피로는 현재 경기 결과를 보지 않고 앞선 일정과 분만 시간순으로 전달하며, 새 부상은 자동 생성하지 않는다.

## 1. 방법 네 안

| 안 | 방법 | 장점 | 치명적 위험 | 판정 |
|---|---|---|---|---|
| A | 실제 2018-19 BPM·per-36을 그대로 복사 | 단순하고 재현이 쉬움 | 173~463분 소표본·센터 마무리 효율을 과신 | 기각 |
| B | 2017-18 이전 자료만 사용 | 결과 누출이 가장 적음 | Hamilton·Poythress 등 역할 표본이 희박해 전원을 임의 서열화 | 기각 |
| C | 전원을 같은 중립 영향값으로 처리 | 작가 편향 최소 | 실제 역할·표본 차이를 모두 버림 | 예비 fallback |
| D | 실제 시즌율에 사전등록한 수축 규칙을 적용하고 주인공은 비교군+중립 영향 중심값 사용 | 역할 증거·소표본 통제·재현성을 함께 확보 | 평균·pseudo-minutes·band가 외부 표본으로 교정되지 않음 | **잠정 선택 / 교정 HOLD** |

선택 D는 해당 경기 점수·승패·그날 박스스코어를 입력으로 사용하지 않는다. 다만 현 단계의 `-2.75`, pseudo-minutes `750`, band 계수는 경험적으로 추정된 값이 아니라 명시적 수축 후보이므로 `empirical Bayes PASS`라고 부르지 않는다. 외부 비교군 교정 또는 보수적 공통평균 fallback 중 하나를 독립 검토로 통과하기 전 outcome runner에 넣지 않는다.

## 2. 박스 생산성 후보

단위는 36분당이며, `TS%`만 비율이다. 실제 선수의 수치는 2018-19 정규시즌 총계에서 환산한 관측값이다. 이 표는 역할 비교와 이후 교정의 입력 후보이며 현재 개인 기록 생성에는 쓰지 않는다. 향후 승인돼도 승패 영향치와 다시 더하지 않는다.

| 선수 | PTS | TRB | AST | STL | BLK | TOV | PF | TS% | 3PA | 3P% | 성격 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 주인공 | 10.0 | 7.5 | 1.8 | 1.3 | 0.9 | 1.6 | 3.6 | .500 | 2.5 | .280 | 후반 지명 수비·리바운드형 SF/PF 중심값 |
| Omari Spellman | 12.2 | 8.7 | 2.1 | 1.2 | 1.1 | 1.4 | 3.0 | .516 | 5.7 | .344 | 실제 제거 donor 비교선 |
| Justin Anderson | 13.8 | 6.5 | 1.8 | 1.7 | 1.0 | 1.8 | 3.7 | .516 | 강한 체격의 수비 윙 |
| Alex Poythress | 12.6 | 9.0 | 2.0 | 0.5 | 1.2 | 1.5 | 5.5 | .571 | 에너지·리바운드 포워드 |
| Miles Plumlee | 16.6 | 8.1 | 3.5 | 1.2 | 0.8 | 2.1 | 2.9 | .654 | 센터 소표본; 윙 prior로 전용 금지 |
| Daniel Hamilton | 10.1 | 8.3 | 3.9 | 1.1 | 0.2 | 2.8 | 3.4 | .455 | 장신 핸들러·리바운딩 윙 |

주인공 중심값은 Hutchison·Spellman·Kurucs·Bates-Diop·Evans의 2018-19 루키 per-36 중앙값을 출발점으로 한다. 현 정본 역할에 맞춰 득점·3점 시도는 낮추고 리바운드·수비 사건·파울은 보수적으로 높였다. 이는 확정 시즌 기록이 아니다.

## 3. 경기 영향 수축 후보

단위는 평균 NBA 선수 대비 100포제션당 점수 영향이다. 아래 규칙은 방법 비교용 수축 후보이며 교정 전 `HOLD`다.

```text
weight_i = observed_minutes_i / (observed_minutes_i + 750)
base_i = weight_i × observed_BPM_i + (1-weight_i) × (-2.75)
band_i = 0.75 + 500 / (observed_minutes_i + 500)
low_i  = max(-6.0, base_i - band_i)
high_i = min(+2.0, base_i + band_i)
```

주인공 후보는 관측 NBA 분이 없으므로 `base=-2.75`, `low=-4.25`, `high=-1.25`다. 수비형이라는 설정만으로 Spellman보다 높은 평균을 주지 않는 안전성 확인용이며 아직 정본 수치가 아니다.

| 선수 | 관측 분 | 관측 BPM | LOW | BASE | HIGH |
|---|---:|---:|---:|---:|---:|
| 주인공 | 0 | — | -4.250 | -2.750 | -1.250 |
| Omari Spellman | 805 | -1.2 | -3.081 | -1.948 | -0.814 |
| Justin Anderson | 463 | -2.7 | -4.000 | -2.731 | -1.462 |
| Alex Poythress | 305 | -3.5 | -4.338 | -2.967 | -1.596 |
| Miles Plumlee | 173 | +1.6 | -3.428 | -1.935 | -0.442 |
| Daniel Hamilton | 204 | -4.1 | -4.499 | -3.039 | -1.578 |

Plumlee의 높은 실제 효율은 173분 센터 마무리 표본이므로 강하게 수축한다. Hamilton·Poythress의 낮은 표본도 같은 방식으로 완화한다.

## 4. 같은 805분의 차이와 불확실성 방향

```text
rotation_delta_100,g(LOW)
= [m_protagonist,g × impact_protagonist(LOW)
   + Σ(m_receiver,g × impact_receiver(LOW))
   - m_spellman,g × impact_spellman(HIGH)] / 48

rotation_delta_100,g(BASE)
= [m_protagonist,g × impact_protagonist(BASE)
   + Σ(m_receiver,g × impact_receiver(BASE))
   - m_spellman,g × impact_spellman(BASE)] / 48

rotation_delta_100,g(HIGH)
= [m_protagonist,g × impact_protagonist(HIGH)
   + Σ(m_receiver,g × impact_receiver(HIGH))
   - m_spellman,g × impact_spellman(LOW)] / 48
```

- LOW는 대체측 LOW에서 donor HIGH를 빼고 HIGH는 대체측 HIGH에서 donor LOW를 빼 교체효과 불확실성을 같은 방향으로 상쇄하지 않는다.
- `rotation_delta_100`은 고정 100포제션 경기에서 해당 분 점유율만큼 환산한 순평점 변화다. 실제 경기 pace나 사후 점수차는 쓰지 않는다.
- `m_protagonist + Σm_receiver = m_spellman`을 날짜별로 만족해야 한다.
- 수취자의 실제 기존 분은 실제 기준선에 이미 들어 있으므로 추가분만 rotation 항에 넣는다.
- Young·Huerter·Collins 분은 0.0분도 차감하지 않는다.
- 박스 생산성과 BPM 영향치를 동시에 더하지 않는다.
- 검증된 라인업 상호작용이 없으므로 `interaction=0`으로 잠근다.

## 5. 피로 함수 후보

피로는 결과가 아니라 이전 부하만 본다. 정방향 계산·새 부상 자동 생성 금지는 방화벽으로 고정하지만 아래 계수·0.85 가중·임계값은 외부 교정 전 `HOLD`다.

```text
F(M24,M72,M7)
= -min(0.50,
       0.0125×M24
       + 0.005×max(0,M72-45)
       + 0.0025×max(0,M7-120))
```

- `M24`, `M72`, `M7`은 현재 경기 시작 전 24시간·72시간·7일의 선수분이다.
- G League 분은 NBA 분의 `0.85`로 환산한다.
- 수취자의 후속 피로는 `F(실제 부하+앞선 추가 부하)-F(실제 부하)`만 사용한다.
- 주인공과 Spellman은 각각의 시간순 부하를 계산해 같은 날짜 donor 분에 대한 피로 차이만 반영한다.
- 한 선수의 피로 영향은 `[-0.50, 0]점/100포제션`으로 제한한다.
- 추가분이 18분 이상인 백투백 2차전, 30분/72시간, 45분/7일 중 하나를 넘으면 자동 부상 대신 `AVAILABILITY_SENSITIVE/HOLD`로 중단한다.
- 실제 Spellman의 3월 1일 발목 부상이나 수취자의 실제 사후 부상을 주인공에게 복사하지 않는다.

## 6. 승률 변환 HOLD와 latent 재현 규격

```text
delta_mu_g = rotation_g + delta_fatigue_g + availability_g
logit(pCF_g) = logit(pB_g) + delta_mu_g / k_calibrated
```

- `pB`는 경기 전 양방향 closing moneyline을 사용한다. 출처 우선순위·closing 시각·implied probability 정규화 공식은 입력 수집 전에 별도 잠가야 하며, 어느 하나라도 없으면 `PREGAME_PROBABILITY_HOLD`다.
- `pB`는 `[0.03,0.97]`로 제한한다.
- `k_calibrated`는 Atlanta 원점수차 표준편차로 정하지 않는다. 경기 전 시장 기대 대비 잔차 또는 결과를 보지 않는 별도 리그 표본으로 교정·감사하기 전 `LOGIT_SCALE_HOLD`다.
- `availability=0`이 기본값이다. 앞선 분 재배분이 실제 가용성을 바꾼다는 증거가 생기면 자동 승패 대신 HOLD한다.
- 한 경기 `delta_mu`는 `[-1.75,+1.75]`로 제한하며 초과 시 모델 감사를 다시 연다.
- 정확한 대체 점수·점수차·연장 횟수는 생성하지 않는다.

이 절의 `pB` cap, `delta_mu` cap, ±2승 재감사선도 logit scale과 함께 교정·승인해야 하는 후보 guardrail이다. outcome runner 전까지 수치 정본으로 사용하지 않는다.

고정 seed 문자열과 SHA-256은 다음과 같다.

```text
FIRST_REBOUND|R09|ATL_2018_19|PRIOR_v1
228aac4642a599e4545ed878efda7952bf04bf1b0ad73b20b217d44f5aa19cab
```

`event_id`는 일정 순번 그대로 `ATL_2018_19_G001`부터 `ATL_2018_19_G082`까지 사용한다. 게임별 `h`는 `SHA256(seed|event_id)`의 첫 8바이트를 big-endian unsigned 64-bit로 읽고, 오른쪽으로 11비트 이동한 정수를 `2^53`으로 나눈 `[0,1)` 값이다.

```text
실제 W: u = h × pB
실제 L: u = pB + h × (1-pB)
대체 W: u < pCF
```

이 conditional latent는 입력 변화가 0이면 실제 82경기 승패를 모두 재현한다. LOW·BASE·HIGH는 같은 `u`를 공유한다.

## 7. 실행 중단선

- 세 시나리오가 모두 같은 승패면 `ROBUST`다.
- 하나라도 다르면 해당 경기는 `SENSITIVE/HOLD`이며 작가가 원하는 결과를 고르지 않는다.
- 시즌 기록은 민감 경기까지 포함한 최소~최대 범위로만 보고한다.
- Atlanta 승패 변경은 상대팀 승패도 반대 방향으로 한 번만 갱신한다.
- Atlanta 예상 승수 변화가 실제 29승에서 ±2승을 넘으면 v1 입력·결과·manifest를 그대로 보존하고 자동 정본화하지 않는다. 변경 사유·새 버전·독립 승인이 있는 v2에서만 모델을 다시 열며 v1 결과에 맞춘 계수 조정은 금지한다.
- Spurs·Dallas·Denver 연쇄와 비플레이오프 14팀 원장이 닫히기 전 2019 standings·lottery를 `FINAL`로 만들지 않는다.
- 시뮬레이션 결과를 보기 전 대표 경기·서사적 하이라이트를 고르지 않는다.

## 아직 열지 않는 것

- 82경기별 `pB` 수집·감사
- 공통 평균·pseudo-minutes·band·피로 계수·G League 가중·임계값의 외부 교정 또는 공통평균 fallback 승인
- `k_calibrated`의 독립 표본 교정
- 선수별 실제 전체 game log를 이용한 시간순 피로 상태
- 조건부 latent와 대체 승패 실행
- 정확한 개인 시즌 박스스코어·온오프·대체 점수
- 상대팀 전체 순위·2019 로터리·보호픽·드래프트

따라서 현재 판정은 `PRIOR_METHOD_HOLD / OUTCOME_INPUTS_HOLD`다. 같은 805분·이중계산 금지·interaction 0·hash 규격만 방화벽 PASS이며 수치 prior는 PASS가 아니다.

## 출처

- [NBA Stats — Atlanta 2018-19 선수 총계](https://www.nba.com/stats/players/traditional?Season=2018-19&SeasonType=Regular%20Season&TeamID=1610612737&PerMode=Totals)
- [Basketball-Reference — Atlanta 2018-19 로스터·총계](https://www.basketball-reference.com/teams/ATL/2019.html)
- [Basketball-Reference — 2018-19 per-36](https://www.basketball-reference.com/leagues/NBA_2019_per_minute.html)
- [Basketball-Reference — 2018-19 advanced](https://www.basketball-reference.com/leagues/NBA_2019_advanced.html)
- [Atlanta Hawks — Justin Anderson 시즌 리뷰](https://www.nba.com/hawks/features/five-things-know-about-justin-andersons-2018-19-season)
- [Atlanta Hawks — Alex Poythress 시즌 리뷰](https://www.nba.com/hawks/five-things-know-about-alex-poythress-2018-19-season)
- [Atlanta Hawks — Miles Plumlee 시즌 리뷰](https://www.nba.com/hawks/features/five-things-know-about-miles-plumlees-2018-19-season)
- [Atlanta Hawks — Daniel Hamilton 웨이브](https://www.nba.com/hawks/atlanta-hawks-request-waivers-daniel-hamilton)
