# O-15G15W — 2022-01-23 두 경기·네 팀 기회 부채

- 기준: `main` `14427ea` / PR #206. [G15V의 시즌 총분 압박](O15G15V_2021_22_FRONTCOURT_OPPORTUNITY_DEBT.md)을 [G15B의 Orlando 한 경기 조건부 240분](../simulation/CHICAGO_2021_22_G15B_STRESS.json)과 같은 날짜의 다른 팀 경기로 좁힌다. 시즌 경로나 실제 점수는 선택하지 않는다.
- 판정: `DATED_MULTI_GAME_COLLISION_IDENTIFIED / MEDICAL_TRADE_ROLE_HOLD`. Chicago 센터 48분은 기존 G14에 이미 배정되어 **재계산 대상이 아니다**. Denver의 Nnaji 이탈과 Detroit 상대 변화, Orlando의 Moritz 역사적 역할 손실이 남는다.
- 입력 계보: Orlando의 **Mobley3는 G7 드래프트 비교 후보**이고 Nnaji는 **Gordon A 거래 방향**의 반환 자산이다. 두 선수를 같은 거래로 들여오지 않는다. Mobley3의 실제 지명·서명, Gordon A의 정확 거래 실행은 모두 별도 `HOLD`다.

## 1. 원역사 날짜와 조건부 세계를 분리

