# A11 주인공 첫 Finals·FY25 Chicago 서비스 입력

- 기준 main `38c09a44a7940760eebcd635629cc947fa5ea2dd`. 정적 입력·새 역할 권고이며 독립 검문 전이다.
- F26 목표는 root선택, 이 패킷의 이전결과·감독·건강·시리즈 실행 선택은0.

## 1. ‘첫’과 이전 시즌

원 CP2 A11 출구는 **MIN과 첫 파이널 패배 후보·구조적 결함 노출**다. 원 후보 문구 자체는 첫의 주체를 확정하지 않는다. [후행 root 선택](../canon/DELEGATED_A11_F26_FIRST_FINALS_LOSS_SELECTION_2026_10_08.json) `/selected_target`이 주인공의 첫 NBA Finals로 명명한다. Chicago프랜차이즈첫이 아니며 이전 국소 연습은 Finals 플레이가 아니다.

| 시즌 | 현재 근거 | 판정 |
|---|---|---|
| 2018–19 | [Chicago itself league lotteryseed4/own7, not anotherteam pickholder; exact22–24 unselected. NBABylaws7.02(a)(i) PDF85 supplies precedingSeason nonplayoff eligibility.](../simulation/CHICAGO_2019_COBY_WHITE_DRAFT_BOARD.md) | no-Finals 지원 |
| 2019–20 | [CHI LOTTERYseed7/7.5%/own4, NOT Eastern playoffseed7. OfficialNBA2020tiebreaker Note1: nonplayoff lotteryorigins vs playoff15–30. Exact21–22 staysHOLD.](../design/CHICAGO_2020_LOTTERY_DECISION_PACKET.md) | no-Finals 지원 |
| 2020–21 | [IND defeatsCHI on2021-05-20; EASTqualifiersBOS/IND.](../simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json) | no-Finals 지원 |
| 2021–22 | [PHI eliminatesCHI R1 4–3 on2022-04-30.](../simulation/NBA_2022_SELECTED_FULL_POSTSEASON.json) | no-Finals 지원 |
| 2022–23 | [MIL eliminatesCHI R1 4–0 on2023-04-21.](../simulation/NBA_2023_SELECTED_FULL_POSTSEASON.json) | no-Finals 지원 |
| 2023–24 | 현재선택결과없음 | 미해소 |
| 2024–25 | [CHI6/PHI3 R1setting and G1/G2 cost observations; no serieswinner/laterround result.](../simulation/A10_QUAL1_SELECTED_COST_WINDOW.json) | 미해소 |

**직접 탈락3+로터리 원소유 참가/공개 규칙 추론2, 미해소2.** 로터리7은 PO7시드와 다르다. 타팀 로터리픽 소유 역시 팀 미진출의 증거가 아니다. 두 승인 원문이 Chicago자체를 로터리 참가 원소유 팀으로 명명한 범위만 소비한다. 정확 승수는 계속HOLD다.

