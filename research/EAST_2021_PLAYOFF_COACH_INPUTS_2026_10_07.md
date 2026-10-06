# 동부 2021 플레이오프 감독 작업 입력

기준 main `1401b74` / 기존 건강·시즌 설계 위임. PHI·IND·BKN·BOS·MIL·MIA·NYK·ATL 8팀의 전체 작업 명단과 6분×8블록을 준비했다. 중앙 상태 문서는 수정하지 않았다.

## 범위

- **사실:** NBA 2020-12-22 opening 원문, frozen movement 원자료, 역사 특정일 부상 보고.
- **추론:** 공개 계약 흐름에 승인된 Boston 이동을 연결한 작업 명단.
- **위임된 설계:** 감독 배치, 제한 출전·계속 결장·이후 새 접촉부상 없음. 원역사 실제 분배/의료 인증이 아니다.
- 전체 법적 등록·시즌 확정·원고 허용을 인증하지 않는다. 예비선수 예정 0분은 결장/명단 부재가 아니다.

## 검산

|항목|결과|
|---|---|
|팀|8|
|6분 블록|64|
|블록별 고유 선수|5|
|팀별 48분 총 선수분|240|
|전체 템플릿 분|1,920|
|modeled_available|블록 합집합과 정확히 동일|
|reserve_health|사용/결장 모델 밖 전원 null|

## 팀별 작업 계획

### PHI

일반 15명 / 투웨이 2명. 감독 모델: Doc Rivers.

전체 일반: Ben Simmons, Seth Curry, Danny Green, Tobias Harris, Joel Embiid, George Hill, Matisse Thybulle, Dwight Howard, Furkan Korkmaz, Shake Milton, Tyrese Maxey, Isaiah Joe, Paul Reed, Mike Scott, Anthony Tolliver.
투웨이: Rayjon Tucker, Gary Clark.

모델 결장: 별도 지속 결장 선택 없음.

예정 분: Ben Simmons 36, Danny Green 36, Dwight Howard 12, George Hill 24, Joel Embiid 36, Matisse Thybulle 24, Seth Curry 36, Tobias Harris 36.

|경과 분|5인 배치|
|---|---|
|0–6|Ben Simmons, Seth Curry, Danny Green, Tobias Harris, Joel Embiid|
|6–12|George Hill, Seth Curry, Matisse Thybulle, Tobias Harris, Joel Embiid|
|12–18|Ben Simmons, George Hill, Danny Green, Matisse Thybulle, Dwight Howard|
|18–24|Ben Simmons, Seth Curry, Danny Green, Tobias Harris, Joel Embiid|
|24–30|Ben Simmons, Seth Curry, Danny Green, Tobias Harris, Joel Embiid|
|30–36|George Hill, Seth Curry, Matisse Thybulle, Tobias Harris, Dwight Howard|
|36–42|Ben Simmons, George Hill, Danny Green, Matisse Thybulle, Joel Embiid|
|42–48|Ben Simmons, Seth Curry, Danny Green, Tobias Harris, Joel Embiid|

- Simmons initiates; Harris/Embiid carry half-court scoring; Hill/Thybulle supply perimeter defense.
- Embiid rest is covered by Howard; bench reserves remain on full roster.

- Joel Embiid: May16 listed Out with non-Covid illness. Available 36-minute role after recovery modeled by May23; May31 fall/meniscus injury not copied.

### IND

일반 15명 / 투웨이 2명. 감독 모델: Nate Bjorkgren.

전체 일반: Malcolm Brogdon, Caris LeVert, T.J. McConnell, Domantas Sabonis, Myles Turner, T.J. Warren, Jeremy Lamb, Aaron Holiday, Justin Holiday, Doug McDermott, Edmond Sumner, Goga Bitadze, JaKarr Sampson, Kelan Martin, Oshae Brissett.
투웨이: Cassius Stanley, Amida Brimah.

모델 결장: Caris LeVert, Myles Turner, T.J. Warren, Jeremy Lamb.

예정 분: Domantas Sabonis 36, Doug McDermott 36, Edmond Sumner 24, Goga Bitadze 12, Justin Holiday 36, Malcolm Brogdon 36, Oshae Brissett 36, T.J. McConnell 24.

