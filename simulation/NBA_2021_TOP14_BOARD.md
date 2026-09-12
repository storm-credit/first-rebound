# 2021 Draft 상위14 — 팀별 비교와 Chicago 후보의 선점 위험

- 단계: `O-15G4 / TOP14_FOUR_AUTHORED_OPTIONS_NOT_FINAL_DRAFT`.
- [입력](NBA_2021_TOP14_BOARD_INPUTS.json) · [산출](NBA_2021_TOP14_BOARD.json) · [출처](../research/NBA_2021_TOP14_BOARD_SOURCES.json).
- 기존 CP2 절차 승인 아래의 **창작 검토안**이다. 구단 비공개 보드를 재현한 예측 모델이 아니며 네 안의 확률도 부여하지 않았다. `selected_scenario=null`, 모든 최종 잠금 false.

## 주안과 G3의 관계

**DB1을 추천한다: New Orleans9 Moody → Chicago10 Duarte.** G3의 ‘Moody가 남으면 우선’ 조건을 상위 팀에 적용했을 때 나온 설계안이다. G3가 잘못 지명한 선수를 되돌리는 것이 아니다. G3에서는 실제 지명이나 계약을 한 적이 없다. New Orleans의 외곽 보강 필요에 Chicago보다 앞선 지명권을 주고 그 비용을 Chicago의 선택 폭에 반영했다.

