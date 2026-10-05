# Chicago 동시대 원장 회수와 날짜 연결

기준 main `3a5036c` / `SOURCE_SUPPORTED_PARTIAL_LEDGER_AND_ROSTER_BRIDGE`. [기계 기록](CHICAGO_DATED_PUBLIC_LEDGER_2026_10_05.json). 전체 법적 비용 `HOLD`.

## 새 사실

[Basketball Insiders 본문](https://web.archive.org/web/20210422012709id_/http://www.basketballinsiders.com/chicago-bulls-team-salary/)은 2021-03-29 갱신을 표시하며 4/22에 보존됐다. 본문이 직접 호출하는 [원 급여 위젯](https://web.archive.org/web/20210424143800id_/http://hw-files.com/tools/salaries/salaries_widget_new.php?team_id=11)은 **별도 4/24 보관본**이다. 원 HTML/JS와 해독 표를 실제 읽고 SHA를 검문했다. 웹 열기는 실패했으며 로컬 성공 캐시를 사용했다. 당시 cap 분석 사이트의 공개 장부로 분류하며 공식 리그 영수증으로 분류하지 않는다.

표의 2020–21 선수 15명 **$127,968,089**와 Vonleh 방출 행 **$97,261**은 **$128,065,350**이다. Guaranteed/Inclusive 합계 두 행과 정확히 일치한다. 현재연도 TW 두 행은 빈 칸이다. 표의 Young 메모는 incentives 미정이다. 본문은 FA cap holds·미서명 1라운더·trade kickers 등을 없다고 보고하지만, 이를 모든 법적 비용 부재로 확대하지 않는다.

[Keith Smith의 2020-11-30 원글](https://twitter.com/KeithSmithNBA/status/1333424139563098113)을 X 공식 oEmbed의 실제 본문으로 회수했다. Temple **1년 $4,767,000**은 NTMLE 일부를 사용했다는 직접 보도다. Room MLE와 같은 금액이라는 이유로 Room 사용으로 분류하지 않는다. [공식 응답](https://publish.x.com/oembed?url=https%3A%2F%2Ftwitter.com%2FKeithSmithNBA%2Fstatus%2F1333424139563098113&omit_script=true)의 SHA/접근 구분은 JSON에 있다.

## 날짜 연결의 범위

[NBA 공개 거래 feed](https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json)의 동결 사본에서 Chicago 직접 연계 3/25~4/24 **11행·2그룹**을 전수 대조했다. 모두 3/25 거래이며 이후 등록 거래는 0행이다. 따라서 위젯의 선수 코호트는 3/25 직후 명단과 연결된다. 위젯의 실제 갱신일·보너스·권리·보장·예외·중재 조정까지 같다는 증거는 아니다. 본문 갱신일을 동적 표의 기준일로 복사하지 않는다.

## 남은 산입과 종료식

본문은 MLE 잔액 **$4,491,000**, BAE **$3,623,000**을 별도로 표시한다. [2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) VII§6(m)(1)–(2), PDF239–240은 자격·미사용 잔액·Team Salary 산입을 구분한다. 이미 산입된 예외를 후기 높은 급여만으로 제거하지 않는다. §6(d)(4)/§6(e)(4), PDF228–229의 당해 cap year 발생·마지막 정규시즌 경기 만료도 적용 시점 검문에 포함한다. Smith의 실제 사용 보도는 선행 미산입을 증명하지 않는다.

기존 15인 차액을 재사용하고 대체 Young unlikely bonus $1m를 전액 스트레스하면, **동일일·동일정의의 역사 전체 상단 + 모든 나머지 차액 상단 ≤ $133,578,061**이 비교 종료 조건이다. 이번 공개 표 합계와의 차이는 **$5,512,711**이다. 이는 빠진 실제 산입액과 대체 차액을 함께 감쌀 허용폭이며, 현재 합상단은 미확인이다. 두 예외가 모두 유효·산입된다는 반례를 놓으면 $136,179,350로 기준보다 $2,601,289 크다. 이는 실제 산입 판정도 자동 가산도 아니다.

남은 검문은 세 묶음이다: **법적 산입 범위·시점**, **Theis/Green 및 모든 비공통 비용 차액**, **유효 예외의 산입/사용/포기 이력**. 공개된 유한 사건·구간으로 닫을 수 있으며 비공개 전체 원장이나 모든 미공표 비용의 절대 부재를 새 필수조건으로 요구하지 않는다.

사실은 원장 숫자·명시 필드·기자 보도·공개 명단 연결이다. 추론은 조건부 허용폭과 적용 범위다. 후보는 동일 정의의 비교 종료 경로다. 작가확정은 기존 방향만 유지하며 새 선택 0건이다. S2 법적 **2완료/10HOLD**, F0/5·A0/3·K0/4, freeze v0.30 PARTIAL·설계/원고 CLOSED·원고 0을 유지한다.
