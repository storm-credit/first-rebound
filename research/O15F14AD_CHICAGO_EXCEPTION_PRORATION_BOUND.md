# O-15F14-AD — Chicago 2021-03-25 예외 감소일 반례와 F1 위험

- 기준: `main` `1c6973f`; 분류: `FACT / INFERENCE / CONDITIONAL`, F1 `HOLD`.
- 목적: F1의 `EXCEPTION_HISTORY`에 평년 1월 10일 감소 규칙을 기계적으로 대입하는 오류를 차단하고, 2020–21 변경일을 적용한 위험 분기를 계산한다. `R_CHI`의 나머지 항목이나 Chicago의 실제 Team Salary를 인증하지 않는다.
- 후속 적용 제한: [AE 급여 하한](O15F14AE_CHICAGO_OVER_CAP_EXCEPTION_TRIGGER.md)은 드래프트 뒤~3월 25일 거래 직전 기존 계약 보유 경로가 캡 위였음을 보여준다. 아래 양쪽 예외 산입 숫자는 **트리거가 별도로 증명될 때만** 쓰는 스트레스이며 Chicago의 실제 잔여 예외액으로 읽지 않는다.

## 원문과 적용 범위

1. [2017 NBA–NBPA CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) Article VII §6(m)(2), 인쇄 214–215쪽: 조건에 맞아 Team Salary에 들어간 예외는 사용·권리 소멸·포기 전까지 **미사용분**만 남는다. 선수 서명으로 사용한 부분은 선수 급여와 중복 산입하지 않는다. §6(m)(5), 인쇄 216쪽의 **평년 원문**은 1월 10일 감소를 규정하고 TPE·DPE는 제외한다. 이 날짜를 코로나 단축 시즌에 그대로 적용하지 않는다.
2. 같은 CBA §6(d)(1)·§6(e)(1), 인쇄 203–204쪽: BAE·비납세 MLE는 전년도 금액에 샐러리캡 증가율을 적용한다. [NBA의 2019–20 공식 발표](https://pr.nba.com/nba-salary-cap-for-2019-20-season-set-at-109-140-million/)는 비납세 MLE `$9,258,000`, [NBA/NBPA의 2020–21 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)는 2019–20과 같은 캡 `$109,140,000`을 명시한다. 따라서 이 규칙만 적용하는 계산에서 2020–21 비납세 MLE 기준도 `$9,258,000`이다. BAE `$3,623,000`은 [CBA FAQ의 해당 시즌 표](https://www.cbafaq.com/salarycap17.htm)로 교차 대조한 **2차 자료 입력**이다.
3. [NBA 일정 공지](https://pr.nba.com/2020-21-nba-season-structure/)와 [후반 일정 공지](https://www.nba.com/news/nba-schedule-second-part-official-release): 정규시즌은 2020-12-22부터 2021-05-16까지, 양 끝 포함 146일이다. [Hoops Rumors의 당시 2020–21 예외 장부](https://www.hoopsrumors.com/2020/12/how-teams-are-using-202021-mid-level-exceptions.html)는 **해당 시즌 감소가 2월 27일부터 `1/146`씩 시작**됐다고 명시한다. 2026-09-28에 HTML 본문을 직접 열어 해당 문장과 Chicago–Temple 행을 확인했다. 이는 2차 자료이며 수정된 NBA–NBPA 원문은 확보하지 못했다. 02-27부터 거래 전날 03-24까지 26일이므로, 이 변경이 §6(m)(2)의 예외 보류액에도 적용된다는 조건에서 거래 당일 감소를 제외한 보수적 계수는 `120/146`이다. 평년 1월 10일을 적용한 `72/146`은 2020–21 계산에 쓰면 안 된다.
4. [Chicago의 Temple 영입 설명](https://www.nba.com/bulls/news/bulls-add-garrett-temple)은 예외의 상당 부분을 쓴 것으로 표현한다. [Hoops Rumors의 2020–21 MLE 집계](https://www.hoopsrumors.com/2020/12/how-teams-are-using-202021-mid-level-exceptions.html)는 Chicago 사용액 `$4,767,000`을 Temple로 적는다. 정확한 예외 종류·법적 서명 원문은 확보하지 못했으므로, 아래 Temple 차감은 **조건부**다. Temple 기본급 자체는 기존 15인 합계에 이미 포함됐다.

## 3월 25일 계산 증인

`2021-03-25`에 두 예외가 실제로 §6(m)(2)에 따라 Team Salary에 남아 있고 다른 사용·소멸·포기가 없으며, 보도된 2월 27일 변경이 그대로 적용된다는 **위험 시험 가정**을 둔다. 이 표는 `WAIVED_PAY`, `OTHER_FA_RIGHTS`, `UNSIGNED_FIRSTS`, TPE/DPE, 기타 조정을 포함하지 않는다.

| 조건 | 2/27 미사용 비납세 MLE | 2/27 미사용 BAE | 3/25 조건부 금액: 두 항목 ×120/146 | 기존 F1 여유 `$5,609,972`에서 남는 금액 |
|---|---:|---:|---:|---:|
| Temple 사용을 입증하지 못한 넓은 시험 | $9,258,000 | $3,623,000 | $10,587,123.29 | −$4,977,151.29 |
| Temple `$4,767,000`을 비납세 MLE로 사용했고 다른 차감이 없을 때 | $4,491,000 | $3,623,000 | $6,669,041.10 | −$1,059,069.10 |

계산: `MLE_remaining = 9,258,000 − 4,767,000 = 4,491,000`; `factor = (146 − 26)/146 = 120/146`; `(4,491,000 + 3,623,000) × 120/146 = 6,669,041.0958...`. 달러 소수 둘째 자리 표시는 반올림이며 팀 원장의 센트 확정값이 아니다. BAE가 사용·소멸했거나 §6(m)(2) 산입 조건을 충족하지 않았다면 실제 예외 부담은 이 표보다 작다. **두 예외가 모두 산입되는 분기는 다른 잔여액을 0으로 놓아도 기존 비납세 한도를 초과한다.**

## F1 판정과 다음 증거

- **사실:** 평년 CBA의 감소 규칙, 2020–21의 146일 정규시즌과 캡 동결. 2월 27일 변경은 당시 2차 예외 장부에 명시되며, 수정된 원문은 미확보다.
- **추론:** Temple MLE 사용과 양쪽 예외의 §6(m)(2) 산입을 모두 가정하면 3월 25일 약 `$6.669m`의 위험 시험값이 나온다. 이는 기존 비납세 여유보다 `$1.059m` 크다. **예외 자격 보유**와 **Team Salary 산입**은 다른 질문이다. Chicago가 §6(m)(2)의 특정 산입 조건을 충족했는지는 확인하지 못했다.
- **후보/정본:** 새 사건 후보·작가확정은 없다. F1 `R_CHI` 전체는 `null`, 비납세 자격과 거래 matching은 `HOLD`다. 이 시험값을 실제 Chicago 급여나 납세 확정으로 승격하지 않는다.
- **다음 회수:** 2020–21 변경된 예외 감소 조항 원문, Temple 계약의 실제 예외 분류, 당시 Bulls cap sheet와 §6(m)(2) 트리거/BAE/TPE/DPE 이력, 방출잔액·FA/1R 보류액. 같은 사건의 송출/수취 charge를 다시 계산한다.

검증은 날짜 차이와 유리수 산술만 자체 재현했다. Claude CLI에 별도 반증 검토를 요청했으나 60초 이상 출력 없이 대기해 중단했으므로 `ATTEMPTED / NO_RESULT`이며 독립 검수로 세지 않는다. Anti-Gravity·NotebookLM·source-blind는 이번 증인에 `NOT_RUN`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, `manuscript_allowed=false`.