[NBABylaws §7.02(a)(i), PDF85](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf)의 로터리 미진출 정의와 [NBA2020 당시 Note1](https://pr.nba.com/2020-nba-draft-tiebreakers/)을 직접 읽었다. 2020 Note1은 nonplayoff 로터리 원소유팀과 PO15–30을 구분한다. 승인된 참가와 규칙의 연결 추론이며 실제CHI22–43이나 탈락경기를 새선택하지 않는다. [NBA2019 당시 자료](https://www.nba.com/news/draft-lottery-odds-order-decided-official-release)는 Chicago12.5% 맥락만 보조한다.

실제남은 이전결과는 **2023–24/2024–25**다. A10 QUAL1은 CHI6/PHI3 자격·두 비용창까지만 실행했고 serieswinner/laterround는 미정이다. Root가 유한 non-Finals endpoint를 선택·검문하면 첫조건을 연결할 수 있다. 전체82/30/17시즌이나 사적영수증을 새 필수로 만들지 않는다.

## 2. FY25 명명15의 원서비스

[원명명15](../simulation/CHICAGO_2025_NAMED15_CONTRACT_JOIN_2026_10_08.json)의 `/named15/i`, 계약pointer15·서비스pointer15를 직접resolve했다. carry5+새Bird3+기존RSC옵션2+minimum5=15STD/0TW. 원Γ/보호와같은claim 한 번을 보존한다.

| i | 선수 | FY25 Salary / 기본cash |
|---:|---|---|
| 0 | Lauri Markkanen | `38661750` / `38661750` |
| 1 | Alex Caruso | `19330875` / `19330875` |
| 2 | Wendell Carter Jr. | `10850000` / `10850000` |
| 3 | Protagonist | `27280000` / `27280000` |
| 4 | Zach LaVine | `45999660` / `45999660` |
| 5 | Coby White | `12000000` / `12000000` |
| 6 | Chris Duarte | `12000000` / `12000000` |
| 7 | Walker Kessler | `134977956/25 with original II6/CBA conformity` / `134977956/25 with original II6/CBA conformity` |
| 8 | LaMelo Ball | `LaMelo_HigherMax_legal_predicate ? 45550512 : 37958760` / `LaMelo_HigherMax_legal_predicate ? 45550512 : 37958760` |
| 9 | Jaime Jaquez Jr. | `6/5*S23(16,3) with original II6/CBA conformity` / `6/5*S23(16,3) with original II6/CBA conformity` |
| 10 | Thaddeus Young | `M25(2,Year1)` / `M25(10,Year1)` |
| 11 | Javonte Green | `M25(2,Year1)` / `M25(6,Year1)` |
| 12 | Joe Wieskamp | `M25(2,Year1)` / `M25(4,Year1)` |
| 13 | Denzel Valentine | `M25(2,Year1)` / `M25(9,Year1)` |
| 14 | Tomas Satoransky | `M25(2,Year1)` / `M25(9,Year1)` |

**회계 FY말은 NBASeason 서비스 종료가 아니다.** [2023 CBA I1(ooo), PDF34](https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf)는 훈련캠프부터 마지막 Finals 경기 직후까지 Season으로 정의한다. E26값은null이며 후속선택 d를 원2025–26 UPC서비스가 덮는 가족을 소비한다. June30을 자동서비스끝으로 치환하지 않는다.

FY26July7 새 P/Carter/Coby3·minimum5는 **2026–27 서비스**다. June2026 Finals에 UPC8/M26을 소급하지 않는다. 원2025–26 서비스완료 조건과 원지급·보호·기타채무는 유지된다.

비용은 원 `/salary_and_cash_join`·`/six_typed_cost_categories`6범주다. 옵션/minimum 전 base는 ordinary **204,081,045**, 적법HigherMax의 경우 **211,672,797**. LaMelo 수상자격은 미선택이다. normal/apron 기본 `B_LM+K25+J25+5*M25(2,1)`, cash는 선수별M25(10/6/4/9/9,1)전액을 별도 계수한다. 원 적법환급은 coveredSeason후이며 즉시현금0이 아니다.

R25N/R25A·FA/QO/FRN·N25/A25/D24·연간예외·floor/tax/cash는 typed unknown을 유지한다. 역할후보 추가UPC/Salary/cash Δ0은 **기존총비용0이 아니다**. whole상단null, 이전높은apron만으로 Bird/min자체를위법으로 판정하지 않는다. 원trigger/후속거래제약은 보존한다.

## 3. 새 FY25 감독·가용 권고

A10의24×120초 문법을 신규FY25 제안에 이용하되 과거가용/건강/효율은 자동이월하지 않는다. JSON은 sourcegrammar와정확patch관계 및 B32의24블록을 저장한다.

| 후보 | P | LaMelo | Duarte | Coby | 공통나머지 | 합계 |
|---|---:|---:|---:|---:|---|---:|
| A34 | 34 | 30 | 10 | 14 | LaVine30/Mark30/Carter28/Jaquez20/Kessler14/Caruso20/Young10 | 240 |
| **B32 권고** | **32** | **28** | **12** | **16** | 동일 | **240** |

B32는360–480초 SF P→Duarte,840–960초 PG LaMelo→Coby만 교체한다. 개인점유창을 양도하는 비용을 명명하며 분담의 성공·실점·승패를 지급하지 않는다. 선발은 LaMelo/LaVine/P/Mark/Carter.

양안 모두 양수11+0분 JavonteGreen/TomasSatoransky=가용·active13 후보, inactive는JoeWieskamp/DenzelValentine2. court5+otherdressed8을 구성한다. CBA XXIX1 PDF453의active12–15/bench8 문구는 **RegularSeason** 범위다. postseason별도 법정min13이라고 바꾸지 않는다. XXIX2(a)의총14–15는 진출팀 마지막경기까지 유지된다. 12active가 항상불법이라는 판정도 하지 않지만 court5+otherdressed7만으로bench8 충족을 주장하지 않는다.

두안 각각2880초, 유일5인·5포지션 각각2880초·총14400 playerseconds를 실제검산했다. **coachselection/healthselection=false**, 시즌GP/GS/분/QO·효율/BPM/상·OT/득점/결과null. B32는권고이며 root후속선택전행사0.

## 4. 다음유한인계

1. 이전두시즌의 no-Finals endpoint를 root선택·검문.
2. root가 B32/A34·가용13을 선택하면 현재CHI15서비스와 날짜시계 결합.
3. MIN FY25 명명계약·가용·6비용을 같은480분 시계로 결합. 원역사/옛시즌임상자동복사0.
4. F26 경로·패배와독립판단/도움/동료비용/영상전달 실행. 옛연습으로실제Finals출구를대체하지 않음.

## 실제검문과범위

current LF핀24개, 계약15/서비스15 pointer, ownership/Gamma/FYmarker15행, 역할2안48/240·13+2/유일5인, FY26신규8소급금지. NBABylaws PDF85–86/CBA34·453 raw/textSHA 직접대조. 정적2파일: constructor/변조0·조상자체검사반복0·새독립검문0. 웹본문관측과 providerHTMLraw인증구분. 부모generationpendingfalse이력rewrite0.

## 진행표

| 번호 | 묶음 | 상태 |
|---:|---|---|
| 1 | 2020 드래프트 연쇄 | 완료 |
| 2 | 2020–21 세계·시즌 | 완료 |
| 3 | 2021–23 계약·선택시즌 | 완료 |
| 4 | 장기 커리어·막 출구 | 진행 |
| 5 | G13 사건·기능·최종배치 | 미완료 |
| 6 | 집필규격·Context Pack | 미완료 |
| 7 | 통합·독립·최종승인 | CLOSED |

미완료큰묶음4 / 6번까지3. v0.30 PARTIAL·CLOSED·Pack0·원고0. 전체A11/G13/G14·후기주요좌표 완료0.