|경과 분|5인 배치|
|---|---|
|0–6|Malcolm Brogdon, Justin Holiday, Doug McDermott, Oshae Brissett, Domantas Sabonis|
|6–12|T.J. McConnell, Justin Holiday, Edmond Sumner, Oshae Brissett, Domantas Sabonis|
|12–18|Malcolm Brogdon, T.J. McConnell, Doug McDermott, Edmond Sumner, Goga Bitadze|
|18–24|Malcolm Brogdon, Justin Holiday, Doug McDermott, Oshae Brissett, Domantas Sabonis|
|24–30|Malcolm Brogdon, Justin Holiday, Doug McDermott, Oshae Brissett, Domantas Sabonis|
|30–36|T.J. McConnell, Justin Holiday, Edmond Sumner, Oshae Brissett, Goga Bitadze|
|36–42|Malcolm Brogdon, T.J. McConnell, Doug McDermott, Edmond Sumner, Domantas Sabonis|
|42–48|Malcolm Brogdon, Justin Holiday, Doug McDermott, Oshae Brissett, Domantas Sabonis|

- Brogdon/McConnell initiate with Sabonis hub; Brissett/McDermott spacing replaces unavailable LeVert/Turner.
- Turner absence leaves real rim-defense cost; no invented equivalent protector.

- Caris LeVert: Official May20 report lists inactive. Keep unavailable throughout five modeled first-round dates; no dated clearance invented. Continued absence is a design selection, not proven protocol duration.
- Myles Turner: Official May20 report lists inactive. Keep unavailable throughout five modeled first-round dates; no dated clearance invented. Continued absence is a design selection, not proven protocol duration.
- T.J. Warren: Official May20 report lists inactive. Keep unavailable throughout five modeled first-round dates; no dated clearance invented. Continued absence is a design selection, not proven protocol duration.
- Jeremy Lamb: Official May20 report lists inactive. Keep unavailable throughout five modeled first-round dates; no dated clearance invented. Continued absence is a design selection, not proven protocol duration.
- Malcolm Brogdon: May20 report records positive playing time. Available within conservative 6-minute blocks; earlier questionable status not read as full clearance.
- Edmond Sumner: May20 report records positive playing time. Available within conservative 6-minute blocks; earlier questionable status not read as full clearance.
- Domantas Sabonis: May20 report records positive playing time. Available within conservative 6-minute blocks; earlier questionable status not read as full clearance.

### BKN

일반 15명 / 투웨이 2명. 감독 모델: Steve Nash.

전체 일반: Kevin Durant, Kyrie Irving, James Harden, Joe Harris, DeAndre Jordan, Bruce Brown, Jeff Green, Landry Shamet, Tyler Johnson, Timothe Luwawu-Cabarrot, Nicolas Claxton, Blake Griffin, Alize Johnson, Mike James, Spencer Dinwiddie.
투웨이: Chris Chiozza, Reggie Perry.

모델 결장: Spencer Dinwiddie.

예정 분: Blake Griffin 24, Bruce Brown 24, James Harden 36, Jeff Green 24, Joe Harris 36, Kevin Durant 36, Kyrie Irving 36, Nicolas Claxton 24.

|경과 분|5인 배치|
|---|---|
|0–6|James Harden, Kyrie Irving, Joe Harris, Kevin Durant, Blake Griffin|
|6–12|Bruce Brown, Kyrie Irving, Jeff Green, Kevin Durant, Nicolas Claxton|
|12–18|James Harden, Bruce Brown, Joe Harris, Jeff Green, Nicolas Claxton|
|18–24|James Harden, Kyrie Irving, Joe Harris, Kevin Durant, Blake Griffin|
|24–30|James Harden, Kyrie Irving, Joe Harris, Kevin Durant, Blake Griffin|
|30–36|Bruce Brown, Kyrie Irving, Jeff Green, Kevin Durant, Nicolas Claxton|
|36–42|James Harden, Bruce Brown, Joe Harris, Jeff Green, Nicolas Claxton|
|42–48|James Harden, Kyrie Irving, Joe Harris, Kevin Durant, Blake Griffin|

