# GSW G1 날짜별 나머지 apron 비용 입력

상태: **공개 비용 구간·잔여 임계값 검문 / G1 미선택 / 전체 하드캡 HOLD**. 기준 main `47e5c80` 고정. [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md), [입력](GSW_G1_REMAINING_APRON_COSTS_2026_10_07.json), [기존 matching 범위](GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.md).

## 새로 확보한 범위

SalarySwish 자체 계약표 신규13개와 기존 McKinnie 원캐시를 읽고 당시2019–20 행을 유형별로 연결했다. 이는 공개 편집 계약 입력이며 리그 계약원장 인증은 아니다. Looney 표시 기본급4,464,286과 후대/보도15m 총액의 차액을 임의로 해소하지 않는다. 날짜·옵션·보너스가 대체세계 작가확정이 된 것은 아니다.

[2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) I1(cc)/(ggg),VII6(m)(3),12(f)(2)(ii)를 직접 읽었다. 독점협상권이 살아 있는 #41 Paschall/#39 Smailagic은 Free Agent가 아닌 Draft Rookie이므로 자유계약0/1년차의 2년차최저 상향을 일괄 적용하지 않는다. 현재공개금액은898,310씩이다. Burks/GRIII는 일년최저급여 환급 규칙으로 팀Salary1,620,564씩이며 선수 현금2,320,044/1,882,867과 다르다. Chriss는 FA 원계약의 방출 비용을 자동0으로 하지 않고 전체이전cap1,620,564를 상단에 남긴다.

## 실제 비용 구간

B는 Hutchison을 제외한 공개 연결 비용이다. X는 표/날짜 연결만으로 닫히지 않은 명명된 비용 잔여다. X=0이나 실제 계약수락을 선택하지 않았다.

| 날짜·상태 | B 공개 구간 | H 상단 | 충분한 X 상단 |
|---|---:|---:|---:|
| 2019-07-08 after named guide transactions | 92,386,069–104,793,654 | 2,400,000 | 31,734,346 |
| 2020-02-06 before both named trades | 133,671,476–135,292,040 | 2,400,000 | 1,235,960 |
| 2020-02-06 after G1 before PHI | 131,993,306–133,613,870 | 0 | 5,314,130 |
| 2020-02-06 after PHI before G1 | 130,430,348–132,050,912 | 2,400,000 | 4,477,088 |
| 2020-02-06 after both named trades | 128,752,178–130,372,742 | 0 | 8,555,258 |

7/8은 guide와 공개 계약표의 Poole/Paschall/Smailagic/GRIII 서명 날짜 차이를 양쪽을 덮는0~현재표금액으로 처리한다. Livingston의 표기 waiver7/8과 guide7/10 차이도666,667~7,692,308으로 보존한다. 아직 미서명 Klay/Looney UFA hold는 apron 제외이며 살아 있는 RFA 제안은 X에 남긴다. 두 자료 날짜를 숨겨 동일 실행일로 인증하지 않는다.

2/6는 Wiggins 원자거래와 같은날 PHI Burks/GRIII 거래의 양순서를 따로 계산했다. 정확 당일 접수순서는null이며 미래2/7 표준계약은 끌어오지 않는다. 표의 각 충분조건은 해당 상태의 X 상단이 지원될 때만 유효하고 모든상태X동일/전체시즌 비용을 인증하지 않는다.

## 구체 남은 입력과 실패 제어

7/8의 Cook/Bell 살아 있는 qualifying/first-refusal 제안, Washburn 당시계약유형, 기타 bonus/grievance/보호·지급액을 X로 이름 붙였다. 2/6의 camp/해제 잔여와 Looney 총액차이도 X이며 미확인=0 가정은 없다. 공개 상단 또는 허용 계약family 전체증인으로 각 임계값을 닫으면 충분하고 비공개 영수증의 회수를 영구필수 요건으로 만들지 않는다.

Washburn 공개 계약페이지에는 당시 행이 없고 잘못된 Robinson slug는 Player not found였다. 공식Washburn release 원문 다운로드는403이라 cached본문 인증으로 채택하지 않았다. 현대 선수상태를 과거 계약으로 대입하지 않았다. raw14(신규13+재사용1)/SHA·CBA14쪽·guide433쪽 지문은JSON에 있고 원PDF지문은 불변이다.

G1 선택·정확H계약비율·옵션·거래수락·전체금융/명단/법적PASS·중앙원장 승격·기존L2 변경0. 이 한정 검문에서 Antigravity/NotebookLM/Claude는 NOT_RUN이며 독립 검문은 pending이다.

## 전체7행 진행표 (PR438/E6 입력 시점)

| 번호 | 범위 | 상태 |
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|법적11/12·F4/5·A0/3·K0/4, 시즌 미확정|
|3|2021–23 거래·계약|승인방향 반영, 정확 실행 미완|
|4|장기 커리어|선행 시즌 종료 대기|
|5|결말·전체 구조|골격 완료, 전체 기능표 미완|
|6|집필규격·Context Pack|A01기능6/잔여30, 전체780 중 미배정774, 실제Pack0|
|7|통합·독립·작가 승인|미완|

미완료 큰묶음 **6** · **v0.30 PARTIAL** · 설계/원고 **CLOSED** · 원고 **0**. 현행로드맵의 이후진전은 이 고정 입력시점 표보다 우선한다.
