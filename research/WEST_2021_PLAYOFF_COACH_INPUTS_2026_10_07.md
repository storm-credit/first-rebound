# 서부 6팀 — 2021 플레이오프 작업 감독 입력

기준 main `1401b74` / **기존 작가 위임에 따른 작업 건강·감독 설계, 루트 독립 검문 대기**. [기계 입력·전체 명단·블록·원자료 지문](WEST_2021_PLAYOFF_COACH_INPUTS_2026_10_07.json).

이 입력은 실제 건강·등록 인증이나 원고 승인이 아니다. 기존 88경기 작업 달력의 각 팀 출현 날짜에 적용하는 감독 설계다. 중앙 달력·기존 DEN/LAL 6경기·진행 문서는 이 하위 작업에서 수정하지 않았다. 정규시간48분·연장0을 모델로 택했으며 원역사 연장을 복사하지 않는다.

## 전체 작업 명단과 분

| 팀 | 일반계약/TW 작업 명단 | 기본 양의 분 선수 수 | 팀 합계 | 적용 출현 경기 |
|---|---:|---:|---:|---:|
| UTA | 15+2 | 9 | 240분 | 11 |
| MEM | 15+2 | 11 | 240분 | 5 |
| PHX | 15+1 | 10 | 240분 | 25 |
| POR | 15+2 | 11 | 240분 | 6 |
| LAC | 15+2 | 12 | 240분 | 19 |
| DAL | 15+2 | 11 | 240분 | 7 |

매 블록은 서로 다른5명이6분을 소화하며8블록이 끊김 없이48분을 덮는다. 팀 합계240분, 개인 상단48분, 블록 합집합=`modeled_available`, 출전·결장 겹침0을 검사했다. 양의 분 선수만 모델에서 available로 선택한다. 명단에 남은0분 선수의 건강은 null이며 0분을 부상·방출로 바꾸지 않는다. 계속 결장하는 선택 모델은 POR Collins와 DAL Redick뿐이며 실제 진단/복귀 일자를 인증하지 않는다.

### 기본 감독 분 배정

- **UTA**: Bojan Bogdanovic 30, Derrick Favors 12, Donovan Mitchell 36, Georges Niang 12, Joe Ingles 30, Jordan Clarkson 24, Mike Conley 30, Royce O'Neale 30, Rudy Gobert 36분.
- **MEM**: Brandon Clarke 18, De'Anthony Melton 18, Desmond Bane 18, Dillon Brooks 30, Grayson Allen 12, Ja Morant 36, Jaren Jackson Jr. 24, Jonas Valanciunas 30, Kyle Anderson 30, Tyus Jones 12, Xavier Tillman Sr. 12분.
- **PHX**: Cameron Johnson 18, Cameron Payne 18, Chris Paul 36, Dario Saric 18, Deandre Ayton 30, Devin Booker 36, E'Twaun Moore 6, Jae Crowder 30, Mikal Bridges 36, Torrey Craig 12분.
- **POR**: Anfernee Simons 12, CJ McCollum 36, Carmelo Anthony 18, Damian Lillard 36, Derrick Jones Jr. 12, Enes Kanter 18, Jacob Evans 12, Jusuf Nurkic 30, Nassir Little 12, Robert Covington 30, Rodney Hood 24분.
- **LAC**: DeMarcus Cousins 6, Ivica Zubac 24, Kawhi Leonard 36, Luke Kennard 12, Marcus Morris Sr. 30, Nicolas Batum 30, Patrick Beverley 12, Paul George 36, Rajon Rondo 12, Reggie Jackson 24, Serge Ibaka 6, Terance Mann 12분.
- **DAL**: Dorian Finney-Smith 30, Dwight Powell 12, Jalen Brunson 24, Josh Green 12, Josh Richardson 18, Kristaps Porzingis 30, Luka Doncic 36, Maxi Kleber 24, R.J. Hampton 12, Tim Hardaway Jr. 30, Willie Cauley-Stein 12분.

UTA는 `overrides_by_date`가 기본 계획보다 우선한다. **5/23 Mitchell0분**, **5/26 Mitchell24분**, 이후 기본36분이다. 첫 대체 블록은 Conley/Clarkson/Ingles와 Oni로 분을 재배정했다. 날짜별 모델은 원역사 복귀 자동 복사가 아니라 기존 건강 위임 아래 보수적으로 선택한 회복 설계다. 두 override도240분·5명·명단 소속·available 합집합을 각각 검사했다. 새 세계의 동일한 발목 상태나 의료진 판단이 증명됐다는 뜻은 아니다.

## 승인된 차이를 명단에 반영

- **POR**: 기존2018 사슬의 **Jacob Evans**가 Trent의 자리에 있다. Tyreke Evans가 아니다. [T4 승인](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)에 따라 Powell 거래를 생략해 Hood를 남기고 Powell/Trent를 POR에 넣지 않는다. Jacob12분은 감독 선택이며 Trent 생산량을 선물한 수치가 아니다.
- **DAL**: [Hampton31 승인](../simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md)과 [Terry32→CHA 승인](../simulation/2020_DRAFT_TYRELL_TERRY_RELANDING_BOARD.md)을 연결한다. Hampton12분을 모델로 선택했고 Terry의 원역사 결장 이력은 복사하지 않는다.
- **LAC**: [Carey 보드](../simulation/2020_DRAFT_VERNON_CAREY_RELANDING_BOARD.md)의 승인안은33–41 실제 유지다. Carey33는 기각 비교이므로 Oturu를 유지한다.
- **UTA/MEM/PHX**: 승인된 Azubuike/Hughes, Bane/Tillman, Jalen Smith를 유지한다. 지명 순번 이동 자체가 다른 선수로 바뀌었다는 뜻이 아니다.

