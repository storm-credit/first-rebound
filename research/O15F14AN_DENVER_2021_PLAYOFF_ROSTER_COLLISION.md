# O-15F14-AN — Denver 2021 플레이오프 McGee·Nnaji 이중 이탈 검문

- 판정: `F5_FOUR_GAME_LINEUP_CLOCK_AND_ROSTER_COLLISION_PASS / FULL_PLAYOFF_HEALTH_SCORE_HOLD`.
- 작가 확정 방향: [Gordon A 선수 이동](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)은 Nnaji를 Orlando로 보내고 Bey를 Denver에 남긴다. [F5 별도 선택](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)은 McGee–Hartenstein 거래를 생략해 McGee가 Cleveland에, Hartenstein이 Denver에 남는다. 두 방향은 재승인 대상이 아니다.
- 재현: [6/13 전체 5인조 시계](../simulation/DENVER_2021_PLAYOFF_GAME4_LINEUP_WITNESS.json)·[나머지 3경기 교대 시계](../simulation/DENVER_2021_PLAYOFF_OTHER_LINEUPS.json)·[선택 명단 겹침 검사](../simulation/DENVER_2021_PLAYOFF_SELECTED_LINEUP_BRIDGE.json). 각 [도구](../tools/build_denver_2021_playoff_selected_lineup_bridge.py)는 원경기 교대 사건의 조건부 이름 치환을 검사한다.

## 사실·추론·후보·작가 확정

| 등급 | 내용 |
|---|---|
| 사실 | [NBA 공식 5/29](https://statsdmz.nba.com/pdfs/20210529/20210529_DENPOR_book.pdf)·[6/1](https://statsdmz.nba.com/pdfs/20210601/20210601_PORDEN_book.pdf)·[6/9](https://statsdmz.nba.com/pdfs/20210609/20210609_DENPHX_book.pdf)·[6/13](https://statsdmz.nba.com/pdfs/20210613/20210613_PHXDEN_book.pdf) 경기책에서 McGee는 4경기 **33:49**(공식 박스 2,029초)에 출전했다. 6/13 공식 최종 박스의 Denver는 118–125로 패하고 McGee의 원경기 `+5`는 출전 구간 동시 점수차이지 인과 효과가 아니다. |
| 추론 | 원경기에서 5/29 4Q `5:12→0:00`과 6/9 4Q `6:05→0:00`에는 McGee와 Nnaji가 **동시에** 뛰었다. 합계 `5:12 + 6:05 = 11:17`(677초). 따라서 이전 [M1 단일 이름 치환](O15F14AC_DENVER_PLAYOFF_NONTRADE_STINT_WITNESS.md)만으로는 선택된 Denver 명단이 성립하지 않는다. |
| 후보 | 원경기 대진·교대 시계를 잠정 유지할 때 McGee 구간에 Hartenstein을, Nnaji 겹침 구간에 Bey를 배치한다. McGee 출전 4경기의 14개 양수 시간 구간은 모두 5명 고유 선수와 [K1 Denver 역할 목록](../simulation/NBA_2020_21_FINAL859_MINUTES.json)의 핸들러·윙·센터 검사에 통과한다. 출전 가능·감독 선택·효율·승패는 별도다. |
| 작가 확정 | 위 두 거래 방향만 기존대로 확정. Hartenstein/Bey의 플레이오프 분, 원역사 대진·시리즈 결과는 미확정. |

| 원경기 | McGee 공식 분 | 원경기 Nnaji 겹침 | 조건부 교대 시계 검문 |
|---|---:|---:|---|
| 5/29 @POR | 7:14 | 5:12 | 4Q 두 5인조; 마지막 5:12에 Nnaji→Bey도 필요 |
| 6/1 POR | 0:02 | 0 | 1Q 한 5인조; McGee→Hartenstein |
| 6/9 @PHX | 6:53 | 6:05 | 4Q 두 5인조; 마지막 6:05에 Nnaji→Bey도 필요 |
| 6/13 PHX | 19:40 | 0 | 경기 전체 10명 분 합계 240:00, 박스 대조 선수별 오차 최대 0.7초. McGee 구간 9개 중 Jokić 퇴장 뒤 15:49.3 |
| **4경기 합** | **33:49** | **11:17** | 양수 14구간의 5명 고유·역할 검사 통과 |

6/13은 공식 경기책의 **1~4쿼터 전체** 선발·교대를 복원해 McGee 외 9명을 포함한 **모든 Denver 선수의 출전 총초**를 박스와 대조했다. 다른 세 경기는 McGee가 나온 **해당 쿼터**의 Denver 선발·교대를 복원했고, 전체 경기의 모든 선수를 검증했다는 주장은 하지 않는다. McGee 출전 시계의 소수점 합 `2,029.4초`와 공식 박스 반올림 `2,029초`는 구분한다.

## 남은 Nnaji 출전과 나비효과

원역사 Nnaji가 McGee와 겹치지 않고 출전한 확인된 세 경기는 [5/24 POR 2:43](https://www.nba.com/game/por-vs-den-0042000162/box-score), [6/7 @PHX 2:15](https://www.nba.com/game/den-vs-phx-0042000231/box-score), [6/11 PHX 1:24](https://www.nba.com/game/phx-vs-den-0042000233/box-score)로 합계 **6:22**다. 위 11:17과 더하면 최소 **17:39**의 원역사 Nnaji 출전분을 선택된 Denver에서 다시 배분해야 한다. 세 경기의 시간별 5인조는 이번 도구 범위 밖이며 Bey가 그대로 출전한다고 확정하지 않는다. [원경기 10경기 표](O15F14Z_DENVER_2021_PLAYOFF_NONTRADE_SCREEN.md)의 McGee 감독 선택 DNP 6경기도 거래 생략만으로 Hartenstein DNP라고 확정할 수 없다.

특히 6/13의 `15:49.3`은 Jokić이 원역사대로 퇴장한 뒤의 구간이다. 같은 퇴장 사건을 유지하는 분기에서는 그 시간을 Jokić에게 재배정할 수 없다. Hartenstein의 19:40 출전 가능성, Bey의 시즌 말 가용성·등록, Nnaji 이탈 뒤 Denver의 나머지 플레이오프 6:22, 양 팀 경기 결과와 추가 일정, 계약·픽 파급은 `HOLD`다. 원역사 `+5` 또는 평년 선수 평점으로 6/13의 7점차 결과를 고정하지 않는다. F5·`K_TRANSACTIONS`·`K_METHOD_EVENTS` 및 2번 시즌 원장은 여전히 미완료다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`와 원고 금지를 유지한다.
