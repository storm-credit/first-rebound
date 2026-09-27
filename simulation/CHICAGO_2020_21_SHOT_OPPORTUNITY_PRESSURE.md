# O-15G8G — Chicago 2020–21 후반 슛 기회 총량 압박

- 기준: `main` `09b8d10`; [G8F 슛 감소 감사](../research/O15G8F_MARKKANEN_SHOT_OPPORTUNITY_AUDIT.md), [K1 시즌 추천](CHICAGO_2020_21_SEASON_RECOMMENDATION.md), [F6B 조합 감사](CHICAGO_2020_21_POSTDEADLINE_EXECUTION_AUDIT.md).
- 상태: `NINE_CASE_PRESSURE_REPRODUCED / PLAYER_SHOT_SPLIT_HOLD / TEAM_PACE_HOLD / G1A_CONSENT_HOLD`.
- 산출: [29경기·9조건 JSON](CHICAGO_2020_21_SHOT_OPPORTUNITY_PRESSURE.json), [재현 검사기](../tools/audit_chicago_2020_21_shot_pressure.py). 대체 세계의 정수 경기 박스·확정 슛/터치·시즌 승패가 아니다.

## 무엇을 고정하고 무엇을 비교했나

K1 `PORTER_ZERO`의 F6B 최소 변경 5인 조합에서 Chicago 후반 29경기의 선수별 분을 사용했다. 팀 분은 매 경기 240분, Markkanen은 합계 36,899초이며 04-30에는 0분이다. 주인공과 LaMelo를 제외한 실존 선수는 2021-03-24까지의 [관측 FGA/FTA/초](CHICAGO_2020_21_POSTDEADLINE_OBSERVED_PRIORS.csv)를 해당 조건부 분에 곱했다. 이는 인과 예측이 아니라 분량에 따른 **관측 시도율 민감도**다. Mokoka·Felicio·Dotson의 cutoff 표본은 각 120분 미만이라 특히 불안정하다.

Markkanen 시도율은 세 가지로 분리했다. `PRE_CUTOFF`는 당시 확보 가능한 전반 관측치 303 FGA/61 FTA/41,429초다. `POST_HINDSIGHT`는 **원역사 후반에 뒤늦게 관측된** 218 FGA/31 FTA/37,617초이고, `MID_HINDSIGHT`는 두 시도율의 단순 평균이다. 뒤의 두 가지는 3/25 시점의 팀이 알 수 있는 정보가 아니라 후행 민감도다. 세 가지 모두 코치 선택이나 대체 Markkanen의 만족도는 증명하지 않는다.

주인공·LaMelo는 저장된 [LOW/BASE/HIGH 생산성 prior](CHICAGO_2020_21_PREDEADLINE_PRODUCTION_PRIORS.csv)의 `pts36`와 `TS` 및 같은 K1 분을 사용한다. 각자의 거친 슛 종료량은 `예상 PTS ÷ (2×TS) = FGA + 0.44×FTA`로 역산했다. **개인별 FGA·FTA 분해는 존재하지 않는다.** prior의 `three_pa36`으로 환산한 두 선수의 3PA 합계는 일관성 하한 참고값일 뿐 실제 3점 슛 원장이 아니다. LaMelo의 Charlotte 원역사 시도율을 대체 Chicago에 복사하지 않았다.

비교선은 [공개 NBA V3 이차 미러](CHICAGO_2020_21_POSTDEADLINE_INPUT_PROVENANCE.json)의 **원역사** 후반 Chicago 29경기 2,558 FGA·451 FTA, 즉 `FGA+0.44×FTA = 2,756.44`다. Vučević의 원역사 Chicago 488 FGA는 이 안에 들어 있으나 대체 K1 명단에는 없다. 대체 팀의 실제 페이스·공격리바운드·턴오버·자유투 유형이 달라질 수 있으므로 2,756.44를 대체 세계의 규칙상 상한으로 간주하지 않는다. `0.44`도 NBA 포제션의 정확한 수가 아니다.

## 9조건의 팀 총량 압박

`압박 = 실존 선수 관측률×K1분의 (FGA+0.44FTA) + 주인공/LaMelo pts·TS 역산량 − 원역사 팀 2,756.44`. 양수는 **원역사 팀 총량을 동시에 고정하면 초과**, 음수는 그 비교선까지의 차이다. 음수도 전술이 완성됐다는 뜻이 아니다. 단위는 29경기 전체의 거친 슛 종료량이며, 소수 박스 수치는 입력 산술의 흔적이다.