원역사 2022-01-23에는 [Chicago @ Orlando `0022100701`](https://www.nba.com/game/chi-vs-orl-0022100701/box-score)과 [Detroit @ Denver `0022100707`](https://www.nba.com/game/det-vs-den-0022100707/box-score)가 각각 열렸다. 아래 박스 행은 **원역사 관측**이다. 점수·의료·출전이 대체세계에도 그대로 발생했다는 뜻이 아니다.

| 경기·팀 | 원역사 1차 자료의 해당 선수 | 이미 있는 대체세계 조건부 배정·미해결 인과 |
|---|---|---|
| CHI @ ORL / Chicago | Vučević **30:19**, 13점·19 FGA. Chicago 원역사 선발 센터였다. | [G14 CHI 1/23](../simulation/CHICAGO_2021_22_PAIRED_INPUTS.json)는 Vučević를 **넣지 않고** 센터 Carter 28+Young 8+Bradley 12=48분으로 이미 배정했다. 그 48분을 다시 구멍으로 세지 않는다. 세 선수의 그날 계약·건강·경기력, 원역사 Vučević의 19 FGA/공격 기능 대체는 여전히 조건부다. |
| CHI @ ORL / Orlando | Carter Jr. **28:11**, Bamba **6:51**, Moritz Wagner **25:08·23점·13 FGA**, Okeke **30:09**; Lopez는 `DNP - Coach's Decision`. 원역사 결과는 Orlando 114–Chicago 95. | G15B O15A/O15C는 C=Vučević36+Bamba12, PF=Mobley24+Nnaji12+Okeke12. 두 증명 모두 Moritz/Lopez **0분**, Okeke 총24분이다. 원역사의 Moritz 25:08·23점 및 Carter/Suggs/Franz의 득점·분을 결과에 복사할 수 없다. M1에서 Moritz가 계약상 있어도 그날 0분의 **코칭 근거**가 필요하다. |
| DET @ DEN / Denver | Nnaji **16:45·12점·5/5 FG**, Gordon **31:15**, Jokić **36:06**, Cousins **11:49**. 원역사 결과는 Denver 117–Detroit 111. | 승인된 **Gordon A 방향**에서 Nnaji를 Orlando로 보내는 정확 실행이 성립했다면 Denver가 원역사 Nnaji 16:45를 사용할 수 없다. `Gordon 31:15 + Nnaji 16:45 = 48:00`은 PF로 놓는 **가능한 산술 분해**일 뿐 원역사 실제 동시 5인/포지션 증명이 아니다. 새 수신자·포지션·활동 가능성을 지정해야 한다. |
| DET @ DEN / Detroit | [원역사 Denver 경기 요약](https://www.nba.com/game/det-vs-den-0022100707)은 Detroit 111점, Denver 117점을 기록한다. | G7의 Suggs5 Detroit 및 기존 2020 대체 선수들이 성립하면 Detroit 역시 원역사 명단과 다르다. Denver에 새 빅맨 분을 주더라도 **Detroit 원역사 111점·Denver 117점을 고정할 수 없다**. G14의 DET `PRIOR_HOLD`를 덮어쓰지 않는다. |

Denver [공식 경기 박스](https://www.nba.com/nuggets/game/0022100707)는 Nnaji 16:45와 Cousins 11:49를 함께 표시한다. 같은 페이지의 경기 요약은 Cousins의 Denver 첫 경기, Jeff Green의 왼쪽 대퇴사두근 타박상 결장, JaMychal Green의 방역 결장을 전한다. 다만 박스의 Jeff Green 상태란은 `DNP - Coach's Decision`으로 표시되어 **요약과 사유가 다르다**. 어느 표기가 공식 의료 상태인지 추가 확인 전에는 둘 중 하나를 대체세계의 확정 결장 사유로 쓰지 않는다. Cousins의 원역사 계약·데뷔도 Gordon A 대체세계에서 자동 유지하지 않는다.

## 2. Cleveland는 그날 같은 경기의 분 수신자가 아님

[Cleveland의 미국 현지 1/22 Oklahoma City전](https://www.nba.com/game/0022100695) 경기 요약은 다음 경기를 월요일 New York전으로 안내하고, [현지 1/24 New York전 공식 박스](https://www.nba.com/game/nyk-vs-cle-0022100709/box-score)는 Mobley **38:27**을 기록한다. 원역사 Cleveland는 **현지 1/23 경기가 없다**. NBA 페이지의 UTC 시각은 전날 미국 현지 경기일과 다르게 보일 수 있다. 따라서 G15B Orlando의 `Mobley24`와 같은 달력 날짜에 Cleveland `Mobley−24분`을 새 경기로 만들어서는 안 된다. Cleveland가 실제 잃는 것은 G15V의 **원역사 시즌 69선발·2,331분 및 각 Cleveland 경기의 역할**이다. 1/22와 1/24의 원역사 내용은 일정·기회 비용 표식이며, 대체세계의 Mobley 건강이나 Cleveland 경기 결과를 복사할 수 없다.

## 3. 닫힌 항목과 열린 항목

1. **중복 차감 방지:** G14 Chicago `Carter28+Young8+Bradley12=48`을 기계 대조했다. Vučević의 원역사 Chicago 30:19는 실제 박스 기준선이며, 대체세계 Chicago 48분에 다시 더하거나 빼지 않는다.
2. **같은 날 두 경기 연결:** Orlando에 Nnaji12를 두는 1/23 증명에는 Denver의 원역사 Nnaji16:45와 Detroit 상대의 대체 로스터 검토가 따라야 한다. G15B Orlando 240분만 성립해도 같은 날짜 리그 전체의 분/공격·승패는 아직 성립하지 않는다.
3. **Moritz 기회 비용:** M1 서명 분기에서는 기존 G15B의 Moritz 0분이 원역사 25:08과 다른 **역할 선택**이다. M0 비서명 분기에서는 원역사 그날 Orlando 23점·13 FGA의 주체 자체가 사라진다. 어느 쪽도 그 점수를 Vučević/Mobley에게 무상 배분하지 않는다. Lopez의 원역사 DNP는 L1 계약 필요성이나 시즌 612분의 소멸을 증명하지 않는다.
4. **다음 종료 조건:** Gordon A의 정확 계약/픽/등록 실행, Denver 1/23 빅맨 대체 수신자와 Jeff/JaMychal/Cousins의 대체세계 가용성, Detroit의 Suggs/Patrick/Stewart 연쇄, Orlando의 Moritz M1/M0·Vučević 여름 잔류·의료/코칭을 **한 날짜 장부**에서 연결한다. Cleveland는 자체 경기일에만 Mobley 이탈을 계산한다. 그 뒤에야 두 경기의 새로운 FGA/FTA/실책/분과 결과를 계산한다.

**도구·출처 경계:** Codex는 NBA 공식 경기 박스/요약의 검색 가능한 행과 G14/G15B JSON을 대조했다. Anti-Gravity CLI의 같은 NBA URL 직접 읽기 시도는 45초 제한 뒤 `SUCCESS`/빈 최종 응답(`957ea310-6dbf-402b-9031-c68e754e8abe`)으로 끝나 **본문 증거 0건**이다. NotebookLM CLI에는 URL 소스 `d7a66357-edc3-4778-8f84-e400a4d88db8` 추가가 성공했지만 질의 `58a376b6-21a1-4842-9413-e97a61828250`는 내비게이션만 수집되어 선수 표가 없다고 답했다. **이번 경기 박스 수치의 NotebookLM 교차검증도 0건**이다. 두 실패를 도구 통신 성공이나 원문 독립 확인으로 부풀리지 않는다.

[Claude 제한적 맹점 검토](../reviews/R01_O15G15W_CLAUDE_SOURCE_BLIND.md)는 Chicago/Orlando 산술을 확인하고 Denver Nnaji 분 수신자 미지정과 Mobley 경로 분리를 지적했다. 전자는 이미 열린 `HOLD`, 후자는 G7 드래프트 후보라는 입력 계보를 명시해 보강했다. Claude의 무도구 응답을 경기 원문 검증으로 세지 않는다.

**사실:** 원역사 두 경기 날짜·박스 행, Cleveland 1/22·1/24 일정, 기존 G14/G15B의 숫자 배정. **추론:** 같은 날짜 기회 부채와 원역사 점수 이월 불가. **후보:** Denver/Detroit/Orlando의 구체 수신자·공격 예산. **작가확정:** 신규 0건. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.
