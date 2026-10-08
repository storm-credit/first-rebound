# 2024 Denver 핵심5 서비스 연결과 공동 코트3창

상태: 루틴 가상 실행 입력·Jokic 재계약 권고 준비, 독립 검수/현재 채택 전. DEN 결승 진출·2024 우승·개인상은 이 문서에서 선택하지 않는다.

## 원 계약4 + 신규 권고1

| 배우 | 2023–24에 쓰는 기간 | 신규2023 UPC | 준비 가격·조건 |
|---|---|---:|---|
| Murray | 원2019 연장2020–25의 Year4 | 0 | 원 급여33,833,400·원 보호/의무 carry |
| Porter | 원2021 연장2022–27의 Year2 | 0 | ordinary 공개 열33,386,850; 원 Year5 보호/자격 트리거 보존 |
| Gordon | 원2021 연장2022–26의 Year2 | 0 | base21,266,182+likely1m+unlikely0.2m의 outer22,466,182; 분류·원PO 보존 |
| Morris | 원2020 연장2021–24의 Year3 | 0 | 원 급여9,800,926; 실제WAS/DET 거래 수입0 |
| Jokic | 원2018 계약은2022–23 서비스후 만료 | 1 권고 | 2023Jul7 12:01ET ownBird5년, 첫30%C23_world·firstsalary8% 인상, bonus/option0 |

Murray의 2019 연장은 [공식 발표](https://www.nba.com/news/denver-nuggets-sign-jamal-murray-contract-extension-official-release), Morris의 2020 연장은 [구단 발표](https://www.nba.com/nuggets/news/morris-20201209b)를 읽었다. [Denver2022–23 미디어가이드](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/11/2022-23-Denver-Nuggets-Media-Guide.pdf) PDF274–275의 계약 연혁도 HTTP200 원문으로 확인했다. Porter/Gordon의 연장 기간 보도와 공개 계약 열은 실제 NBA의 참고 입력이다. 작품의 기존 같은 소유자 UPC에 연결하는 것은 명시적인 가상 carry 구현이며 개인 서명/동의·실제 사적 장부를 인증하지 않는다.

Porter/Gordon의 세부 기간은 각각 [NBA 게재 보도](https://www.nba.com/news/reports-nuggets-michael-porter-jr-agree-to-max-extension), [NBA 게재 보도](https://www.nba.com/news/reports-aaron-gordon-reaches-contract-extension-with-nuggets)와 공개 secondary 표를 구분했다. 팀 공식 UPC의 원문을 취득했다고 주장하지 않는다. 캐시·HTTP·raw SHA·원 표 열은 JSON에 보존했다.

Jokic 권고는 직전3시즌 같은 DEN 표준 UPC/rendering과 Bird 권리 유지, 원 계약 서비스 종료, 기존2022 DV 연장이 미실행인 가족 안에서만 적용한다. 실제 NBA MVP·35% 자격을 가져오지 않는다. 첫30%C23는 ordinary 7–9YOS max 이하이며 최저급여를 충족해야 한다. 5년 계수는 C23의0.30/0.324/0.348/0.372/0.396, 합1.74다. 원 보너스·보호·Gamma·지급 의무를 삭제하거나 같은 FA hold와 새 급여를 이중 가산하지 않는다. [2023 CBA](https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf)의 Bird·ordinary max·8%·5년·Season 정의를 캐시 원문에서 직접 읽었다.

## 2024 첫6월 대표 창의 세 접촉

실제 Finals 첫날은 [NBA의 June6 일정](https://api-hub.nba.com/news/nba-starting-5-may-31-2024)을 참고한다. CHI–DEN 대진·홈·게임 결과는 아직 후보이고 실제 BOS–DAL 점수/홈을 가져오지 않는다. 같은 양팀 코어5가 각 창에 출전한다.

| 창 | 길이 | 선택·공동 비용 |
|---|---:|---|
| Q1 10:00→9:40 | 20초 | Carter 높은 도움→Gordon 컷·LM bump 비용→Jokic가 Morris에게 패스해 실제 슛 기회를 준다. Carter/Mark의 리바운드 노동으로 끝낸 제한 가상 표본 |
| Q2 7:30→7:08 | 22초 | LM 첫 시작권→Carter 스크린→P가 자기 슛을 내려놓고 LV에게 이양. LV 독립 슛 실패 뒤 Jokic가 리바운드한다. 패스가 자동 성공이 아님 |
| Q4 2:10→1:50 | 20초 | P 완전 더블을 줄여 Carter가 Jokic 포스트를 감당. Murray→Porter→Morris→Jokic 재진입 기회를 남기고 Mark의 박스아웃과 Carter의 리바운드로 끝낸 표본 |

각 슛은24초에서18초 경과/잔여6초에 릴리스한다. 각 창의 배우10명·순서·게임시계·동시코트5를 검산했고, 선수마다 합62초의 양수 사용분이 있다. 이것은3개의 부분 코트로 각팀310 player-seconds다. 전체240+240이나 경기 점수·승패를 검산한 것은 아니다. Murray의 대표 창 가용은 제한 가상 입력이며 실제 임상/전체 시즌 건강 인증이 아니다.

## 명부와 남은 연결

원 DEN15에 핵심5+기존 다른10 슬롯이 있다. 네 명에게 신규 UPC를 더 만들지 않고 Jokic만 만료 FA claim을 신규 UPC로 한번 대체한다. 슬롯 예약은 전체 live15 등록이 아니다. 남은 벤치10은 원 같은 소유자 경로에서 현재 기간/carry 또는 만료후 합법 재계약만 좁게 연결해야 한다. 전체 활성명단·240분 완료를 주장하지 않는다. Chicago 대표 코어는 원2023–24 계약을 쓰며 LM은 fourth RSC다. Jaquez old16→current20와 원20분은 별도 교정 상태를 유지한다.

2025 MIN의 기존2024 계약15 사슬과 마지막 LM 독립 판단은 동결 최소포트93a8의 후속 사용점이다. old2028/31 계약·시계·점수 이동0, C01 미선택, 원고/Pack/일정0·CLOSED.