DB1의 Duarte10·G3의 Edwards39/Bradley/Stanley/Valentine 조합은 **39순위 가용성까지 검증한 명단이 아니다**. Duarte는 같은10순위 scale 예산 $4,373,040을 사용하므로 G3와 금액 차이는0이다. G2 장기 구조에서 이 신인을 10대 성장형 윙으로 쓰지 않는다. 그의 실제 생년은1997년이며 P의1999년생보다 앞선다. [2021 Duarte 프로필](https://www.nba.com/draft/2021/prospects/chris-duarte).

## 서로 배타적인 네 안

| 안 | 핵심 선택 | Chicago10 | 비교 비용 |
|---|---|---|---|
| **DB1 추천** | GSW7 Franz, TOR8 Giddey, NOP9 Moody | **Duarte** | 앞선 팀의 무볼 윙 수요가 Chicago 우선 후보를 소진 |
| DB2 | NOP9 Bouknight | Moody | NOP가 즉시 무볼 역할보다 자가 득점 성장을 우선하는 반대 판단 |
| DB3 | GSW7 Moody, TOR8 Franz, NOP9 Giddey | Duarte | 첫 선점이7번으로 이동; 다른 팀의 남은 후보도 순차 변경 |
| DB4 | DB1의1~9 유지, CHI가 센터 기술 선택 | Sengun | Carter/Markkanen/Young/Bradley·윙 분을 재설계해야 함 |

DB1/2/3은 어느 구단이 실제로 이런 내부 평가를 했다는 주장이 아니다. DB4도 현재14분 SF 자리를 센터에게 그대로 주는 안이 아니다. 숫자 순위표를 조정해 이미 뽑힌 선수를 재등장시키지 않는다.

## 1~14 순서별 결과

표의 구단은 **이 네 안에서 새 상위14 픽 거래가 없다는 조건의 통제 구단**이다. 원소유 MIN7은 기존 top3 보호 경로에 따라 GSW가 받는다. Chicago10은 Vucevic 거래를 하지 않아 보존한 자기 픽이다. NOP9를 Memphis에 넘기는 새 거래는 이 네 안에서 실행하지 않았다. 바뀐9/17 거래가 불가능하다고 판정한 것은 아니다.

| 순번 | 통제 조건 | DB1 | DB2 | DB3 | DB4 |
|---:|---|---|---|---|---|
| 1 | CHA | Cade Cunningham | Cade Cunningham | Cade Cunningham | Cade Cunningham |
| 2 | HOU | Jalen Green | Jalen Green | Jalen Green | Jalen Green |
| 3 | ORL | Evan Mobley | Evan Mobley | Evan Mobley | Evan Mobley |
| 4 | OKC | Scottie Barnes | Scottie Barnes | Scottie Barnes | Scottie Barnes |
| 5 | DET | Jalen Suggs | Jalen Suggs | Jalen Suggs | Jalen Suggs |
| 6 | CLE | Jonathan Kuminga | Jonathan Kuminga | Jonathan Kuminga | Jonathan Kuminga |
| 7 | GSW | Franz Wagner | Franz Wagner | Moses Moody | Franz Wagner |
| 8 | TOR | Josh Giddey | Josh Giddey | Franz Wagner | Josh Giddey |
| 9 | NOP | Moses Moody | James Bouknight | Josh Giddey | Moses Moody |
| 10 | CHI | Chris Duarte | Moses Moody | Chris Duarte | Alperen Sengun |
| 11 | SAC | Davion Mitchell | Davion Mitchell | Davion Mitchell | Davion Mitchell |
| 12 | WAS | Corey Kispert | Corey Kispert | Corey Kispert | Corey Kispert |
| 13 | SAS | Joshua Primo | Joshua Primo | Joshua Primo | Joshua Primo |
| 14 | GSW | James Bouknight | Chris Duarte | James Bouknight | Chris Duarte |

NBA의 당시 [consensus](https://www.nba.com/news/2021-consensus-mock-draft)는 상위권 평가 범위와 이후 불확실성을 확인하는 자료다. 이를 특정 확률·구단 내부 서열로 변환하지 않는다. [실제 보드](https://www.nba.com/draft/2021/draft-board)는 사실 대조 기준이며 새 결과의 보존 목표가 아니다.

## 팀 입력·비교·실제 비용

아래 해석은 프로젝트의 추론이다. 공개 자료의 역사적 로스터를 그대로 적용하지 않고 승인된2020 연쇄와2021 방향을 먼저 반영했다. 각 픽의 후보 순서는 이 제안의 입력이다. 코드는 입력 순위를 증명하지 않고 선행 선택 제외와 후속 연결만 검증한다.

### 1. CHA — Cade Cunningham

- 새 입력: Edwards3·Terry32·Carey42·Richards56; LaMelo 없음.
- 현재 가용 비교: Cade Cunningham, Evan Mobley, Jalen Green. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Edwards의 득점과 다른 대형 창출 기능을 Cade로 보강. 센터 Mobley와 득점 Green도 남지만 전체1번 평가와 창출 공백을 먼저 고려. Terry는 기존 건강 스트레스 이후의 복귀/역할을 별도 검토.
- 비용/반대: 가드 분·Graham RFA·센터 보강은 별도. Cade가 센터 부족까지 해결하지 않는다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/charlotte-hornets). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 2. HOU — Jalen Green

- 새 입력: Wood·Kevin Porter Jr. 중심, 새2순위 유지.
- 현재 가용 비교: Jalen Green, Evan Mobley, Jalen Suggs. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Cade가 먼저 사라진 조건에서 실제 Green 선택을 비교 기준으로 유지. Mobley의 수비/장기 빅과 Suggs의 조직 대안보다 외곽 득점 성장에 자원을 쓴다.
- 비용/반대: Green에게 실제 이후 성과나 특정 사용률을 선물하지 않는다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/houston-rockets). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 3. ORL — Evan Mobley

- 새 입력: Vucevic·Aminu 잔류; Carter/Porter/CHI1R 없음; Nnaji·Harris 유입; Hampton 없음.
- 현재 가용 비교: Evan Mobley, Jalen Suggs, Scottie Barnes. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: 3순위까지 남은 Mobley의 2021 상위 재능 범위를 우선. Suggs의 가드 보강·Barnes의 윙 연결보다 장기 빅 축을 선택하는 제안.
- 비용/반대: Vucevic·Bamba·Nnaji·Okeke와 개발 분/등록이 충돌한다. 센터가 비었다는 설명 금지; Vucevic 후속 거래를 자동 채택하지 않는다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/orlando-magic). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 4. OKC — Scottie Barnes