- Harden/Kyrie stagger; Durant remains primary wing creator; Griffin/Claxton/Jeff Green share frontcourt.
- DeAndre Jordan remains rostered despite zero planned minutes; no absent inference.

- Spencer Dinwiddie: Partially torn ACL listed Out. Carry absence across modeled playoffs.
- James Harden: Preplayoff article describes star trio ready. Available 36 minutes; do not copy subsequent June5 hamstring event.
- Kyrie Irving: Preplayoff article describes star trio ready. Available; June13 opponent-foot landing not copied.

### BOS

일반 15명 / 투웨이 2명. 감독 모델: Brad Stevens.

전체 일반: Jaylen Brown, Jayson Tatum, Marcus Smart, Kemba Walker, Evan Fournier, Tristan Thompson, Robert Williams III, Grant Williams, Payton Pritchard, Aaron Nesmith, Romeo Langford, Semi Ojeleye, Carsen Edwards, Luke Kornet, Jabari Parker.
투웨이: Tacko Fall, Tremont Waters.

모델 결장: Jaylen Brown.

예정 분: Evan Fournier 36, Jayson Tatum 36, Kemba Walker 36, Marcus Smart 36, Payton Pritchard 24, Robert Williams III 12, Romeo Langford 24, Tristan Thompson 36.

|경과 분|5인 배치|
|---|---|
|0–6|Kemba Walker, Marcus Smart, Evan Fournier, Jayson Tatum, Tristan Thompson|
|6–12|Payton Pritchard, Marcus Smart, Romeo Langford, Jayson Tatum, Tristan Thompson|
|12–18|Kemba Walker, Payton Pritchard, Evan Fournier, Romeo Langford, Robert Williams III|
|18–24|Kemba Walker, Marcus Smart, Evan Fournier, Jayson Tatum, Tristan Thompson|
|24–30|Kemba Walker, Marcus Smart, Evan Fournier, Jayson Tatum, Tristan Thompson|
|30–36|Payton Pritchard, Marcus Smart, Romeo Langford, Jayson Tatum, Robert Williams III|
|36–42|Kemba Walker, Payton Pritchard, Evan Fournier, Romeo Langford, Tristan Thompson|
|42–48|Kemba Walker, Marcus Smart, Evan Fournier, Jayson Tatum, Tristan Thompson|

- Tatum/Walker creation; Smart/Fournier shooting/defense; Thompson plus managed Williams III at center.
- Brown absence costs wing offense; reserve Parker/Nesmith/Kornet not removed by zero plan.

- Jaylen Brown: Wrist ligament surgery listed Out. Carry zero minutes across Boston modeled postseason; changed-contact identity not asserted.
- Robert Williams III: Turf toe listed Questionable. Choose managed 12-minute role; medical clearance remains null.

### MIL

일반 15명 / 투웨이 2명. 감독 모델: Mike Budenholzer.

전체 일반: Giannis Antetokounmpo, Thanasis Antetokounmpo, Khris Middleton, Jrue Holiday, Donte DiVincenzo, Brook Lopez, Bobby Portis, Pat Connaughton, Bryn Forbes, Sam Merrill, Jordan Nwora, P.J. Tucker, Jeff Teague, Mamadi Diakite, Elijah Bryant.
투웨이: Axel Toupane, Justin Jackson.

모델 결장: Thanasis Antetokounmpo.

예정 분: Bobby Portis 12, Brook Lopez 36, Bryn Forbes 12, Donte DiVincenzo 24, Giannis Antetokounmpo 36, Jrue Holiday 36, Khris Middleton 36, P.J. Tucker 24, Pat Connaughton 24.

|경과 분|5인 배치|
|---|---|
|0–6|Jrue Holiday, Donte DiVincenzo, Khris Middleton, Giannis Antetokounmpo, Brook Lopez|
|6–12|Pat Connaughton, Bryn Forbes, P.J. Tucker, Giannis Antetokounmpo, Brook Lopez|
|12–18|Jrue Holiday, Pat Connaughton, Khris Middleton, P.J. Tucker, Bobby Portis|
|18–24|Jrue Holiday, Donte DiVincenzo, Khris Middleton, Giannis Antetokounmpo, Brook Lopez|
|24–30|Jrue Holiday, Donte DiVincenzo, Khris Middleton, Giannis Antetokounmpo, Brook Lopez|
|30–36|Pat Connaughton, Bryn Forbes, P.J. Tucker, Giannis Antetokounmpo, Bobby Portis|
|36–42|Jrue Holiday, Pat Connaughton, Khris Middleton, P.J. Tucker, Brook Lopez|
|42–48|Jrue Holiday, Donte DiVincenzo, Khris Middleton, Giannis Antetokounmpo, Brook Lopez|

