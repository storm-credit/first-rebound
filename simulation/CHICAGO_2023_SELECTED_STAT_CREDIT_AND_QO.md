# Chicago2023 선택 가상 통계와 Coby ordinary QO 입력

**STAT23_A는 기존 시즌 위임으로 root가 명시 선택한 가상 credit 정책이다.** 원H21/H22 lowerbound/OTnull 기록과 실제NBA 미인증 필드는 그대로 보존했다. 새 독립검문은 아직 미완료다.

| RSC 정규연도 | GP credit | GS credit | 분 | 범위 |
|---|---:|---:|---:|---|
|3 ·2021–22|58|0|1044|원82개 선택결과의 양수 참여 credit|
|4 ·2022–23|조건부82|0|1476|H22 82날짜 참여 정책을 모두 실행할 때의 projection|

두 시즌 가상 OT0·추가분0·Coby 벤치 GS0를 명시 선택했다. H22의 참여 정책 선택과 모든 미래 참여의 실행·관측은 별개다. **현재2022–23 승자0/82를 완료로 표시하지 않는다.** 이 소비자는 점수·승자·실제박스/임상증명·새가격을 선택하지 않는다.

## 선발과 clock 표현

원H21 M1은 unordered 용량 증인이고 기존 paired clock0는 공식 GS 인증이 아니다. 새 nomination은 LaMelo/LaVine/주인공/Markkanen/Carter5다. 원CHI NORMAL/COBY_OUT의 동일 선수·포지션 총초에서 이 선발로 시작 가능한 공유 증인을 검문한다. 기존 paired 시간배열/선수분/승패는 덮어쓰지 않는다. H22는 실제 선택된 fictional starters5와 ordered 첫블록이 일치하며 Coby가 없다. source coverage를 실제NBA 선발로 뒤집지 않는다.

## CBA OR와 QO

Starter는 GS4≥41 또는 MIN4≥2000 또는 GS3+GS4≥82 또는 MIN3+MIN4≥4000이다. 선택1044/1476·GS0은 합2520/평균1260, 네 OR 모두false다. P2022의2624 하한은 하나의 OR를 직접 충족했지만 Coby1476 하한 자체만으로는 비선발을 증명하지 않는다. 추가524분·GS41 등 변경 시 즉시 재평가한다.

원2019 CHI#7의80–120% base/likely/unlikely 성분 가족과 원조건Γ를 보존한다. 3→4년차×1.270,4년차→자기QO×1.341. 비선발은 자기 전체offer와2019#15 120% base-only offer 중 적법한 작은 패키지다. 원likely/unlikely를 삭제하거나 보너스를 항목별로 임의 상쇄하지 않는다.

**비선발 충분비용 상단7,744,602달러**, 자기offer 상단9,942,120달러와 차2,197,518달러. 이것은 미선택 가격 범위 입력이며 정확UPC/법정반올림/실제수락을 인증하지 않는다. ordinaryQO 발행·MaximumQO·FAhold·FirstRefusal·새 UPC는 별도다.

[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) XI1(c)/4 원쪽 및 [2023 CBA](https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf) XI4(c)/XLII2를 직접 읽었다. June29 발행은2017법, July1 이후는2023법. 발행창 시작의2023 Season 말단은 typed 미입력이다. October1,2023은 일요일이므로 일반기한 projection은 Monday October2이며 원Oct1 최소/명목창을 정확 종료일로 확대하지 않는다. 실제발행/수락/연장/철회는 미선택이다.

## 재현·남은 작업

`python -B -X utf8 tools/build_chicago_2023_selected_stat_credit_and_qo.py --check --self-test`. 원JSON 독립 물리 파싱·rawPDF/쪽 SHA·2019표 원분수 함수를 소비한다. 조상 전체 생성기는 실행하지 않는다. 반환 OT추가524/GS41/Γ삭제/Oct1 종말오독/GP82실증승격을 거부하는 작성자 검문이며 독립감리로 세지 않는다.

다음은 FY23 날짜 결과82개, 선택2023 Season 말단 및 ordinaryQO 발행/서명 장부, 별도 LaMelo extension 함수다. 실제NBA 박스나 비공개 접수증을 새 완료 gate로 추가하지 않는다.

[원 정적 포트](../research/CHICAGO_2023_STAT_QO_AND_CBA_FINITE_PORTS_2026_10_08.md) · [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) · [누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md)

| 묶음 | 상태 |
|---|---|
|1 드래프트 연쇄|완료|
|2 Chicago2020–21|완료|
|3 2021–23|통계credit·QO 입력 선택, FY23 결과/계약 미완료|
|4 장기커리어|진행|
|5 전체구조|현행 기능등록기 참조|
|6 규격·Context Pack|현행 source등록기 참조·Pack0|
|7 통합·작가승인|미완료|

미완료 큰묶음5/6번까지4 · v0.30 PARTIAL · CLOSED · 원고0.
