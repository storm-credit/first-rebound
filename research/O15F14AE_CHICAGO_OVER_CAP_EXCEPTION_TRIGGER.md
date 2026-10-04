# O-15F14-AE — Chicago 2020–21 MLE/BAE 산입 조건의 급여 하한

- 기준: `main` `b694f7f`; 분류: `FACT / INFERENCE / CONDITIONAL`; D1 F1은 계속 `HOLD`.
- 목적: [AD의 감소일 위험 시험](O15F14AD_CHICAGO_EXCEPTION_PRORATION_BOUND.md)이 실제 Chicago 경로에서 발생 가능한지 CBA VII §6(m)(2)의 **캡 아래로 내려간 적이 있는가**부터 검사한다.
- 적용 경로: 승인된 2020 Draft 4순위 LaMelo, Hutchison→주인공 2018 1라운드 계약, 2021-03-25 전 Chicago 기존 선수 보유. 새 계약·거래·시즌 채택이 아니다.

## 규칙과 시점

[2017 NBA–NBPA CBA](https://official.nba.com/2017-nba-collective-bargaining-agreement/) Article VII §6(m)(2), 인쇄 214쪽은 DPE·BAE·MLE·TPE가 발생할 때 **또는 소멸 전** 팀 급여가 샐러리캡 아래로 내려가되 그 부족액이 해당 예외보다 작을 때 미사용 예외액을 Team Salary에 산입한다. 예외를 **쓸 자격**이 있다는 사실만으로 미사용 예외액이 산입되지는 않는다. §4(a)(4)·§4(e)(1), 인쇄 184·186쪽은 1라운드 지명권이 지명 즉시 해당 순번 rookie scale의 120%로 포함되고 계약 체결 시 계약 급여로 대체됨을 규정한다.

[NBA의 2020–21 합의 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)에서 캡은 `$109,140,000`, 드래프트는 11월 18일, FA 협상은 11월 20일, 서명은 11월 22일부터다. [NBA 11월 10일 수정 CBA 발표](https://pr.nba.com/nba-board-of-governors-approves-adjustments-to-collective-bargaining-agreement/)도 이 세 날짜를 확인한다. [당시 리그 연도 일정 설명](https://www.hoopsrumors.com/2020/05/players-eligible-for-rookie-scale-extensions-in-2020-offseason.html)은 **2020–21 리그 연도 첫날을 11월 21일**로 명시한다. 이 첫날 날짜는 2차 보도이며 코로나 수정 CBA 원문으로 독립 확인하지 못했다. [NBA 11월 16일 당시 보도](https://www.nba.com/news/nba-offseason-2020-nov-16-roundup)는 Otto Porter Jr.가 2020–21 `$28.4m` 선수 옵션을 행사한다고 전했다. 따라서 드래프트 뒤 권리가 생기는 11월 18일부터 3월 25일 거래 직전까지의 조건부 하한을 계산하고, **11월 21일을 수정 CBA의 1차 인증 날짜로 승격하지 않는다.**

2017 CBA Article VII §6(d)(4)·§6(e)(4), 인쇄 204·205쪽은 BAE와 비납세 MLE가 **각 Salary Cap Year 첫날 발생**하고 해당 팀의 **정규시즌 마지막 날 소멸**한다고 규정한다. 이 규칙과 위 11월 21일 날짜가 2020–21 수정 합의에서도 유지됐다면, 2019–20 BAE/MLE는 새 연도로 이월되지 않고 2020–21의 두 예외는 11월 21일보다 먼저 산입될 수 없다. 그 첫날에는 11월 18일 4순위 지명권과 이미 행사한 Porter 옵션을 포함하는 아래 급여 하한이 캡 위다. 기존 계약 보유 경로가 3월 25일까지 유지되는 동안에는 §6(m)(2)의 **새 BAE/MLE 미사용분 산입** 또는 같은 시즌의 더 이른 산입 이력을 만들 캡 미만 시점이 없다. 이 결론의 전제인 수정 조항·정확 계약 장부는 여전히 확인 대상이다.

## 독립적인 아래쪽 합계

[2020년 4월 Hoops Rumors의 Chicago 급여 미리보기](https://www.hoopsrumors.com/2020/04/202021-salary-cap-preview-chicago-bulls.html)는 확정 계약 11명 `$77,538,469`, 별도의 Porter 옵션 `$28,489,239`, 4순위 보류액 `$7,068,360`을 열거한다. 계약 금액·보장 분류는 **2차 장부**이며 NBA 팀 cap sheet 원본이 아니다. 11명은 LaVine, Young, Satoransky, Felicio, Markkanen, Coby White, Carter Jr., Arcidiacono, Hutchison, Kornet, Gafford다. D1에서 Hutchison만 주인공으로 치환하고, Porter·나머지 10명의 계약과 4순위 권리를 3월 25일 이전까지 유지한다.

| 단계 | Team Salary에 반드시 들어가는 기존 계약/권리의 하한 |
|---|---:|
| 실제 확정 계약 11명 | $77,538,469 |
| Hutchison 제거 | −$2,443,440 |
| 주인공 2018 1R 3년차 16~30순위·80~120% 범위의 최저값 | +$1,325,520 |
| Porter 2020–21 옵션 행사 | +$28,489,239 |
| Chicago 2020 전체 4순위 권리 또는 120% 계약 기준선 | +$7,068,360 |
| **대체 세계 급여 하한** | **$111,978,148** |
| 2020–21 캡과의 차이 | **+$2,838,148** |

주인공 `$1,325,520`은 [기존 2018 3년차 범위](../simulation/CHICAGO_2020_21_TAX_BOUND.md)의 가장 낮은 시험값이다. 실제 순번·급여를 정한 값이 아니다. 4순위 `$7,068,360`도 기존 [opening roster 기준선](CHICAGO_2020_21_OPENING_ROSTER_BASELINE.md)의 순번 치환값이며 LaMelo의 실제 Charlotte 3순위 계약을 복사하지 않는다. FA 권리, Temple/Valentine 서명, 기타 계약·보너스, 방출잔액을 **전부 빼고도** 캡 위다. 이 하한은 완전한 Team Salary가 아니고 거래 후에도 자동 지속되지 않는다.

더 낮은 민감도 시험으로 4순위 금액을 임의로 80%인 `$4,712,240`만 놓아도 합계 `$109,622,028`, 캡보다 `$482,028` 높다. 이는 실제 4순위 보류액 규칙을 80%로 바꾸는 주장이 아니라 금액 입력 오류에 대한 여유 검사다.

## F1 판정

- **사실:** CBA §6(m)(2)의 산입 트리거는 캡 미만 Team Salary다. 공개 당시 급여 장부의 실제 11계약·Porter 옵션·4순위 보류액과 공식 캡을 위처럼 대조했다.
- **추론:** D1의 기존 계약 보유·4순위 서명 경로라면 드래프트 뒤부터 3월 25일 거래 **직전**까지 기본 계약/권리만으로 캡 위다. 당시 일정의 11월 21일 시작과 기존 §6(d)(4)·§6(e)(4)가 수정 후에도 맞다면, MLE·BAE의 **미사용분은 그 시즌 처음부터 §6(m)(2) 산입 조건을 충족하지 않는다.** Temple의 이미 사용된 액수는 계약 급여로 다른 줄에서 센다. AD의 `$6.669m` 위험 시험은 이 경로의 실제 부담으로 승격할 수 없다.
- **조건부 한계:** 11월 21일을 적은 일정은 2차 보도다. 코로나 수정 CBA의 첫날·§6(m)(2) 변경 여부와 11명 계약의 보장/이탈/조정에 관한 1차 cap sheet는 미확보다. 위 전제 아래서는 과거 시즌 BAE/MLE 이월이나 **같은 시즌 첫날 이전 산입**을 걱정할 이유가 줄지만, 전제 자체를 아직 인증하지 못했다. [AF 거래 연혁 검문](O15F14AF_CHICAGO_PREDEADLINE_EXCEPTION_ORIGIN.md)은 승인 경로에서 3/25 거래 직전 기존 Chicago TPE를 조건부 0으로 좁혔지만 DPE 허가·사용과 모든 §6(m)(2) 수정 조항을 인증하지 않는다. 따라서 `EXCEPTION_HISTORY` **전체값은 null**이고 F1 전체 R과 비납세/거래 판정도 `HOLD`다.
- **다음 회수:** NBA–NBPA 2020–21 일정 변경 원문에서 cap-year 첫날과 §6(d)(4)·§6(e)(4)·§6(m)(2) 변경 여부, Chicago 최초 cap sheet·DPE/다른 예외의 실제 사용, 미서명 1R/FA·방출액. 이 확인 후에만 MLE/BAE 소항목을 0으로 닫는다.

이 증인은 공개 CBA 원문과 급여 2차 장부를 Codex가 대조한 **자체 검토**다. Anti-Gravity·NotebookLM·Claude·source-blind 독립 검수는 이번 증인에서 `NOT_RUN`; 독립 통과로 세지 않는다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, `manuscript_allowed=false` 유지.

2026-10-04 [존속기간·QO 경계 검수](../reviews/CHI_EXCEPTION_LIFETIME_REVIEW_2026_10_04.md)는 기존 하한을 보존하고 신규 산입 차단과 초기·이월 산입 잔액 부재를 구분했다. Valentine QO 서명일은 구단 원문에서 11/21로 대조했지만 그 계약 급여를 서명 전으로 소급하지 않는다. 4순위 권리를 넣은 위 기존 하한은 유지하며, 같은 계산을 새 증인으로 세지 않는다. 후속의 AG 기사 대조/NLM 2017조항 분석·국소 Codex 검수는 당시 NOT_RUN 기록을 소급 교체하거나 2020 수정·전체 법적 PASS를 인증하지 않는다.
