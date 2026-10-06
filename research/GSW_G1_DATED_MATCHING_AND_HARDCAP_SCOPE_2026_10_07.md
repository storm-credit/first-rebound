# GSW G1 날짜별 matching·하드캡 범위 검문

**G1 미선택 후보 / 양팀 공개입력 범위 matching 증인 / 전체 하드캡 HOLD / ROOT_REVIEW_PENDING**.
[원 후보](../simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.md), [재현 입력](GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.json), [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md).

## 새 원자료와 원계약 입력

원Warriors 공식 guide의 2019 S&T/Spellman 영입과2020 Wiggins 완료 사건을 기존 SHA로 연결했다. 구단 guide는 개별 급여 금액을 제시하지 않아 실제 부족한 원계약 숫자만 공개 작성자의 자체 표에서 회수했다. [Wiggins](https://www.salaryswish.com/players/andrew-wiggins) 2019–20 nominal27,504,630, [Russell](https://www.salaryswish.com/players/dangelo-russell)27,285,000, [Spellman](https://www.salaryswish.com/players/omari-spellman)1,897,800이다. 세 표의 해당시즌 likely/unlikely는0이며 이 공개 계약군을 보존하는 후보 범위다. 현대 선수 상태·후대 커리어·league private memo 인증은 가져오지 않았다.

SalarySwish 거래요약의 원Evans0/signingrights 표시는 전체 급여 증인으로 채택하지 않았다. 각 계약표를 따로 읽었으며 실제 Evans/Chicago22 Hutchison 금액의 대체복사0이다. ESPN salary 본문 요청은403으로 실패하여 근거0이다. 새 원자료는 계약표3+cap표1 rawHTML이며 원문/SHA/추출방식은 JSON에 있다.

## 표 정밀도와 전범위

[NBA2018 표](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) #28 두번째시즌 표시는1,604.9($000s)다. 이를 정확원장 값이나 새 계약%로 고정하지 않고, 그 공개 magnitude보다 훨씬 넓은 scale **$1m–$2m** 외부입력 envelope로 계산했다. 모든80–120%와 VIII1(d)의 current-year tradebonus 상한을 포함해 H outgoing하한800,000 / incoming salary+unlikely상한2,400,000이다. 향후 옵션으로 bonus기초가 늘어도 이번 current120% 상한을 넘을 수 없다. 정확H salary·%·bonus·옵션은null이다.

[2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF64–65 II7(f)에 따라 Russell의 현재 bonus양수여유는 max(0,max(25%cap,105%prior)-current)=0이다. Wiggins도 prior25,467,250×105%=26,740,612.5와25%cap27,285,000보다 current27,504,630이 커서 bonus양수여유0이다. 기존8% 인상 급여를 줄이거나 bonus가 없다는 비공개 부재증명을 요구한 것이 아니다. Spellman은 이미2019-07-08 최초 계약양도를 거쳤으므로 XXIV2(a)에 따른 원contract bonus를 다시 지급하는 가정을 넣지 않는다. VII3(b)로 current protectedyear를 건너뛰어 미래에만 bonus를 밀어놓을 수도 없다.

## 양팀 동시 매칭 증인

VII6(j)의125%+100,000은 납세/비납세/아래cap 구간 모두에서 사용할 수 있는 충분한 한도다. GSW는 Russell+Spellman+Hutchison을 동시 aggregate하며2개월 제한은 이미 경과했다. July7/8부터February6까지214/213일이다. S&T 최초거래의 BKN BYC를 이번GSW outgoing에 다시 적용하지 않는다. January10 이후 current base는 matching에서 전액 보호로 계산된다.

| 팀 | outgoing 하한/고정 | incoming 상한 | 충분 한도 | 최소 여유 |
|---|---:|---:|---:|---:|
|GSW|29,982,800|27,504,630|37,578,500|**10,073,870**|
|MIN|27,504,630|31,582,800|34,480,787.5|**2,897,987.5**|

이것은 선언된 공개 보존 계약군·넓은 신인scale입력에서의 모든 허용H%/bonus 매칭 증인이다. 실제 Minnesota 가치평가/수락·거래 전체·H 행선지·정확 계약을 선택하거나 인증한 것은 아니다. bonus면제 선택q0이며 새 금융 선택0이다. 초과 extension의6개월 제한과 일반 renegotiation eligibility를 구분했고 실제 후속 extension은null이다.

## 하드캡에서 실제 닫히는 것과 남는 것

VII8(e)와6(m)(3)의 apron은 원2019-07-07 S&T 이후 해당capyear의 모든 상태에 적용된다. 공개 cap표의2019 apron은138,928,000이다. **B(t)=H를 제외한 모든 apron-adjusted 비용**으로 두면 원G1이전 전체범위 충분조건은 B(t)≤136,528,000이다. A-G 조정·deadcost·incomingbonus·원거래 중간상태가 B(t)에 포함되어야 한다.

G1 원자거래 자체는 다른 비용을 보존하고 이전상태가 적법하다면 **apron delta≤−2,478,170**이다. 이 거래는 새로운 하드캡 초과를 만들지 않는다. 원Evans의 급여나 선수 수락을 이식하는 증명이 아니다. 이전모든B(t)의 실제 공개합계/구간은 아직없고, 거래후 다른 서명/방출/10일계약과COVID변경capyear말일까지 전체 비용도 미인증이다. 따라서 이 국소 비증가 관계로 whole hardcap을PASS시키지 않는다. annualcashlimit/지급 tradebonus cash도 별도 미인증이다.

다음 입력은 반복된 새 private receipt 요구가 아니라, guide가 보여준 유한 사건의 **GSW 나머지 비용구성·보호/성과 상단·날짜별 A-G 조정표**다. 각 후보의 수락·정확 자산 선택은 여전히 별도다. 현재 두GSW L2의8명·240분 객체 변경0이다.

재현: `python tools/build_gsw_g1_matching_hardcap_scope.py --check`.
상위 원후보를 source까지 전재구성 검문한 뒤 새 숫자를 계산한다. Antigravity/NotebookLM/Claude 이번범위NOT_RUN·독립PENDING이다. 중앙·원장·staging0.

## 7행 진행표 — 작성 시점 한정 복구

|번호|큰 묶음|현황|
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|법적11/12·F4/5·A0/3·K0/4; 전체시즌 미완|
|3|2021–23 거래·계약|승인 방향 반영·정확 실행 미완|
|4|장기 커리어|선행 시즌 확정 대기|
|5|결말·전체 구조|골격 보존·전체 회차기능표 미완|
|6|집필 규격·Context Pack|E1/E2 기능2·A01잔여34·전체780 중 미배정778·실제Pack0|
|7|통합·독립·작가 승인|전체 게이트 미완|

**미완료 큰 묶음6 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.** 이번 양팀 수식은 전체 금융/등록/정본 선택 완료가 아니다.
