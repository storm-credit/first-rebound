# O-15F14-AE — Chicago 2020–21 MLE/BAE 산입 조건의 급여 하한

- 기준: `main` `b694f7f`; 분류: `FACT / INFERENCE / CONDITIONAL`; D1 F1은 계속 `HOLD`.
- 목적: [AD의 감소일 위험 시험](O15F14AD_CHICAGO_EXCEPTION_PRORATION_BOUND.md)이 실제 Chicago 경로에서 발생 가능한지 CBA VII §6(m)(2)의 **캡 아래로 내려간 적이 있는가**부터 검사한다.
- 적용 경로: 승인된 2020 Draft 4순위 LaMelo, Hutchison→주인공 2018 1라운드 계약, 2021-03-25 전 Chicago 기존 선수 보유. 새 계약·거래·시즌 채택이 아니다.

## 규칙과 시점

[2017 NBA–NBPA CBA](https://official.nba.com/2017-nba-collective-bargaining-agreement/) Article VII §6(m)(2), 인쇄 214쪽은 DPE·BAE·MLE·TPE가 발생할 때 **또는 소멸 전** 팀 급여가 샐러리캡 아래로 내려가되 그 부족액이 해당 예외보다 작을 때 미사용 예외액을 Team Salary에 산입한다. 예외를 **쓸 자격**이 있다는 사실만으로 미사용 예외액이 산입되지는 않는다. §4(a)(4)·§4(e)(1), 인쇄 184·186쪽은 1라운드 지명권이 지명 즉시 해당 순번 rookie scale의 120%로 포함되고 계약 체결 시 계약 급여로 대체됨을 규정한다.

[NBA의 2020–21 합의 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)에서 캡은 `$109,140,000`, 드래프트는 11월 18일, FA 협상은 11월 20일, 서명은 11월 22일부터다. [NBA 11월 16일 당시 보도](https://www.nba.com/news/nba-offseason-2020-nov-16-roundup)는 Otto Porter Jr.가 2020–21 `$28.4m` 선수 옵션을 행사한다고 전했다. 공개된 코로나 수정 CBA의 **정확한 새 cap-year 첫날**은 확보하지 못했다. 따라서 첫날 자체의 증명으로 과장하지 않고, 드래프트 이후 지명권이 존재하는 구간부터 3월 25일 거래 직전까지의 조건부 하한을 계산한다.

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
- **추론:** D1의 기존 계약 보유·4순위 서명 경로라면 드래프트 뒤부터 3월 25일 거래 **직전**까지 기본 계약/권리만으로 캡 위다. 이 구간에서 MLE·BAE의 **미사용분은 §6(m)(2) 때문에 산입될 조건을 충족하지 않는다.** Temple의 이미 사용된 액수는 계약 급여로 다른 줄에서 센다. AD의 `$6.669m` 위험 시험은 이 경로의 실제 부담으로 승격할 수 없다.
- **조건부 한계:** 코로나 수정 CBA의 cap-year 첫날 원문, 예외가 그보다 앞서 발생·산입된 이력, 11명 계약의 보장/이탈/조정에 관한 1차 cap sheet가 미확보다. 과거에 산입된 예외의 잔액이 계속 살아 있는 가능성을 첫날 이후 하한만으로 지울 수 없다. TPE/DPE 발생·사용도 별개다. 따라서 `EXCEPTION_HISTORY` **전체값은 null**이고 F1 전체 R과 비납세/거래 판정도 `HOLD`다.
- **다음 회수:** NBA–NBPA 2020–21 일정 변경 원문에서 cap-year 첫날과 6(m)(2) 변경 여부, Chicago 최초 cap sheet·과거 TPE/DPE, 미서명 1R/FA·방출액. 이 확인 후에만 MLE/BAE 소항목을 0으로 닫는다.

이 증인은 공개 CBA 원문과 급여 2차 장부를 Codex가 대조한 **자체 검토**다. Anti-Gravity·NotebookLM·Claude·source-blind 독립 검수는 이번 증인에서 `NOT_RUN`; 독립 통과로 세지 않는다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, `manuscript_allowed=false` 유지.
