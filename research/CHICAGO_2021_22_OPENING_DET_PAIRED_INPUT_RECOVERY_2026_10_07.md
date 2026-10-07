# Chicago 2021–22 첫 Detroit 경기 입력 복구

`INDEPENDENTLY_REVIEWED_STATIC_RECOVERY_NOT_EXECUTION`

## 완료한 연결

첫 대면은 **0022100004 / 2021-10-20 / DET 홈·CHI 원정**이다. 같은 날짜는 조건부 일정 가설이며 건강·승패 선택이 아니다. 현행 독립 검문된 [M1 carrier](../simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.md)의 NORMAL과 기존 [G14](../simulation/CHICAGO_2021_22_PAIRED_REVIEW.md)의 Detroit 조합을 직접 대조했다.

|입력|CHI M1 NORMAL|DET G14 조건부|
|---|---:|---:|
|정규 팀분|240|240|
|순서없는 5인 블록|11|9|
|양수 선수|10|10|
|작업 등록 명단|15 STD·2 TW 조건|전체 비용·명단 미완료|
|날짜별 상태·승패 선택|0|0|

두 팀 480분은 각각의 용량 증인 합계이며 공동 교체 순서·공격권·스코어 증인이 아니다. 기존 Chicago G14의 Markkanen28/Caruso22는 사용하지 않았다. 현행 M1은 Mark32/Caruso18/주인공32다. 실제 연장전·원래 부상·원역사 88:94를 새 사건으로 가져오지 않았다.

Detroit은 Kira24·Joseph24·Suggs24·Josh Jackson24·Diallo20·Patrick28·Grant30·Olynyk18·Stewart24·Plumlee24다. 9개 블록의 중복 없는 5명, 포지션 자격·각48분·창조자·총240분을 원 입력에서 다시 계산했다.

## 정본과 후보를 분리

**작가확정:** 2020 Patrick Detroit7, Kira Detroit16, Stewart Detroit19. **후보:** 2021 DB1 Suggs Detroit5, Aldama37, Livers38, Garza53. Suggs는 2020 착지 선수가 아니다. 2021 보드는 권리 비교안이며 선수별 새 NBA 계약·Tender를 자동 생성하지 않는다. 특히 Aldama 권리를 표준계약 한 자리로 몰래 추가하지 않는다.

