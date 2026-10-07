# Carter2021 연장: 기존 CX1–4의 계약 구현 후보

`INDEPENDENTLY_REVIEWED_FOUR_EXISTING_ALTERNATIVES_CONSENSUAL_LEGAL_FORM_CANDIDATES`. M1/A 성장 코어를 보존하는 기존 비교안입니다. CX1 권고는 선택·합의가 아니며 세 연장안과 무연장 RFA안 중 어떤 것도 정본화하지 않았습니다.

## 기존 금액과 구체 법적 형태

|안|2022–23|2023–24|2024–25|2025–26|4년합계|매년감액|
|---|---:|---:|---:|---:|---:|---:|
|CX1|14,150,000|13,050,000|11,950,000|10,850,000|50,000,000|1,100,000|
|CX2|11,320,000|10,440,000|9,560,000|8,680,000|40,000,000|880,000|
|CX3|16,980,000|15,660,000|14,340,000|13,020,000|60,000,000|1,320,000|
|CX4|미선택|미선택|미선택|미선택|2022 RFA|무연장|

3개 안은4새시즌·기존마지막2021–22와 총5시즌이며, 선수·Chicago의 조건부 동의를 전제로 표의 Regular Salary 전액을 lack-of-skill 및 injury/illness 표준 CBA 보호조건 아래 보장하는 제안입니다. 추가 signing/performance/promotional/loan/buyout bonus, 새 trade kicker, 옵션·ETO는 넣지 않는 유한 구현입니다. 이는 사적 계약의 실제조건을 인증하는 것이 아닙니다. CX2의 할인 수락은 자동 충성심 사실이 아닙니다.

## 기한·급여·QO

[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) VII7b(PDF245–246), VII5c3(PDF219), IX1(PDF299)을 직접 대조했습니다. 연장 제안 시각은2021-10-15 12:00 ET이며 허용창은Aug6 12:01 ET부터Oct18 18:00 ET까지입니다. 말단은 [NBA 공식2021 캘린더](https://pr.nba.com/2021-22-nba-schedule-75th-anniversary-season/)의Oct19 개막과 CBA의 전날 규칙으로 구했습니다. 실제접수일·동의는 null입니다.

매년감액은 첫 연장년 급여의8% 이내이고 최대첫해16.98m도2022 cap25%인30.91375m보다 작습니다. 기존2021–22 급여6,920,027은 연장 서명으로 올리거나 줄이지 않습니다. 법정 minimum/max 자동조정과 향후 적용 규칙은 보존하며2025–26 실제행정·새 CBA 전체 검문으로 승격하지 않습니다. 새 MLE 사용/하드캡 발동도 이 연장으로 자동추론하지 않습니다.

연장안이 실제 구현된 경우2022–23은 live contract여서2022 FAhold/QO/RFA가 새로 생기지 않습니다. 무연장CX4만2022-06-30 만료 후 QO·시장·offer sheet·starter test로 연결되며 그 계산은 별도 RFA/QO 가족에 맡깁니다. 무연장을 미래급여0이나 권리 renounce로 바꾸지 않습니다.

## 거래 매칭과 원 보너스 권리

VII8f(PDF255)의 일반6개월 연장 거래금지는 VII7a에 대한 조항입니다. 이번 VII7b rookie 연장에 그것을 자동 적용하지 않습니다. 다만 VII8g(PDF256)에 따라2022-07-01 전에는 수취 팀의 급여 참조가 원 마지막 해+4새년의 평균이 됩니다. 기본급만의 참조는 아래와 같고, 실제 trade·양측 매칭 전체 PASS가 아닙니다.

|안|Chicago 송출 기본급 참조|수취 기본급 poison-pill 참조|
|---|---:|---:|
|CX1|6,920,027|11,384,005.4|
|CX2|6,920,027|9,384,005.4|
|CX3|6,920,027|13,384,005.4|

원 rookie 계약의 미지 trade bonus를 부재로 인증하지 않습니다. 존재하면서 아직 미지급이면 XXIV2a(v)(PDF399–400)가 허용한 같은 원조건의 대체 Exhibit4로 extended term만 bonus 적용에서 제외하는 제안입니다. 원기간의 권리는 보존합니다. 그 원기간 fullannual15% 넓은 상한은1,038,004.05이며 실제 earned·allocation·waiver는 null입니다. 가상 거래가 있다면 그 비용을 규칙대로 더해야 하므로 표의 기본급만으로 매칭을 인증하지 않습니다. bonus의 합의 면제를 별도로 택하는 거래에는 VII7d3의 후속 연장/재협상6개월 하한이 다시 적용됩니다.

2022-07-01 이후 poison-pill이 끝나도 거래·상대팀 여유·접수는 자동완료가 아닙니다. 본 제안의 extended-term kicker0은 허용된 상호합의 조건의 후보이고 원현실 사적조항0 인증이 아닙니다. [NBA의 원 Carter 기사](https://www.nba.com/news/orlando-magic-sign-wendell-carter-jr-to-contract-extension)는 역사적 맥락만 제공하며 Chicago 수락을 상속하지 않습니다.

## 검문 범위

고정8repo+SELF/current core producer, 새official2raw·재사용2021moratorium과Carter rookie row·CBA16쪽 지문을 연결했습니다. source-schedule 의미반전, 창밖날짜, 기존bonus소거, 권위승격을 실제 negative controls로 검사합니다. 국소 계약형태와 기존 스케줄 검문이며 전체비용·거래 실행·macro3·원장 승격0입니다.

[JSON](CARTER_2021_EXTENSION_CANDIDATE_FAMILY_2026_10_07.json) · [전체로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)

|번호|묶음|상태|
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|S2완료|
|3|2021–23 거래·계약|기존Carter4안 법적형태 후보,중요선택 미완료|
|4|장기 커리어|후속설계|
|5|결말·전체 구조|전체기능표 미완료|
|6|집필규격·Context Pack|현행 누적 등록기 참조·Pack0|
|7|통합·독립·작가승인|최종게이트 CLOSED|

미완료 큰 묶음 **5**. `v0.30 PARTIAL`/게이트`CLOSED`/원고0.
