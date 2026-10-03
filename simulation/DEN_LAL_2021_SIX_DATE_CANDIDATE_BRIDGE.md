# DEN–LAL 2021 6경기 날짜 후보 연결

기준 main `51da5e5` / 2026-10-04. **날짜 후보**이며 대체세계 실제 경기 일정이나 건강 인증이 아니다. 이미 선택된 LAL 4–2와 경기별 승자·홈 순서는 보존한다.

## 사실 / 추론 / 후보 / 작가확정

- **사실:** NBA 공식 DEN–POR 원역사 경기 페이지의 현지 날짜는 5/22, 5/24, 5/27, 5/29, 6/1, 6/3이다. 이번에 각 페이지 날짜 본문을 직접 확인했다. G5는 원역사 2OT다.
- **추론:** 같은 날짜를 쓰면 경기일 간격은 2·3·2·3·2일이고 사이의 비경기 날짜는 1·2·1·2·1일이다. 실제 휴식 시간·이동 시간은 팁오프와 여행 계획이 없으므로 계산하지 않는다.
- **후보:** DEN–POR의 날짜 골격을 대체 DEN–LAL에 사용한다. Portland 홈 날짜를 Lakers 홈 날짜로 옮기는 것은 역사적 사실이 아니며 LA 경기장 예약·방송/리그 편성은 검증되지 않았다.
- **기존 작가확정:** [선택 시리즈](DEN_LAL_2021_DELEGATED_SERIES.json)의 LAL 4–2 및 홈/승자 순서. [전체 결과](NBA_2021_DELEGATED_PLAYOFF_RESULTS.json)의 W2 PHX 4–2 POR와 W6 PHX 4–3 LAL에 따라 Lakers 다음 상대는 **PHX**다. 옛 `PHX or POR` 문구만 이 승인 결과에 맞게 정정한다.

| 경기 | 현지 날짜 후보 | 홈 | 기존 선택 승자 | 이전 경기와 날짜 간격 | 사이 비경기 날짜 수 |
|---|---|---|---|---:|---:|
| G1 | 2021-05-22 | DEN | DEN | — | — |
| G2 | 2021-05-24 | DEN | LAL | 2 | 1 |
| G3 | 2021-05-27 | LAL | LAL | 3 | 2 |
| G4 | 2021-05-29 | LAL | DEN | 2 | 1 |
| G5 | 2021-06-01 | DEN | LAL | 3 | 2 |
| G6 | 2021-06-03 | LAL | LAL | 2 | 1 |

## 승격하지 않는 입력

대체 경기 점수·연장·팁오프·선수별 박스·당일 등록·의학적 상한·이동/회복은 null이다. 기존 48분/팀 240분 로테이션은 정규시간의 **가능성 증인**이지 6경기 모두 무연장이라는 선택이 아니다. 원역사 G5 2OT/팀 290분 역시 이 세계에 복사하지 않는다. PHX 2라운드 정확 날짜와 후속 건강은 계산하지 않았다.

F5/A1/A3/K 전체 종료나 실제 시즌 채택을 올리지 않는다. 신규 작가확정0, 원고0, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.

## 출처

NBA 공식 각 경기 페이지의 날짜 본문과 [첫 라운드 색인](https://cdn-uat.nba.com/news/2021-nba-playoffs-first-round-schedule)을 직접 열람했다. 아래 원역사 상대는 POR이며 대체 LAL의 증거가 아니다.

- [G1 May22](https://www.nba.com/game/por-vs-den-0042000161/box-score)
- [G2 May24](https://www.nba.com/game/por-vs-den-0042000162/game-charts)
- [G3 May27](https://www.nba.com/game/den-vs-por-0042000163)
- [G4 May29](https://www.nba.com/game/den-vs-por-0042000164)
- [G5 June1·원역사2OT](https://www.nba.com/game/por-vs-den-0042000165)
- [G6 June3](https://www.nba.com/game/den-vs-por-0042000166)

기존 [6경기 공식 경기책 검문](../research/O15F14Z_DENVER_2021_PLAYOFF_NONTRADE_SCREEN.md)과도 날짜가 일치한다. 기존 경기책을 새로 수집했다고 세지 않는다.

기계 원장: [JSON](DEN_LAL_2021_SIX_DATE_CANDIDATE_BRIDGE.json).
