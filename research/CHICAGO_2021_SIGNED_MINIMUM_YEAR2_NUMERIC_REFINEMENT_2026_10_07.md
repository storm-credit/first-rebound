# 2021서명 최소계약: 2022–23 Year2 공개 수치 정밀화

`PUBLIC_TABLE_NUMERIC_REFINEMENT_COMPLETE_LEGAL_ROUNDING_UNCERTIFIED`. 기존 승인 코어 파일은 수정하지 않았습니다. 공개 보고표의 다섯 숫자는 회수됐으며 NBA 공식 반올림 절차는 아직 인증하지 않습니다.

## 회수한 다섯 행

|선수|2022–23 YOS|ExC2017 Year2|2021–22 공개표 Year2($)|직접비율 floor..ceil($)|
|---|---:|---:|---:|---:|
|Green|3|1,600,520|1,815,677|1,815,676..1,815,677|
|Joe Wieskamp|1|1,378,242|1,563,518|1,563,518..1,563,519|
|Tony Bradley|5|1,795,015|2,036,318|2,036,317..2,036,318|
|Stanley Johnson|7|2,072,867|2,351,521|2,351,521..2,351,522|
|Denzel Valentine|6|1,933,941|2,193,920|2,193,919..2,193,920|

[SalarySwish 자체 역사표](https://www.salaryswish.com/minimum-salary-faq)는 `data-year=2022`에 붙은 **2021–22** 라벨과 `tbody#cba_2022`의 Year2 열을 직접 읽었습니다. 현재 페이지 갱신일은2026-07-10입니다. [당시 HoopsRumors 분석](https://www.hoopsrumors.com/2021/08/nba-minimum-salaries-for-2021-22.html)의 두 번째 표도 같은 다섯 값입니다(2021-08-05 게시). 이 표의 Experience는2021 첫 시즌 YOS이므로 다음 해 YOS보다1 작다는 점을 대조했습니다. 해당 기사는 NBA 법정표의 원문이 아닌 당시 저자의 분석이며 corroboration 역할만 가집니다.

## 법규와 수치의 구분

[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) II6a/d, PDF54–55(인쇄32–33)와 ExC PDF561(C-1)을 직접 읽었습니다. 계약 첫 시즌2021–22의 scale과 두 번째 해의 해당 YOS를 사용합니다. 2022 새 계약 Year1 표로 바꾸지 않습니다. [2017 cap 발표](https://pr.nba.com/nba-salary-cap-2017-18-season/)와 [2021 cap 발표](https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/)의99.093m·112.414m 입력을 보존했습니다.

각 행의 직접비율은 `ExC2017 Year2×112414000/99093000`입니다. 공개 보고점은 모두 그 floor/ceil 구간 안에 있습니다. 다만 CBA 본문에서 법정 반올림 알고리즘을 회수하지 않았고, 연도별 표시·반올림을 무시한 직접비율 계산만으로 모든 법정 정수값을 확정하지 않습니다. 해당 실제표가 이 구간에 속한다는 **수치 조건**과 공개 보고표 가족을 채택할 때에만 좁힌 상단을 사용할 수 있습니다. 실제 정확 센트·사적 계약 접수 인증은 false입니다.

## 제안 가능한 좁힘

기존 각 행의 `ceil+10` 대신 조건부 `ceil`을 쓰면5개 상단 합계가50달러 줄어듭니다. 코어 **57,131,991**, 기존 stretch/camp/QO 예약을 유지한 screen **139,703,092**, 잔여 X 충분조건 **X≤17,278,908**입니다. 두 보고표의 정수점 그대로면 코어57,131,989이며 이는 reference일 뿐 법정 정확금액 선택이 아닙니다. X 충족·전체비용·새 계약5개·macro3 PASS는 여전히 false입니다.

NBA/NBPA2021–22 정확표와 반올림을 겨냥한 세 검색은 결과가 없었고, 기존 CBA101 검색은2018–19판만 반환했습니다. 이는 이번 회수 한계이며 공식표가 없다는 증명은 아닙니다. RealGM 직접본문은403으로 미채택, SalarySwish와HoopsRumors는HTTP200 실제본문·SHA를 보존했습니다. 같은 URL의 반복 다운로드는0입니다.

Wieskamp의 원역사2021 TW→2022 새 계약을 이번2021 standard2년의 증거로 대체하지 않습니다. Green/Bradley 등 실제 후대 계약도 해당 서명연도·계약기간의 동등성 없이 복사하지 않습니다. 최소숫자 정밀화를 비공개 계약/접수 필수요건으로 확대하지 않습니다.

원 raw3/재사용 official cap2/원CBA3쪽 지문과 DOM·수학 대조는 [JSON](CHICAGO_2021_SIGNED_MINIMUM_YEAR2_NUMERIC_REFINEMENT_2026_10_07.json)에 기록했습니다. 독립검문은 pending이며 기존 코어3파일과 중앙·원장은 변경0입니다.

## 현재 전체 진행

|번호|묶음|상태|
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|S2완료|
|3|2021–23 거래·계약|2021 후보보드·비용·권리 검문,2022 코어 정밀화|
|4|장기 커리어|후속설계|
|5|결말·전체 구조|전체기능표 미완료|
|6|집필규격·Context Pack|누적22기능,Pack0|
|7|통합·독립·작가승인|최종게이트 CLOSED|

미완료 큰 묶음 **5**. `v0.30 PARTIAL`/게이트`CLOSED`/원고0.
