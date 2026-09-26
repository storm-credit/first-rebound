# O-15G15M — Bacon 보장 시점·방출 비용과 Mobley3 미서명 cap hold

- 기준: `main` `78515ea` / PR #196. [G15L 여름 날짜 원장](O15G15L_ORLANDO_SUMMER_CONTRACT_EVENT_LEDGER.md)의 Bacon `−1`과 신인 지명권 `0 roster / ? Team Salary`를 계약·CBA 규칙으로 더 세분한다. 새 방출·지명·시즌을 작가확정하지 않는다.
- 상태: `HISTORICAL_GUARANTEE_RECONCILED / ALTERNATE_COST_BRANCH_HOLD`.

## 1. 원역사에서 확인되는 서로 다른 숫자

| 항목 | 확인과 등급 | 해석 경계 |
|---|---|---|
| Orlando의 Bacon 방출 | [Magic 공식 거래 연표](https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf) 2021-08-08. [NBA 드래프트 당시 팀 프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)은 그를 앞서 `Under Contract`로 분류. | 원역사 날짜와 7월→10월 이탈은 사실. 대체 Orlando가 같은 날 방출했다는 증거 아님. |
| 2021–22 계약 기본급과 보호액 | [SalarySwish 계약표](https://www.salaryswish.com/players/dwayne-bacon)는 기본급 **$1,824,003**, 실제 8/8 방출 때 `Guaranteed $0`과 미충족 보장 조건을 표시. [2021-08-08 당시 보도](https://www.hoopsrumors.com/2021/08/dwayne-bacon-waived-by-magic.html)는 미보장이라 Orlando에 dead money가 없었다고 설명. | 비공식 계약 세부값이지만 서로 부합. SalarySwish 표의 `Cap Hit $1,824,003`는 **계약 기본급 열**과 함께 보인 값이지, 8/8 이후 Orlando가 실제로 부담한 dead charge가 $1,824,003이라는 증거가 아니다. |
| 보장 시점 | SalarySwish는 선수가 **FA moratorium 종료 후 최장 3일 이내까지 방출되지 않으면** $0→$1,824,003 보장이라고 표기한다. [NBA 2021 공식 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)는 moratorium이 **8/6 정오 ET**에 끝났다고 명시한다. | 두 자료를 결합하면 **8/9 무렵이 보장 경계**라는 추론은 가능하다. 공개 문구의 `at the latest` 때문에 **8/9 정오 ET가 계약서의 정확한 데드라인이라고 단정할 수 없다.** 원계약서·통지 시각 미확보. 원역사 8/8 방출과 $0 보호액은 추적표·당시 보도에서 확인. |
| Knicks 후속 | [Magic 2021-08-20 보도](https://www.nba.com/magic/news/10-most-intriguing-orlando-magic-games-2021-22-20210820)는 방출 직후 New York 계약을 언급하고, [Knicks 공식 2021-10-14 발표](https://www.nba.com/knicks/front-office-news/knicks-sign-brandon-goodwin)는 Bacon 방출을 기록한다. | 대체 Orlando가 Bacon을 유지하면 이 원역사 Knicks 캠프 경로도 자동으로 일어나지 않는다. 당시 Knicks 계약의 정확 보장액은 이 두 공식 기사에 없음. |

[2017 NBA–NBPA CBA Article VII §4(a)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)와 [NBA CBA 101 `I.L`·`I.U`](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)는 **계약을 보유한 때의 Team Salary**, 방출 뒤 **보호급여/잔여 지급에 따른 charge**, 표준 명단 자리를 서로 분리한다. 비보장 계약도 보유 중에는 해당 시즌 계약 급여를 전체 팀 샐러리 계산에서 무조건 `0`으로 만들지 않는다. 방출 뒤 실제 보호급여가 0이었다는 원역사 결과와 별개다. 전체 Orlando cap room은 아직 산정하지 않는다.

## 2. 대체 Orlando의 Bacon 사건 세 갈래

| 조건부 사건 | 10/16 자리와 대략 비용 | 빠뜨리면 안 되는 파급 |
|---|---|---|
| **B0: 원역사처럼 8/8 waiver 사건을 선택** | 10/16까지 이탈이 끝난다는 추가 조건에서 G15L의 `−1`을 적용. 원계약의 보호조건이 같고 보장 전에 적법하게 놓인 경우 **원역사식 보호급여 $0 시험**. | 8/8 **waiver 발표/요청**과 실제 통과 시각은 다르므로 효력·계약 조항을 다시 확인. Knicks 캠프 후속은 가능성일 뿐 자동 확정 아님. 이 한 자리는 G15E의 10월 공통 11명에 이미 반영돼 **Aminu 추가 초과를 또 해결하는 공짜 −1이 아님**. |
| **B1: 보장 경계 뒤에 방출** | 자리는 `−1`이 될 수 있으나 같은 계약·완전 보장·후속 조정 없음이라는 조건에서 **$1,824,003 보호급여의 잠재 dead charge**. | 실제 정확 보장일, waiver 효력, 새 팀 수입에 따른 set-off/합의·stretch와 상대 선수 경로를 확인. 8/9 정오라는 정확 시각 가정 금지. |
| **B2: 10/16까지 계속 보유** | G15L의 원역사 방출 채택 시험보다 표준 **+1**. 다른 변화가 없으면 O15A의 Aminu 사전 이탈 후에도 `16/15`; Bacon 계약 기본급 $1,824,003은 전체 팀 샐러리의 한 입력 후보. | Bacon의 [원역사 2020–21 기록](https://www.nba.com/players/dwayne/bacon/1628407) 72경기·50선발·25.7분 역할을 대체 Orlando가 왜 유지하는지, 다른 가드/윙의 자리·출전분과 Knicks 캠프 경로 소실을 설명. 전 시즌 기록을 다음 시즌 분으로 자동 복사하지 않음. |

`B0`이 경제적으로 가장 가벼워 보이는 것은 **원계약 조항과 실제 방출 시점이 같다는 조건의 추론**이다. 장면/커리어 설계에서 Bacon을 어느 팀에 둘지는 작가확정이 아니다. 2020–21 Chicago/Orlando의 정확 시즌 결과와 선수 평가가 달라지면 Orlando가 원역사처럼 포기할 동기도 재검토해야 한다.

**자리와 급여의 인과:** B0의 표준 `−1`은 **Bacon 본인의 계약이 10/16 전에 명단에서 이탈한 효과만** 뜻한다. Mobley의 미서명은 이 감소 사건과 무관하고, 서명 전까지 그에게 표준 자리 `0`을 세는 별도 상태다. B0의 후보 dead charge `0`도 `방출`이라는 단어만으로 발생하지 않는다. **같은 원계약 보호조건 + 보장 발생 전 적법한 waiver + 그 계약에서 남는 지급의무 없음**을 함께 충족한다는 원역사식 시험이다. waiver 접수/통과 시각과 보호조건이 다르면 비용을 다시 계산한다.

## 3. Mobley3 지명권의 별도 팀 샐러리 비용

[NBA–NBPA 2017 CBA Article VII §4(e)(1)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)은 **1라운드 선수가 지명되는 즉시** 그 지명권 보유 팀의 `Team Salary`에 신인 스케일 **120%**의 hold를 둔다. 서명·권리 양도/소멸 및 §4(e)(2)·(3)의 정해진 예외에 따라 달라진다. 이는 **선수 표준계약 명단 자리 1개**와 다르다. 2021년 3번을 Orlando가 실제 보유·Mobley를 선택하는 분기라면 **서명 전에도** cap hold를 넣고, 계약 후에는 실제 계약액으로 교체해야 한다. 원역사 Cleveland가 [2021-08-03 Mobley와 계약](https://www.nba.com/cavaliers/releases/mobley-signing-210308)한 날짜를 대체 Orlando 서명일로 복사하지 않는다.

[RealGM의 2021–22 #3 신인 스케일](https://basketball.realgm.com/nba/info/rookie_scale/2022) **$6,729,300 × 120% = $8,075,160**은 CBA 공식 **공식(120%)**에 비공식 스케일 표를 대입한 **작업상 cap hold 후보**다. [SalarySwish의 원역사 Mobley 2021–22 계약표](https://www.salaryswish.com/players/evan-mobley)의 $8,075,160과 일치하지만, 이는 원역사 Cleveland **실제 서명액**이고 대체 Orlando 서명 사실이나 전체 팀 샐러리 증거가 아니다. Mobley의 1R hold는 **G15J의 Vučević+Aminu 두 사람 부분합 $34,183,800에 포함되지 않는다.** Herbert33은 2라운드라 이 `1R 120% hold`를 붙이지 않는다. 33번 required tender·대체 서명 급여는 별도 `HOLD`다.

**사실:** 원역사 공식 방출/FA 모라토리엄·Knicks 방출과 2017 CBA의 1R hold 규칙. **추론:** 같은 계약·날짜의 Bacon B0 $0 보호액 시험, B1/B2 비용 및 Mobley3 $8,075,160 스케일 산술. **후보:** B0/B1/B2, Mobley3/Herbert33 지명·서명. **작가확정:** 신규 0건.

## 4. 도구 기록과 다음 인수

- **NotebookLM CLI:** SalarySwish 소스 `95cbd084-0808-4a82-8ee4-4de0f1d2d13f`와 NBA 캡 발표 `605e9737-8fa5-42b1-9ca7-130873b289f1`만 지정한 질의 `1774ae18-99b6-4bbc-83e0-5d8c357fa903`에서 $1,824,003/$0와 8/6 정오를 분리 추출했다. 답변은 8/9 **정오**를 정확 데드라인처럼 추론했으나 계약 원문에 그 시각이 없어 **기각**한다.
- **Antigravity CLI:** 두 공개 URL 읽기를 절대경로 CLI에 요청했으나 40초 `print timeout`, 본문 0건. `AGY_SOURCE_READ_FAILED`이며 별도 증거로 세지 않는다.
- **Codex:** NBA/NBPA 2017 CBA의 실제 적용 조항, NBA/구단 공식 거래일, 비공식 계약표의 보호액과 명목 `Cap Hit`를 구분해 G15L의 미서명 1R 급여 보류 표현을 **규칙 확인으로 정정**했다. 같은 원문을 NotebookLM이 재질의한 것은 독립 검수 횟수가 아니다.
- **Claude CLI 제한 반증 / 결과 단독 맹점:** [검토 기록](../reviews/R01_O15G15M_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)의 첫 긴 호출은 실질 검토 없이 준비 설명만 했고, 짧은 반증은 waiver **요청과 실제 통과** 및 보호조건 근거가 빠지면 안 된다고 지적했다. 새 결과 요약만 받은 source-blind 편집 호출은 Bacon의 `−1`과 Mobley 미서명 `0`의 인과가 혼동되고, `dead money 0`의 조건이 압축됐다고 지적해 위 문단을 보강했다. Claude에 원문을 독립 수집시키지 않았으므로 CBA/계약 독립 감사나 G16 통과가 아니다.

다음은 **Bacon의 원계약 보장일·waiver 효력**을 문서로 고정할 수 있는지, Mobley3 공식 2021 스케일·Herbert33 required tender, 나머지 Orlando 2021–22 계약 및 FA holds를 선수별로 수집하는 것이다. 그 뒤에만 Aminu B/C와 세 FA 선택을 더해 전체 팀 샐러리/캡 공간을 시험한다. G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, G16/G17 미완료, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, author/season/exact/manuscript false 유지.