- Holiday/Middleton creation; Giannis plus Lopez rim protection; Tucker/Portis/Connaughton and Forbes split bench roles.
- Do not copy later DiVincenzo foot or Giannis contact injury.

- Thanasis Antetokounmpo: Patellar tendon avulsion fracture listed Out. Carry zero reserve role; injury mechanism not asserted equal in alternate world.

### MIA

일반 15명 / 투웨이 2명. 감독 모델: Erik Spoelstra.

전체 일반: Bam Adebayo, Jimmy Butler, Goran Dragic, Duncan Robinson, Kendrick Nunn, Tyler Herro, Andre Iguodala, Trevor Ariza, Nemanja Bjelica, Dewayne Dedmon, Precious Achiuwa, KZ Okpala, Udonis Haslem, Victor Oladipo, Omer Yurtseven.
투웨이: Max Strus, Gabe Vincent.

모델 결장: Victor Oladipo.

예정 분: Andre Iguodala 24, Bam Adebayo 36, Dewayne Dedmon 12, Duncan Robinson 36, Goran Dragic 24, Jimmy Butler 36, Kendrick Nunn 24, Trevor Ariza 36, Tyler Herro 12.

|경과 분|5인 배치|
|---|---|
|0–6|Kendrick Nunn, Duncan Robinson, Jimmy Butler, Trevor Ariza, Bam Adebayo|
|6–12|Goran Dragic, Duncan Robinson, Andre Iguodala, Trevor Ariza, Bam Adebayo|
|12–18|Goran Dragic, Tyler Herro, Jimmy Butler, Andre Iguodala, Dewayne Dedmon|
|18–24|Kendrick Nunn, Duncan Robinson, Jimmy Butler, Trevor Ariza, Bam Adebayo|
|24–30|Kendrick Nunn, Duncan Robinson, Jimmy Butler, Trevor Ariza, Bam Adebayo|
|30–36|Goran Dragic, Duncan Robinson, Andre Iguodala, Trevor Ariza, Dewayne Dedmon|
|36–42|Goran Dragic, Tyler Herro, Jimmy Butler, Andre Iguodala, Bam Adebayo|
|42–48|Kendrick Nunn, Duncan Robinson, Jimmy Butler, Trevor Ariza, Bam Adebayo|

- Butler/Bam hubs; Robinson movement shooting; Dragic/Herro second-unit offense with Dedmon rim minutes.
- Oladipo absent role not transferred to one scorer as free production.

- Victor Oladipo: Knee surgery listed Out. Carry zero minutes; preplayoff surgery retained as explicit model.

### NYK

일반 15명 / 투웨이 2명. 감독 모델: Tom Thibodeau.

전체 일반: Derrick Rose, RJ Barrett, Reggie Bullock, Julius Randle, Nerlens Noel, Alec Burks, Immanuel Quickley, Elfrid Payton, Obi Toppin, Taj Gibson, Kevin Knox II, Frank Ntilikina, Mitchell Robinson, Norvel Pelle, Luca Vildoza.
투웨이: Theo Pinson, Jared Harper.

모델 결장: Mitchell Robinson, Luca Vildoza.

예정 분: Alec Burks 24, Derrick Rose 36, Immanuel Quickley 24, Julius Randle 36, Nerlens Noel 36, RJ Barrett 36, Reggie Bullock 36, Taj Gibson 12.