- 새 입력: SGA·Dort·Poku 유지 조건; 4순위로 상승.
- 현재 가용 비교: Scottie Barnes, Jalen Suggs, Josh Giddey. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Barnes의 포워드 연결 기능을 SGA/Dort 옆에 두는 안. Suggs/Giddey의 추가 가드 창출과 비교한다.
- 비용/반대: 슈팅 성장을 가정한 즉시 완성 코어가 아니다. 실제 Giddey6 선호만으로 Barnes4를 지우지 않고 대안으로 남긴다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/oklahoma-city-thunder). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 5. DET — Jalen Suggs

- 새 입력: Patrick7·Kira16·Stewart19; Hayes/Bey 없음.
- 현재 가용 비교: Jalen Suggs, Josh Giddey, Jonathan Kuminga. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Kira가 이미 있어도 Suggs의 주/보조 창출과 당시 상위 평가를 우선한다. Giddey의 크기·Kuminga의 윙 상방과 비교한다.
- 비용/반대: 가드 자리가 완전히 비었다는 주장 금지. Kira와 볼/분 경쟁, Patrick과 비슈팅 조합을 후속에서 치른다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/detroit-pistons). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 6. CLE — Jonathan Kuminga

- 새 입력: Garland·Sexton·Okoro·Allen 기준; Mobley가 앞서 사라짐.
- 현재 가용 비교: Jonathan Kuminga, Franz Wagner, Moses Moody. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Kuminga의 대형 윙 득점 성장에 투자. Franz의 연결/즉시성, Moody의 슛을 더 빨리 쓰는 대안도 유효하다.
- 비용/반대: Okoro와 슈팅 부담이 겹친다. 가장 강한 반대 후보 Franz를 불가 판정하지 않으며 내부 순위 미확보다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/cleveland-cavaliers). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 7. GSW — Franz Wagner

- 새 입력: Curry·Klay·Draymond·Wiseman; Hutchison 경로 조건; 7/14 양자산.
- 현재 가용 비교: Franz Wagner, Moses Moody, Davion Mitchell. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: 7번은 큰 윙의 연결 역할을 먼저 확보하고 14번에서 외곽 자원을 비교한다. Moody·Mitchell을 더 먼저 쓰는 반대 경로도 유지.
- 비용/반대: Klay 가용성·Hutchison의 실제 가치·트레이드 시장 미확정. Franz의 후대 활약을 수입하지 않는다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/golden-state-warriors). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 8. TOR — Josh Giddey

- 새 입력: Barnes가 앞서 사라짐; Powell 잔류·Trent/Hood 자동 유입 금지; Lowry FA.
- 현재 가용 비교: Josh Giddey, Moses Moody, Alperen Sengun. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Giddey의 대형 패싱을 FVV/Powell 및 포워드 코어와 연결하는 성장안. Moody의 슈팅과 Sengun의 빅 기술을 비교.
- 비용/반대: Lowry 이탈이나 정해진 보상을 먼저 채택하지 않는다. 신인 슈팅·볼 기회가 비용이다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/toronto-raptors). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 9. NOP — Moses Moody

- 새 입력: Zion/Ingram; Killian Hayes13, Kira 없음; Lonzo/Hart FA; 원소유9.
- 현재 가용 비교: Moses Moody, James Bouknight, Chris Duarte. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Moody의 무볼 슛과 윙 길이를 우선해 주축의 공간을 보강한다. Bouknight의 자가 득점, Duarte의 즉시성은 대안.
- 비용/반대: 9번을 유지하는 조건부 사건. Memphis와의 실제10/17 거래는 바뀐9/17 및 급여/자산 대가를 따로 판정한다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/new-orleans-pelicans). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 10. CHI — Chris Duarte

