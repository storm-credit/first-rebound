# L2 플레이인 6날짜 분·가용성 작업 모델

기존 L2 승패·날짜에 12개 팀 분 모델을 연결했다. 승패는 작가 선택이며 분으로 예측한 결과가 아니다.

| 날짜 | 경기 | 작가 선택 승자 | 팀별 분 |
|---|---|---|---|
| 2021-05-18 | BOS–IND | BOS | 240 |
| 2021-05-18 | WAS–CHI | CHI | 240 |
| 2021-05-20 | IND–CHI | IND | 240 |
| 2021-05-19 | POR–GSW | POR | 240 |
| 2021-05-19 | MEM–SAS | MEM | 240 |
| 2021-05-21 | GSW–MEM | MEM | 240 |

CHI는 마지막 전체 코어 양수분인5/13을 작업 입력으로 선택했다. LaVine 가용성을 새로 모델링하고,
원역사 Charlotte의 LaMelo 손목 접촉이나5/16 비참여를 플레이인에 자동 이월하지 않는다.
WAS/GSW/SAS는5/16 분을 새 날짜의 작업 배분으로 채택했다. BOS/IND/POR/MEM은 기존 playoff 배분을 앞선 날짜에 새로 채택했다.
[LeVert 5/18 공식 결장 보도](https://www.nba.com/news/pacers-swingman-caris-levert-to-miss-play-in-game-vs-hornets)와5/20 공개 입력은 출처 앵커다. 대체 BOS/CHI전 지속은 별도 작가 모델이다.

48분·연장0은 작업 선택이다. 5인조 증인은 순서 없는 분 존재 증명이며 감독 교대 시계·매치업 증명이 아니다.
CHI/WAS/GSW/SAS 전체15+2명단은 이 모델에 없다. 실제 등록·의료·점수·박스·전체시즌 인증을 하지 않는다.
기존 L2 진출팀4·playoff 첫 대진8쌍 및 진출일→첫경기 날짜를 직접 대조했다. 진출팀 변경0이며 두 단계는 의존관계다.
LeVert 절차 지속과 LaVine 가용은 모두 새 작가 선택이다. 같은 세계 소속의 공개 절차·기존 휴식/경쟁자팀 접촉 사건은 인과 조건이 다르다.
정규시즌1080 / 플레이인6 / playoff88의 단계 구분을 유지한다. 원고0·v0.30 PARTIAL·설계/원고 CLOSED.

[기계 입력](NBA_2021_L2_WORKING_MINUTE_MODELS.json)
[날짜·결과 권위](NBA_2021_L2_DATED_WORKING_CALENDAR.md)
[정규시즌 분 증인](NBA_2020_21_REGULAR_CLOCK_COMPLETION.md)
[playoff 감독 모델](NBA_2021_ALL_DATED_PLAYOFF_COACH_PLANS.md)
