# O-15F14-AO — Denver 플레이오프 Nnaji 단독 구간 6:22

- 판정: `THREE_GAME_SECONDARY_LINEUP_CLOCK_AND_NBA_BOX_PASS / F5_HEALTH_SCORE_HOLD`.
- [재현 JSON](../simulation/DENVER_2021_PLAYOFF_NNAJI_OTHER_STINTS.json)·[도구](../tools/build_denver_2021_playoff_nnaji_other_stints.py)는 앞선 [McGee 동시 출전 11:17](O15F14AN_DENVER_2021_PLAYOFF_ROSTER_COLLISION.md) **밖**의 확인된 Nnaji 세 경기만 다룬다. FOX Sports의 공개 교대·5인조 표기를 시간 자료로 전사하고 NBA 공식 박스의 분으로 검산했다. FOX 교대 표기는 NBA 경기책과 같은 등급의 1차 자료로 올리지 않는다.

| 원역사 경기 | 공식 NBA 박스 | FOX 4Q 5인조 시작·변경 | 재배정 초 |
|---|---|---|---:|
| 5/24 POR | [Nnaji 2:43](https://www.nba.com/game/por-vs-den-0042000162/box-score) | [2:43에 Harrison/Campazzo/Howard/Čančar/Nnaji, 2:17에 Campazzo→Bol](https://www.foxsports.com/nba/boxscore?id=37619&tab=playbyplay) | 26+137=163 |
| 6/7 @PHX | [Nnaji 2:15](https://www.nba.com/game/den-vs-phx-0042000231/box-score) | [2:15에 Harrison/Howard/Nnaji/Čančar/Bol](https://www.foxsports.com/nba/boxscore?id=37674&tab=playbyplay) | 135 |
| 6/11 PHX | [Nnaji 1:24](https://www.nba.com/game/phx-vs-den-0042000233/box-score) | [1:24에 Howard/Nnaji/Harrison/Bol/Čančar](https://www.foxsports.com/nba/boxscore?id=37687&tab=playbyplay) | 84 |
| **세 경기** | **6:22** | **양수 4구간** | **382** |

**사실:** 세 NBA 박스의 Nnaji 분과 FOX 교대 표기의 네 5인조. **추론:** 같은 시계를 유지하는 분기에서 선택된 Gordon A로 Denver를 떠난 Nnaji의 382초를 다른 선수에게 배정해야 한다. 앞선 McGee 겹침 677초와 합치면 확인된 원역사 Nnaji 분의 대체 부담은 **최소 1,059초 = 17:39**다. **후보:** Nnaji가 없는 위 네 구간에 Denver에 남은 Hartenstein을 넣으면 K1의 핸들러·윙·센터 역할 검사 4/4와 5명 고유 검사가 통과한다. Bey 단독 이름 치환은 5/24의 첫 **26초**에 K1 센터 태그가 없어 3/4만 통과한다. 그 구간의 원역사 Nnaji 자신도 K1에서 윙으로 분류돼 센터 검사에 실패한다. 이는 K1의 역할 태그 한계이며 실물 Nnaji/Bey가 센터를 못 뛴다는 증거가 아니다. **작가 확정:** Gordon A와 McGee 거래 생략 방향만 유지한다. 이 구간의 Hartenstein 출전·Bey 출전은 미확정이다.

[선택 명단 종합 검사](../simulation/DENVER_2021_PLAYOFF_SELECTED_LINEUP_BRIDGE.json)는 McGee가 나온 공식 경기책 기반 14구간에 Hartenstein을, 그와 Nnaji가 겹친 구간에 Bey도 배치하고, 이번 FOX 기반 네 구간에 Hartenstein을 배치한 **조건부 18/18 역할·인원 증인**이다. 두 출처 등급을 섞어 모두 공식 교대라고 부르지 않는다. 이는 원역사 교대 시계 보존의 한 가지 후보일 뿐, 감독 선택·Bey/Hartenstein 건강과 등록·체력·경기 득점·시리즈 결과를 검증하지 않는다. 나머지 원역사 경기의 출전 정책도 복사하지 않는다. `F5`, 네 K와 Chicago 최종 시즌은 `HOLD`; `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 원고 금지.

[Claude 제한 반증](../reviews/R01_O15F14AO_NNAJI_OTHER_STINTS_REBUTTAL.md)은 제공된 문서·네 구간 코드만 검토했다. 원자료나 종합 18구간을 독립 확인한 것으로 세지 않는다.