| Markkanen 시도율 | LOW | BASE | HIGH | 해석 한계 |
|---|---:|---:|---:|---|
| 후반 관측 `POST_HINDSIGHT` | −74.10 | −39.06 | −1.64 | 역할 축소를 뒤늦게 본 비교선; cutoff 예측 입력 아님. |
| 전·후반 평균 `MID_HINDSIGHT` | −40.82 | −5.78 | +31.63 | 시도율 평균에 코치·전술 인과 없음. |
| 전반 관측 `PRE_CUTOFF` | −7.54 | **+27.49** | +64.91 | 당시 알 수 있는 Markkanen prior; 역할 유지가 실제로 일어났다는 뜻 아님. |

`PRE_CUTOFF × BASE`에서는 실존 선수 합계가 1,901.56 FGA·425.55 FTA, 주인공·LaMelo의 기존 `pts36/TS`가 합계 695.13 거친 슛 종료량을 요구한다. 따라서 같은 팀 역사 총량 2,756.44를 FGA와 FTA 둘 다 그대로 고정하면 **27.49만큼 초과**한다. 이는 팀 총량을 바꾸거나, 선수별 시도율·득점/TS prior를 다시 맞추거나, 경기별 실제 기회 이전을 명시해야 한다는 조건부 충돌이다. **Markkanen이 27.49회를 빼앗았다**는 인과 주장이 아니다. 역사 총량 대비 초과를 팀 포제션 +27.49로 직접 해석하지 않는다.

시즌 합계만으로 날짜별 적합성이 생기지 않는다. `PRE_CUTOFF × BASE`는 29경기 중 17경기에서 비교선 초과, 12경기에서 미달이다. 03-31은 −17.47, 05-13은 +13.00으로 범위가 넓다. 따라서 9조건 가운데 합계가 0에 가까운 안도 **경기별 선수 FGA/FTA, 팀 기회, 실제 5인 동반자** 없이 PASS가 아니다. S0–S3 선발 후보는 분을 같게 두므로 이 산술을 바꾸지 않지만 슛 배분과 수비 매치업에는 영향을 줄 수 있다.

## 다음 설계 입력과 관문

1. 주인공·LaMelo의 `FGA/FTA`를 `PTS/TS/3PA`와 함께 만족시키는 **서로 다른** 경기별 정수 박스 후보를 만든다. 실제 원역사 Charlotte LaMelo를 대체 Chicago 기록으로 그대로 옮기지 않는다.
2. Markkanen·LaVine·White·Young·Carter·Theis 등 모든 실존 선수의 시도 변화가 누구의 역할·분·부상·선발 선택에서 나왔는지 날짜별로 연결한다. Vučević의 488 FGA를 한 명에게 자동 배정하지 않는다.
3. 대체 팀의 FGA/FTA 범위는 턴오버, 공격리바운드, 페이스와 함께 설명하고 상대 팀·승패·2021 계약/드래프트 나비효과를 별도 검사한다. 현재의 역사 팀 합계는 **진단 비교선**이다.
4. 선수의 2021 잔류 의사, G8C M0–M3 가격/역할과 S0–S3 선발 정책은 별도 관문으로 유지한다. 팀 총량 압박 하나가 작가 선택이나 선수 수락을 대신하지 않는다.

**사실:** 저장된 원역사 이차 미러의 팀 2,558 FGA·451 FTA와 3/24 cutoff 관측표, 저장된 K1 분. **추론:** 아홉 조합의 비교선 압박. **후보:** 시도율/LOW·BASE·HIGH 교차 민감도이며 경기별 슛 배정안은 아직 0건. **작가확정:** 0건. K1/L2·CP2 잠정, D1 F1~F5 전체 PASS 0/5·A1~A3 최종 채택 0/3·네 K 묶음 종료 0/4, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.

[G8H 날짜별 비상쇄 집계](CHICAGO_2020_21_DAILY_SHOT_PRESSURE.md)는 위 9조건의 양수 날짜만 따로 더해 시즌 순합계가 숨기는 비교선 압박을 보인다. 역사상 경기별 총량을 고정한 시험일 뿐 대체 팀의 실제 포제션 상한이나 슛 배분이 아니다.

## 도구와 검증 계보

Codex가 저장된 네 입력만 사용해 29경기·9조건을 재계산했고 출력 JSON에 LF 정규화 SHA-256을 남겼다. `--check`는 저장 JSON과 재계산 결과의 값·날짜·원자료 해시를 대조한다. 이 내부 비교에는 신규 외부 사실 원문이 없어 Antigravity·NotebookLM `NOT_RUN`; Claude와 source-blind도 `NOT_RUN`이다. 이전 G8F의 공식 NBA 본문 회수 실패를 성공으로 바꾸지 않는다. 외부 독립 검증이나 G16/G17 PASS가 아니다.