|경과 분|5인 배치|
|---|---|
|0–6|Derrick Rose, RJ Barrett, Reggie Bullock, Julius Randle, Nerlens Noel|
|6–12|Immanuel Quickley, RJ Barrett, Alec Burks, Julius Randle, Nerlens Noel|
|12–18|Derrick Rose, Immanuel Quickley, Reggie Bullock, Alec Burks, Taj Gibson|
|18–24|Derrick Rose, RJ Barrett, Reggie Bullock, Julius Randle, Nerlens Noel|
|24–30|Derrick Rose, RJ Barrett, Reggie Bullock, Julius Randle, Nerlens Noel|
|30–36|Immanuel Quickley, RJ Barrett, Alec Burks, Julius Randle, Taj Gibson|
|36–42|Derrick Rose, Immanuel Quickley, Reggie Bullock, Alec Burks, Nerlens Noel|
|42–48|Derrick Rose, RJ Barrett, Reggie Bullock, Julius Randle, Nerlens Noel|

- Rose starts by modeled coach choice, replacing historical Payton starting convention.
- Randle/Barrett carry scoring; Noel/Gibson centers; Quickley/Burks guard bench.

- Mitchell Robinson: Foot surgery listed Out. Carry zero minutes across Knicks modeled first round.
- Luca Vildoza: Listed Not With Team. Choose no postseason arrival; registration retained, absent availability is model not permanent medical claim.

### ATL

일반 15명 / 투웨이 2명. 감독 모델: Nate McMillan.

전체 일반: Trae Young, Bogdan Bogdanovic, Kevin Huerter, De'Andre Hunter, Cam Reddish, Clint Capela, John Collins, Danilo Gallinari, Lou Williams, Solomon Hill, Bruno Fernando, Onyeka Okongwu, Tony Snell, Kris Dunn, Brandon Goodwin.
투웨이: Nathan Knight, Skylar Mays.

모델 결장: Cam Reddish, Brandon Goodwin.

예정 분: Bogdan Bogdanovic 36, Clint Capela 36, Danilo Gallinari 12, De'Andre Hunter 36, John Collins 24, Kevin Huerter 24, Lou Williams 24, Onyeka Okongwu 12, Trae Young 36.

|경과 분|5인 배치|
|---|---|
|0–6|Trae Young, Bogdan Bogdanovic, De'Andre Hunter, John Collins, Clint Capela|
|6–12|Lou Williams, Bogdan Bogdanovic, Kevin Huerter, Danilo Gallinari, Clint Capela|
|12–18|Trae Young, Lou Williams, De'Andre Hunter, Kevin Huerter, Onyeka Okongwu|
|18–24|Trae Young, Bogdan Bogdanovic, De'Andre Hunter, John Collins, Clint Capela|
|24–30|Trae Young, Bogdan Bogdanovic, De'Andre Hunter, John Collins, Clint Capela|
|30–36|Lou Williams, Bogdan Bogdanovic, Kevin Huerter, Danilo Gallinari, Onyeka Okongwu|
|36–42|Trae Young, Lou Williams, De'Andre Hunter, Kevin Huerter, Clint Capela|
|42–48|Trae Young, Bogdan Bogdanovic, De'Andre Hunter, John Collins, Clint Capela|

- Trae/Capela pick-and-roll; Collins/Gallinari frontcourt spacing; Bogdan/Huerter guards and Hunter wing defense.
- Reddish/Goodwin absent; reserves Hill/Snell/Dunn remain rostered with null reserve health.

- Cam Reddish: May23 report lists both Out. Carry zero postseason minutes in this working plan; no observed exact return date claimed.
- Brandon Goodwin: May23 report lists both Out. Carry zero postseason minutes in this working plan; no observed exact return date claimed.
- De'Andre Hunter: No Hunter constraint asserted from omission. Available 36 minutes under delegation; subsequent June knee event not automatically copied.

## 원자료와 미회수 경계

Opening PDF는 NBA 작성·Duke 공식 미러, 4쪽 원문 SHA `75a981d64c87de34f7d7896f3a0b1e695b1ed0a3c0e8d4b6638cef71c489ffa0`. 동부 8팀은 1–3쪽. inactive 비투웨이는 일반 명단에 포함했다.

Frozen movement SHA `3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a`; 정수 TEAM_ID로 범위를 추출하고 상대팀 취득 행을 함께 보존했다. 12/22 Brooklyn Chiozza/Martin 당일 교체도 포함한다.

NBA 5/16·5/18·5/22·5/23 injury PDF 4건은 HTTP200 원문·SHA·본문 쪽을 JSON에 기록했다. IND5/20 official scorer report는 web PDF 본문에서 MIN·Inactive를 직접 읽었다; 로컬 HTTP는 timeout이라 raw SHA는 null.

