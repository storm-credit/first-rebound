# O-15F14-Z — McGee 거래 생략 경로의 Denver 플레이오프 분 검문

- 판정: `F5_PLAYOFF_MINUTES_OBSERVED / ALTERNATE_ROTATION_HOLD`.
- 범위: 작가가 이미 선택한 2021년 3월 McGee–Hartenstein 거래 **생략**의 Denver 후속. 원역사 McGee의 플레이오프 경기책을 읽고 대체 세계에서 다시 배분할 기준 출전분을 분리한다. 플레이오프 대진·결과를 확정하지 않는다.
- 기준: 기존 [F5 정규시즌 25경기 화면](O15F14Q_DENVER_MCGEE_NONTRADE_F5_SCREEN.md)은 플레이오프를 포함하지 않았다.

## 원역사 공식 기록

아래 분·초와 DNP는 NBA 공식 경기책 **첫 장 최종 박스**의 McGee 행이다. 10경기 전부를 열람했다. `DNP - Coach's decision`은 부상 결장이나 출전 자격 상실이 아니다.

| 날짜 | 상대·라운드 | NBA 공식 경기책 | McGee | Denver 결과 |
|---|---|---|---:|---|
| 5/22 | Portland 1차전 | [PORDEN](https://statsdmz.nba.com/pdfs/20210522/20210522_PORDEN_book.pdf) | DNP | 109–123 패 |
| 5/24 | Portland 2차전 | [PORDEN](https://statsdmz.nba.com/pdfs/20210524/20210524_PORDEN_book.pdf) | DNP | 128–109 승 |
| 5/27 | Portland 3차전 | [DENPOR](https://statsdmz.nba.com/pdfs/20210527/20210527_DENPOR_book.pdf) | DNP | 120–115 승 |
| 5/29 | Portland 4차전 | [DENPOR](https://statsdmz.nba.com/pdfs/20210529/20210529_DENPOR_book.pdf) | **7:14** | 95–115 패 |
| 6/1 | Portland 5차전 | [PORDEN](https://statsdmz.nba.com/pdfs/20210601/20210601_PORDEN_book.pdf) | **0:02** | 147–140 승, 2OT |
| 6/3 | Portland 6차전 | [DENPOR](https://statsdmz.nba.com/pdfs/20210603/20210603_DENPOR_book.pdf) | DNP | 126–115 승 |
| 6/7 | Phoenix 1차전 | [DENPHX](https://statsdmz.nba.com/pdfs/20210607/20210607_DENPHX_book.pdf) | DNP | 105–122 패 |
| 6/9 | Phoenix 2차전 | [DENPHX](https://statsdmz.nba.com/pdfs/20210609/20210609_DENPHX_book.pdf) | **6:53** | 98–123 패 |
| 6/11 | Phoenix 3차전 | [PHXDEN](https://statsdmz.nba.com/pdfs/20210611/20210611_PHXDEN_book.pdf) | DNP | 102–116 패 |
| 6/13 | Phoenix 4차전 | [PHXDEN](https://statsdmz.nba.com/pdfs/20210613/20210613_PHXDEN_book.pdf) | **19:40** | 118–125 패 |

**사실:** McGee는 원역사 10경기 중 4경기에 총 `7:14 + 0:02 + 6:53 + 19:40 = 33:49`(2,029초) 출전했고, 6경기는 감독 선택 DNP였다. Phoenix 4차전의 Jokic은 28:17만 뛰었고 3쿼터 3:52에 Flagrant 2로 퇴장했다([NBA 시리즈 보도](https://www.nba.com/playoffs/2021/west-semifinal-2)). 이 경기의 19:40은 단순한 평시 백업센터 분으로 취급할 수 없다.

## 선택된 대체 경로의 부담

**추론:** McGee가 Cleveland에 남고 Hartenstein이 Denver에 남는 선택에서는 위 McGee 출전 2,029초를 Denver의 누군가가 소화해야 한다. **후보 M1**은 동일 대진·건강·감독 기용을 잠정 고정하고 4경기 각각 Hartenstein에게 1대1 치환하며 6경기 DNP를 유지한다. 이는 경기별 5인조·가용성·피로·평점·승패의 증명이 아니다. **후보 M2**는 감독이 Jokic/Green/Millsap/기타 실명 가용 선수에게 분을 재배분하는 경우다. 특히 6/13의 퇴장 후 19:40은 별도 분 단위 로테이션 검산이 필요하다. 두 후보는 플레이오프 사건의 작가 선택이 아니다.

원역사 6/13 7점차를 McGee/Hartenstein의 일반 시즌 평점 차이만으로 보존한다고 단정하지 않는다. Phoenix 4차전의 승패가 변하면 시리즈 종료일·추가 경기·후속 계약 영향 범위도 다시 산정해야 한다. 원역사 대진 자체는 Chicago·Minnesota 및 다른 팀의 조건부 정규시즌/플레이인 채택 전에는 대체 세계 확정 입력이 아니다. 이 표는 그 대진이 유지될 때의 **조건부 기준 기록**이다.

**작가확정:** 3/25 McGee 거래 생략만. Varejão C1/C2, Denver M1/M2, 플레이오프 결과는 미선택. 다음 검문은 4경기 중 특히 6/13의 Jokic 퇴장 전후 분과 5인조/평점 구간을 풀고, Cleveland 5월 등록·급여 및 양 팀 건강/후속 사건을 합치는 것이다. F5·`K_TRANSACTIONS`·`K_METHOD_EVENTS`는 `HOLD`; F 전체 `0/5`, A 최종 `0/3`, K 종료 `0/4`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 원고 금지.

### 후속 AC: 6/13 퇴장 전후 출전 구간

[교대 시계 검문](O15F14AC_DENVER_PLAYOFF_NONTRADE_STINT_WITNESS.md)은 네 McGee 출전 경기의 플레이바이플레이 구간을 공식 박스 총 `33:49`와 대조했다. 6/13 `19:40` 중 Jokić의 3Q `3:52` 퇴장 **뒤**가 약 `15:49.3`이다. 이름만 Hartenstein으로 바꾸는 M1은 이 시간 공백을 드러내는 조건부 산술안이고, 퇴장 이후 Jokić에게 시간을 재배분하는 M2는 원역사 퇴장 유지 조건과 충돌한다. 플레이오프 5인조·가용성·결과와 F5/K의 `HOLD`는 그대로다.

[AN 명단 겹침 후속](O15F14AN_DENVER_2021_PLAYOFF_ROSTER_COLLISION.md)은 원역사 McGee 분 가운데 `11:17`에 Nnaji가 함께 뛴 사실을 확인했다. Gordon A 승인 방향에서는 Nnaji가 Orlando 선수이므로 M1의 McGee 이름만 바꾸는 방식은 그 구간에서 성립하지 않는다. Hartenstein·Bey를 각각 배치한 조건부 5인조 수량/역할 증인을 AN에 분리한다. 다른 Nnaji 출전·건강·점수는 여전히 미해결이다.