### Portland 개막 수 정정

개막 PDF3 Portland 열은13명 가운데 **Keljin Blevins가 TW(*)**다. 따라서 active 일반계약12명+inactive Collins/Little2명=**14standard+1TW**다. 앞선 하위 작업의 개막15명·RHJ 추가 시16명이라는 보고는 별표를 놓친 오기였다.

Powell 거래 생략 뒤에도14standard이고, 실제 RHJ ROS 추가를 보존하는 작업 후보는15standard가 된다. Leaf TW 추가 후15+2다. **RHJ 생략을 새로 선택할 필요가 없다.** RHJ는0분·건강null의 명단 예비 선수다. 실제 RHJ 계약 보존 역시 공개 계약군의 작업 후보이며 전체 등록 작가확정이나 실제 접수 인증으로 승격하지 않는다. `new_exact_contract_selection=false`, `full_registration_cleared=false`다.

## 자료·모델의 구분

개막 원자료는 [NBA Dec22 명단 발표의 Duke PDF 미러](https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goduke.com/documents/2020/12/22/2020_21_Opening_Day_Rosters_12_22_20.pdf?timestamp=20201222074936)의 전체 열과 inactive/TW 별표를 직접 읽었다. SHA256 `75a981d64c87de34f7d7896f3a0b1e695b1ed0a3c0e8d4b6638cef71c489ffa0`. inactive 선수는 일반계약에서 삭제하지 않았다. frozen NBA flow는 SHA256 `3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a`; 정수 TEAM_ID/Additional_Sort로6팀의 Dec23~July20 사건을 대조했다. 전체 명단과 사건행은 JSON에 있다.

기본 사건 연결은 UTA Harrison 이탈/Ilyasova·Thomas 취득, MEM Dieng 이탈/Frazier ROS, PHX Damian Jones 이탈/Craig 취득, LAC Kabengele·Williams 이탈/Rondo·Cousins·Ferrell 취득, DAL Johnson·Iwundu 이탈/Redick·Melli 취득이다. 짧은10일 계약을 그대로 시즌말 일반계약으로 남기지 않고 확인된 ROS 서명으로 연결했다. 동일 공개 계약군을 작업 기간에 유지하는 모델이며 비공개 이후 거래의 절대 부재나 전체 급여 적법성 증인은 아니다.

다음 **플레이오프 이전** 자료의 회수 상태·지원 범위·날짜는 JSON에 기록했다. LAC의 과거 정확 출전분은 재확인하지 못해 미확인으로 낮췄다.

- [UTA Mitchell5/20](https://www.nba.com/news/jazz-star-donovan-mitchell-ankle-eyeing-return-for-game-1)
- [MEM JJJ4/21 구단 보고](https://www.nba.com/grizzlies/news/postgame/lac-210421)
- [LAC Ibaka5/14 박스 경로](https://www.nba.com/clippers/game/0022001058-clippers-vs-rockets-houston-tx-05-14-2021): **미확인**. 기존17:15 주장에는 회수 가능한 검색 쿼리/ref가 없고 독립 open은 iframe만이어서 사실 근거에서 제외했다. Ibaka6분은 기존 위임 아래 선택한 작업 건강·감독 모델로 유지하며 의료 인증이나 실제 복귀 사실이 아니다.
- [POR Collins12/30 공식 발표](https://www.nba.com/news/zach-collins-out-indefinitely-after-ankle-surgery)
- [DAL5/21 구단 사전 보고](https://www.nba.com/mavs/mavs-open-playoffs)
- [PHX5/20 NBA preview](https://www.nba.com/news/series-preview-suns-lakers-first-round-2021)

실제 May16 경기책6건은 직접 HTTP timeout으로 본문을 회수하지 못했다. 위 건강 페이지의 직접 raw HTML6건은403이었으며 실패 응답의 cache/SHA를 성공 기사 지문으로 부르지 않는다. LAC 정확분의 미확인 주장·다른 웹 본문 관측·직접 HTTP 실패를 구분한다. 원자료 경로·실패·정본9개 SHA가 JSON에 있다. 없는 raw 기사/PDF 본문을 읽었다고 하지 않는다.

원역사 후발 **Leonard ACL, Paul 어깨·프로토콜, Conley 재발, Saric Finals ACL, Mitchell 재접촉**을 새 날짜·상대·분의 작업 계획에 자동 이식하지 않는다. 로테이션 선수의 추가 접촉 부상 발생을 선택하지 않았으며 모두 위임된 설계다. 이 가정이 의학적으로 입증됐다는 뜻은 아니다.

## 적용·검문 경계

루트 생성기는 88경기 달력의 팀별 연결 목록과 날짜 override를 사용한다. 이 파일 자체는 경기별 승패·점수·개별 박스·실제 active list·의료 사건을 생성하거나 확정하지 않는다. six-team default6개+UTA override2개를 검산했고 독립 검문은 대기다. Antigravity·NotebookLM·Claude는 이 하위 작업에서 실행하지 않았다.

실제 등록/active list/의료 인증false, 전체 건강 게이트false, 시즌미확정, freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0. 기존 정본·중앙 상태 수정0.

저장소 입력 해시는 BOM 제거·CRLF/CR→LF 정규화로 연결한다. 최초 raw 검문 해시는 `initial_audit_repository_raw_sha256`로 보존했고 원자료 cache8개의 raw SHA는 변경하지 않았다. 이 수리는 줄바꿈 해시 범위만 변경한다.

독립 검문 후 LAC exact17:15 사실 승격을 취소했다. May16 PDF의 LAC 제출 목록은 Ibaka의 상태를 직접 적지 않아 누락을 건강 증명으로 쓰지 않았다. 원자료 raw cache8개 해시 변경0, 실제 계획의 Ibaka6분·전체240분 변경0.
