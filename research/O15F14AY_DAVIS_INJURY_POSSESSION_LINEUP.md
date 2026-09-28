# O-15F14-AY — Davis 2/14 재악화 장면의 Denver 코트 5명

- 판정: `HISTORICAL_LINEUP_RECONSTRUCTED / ALT_HEALTH_EVENT_HOLD`.
- 목적: [AX의 A1 건강·대진 민감도](O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)에서 Hampton의 Dallas행이 Davis의 2/14 재악화 장면을 직접 없앤다는 과잉 추론을 막는다.

## 1차 자료와 2쿼터 코트 재구성

[NBA 공식 2/14 Lakers @ Denver 경기책, 2쿼터 플레이바이플레이](https://statsdmz.nba.com/pdfs/20210214/20210214_LALDEN_book.pdf)는 다음 교대를 기록한다. 시각은 **2쿼터 남은 시간**이다.

| 시각 | Denver의 실제 교대·사건 | 그 뒤 해당 장면까지의 다섯 명 |
|---|---|---|
| 9:51 | Paul Millsap ↔ JaMychal Green | 이후 9:07 교대의 출발점 |
| 9:07 | Monte Morris ↔ R.J. Hampton, Michael Porter Jr. ↔ Zeke Nnaji, Nikola Jokić ↔ Jamal Murray | Millsap·Facundo Campazzo·Morris·Porter·Jokić |
| 6:59 | Jamal Murray ↔ Campazzo | **Millsap·Morris·Porter·Jokić·Murray** |
| 2:49 | Davis가 Jokić에게 슈팅 파울, Jokić 자유투 2개 | 교대 없음 |
| **2:39** | **Jokić가 Davis에게 파울, Davis 자유투 2개** | **Millsap·Morris·Porter·Jokić·Murray** |
| 2:36 | Lakers에서 Markieff Morris ↔ Davis | Davis는 그 뒤 뛰지 않음 |

9:07~2:39의 Denver 교대는 6:59의 Murray 투입뿐이다. 따라서 공식 교대 기록의 **원역사 2:39 코트 5명**에는 Hampton과 Nnaji가 모두 없다. [NBA의 당시 부상 보도](https://www.nba.com/news/anthony-davis-exits-lakers-game-vs-nuggets)는 Davis가 2:39에 Jokić를 돌아 돌파하던 중 기존 오른쪽 아킬레스건 문제를 재악화했고, 앞서 이 문제로 두 경기를 결장했다고 보도한다. 공식 경기책은 **파울·자유투·교대 시각**을, 보도는 **부상 설명**을 뒷받침한다. 경기책만으로 진단을 새로 내리지 않는다.

## 대체 세계에 적용할 수 있는 범위

[승인된 2020 Draft](../simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md)에서 Hampton은 Dallas 31순위이고 Denver는 Bey 22·Nnaji 24다. 따라서 원역사 2월 경기의 Hampton `20:23`은 대체 Denver의 분이 아니다. 그러나 Davis가 재악화된 **실제 접촉 장면의 상대 선수는 Jokić**이며, 그때 코트의 Denver 다섯 명 중 Hampton·Nnaji 어느 쪽도 없다. Hampton 이탈이 이 파울 장면의 선수 신원에 **직접 충돌한다는 주장은 자료로 반박된다**.

이것은 `2:39 장면이 대체 경기에도 반드시 발생한다`는 증명이 아니다. Hampton 분을 Bey·다른 선수에게 배정하면 9:07 전후의 점수·파울·교대·피로·작전과 포제션 자체가 달라질 수 있다. Denver 다섯 명이 원역사와 같을 가능성은 열려 있지만, 그 시간대의 같은 5인조·득점·접촉을 자동 복사하지 않는다. 원역사의 선행 건병증도 대체 의료 달력의 필연적 결과로 승격하지 않는다.

**A1 선택 비용:** 원역사 재악화와 뒤이은 Davis 30경기 결장을 보존하는 후보는 알려진 2:39 선수 신원과 직접 충돌하지 않는다. 재악화 회피·결장 길이 변경 후보는 별도 건강 사건, Lakers 30경기와 LeBron 3/20 독립 사건, 정규시즌 승수·시드·Denver 첫 상대를 날짜별로 다시 검문해야 한다. 어느 후보도 여기서 고르지 않는다. [AX](O15F14AX_DEN_LAL_SEED_CAUSAL_SENSITIVITY.md)의 4/15 한 경기 반전→Denver–Dallas 시험은 민감도이지 예측이 아니다.

**분류:** 경기책의 파울·자유투·교대와 NBA 부상 보도는 원역사 **사실**. 2:39 다섯 명은 그 교대의 **재구성**. `Hampton 이탈만으로 이 접촉은 불가능해지지 않는다`는 제한된 **추론**. 원역사 건강 유지/변경은 **후보**. 신규 **작가확정 0**. F5/A1/K_HEALTH/K_METHOD_EVENTS는 `HOLD`, F `0/5`·A `0/3`·K `0/4`; `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`.

Codex가 NBA 공식 플레이바이플레이의 교대 시각과 NBA 부상 보도를 직접 대조했다. 이 국소 검문에서 Anti-Gravity·NotebookLM·Claude·source-blind 독립 검수는 `NOT_RUN`이며, 전체 G16 독립 검수로 세지 않는다.
