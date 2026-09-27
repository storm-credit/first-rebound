# O-15F14-AW — Denver–Lakers 원역사 맞대결의 Hartenstein 출전 선례

- 판정: `SAME_OPPONENT_ROLE_PRECEDENT_OBSERVED / ALTERNATE_ROSTER_AND_HEALTH_CAUSALITY_HOLD`.
- 적용 범위: [K1+L2 조건부 Denver 3번–Lakers 6번 1라운드](../simulation/CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)의 F5 비교 입력. 두 2월 경기의 승패·분은 5월 대체 시리즈 결과가 아니다.

## NBA 공식 최종 경기책의 원역사 사실

| 경기·원자료 | Denver 출전 | Lakers 출전·결과 |
|---|---|---|
| [2021-02-04 DEN @ LAL 공식 경기책](https://statsdmz.nba.com/pdfs/20210204/20210204_DENLAL_book.pdf) | Hartenstein `10:11`, Nnaji `2:53`, Hampton `2:53` | James `35:27`, Davis `33:14`, Schröder `29:50`, Gasol `20:23`, Harrell `24:18`; Lakers 114–93 승리 |
| [2021-02-14 LAL @ DEN 공식 경기책](https://statsdmz.nba.com/pdfs/20210214/20210214_LALDEN_book.pdf) | Hartenstein `3:04`, Nnaji `23:50`, Hampton `20:23`, Murray `34:23` | James `30:56`, Davis `14:14`, Schröder `27:39`, Gasol `17:57`, Harrell `24:15`; Denver 122–105 승리 |

두 공식 PDF의 최종 박스 첫 장을 확인했다. SHA-256은 날짜순 `af997c4e0f8cb5565feb0f7f71da64f27d7a3625a99f43a4de7ea21462951f25`, `7923b02f322bfcfd25720b4fed464991bc1ad6e6c544866fb3137bcf6d5d4a6c`이다. 각 팀 최종 분은 경기마다 `240:00`이며 연장 기록은 없다. 이 관측으로 **Hartenstein이 원역사 Denver 선수로 Lakers를 상대해 실제 출전한 선례**를 얻는다. `3:04~10:11`은 두 관측치의 범위이지 5월 대체 출전시간의 상한·하한이 아니다.

## 대체 세계로 옮길 때의 인과 경계

1. [승인된 대체 2020 Draft/Gordon 방향](../simulation/ORLANDO_DENVER_2021_GORDON_BOARD.md)에서는 Denver가 Bey #22·Nnaji #24를 얻고 Hampton은 Dallas #31이다. 따라서 **2월 거래 전부터** 두 원역사 Denver 경기의 Hampton `2:53`·`20:23`을 대체 Denver 분으로 복사할 수 없다. Bey의 새 출전·역할과 다른 선수의 재배분은 미선택이다. 3월 Gordon A가 실행되면 Nnaji도 Orlando로 가므로 5월 Denver 명단은 다시 바뀐다.
2. [NBA의 2/14 부상 보도](https://www.nba.com/news/anthony-davis-exits-lakers-game-vs-nuggets)에 따르면 Davis는 이미 오른쪽 아킬레스건 건병증으로 출전 불확실이었고, 그날 Jokić를 상대로 드라이브하다 재악화되어 `14:14`만 뛰었다. [NBA의 복귀 보도](https://www.nba.com/news/lakers-anthony-davis-ends-30-game-injury-absence-against-mavs)는 원역사 30경기 공백 뒤 4/22 복귀를 설명한다. 선행 건강 상태와 **그 경기의 재부상·이후 공백**을 구분한다. 대체 Denver의 로테이션이 다른 만큼 같은 접촉·의료 결과가 반드시 재현된다고 볼 수 없다. 반대로 재부상이 없었다고 확정하거나 건강한 5월 Lakers를 자동 채택하지도 않는다.
3. 원역사 두 경기에서 Denver의 Murray가 뛰었어도 5월 조건부 대진에 그 분을 옮기지 않는다. 5월 가용성·상대 전술은 [별도 개막 비교](O15F14AV_DEN_LAL_OPENING_MINUTE_TEMPLATES.md)의 날짜별 관측과 대체 건강 달력을 함께 검문해야 한다.

**다음 실행 입력:** A1 후보 건강 달력에는 2/14 Davis의 `선행 건병증`과 `경기 중 재악화`를 별도 사건으로 표시한다. F5 후보 1라운드 분 원장은 Hampton 0명·Nnaji Orlando 이동·Hartenstein/Bey Denver 잔류를 기본 명단 조건으로 삼고, 2월의 실측 Hartenstein 출전을 전술 선례로만 사용한다. Lakers 센터군·Davis 가용성, Denver의 새 5인조와 경기별 점수/승자는 별도 후보 산출 전까지 `UNKNOWN`이다.

**분류:** 공식 경기책·NBA 부상 보도는 원역사 **사실**; 대체 명단 차이에 따른 분 재배분 필요는 **인과 추론**; 5월 로테이션·건강·승패는 **미선택 후보**. 작가가 확정한 McGee 거래 생략/Gordon A 방향은 유지한다. F5·A1/A3·K_METHOD_EVENTS `HOLD`, F `0/5`·A `0/3`·K `0/4`; 7행 1완료·1진행·5대기/미완료 6개. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, 원고 금지.
