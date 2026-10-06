# L2 플레이인 비플레이오프 4팀 명단·예비 건강 입력 범위

상태: `FOUR_NONPLAYOFF_TEAM_DATED_ROSTER_CANDIDATES_WITH_REGISTRATION_HEALTH_HOLD`. 기존 6경기·12팀 분은 변경하지 않았다.
아래 6개 팀-날짜는 모두 15 표준+2 투웨이 **작업 명단 후보**다.
양수 분 선수는 후보 명단에 들어가며, 0분은 부상이나 등록 제외를 뜻하지 않는다.

|날짜|팀|표준+투웨이|양수/예비|범위|
|---|---|---:|---:|---|
|2021-05-18|WAS|15+2|11/6|CANDIDATE_15_PLUS_2_HOMESLEY_OMISSION_UNSELECTED|
|2021-05-18|CHI|15+2|10/7|EXISTING_APPROVED_TRANSACTION_PATH_15_PLUS_2_WORKING_ROSTER|
|2021-05-20|CHI|15+2|10/7|EXISTING_APPROVED_TRANSACTION_PATH_15_PLUS_2_WORKING_ROSTER|
|2021-05-19|GSW|15+2|8/9|HISTORICAL_15_PLUS_2_CANDIDATE_HUTCHISON_REGISTRATION_HOLD|
|2021-05-19|SAS|15+2|12/5|HISTORICAL_15_PLUS_2_CONDITIONAL_CARRY|
|2021-05-21|GSW|15+2|8/9|HISTORICAL_15_PLUS_2_CANDIDATE_HUTCHISON_REGISTRATION_HOLD|

## 남은 등록 판단

- WAS: 대체 역사에서는 Brown·Trent가 잔류하고 Hutchison이 없다. 원역사 5월 15일 Homesley 표준 계약까지 옮기면 표준 16명이다. Homesley 서명 생략은 슬롯 해결 **후보**이며 작가 선택·계약 접수로 확정하지 않았다. 급여·슬롯 후속 효과도 HOLD다.
- GSW: Hutchison의 드래프트 후 거래·등록 경로가 미결이다. 원역사 15+2와 Hutchison을 동시에 확정할 수 없다. May 16 Payton 표준 계약을 생략하는 안도 미선택 후보로만 남긴다.
- CHI: 기존 15+2 설계 CSV를 사용했다. Theis·Green 등 개별 거래 실행과 날짜별 의료 승인은 별개 HOLD다.
- SAS: 원역사 May 19 경기책의 15+2를 조건부 입력으로 사용했다. Jeffries는 원역사 명단에서 Not With Team이며 대체 세계 등록은 미인증이다.

## 공식 근거

- WAS_MAY18_GAMEBOOK: [https://statsdmz.nba.com/pdfs/20210518/20210518_WASBOS.pdf](https://statsdmz.nba.com/pdfs/20210518/20210518_WASBOS.pdf) — page 1 final box and inactive line; historical roster only; raw PDF SHA-256 `e25e0110b599f6d272e657485b2e82c1b26ee3a9fd5c6ec4c0568e2a567c99d6`. 저장소 원문 캐시 없음.
- GSW_MAY19_GAMEBOOK: [https://statsdmz.nba.com/pdfs/20210519/20210519_GSWLAL_book.pdf](https://statsdmz.nba.com/pdfs/20210519/20210519_GSWLAL_book.pdf) — page 1 final box and inactive line; historical roster only; raw PDF SHA-256 `e98f31556173d2d261ebf31b4e1652ef03e9cc7d5e56a8f433740931b597c594`. 저장소 원문 캐시 없음.
- SAS_MAY19_GAMEBOOK: [https://statsdmz.nba.com/pdfs/20210519/20210519_SASMEM_book.pdf](https://statsdmz.nba.com/pdfs/20210519/20210519_SASMEM_book.pdf) — page 1 final box and inactive line; historical roster only; raw PDF SHA-256 `9bc963d51e51ed66f496724e084cecf425793afff2107858f84fd995f197ee78`. 저장소 원문 캐시 없음.
- MAY19_INJURY_REPORT: [https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-19_05PM.pdf](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-19_05PM.pdf) — historical GSW/SAS listed statuses; raw PDF SHA-256 `5a4bc6da820630da78e4b8ff36d53c98a328b9dedfb5ff93b4e884c99eae0766`. 저장소 원문 캐시 없음.
- MAY21_INJURY_REPORT: [https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-21_05PM.pdf](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-21_05PM.pdf) — historical GSW Lee questionable, Oubre/Thompson/Wiseman out; raw PDF SHA-256 `0973c8d8b824375611ee2f141541e900916975eb5dddb8c6e388f30dccf0c965`. 저장소 원문 캐시 없음.
- NBA_GLEAGUE_TWOWAY_TRACKER: [https://gleague.nba.com/news/two-way-tracker-for-2020-21-season](https://gleague.nba.com/news/two-way-tracker-for-2020-21-season) — 2020-21 CHI/WAS/GSW/SAS two-way table; early season snapshot. 저장소 원문 캐시 없음.
- NBA_GLEAGUE_CALLOUTS: [https://gleague.nba.com/nba-call-ups-for-the-2020-21-season](https://gleague.nba.com/nba-call-ups-for-the-2020-21-season) — Caleb Homesley May 15 standard; Jordan Bell May 13 two-way. 저장소 원문 캐시 없음.
- GSW_TRANSACTION_GUIDE: [https://cdn.nba.com/teams/uploads/sites/1610612744/2023/12/2324-gsw-media-guide.pdf](https://cdn.nba.com/teams/uploads/sites/1610612744/2023/12/2324-gsw-media-guide.pdf) — 2020-21 May 13 JTA conversion/Jordan Bell two-way, May 16 Gary Payton II signing. 저장소 원문 캐시 없음.

공식 경기책과 상해 보고는 실제 역사 기준이다. 현재 날짜·상대가 다른 대체 경기의 의료 증명은 아니다.
양수 분은 기존 감독 작업 모델의 선택일 뿐 의학적 허가가 아니다. 여섯 경기의 재계산·실제 출전 명단·계약 접수·시즌 확정·원고 게이트는 열지 않았다.

재생성: `python tools/build_2021_l2_nonplayoff_roster_scope.py --write`
검증: `python tools/build_2021_l2_nonplayoff_roster_scope.py --check`