- 새 입력: P·LaMelo4·LaVine·Coby·Carter, G1A/Caruso 후속 예산.
- 현재 가용 비교: Chris Duarte, Ziaire Williams, Alperen Sengun. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Moody가9번에서 사라지면 G3의 다음 후보 Duarte. Ziaire 성장 시간과 Sengun의 빅 중복보다 기존 코어 옆 외곽 기여를 우선.
- 비용/반대: 1997년생 신인의 시간표는 Moody와 다르다. 첫해 SF14분은 산술 배정일 뿐 가용성/수비 검증이 아니다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/chicago-bulls). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 11. SAC — Davion Mitchell

- 새 입력: Fox·Haliburton·Hield 조건; 실제 지명보다2자리 뒤.
- 현재 가용 비교: Davion Mitchell, Ziaire Williams, Alperen Sengun. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Franz는 사라졌고 Mitchell은 남았다. 실제 구단 선택과 가드 수비 보강을 유지할 제안. Ziaire/Sengun의 전방 크기도 비교.
- 비용/반대: 가드 중복을 무시하지 않는다. Haliburton 후대 거래를 자동 유지하지 않는다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/sacramento-kings). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 12. WAS — Corey Kispert

- 새 입력: Trent·Brown 잔류, Hutchison 없음; Gafford; Beal/Westbrook 거래 전.
- 현재 가용 비교: Corey Kispert, Ziaire Williams, James Bouknight. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: Kispert의 윙 슈팅을 기준으로 Ziaire의 성장과 Bouknight의 창출을 비교. Trent가 있어도 크기/무볼 역할의 차이를 남긴다.
- 비용/반대: Westbrook/Trent 재계약·거래 결정이 달라지면 이 수요도 재개방. 센터 없는 팀으로 쓰지 않는다.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/washington-wizards). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 13. SAS — Joshua Primo