다른 팀 gamebook 요청은 timeout/reset, livebox JSON 및 원게임 HTML은403. web box UI는 통계표를 표시하지 않았다. 이를 complete historical rotation 회수로 계수하지 않았다. NBA 원기사 preview 역할 근거와 전체 source roster를 사용한 감독 모델이며 미회수 exact 역사 분은 새 의료 인증으로 승격하지 않는다.

Brown·Oladipo·Turner 등 지속 결장은 원역사 제약을 출발점으로 선택했다. LeVert protocol을 전체 IND5경기에 지속하는 선택, Reddish/Thanasis의 이후 복귀 미설계, Williams III12분과 Embiid 회복은 **설계**다. 원역사 후속 Embiid/Harden/Irving/Hunter/DiVincenzo/Giannis 부상을 자동 이식하지 않는다.

## 자료 링크

- [OPENING_20201222](https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goduke.com/documents/2020/12/22/2020_21_Opening_Day_Rosters_12_22_20.pdf?timestamp=20201222074936) — All30 opening roster; inactive non-TW remains standard; not playoff active list.
- [NBA_MOVEMENT_FROZEN](https://www.nba.com/players/transactions) — Frozen public movement JSON; team_id integer filter; simultaneous record duplicates retained, not independent events.
- [INJURY_0516](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-16_08PM.pdf) — NBA submitted historical game injury status; not alternate clearance or permanent status.
- [INJURY_0518](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-18_05PM.pdf) — NBA submitted historical game injury status; not alternate clearance or permanent status.
- [INJURY_0522](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-22_05PM.pdf) — NBA submitted historical game injury status; not alternate clearance or permanent status.
- [INJURY_0523](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-23_05PM.pdf) — NBA submitted historical game injury status; not alternate clearance or permanent status.
- [IND_SCORER_20210520](https://statsdmz.nba.com/pdfs/20210520/20210520_INDWAS.pdf) — NBA official scorer; web PDF text directly recovered, local HTTP timeout; raw bytes unavailable.
- [BKN_BOS_PREVIEW](https://www.nba.com/news/series-preview-celtics-face-huge-challenge-against-nets) — NBA staff original analysis; historical role support, not substitutions
- [MIL_MIA_PREVIEW](https://www.nba.com/news/series-preview-bucks-heat-first-round-2021) — NBA staff original analysis; Holiday/Tucker/Butler/Bam role support
- [NYK_ATL_PREVIEW](https://www.nba.com/news/series-preview-playoff-newbies-knicks-hawks-ready-to-keep-late-rolls-going) — NBA staff original analysis; Trae/Capela/Collins and NYK pointguard options
- [PHI_TEAM_RECAP](https://www.nba.com/sixers/2021/05/23/76ers-vs-wizards-game-1-recap) — Source search body recovered only; not complete historical rotation
- [BROWN_NEWS](https://www.nba.com/news/jaylen-brown-out-for-season-with-torn-ligament-in-wrist) — NBA-published AP report; historical surgery status
- [OLADIPO_NEWS](https://www.nba.com/news/heat-victor-oladipo-to-undergo-season-ending-surgery) — NBA news report; source body opened
- [GOODWIN_NEWS](https://www.nba.com/news/hawks-guard-brandon-goodwin-out-for-playoffs-with-respiratory-condition) — NBA-published AP report; body opened

## 게이트

`v0.30 PARTIAL` / 설계·원고 `CLOSED` / 원고0. 통합 생성기에서 88날짜에 실제 적용·명단/블록 검문을 한 뒤 진행 수를 계수한다. 이 파일만으로 K/시즌을 완료하지 않는다.

정본 입력 source_sha256은 UTF-8 BOM 제거·CRLF/CR→LF 정규화 바이트다. 생성 당시 저장소 raw 해시는 initial_audit_repository_raw_sha256에 별도 보존했다. 회수 원자료 raw_sha256은 다운로드 raw bytes이며 변경하지 않았다. 실제 의료/등록·역사 exact rotation은 HOLD(본 모델이 주장하지 않는 범위).