원역사 [Charlotte Plumlee 거래](https://www.nba.com/hornets/press-releases/charlotte-hornets-acquire-mason-plumlee-and-draft-rights-jt-thor)는 Plumlee+37 Thor ↔57 Koprivica다. DB1 Thor Utah30 / Aldama Detroit37 / Koprivica New York57과 충돌하므로 복사할 수 없다. G14의 Plumlee 잔류는 비교 조건이며 승인된 거래 생략으로 승격하지 않는다. Charlotte 센터·반대급부도 새로 지정하지 않았다.

## 선행 완료 시즌과 연결

[선택된 2020–21 dated roster](../simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.md)의 마지막 Detroit 바인딩은 2021-05-16, STD15·TW2다. Patrick/Kira/Stewart/Plumlee가 보존되고 Diallo 3/13 OKC→DET, Joseph 3/25 SAC→DET는 그 완료된 작업 사건에서 연결된다. 승인된 T1/T2/T4/F4/F5/C2 사건에 Detroit 신규 선수 이동은 없음을 별도로 대조했다. Joseph와 Diallo를 무료 새 영입으로 재작성하지 않는다.

May16 명단 전체를 8월로 자동 연장하지 않는다. Frank Jackson·Saben Lee는 May TW에서 2021 새 표준계약 가족으로 옮겨야 하고, Ellington·Dennis Smith Jr.·Tyler Cook·Sirvydis의 종료/이탈과 남은 비용을 날짜별로 연결해야 한다. Cook은 Chicago 2021 TW 후보와 겹쳐 두 구단 등록으로 남길 수 없다. 이 연결은 macro2를 재개방하는 것이 아니라 다음 계약연도 사건 입력이다.

## 실제 남은 명단·비용

[G15AF](O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md)의 같은 나머지 사건을 조건으로 둔 표준 명단 수는 **16→17→16→15→16**이다. 개막 표준16은 15 상한을 넘는다. 기존 [G15BM](O15G15BM_DETROIT_OPENING_SLOT_TWO_NAMED_OPTIONS.md)에는 이미 두 실명 후보가 있다.

|후보|개막 자리|보존·파급|
|---|---|---|
|A: Garza 투웨이 유지|Garza 표준 전환 생략; STD15, Garza·Smith TW2|G14 양수10 전원과 Lyles 유지. Pickett은 별도 경로 필요. 다음 검문 우선 후보일 뿐 미선택.|
|B: Lyles 합의·서명 생략|STD15, Pickett·Smith TW2라는 후속 조건|G14 양수10 보존, 1월 Lyles 역할·2월 Bagley 거래를 다시 연결해야 함. 10월 방출을 8월 cap room으로 소급하지 않음.|

이 둘은 자리 산술이며 완전한 적법 계약 가족은 아니다. 원 Nets/Jordan 사건도 같은 당사자·계약이 보존될 때만 후속 조건으로 쓸 수 있다. 나중 투웨이 50초과 예외는 확인됐으나 개막 규칙과 적용시점을 섞지 않는다.

[G15AL](O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.md) 후보 장부는 cap112,414,000−명명 비용100,052,228=room12,361,772이고 Olynyk12,195,122 후 **166,650**만 남는다. 다른 공개 dead-money 원천의 차액203,571을 쓰면 **−36,921**이다. Plumlee 미거래 급여 후보8,137,500을 사용하며 거래된 표시 cap9,248,333을 가져오지 않는다. Lyles·Lee·Livers·Frank가 먼저 들어오는 순서도 여유를 바꾼다. 따라서 기존 숫자를 whole 비용 상단으로 인증하지 않았다.

[G15AR](O15G15AR_DETROIT_NAMED_EXIT_AND_ROSTER_CHARGE.md)의 Sekou/Okafor 급여 없는 이탈 표는 아직 수신팀·반대급부가 없는 후보다. 9/4 DeAndre Jordan 거래는 비용이 증가하는 후속 사건이며 8/6 급여 없는 이탈로 대체하지 못한다. 기존 문서의 비공개 리그 장부·실제 접수 요구를 새 필수 게이트로 가져오지 않았다. 다음 구현은 공개 근거의 비용 구간·권리 포기·합의 비용·실명 거래 가족으로 한 연속 경로를 구성하는 것이다.

## 생산성 입력과 다음 최소 단위

[G15B stress](../simulation/CHICAGO_2021_22_G15B_REVIEW.md)에는 개막 전 세 비교 선수로 만든 Suggs24분 FGA8.202–9.963 / FTA1.809–2.285 / TOV1.692–2.039 민감도가 이미 있다. 이를 새 예측 모형·신뢰구간으로 부르지 않는다. 원 FTA 예산을 억지로 고정하는 B14D 세 가지 HOLD도 보존한다. 원래 점수·FGA·FTA를 새 Detroit 팀 예산으로 선택하지 않았다.

다음 산출물은 **DET_OPENING_P0B_NAMED_OPERATING_FAMILY**다. 기존 A의 15+2와 실제 최소 active 지명, Aug6 Olynyk→Lee/Lyles/Frank→Joseph의 연속 비용 경로, 별도 미서명 Aldama/Livers/Garza 권리를 연결한다. 조건부 초안은 나머지58명 지명 확정이나 비공개 영수증을 기다릴 필요가 없다. 방향·비용 가족이 준비된 뒤 현행 M1과 상대 생산성/impact 방법을 연결한다. 이번 두 파일은 새 방향 선택·결과·#16 선택을 하지 않았다.

## 재현 범위

JSON의 정규화 source SHA27개를 실제 읽은 파일과 대조했고, 2020 승인3·2021 Detroit 후보4·9블록/포지션/480분·명단 두 후보·cap 차액을 직접 계산했다. 새 원문 수집0이다. 공식 [개막 gamebook](https://statsdmz.nba.com/pdfs/20211020/20211020_CHIDET_book.pdf)의 기존 저장 관측과 2차 급여표를 새 직접 원본문 회수로 세지 않는다. 정적 복구파일이므로 constructor 음성 검문은 만들지 않았고 독립 정적 원천·분·명단·비용 검문을 수용했다. 실행 검문이나 날짜별 상태 선택이 아니다. 기존 원천·중앙·게이트 변경0, macro2 재개방0.

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md) · [누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md)

|번호|묶음|상태|
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago 2020–21|S2 완료|
|3|2021–23 거래·계약|M1 82날짜 조건부 carrier 독립수용; 첫 DET 입력·명단·비용 경계 복구|
|4|장기 커리어|후속 시즌 입력 대기|
|5|결말·전체 구조|전체 기능표 미완료|
|6|집필 규격·Context Pack|현행 기능 등록기 참조·실제 Pack0|
|7|통합·독립·작가 승인|최종 CLOSED|

미완료 큰 묶음5. v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.