- 새 입력: Vassell·Murray·White·Keldon 기준; DeRozan 시장 미확정.
- 현재 가용 비교: Joshua Primo, Ziaire Williams, Alperen Sengun. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: 실제12번에서 선택한 Primo가13번에 남는 조건을 우선. Ziaire·Sengun이 남았다는 점도 다시 비교한다.
- 비용/반대: 나이만으로 성공을 보증하지 않는다. 후대 사건이나 경기력은2021 선택 근거에 사용하지 않는다.
- [공개 기준선](https://www.nba.com/watch/video/12-josh-primo-announcement-not-at-draft). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

### 14. GSW — James Bouknight

- 새 입력: 7번 선택 뒤 둘째 자산14; Moody는 다른 구단.
- 현재 가용 비교: James Bouknight, Ziaire Williams, Alperen Sengun. 전체 비교 후보와 선행 소진 후보는 JSON에 기록했다.
- 판단: 7번 Franz와 결합해 Duarte가 남으면 즉시 외곽안, 사라졌으면 Bouknight의 추가 득점안. Ziaire·Sengun은 기능 중복/개발 비용을 비교.
- 비용/반대: 실제 Kuminga7/Moody14 동시 보존 없음. 새 쌍의 계약 분·성적과 원래 선수의 하류 행선지는 미완료.
- [공개 기준선](https://www.nba.com/draft/2021/team-profiles/golden-state-warriors). 이 링크는 새 선택이나 비공개 head-to-head를 입증하지 않는다.

## 역사적 운영 주체와 자료 경계

아래는 공개된 당시 담당자 참고이며 바뀐 성적 아래 임명·계약이 이미 모두 선택됐다는 뜻은 아니다. 특히 Orlando·New Orleans·Washington의2021 새 감독 선임은 별도 사건 조건이다. 감독 이름을 근거로 공개되지 않은 선호·대사·사적 감정을 만들지 않는다. 개인 의료자료와 비공개 워크아웃 결과는 확보하지 않았고 null이다. 동명이거나 같은 대학/팀 이력만으로 건강 승인을 추정하지 않는다.

| 구단 | 운영 담당 참고 | 감독 참고 | 근거 |
|---|---|---|---|
| CHA | Mitch Kupchak | James Borrego | [공개 참고](https://fr.wikipedia.org/wiki/Saison_2021-2022_des_Hornets_de_Charlotte) |
| HOU | Rafael Stone | Stephen Silas | [공개 참고](https://www.nba.com/draft/2021/team-profiles/houston-rockets) |
| ORL | Jeff Weltman | Jamahl Mosley | [공개 참고](https://sports.ksl.com/nba/orlando-magic-finalize-hiring-of-new-coach-jamahl-mosley/463206) |
| OKC | Sam Presti | Mark Daigneault | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_Oklahoma_City_Thunder_season) |
| DET | Troy Weaver | Dwane Casey | [공개 참고](https://fr.wikipedia.org/wiki/Saison_2021-2022_des_Pistons_de_D%C3%A9troit) |
| CLE | Koby Altman | J.B. Bickerstaff | [공개 참고](https://www.nba.com/draft/2021/team-profiles/cleveland-cavaliers) |
| GSW | Bob Myers | Steve Kerr | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_Golden_State_Warriors_season) |
| TOR | Masai Ujiri / Bobby Webster | Nick Nurse | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_Toronto_Raptors_season) |
| NOP | Trajan Langdon | Willie Green | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_New_Orleans_Pelicans_season) |
| CHI | Arturas Karnisovas / Marc Eversley | Billy Donovan | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_Chicago_Bulls_season) |
| SAC | Monte McNair | Luke Walton | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_Sacramento_Kings_season) |
| WAS | Tommy Sheppard | Wes Unseld Jr. | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_Washington_Wizards_season) |
| SAS | Brian Wright | Gregg Popovich | [공개 참고](https://en.wikipedia.org/wiki/2021%E2%80%9322_San_Antonio_Spurs_season) |

단일 구단 소개에 후기의 지명 행이 추가된 페이지가 있다. 대학/NBL/G League 스카우팅과 당시 지명 사실만 사용했으며 이후 NBA 수상·계약·사적 사건을 선택 근거로 쓰지 않았다. SAS 구단 프로필은 팀 본문이 비었고 공지 본문도 회수되지 않아, 별도 NBA 발표 캡션과 Primo 프로필을 사용했다. 전체 구단 비공개 평가 검증 완료로 표시하지 않는다.

## 하류 경계

1. **15~60의46픽은 미판정**이다. 원소유 순서는 기존 M에서 그대로 이어지며 전부 실제 선수로 자동 채우지 않는다.
2. DB1에서는 Indiana의 실제 Duarte가 사라져15번부터 재비교해야 한다. 추적 후보 Ziaire·Sengun·Keon·Trey Murphy를 삭제하지 않고 다음 보드에 남겼다. 이 목록은 드래프트 전체 지원자 명단이 아니다.
3. Boston16→OKC의 여름 거래, NOP/MEM9·17 조건과 후반 소유권을 선행 판정한다. 거래 대가를 삭제한 채 원래 선수만 다른 팀에 보내지 않는다.
4. **Chicago39는 아직 Edwards로 배정하지 않는다.** 앞선38픽과2라운드 권리를 확인한 뒤 G3 네 후보를 적용한다.
5. DB1에서 Duarte가 들어가도 G3의 건강한 날 SF14분 치환은 산술 제안이다. 실제 정규시즌 출전수·전술·지표·수상을 보증하지 않는다.

## 검증

네 안×14픽=56행, 매 선택에서 가용 비교 최소3명·중복0·기존MIN7 권리 연결·15명 자리와 동일10순위 예산·센터 대안의 분 재설계 표지·미확정 경계를 검사했다. 신규5개 unittest와 JSON 재현을 수행한다. 자체검토 `NOT_INDEPENDENT`이며 전체 드래프트/시즌/독립 검수 완료가 아니다.

`PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 CLOSED, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. 남은 큰 작업6개.
