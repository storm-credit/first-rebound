# O-15F14-L — Chicago 명단 밖 부담의 항목별 처리

- 기준 main: PR #161 / `042321496cde09219bbafae2d3918ee74a44daf3`.
- 상태: `PARTIAL_COMPONENT_SCREEN / EXACT_RESIDUAL_HOLD`.
- 출처: `research/CHICAGO_2020_21_RESIDUAL_SOURCES.json`. 판정 출력: 동명 JSON.
- K1/L2는 추천이며 H 방향 승인만 보존한다. v0.30 PARTIAL·설계/원고 CLOSED.

## 1. 이번에 좁힌 항목

검색 추출에 없던 구단 본문 세 건을 공개 HTML에서 읽었다. 기존 R은 실제값을 모르는 추가 부담이며, FA 보류액과 방출잔액을 구분해야 한다.

| 선수/항목 | 확인한 근거 | 2021-03-25 조건부 처리 |
|---|---|---|
| Dunn | [Atlanta 영입 공지](https://www.nba.com/hawks/atlanta-hawks-sign-free-agent-guard-kris-dunn), 2020-11-28 | 같은 자유계약 경로라면 Chicago의 종전 FA 보류액 0 |
| Harrison | [Utah 영입 공지](https://www.nba.com/jazz/utah-jazz-sign-free-agent-guard-shaq-harrison), 2020-12-09 | 같은 경로라면 종전 Chicago FA 보류액 0. 이후 Utah 방출은 Chicago 권리를 되살리는 사건으로 입력하지 않음 |
| Vonleh | [Brooklyn 영입 공지](https://www.nba.com/nets/news/2021/02/08/brooklyn-nets-sign-noah-vonleh), 2021-02-08 | 종전 Chicago FA 보류액이 있더라도 같은 경로에서는 계속 산입하지 않음. Chicago 방출 대가는 별도 미확정 |
| 빈 로스터 자리 | CBA VII 4(f), 인쇄187~188쪽; 기존 일반계약15명 | 정규시즌이며15명인 현재 조건에서 추가액 0 |

**네 항목을 제외했다고 급여 여유가 새로 늘어나지 않는다.** 이전 알려진 합계에 이 보류액을 넣은 적이 없으므로 다시 빼면 이중 차감이다. 기존 R 한도 **$5,609,972**를 그대로 유지한다. 위 표는 계약 경로를 유지했을 때의 판정이며 새로운 작가 승인 기록이 아니다.

## 2. 적용 규정과 남기는 경계

[2017 CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) VII 4(d)는 타 NBA팀 계약으로 이전 FA 금액이 종료되는 구조다. 4(a)(1)(i)의 방출 급여는 이와 별개다. 6(m)(2)의 예외액 산입에는 발생·이후 급여 조건이 있으므로 미사용 MLE/TPE 전액을 무조건 추가하지 않는다. 반대로 6(m)(3)의 apron 조정을 6(j)의 거래 판정에 일괄 적용하지 않는다. 실제 과거 예외 발생 경로가 미확인이므로 이 항목의 금액은 null이다.

[Chicago 거래 목록](https://www.basketball-reference.com/teams/CHI/2021_transactions.html)에서 캠프 방출 세 명과 다음 명시 거래인3/25를 대조했다. 이 목록에 중간 계약이 없다는 이유로 과거 dead/stretch·분쟁이 전부0이라고 인증하지 않는다. 실역사 Vučević/Hutchison 거래는 대체 경로에 복사하지 않는다.

Vonleh의 [SalarySwish 이력](https://www.salaryswish.com/players/noah-vonleh)은 기존 확보한 Chicago 보장0·별도 Brooklyn 잔액을 재확인했다. 새 사실 수로 세지 않는다. Spotrac의 검색 요약 금액은 상세 페이지403으로 채택하지 않았다. 보장0과 방출 정산액0은 같은 필드가 아니다.

## 3. R 원장에 남는 항목

| 코드 | 확인할 실제 구성 | 현재 |
|---|---|---|
| WAIVED_PAY | Vonleh/Norvell/Shittu의 Chicago 정산, 이전 적용 dead/stretch | 금액 미확정 |
| OTHER_FA_RIGHTS | 위 세 명 외 보유 FA 권리 및 제안 금액 | 인원·금액 미확정 |
| UNSIGNED_FIRSTS | 과거1R 권리의 미서명 보류액 또는 제외 근거 | 미확정; 현재 LaMelo/주인공 급여 중복 금지 |
| EXCEPTION_HISTORY | VII 6(m)(2)에 해당하는 예외 발생·사용 이력 | 미확정 |
| OTHER_ADJUSTMENTS | 적용 분쟁·은퇴 대가·조건부 합의·offer sheet | 완전한 목록 미확정 |

이는 잔여 분류이며 완전한 금액 원장이 아니다. 코드가 null을0으로 합산하거나 세 명의 FA 종료를 Chicago 전체 비납세 PASS로 바꾸지 못하게 했다. 원래15명 급여나60조건을 새 계산으로 세지 않았다.

## 4. 검증과 다음 입력

신규 검사3개는 계약일 전/당일·경로 변경, 출처 누락, FA와방출급여 혼동, 이중 차감, 정규시즌/개막 전의 빈자리 차이, 부분 목록의 무단 완결을 점검한다. 같은 범위의 세부 단언을 별도 검증 개수로 세지 않는다. JSON 재생성·기존 tax bound 검사도 대조한다. 자체검토 `NOT_INDEPENDENT`다.

다음은 WAIVED_PAY와 이전 FA/1R 권리 잔액의 실제 목록이다. 이번 세 선수의 영입 본문과 빈자리 규칙은 다시 찾지 않는다. R 실측·상한과 정확 거래 charge가 확보되기 전 F1은 열린 상태다. 전체 남은 큰 작업6개, 네K묶음 전체종료0개, 시즌·추첨 미채택 유지.
