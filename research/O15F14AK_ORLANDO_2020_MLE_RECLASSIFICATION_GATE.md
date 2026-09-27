# O-15F14-AK — Orlando 2020–21 MLE와 apron 제한의 재분류 조건

- 기준 `main` `b7c7712`, 2026-09-28 조회. 범위는 F2의 **Orlando hard-cap 발생 조건 한 항목**이다.
- 판정 `MLE_ONLY_RECLASSIFICATION_PATH_CONDITIONAL / F2_HOLD`. 작가확정이나 리그 승인 사건을 새로 만들지 않는다.
- [Claude 제한 반증과 원문 재대조](../reviews/R01_O15F14AK_ORLANDO_MLE_RULE_REVIEW.md)를 별도 기록한다.

## 1. 규칙과 당시 수치

[2017 NBA–NBPA CBA Article VII §6(e)(1), 인쇄 203–204쪽](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)은 비납세 MLE 사용팀의 Team Salary를 **사치세선 + `Tax Apron Amount` 이하**, 즉 여기서 쓰는 **apron 총액 이하**로 제한한다. `$138,928,000`은 두 항의 합계로 제시된 총액이며, 여기에 다시 더하는 증분이 아니다. 같은 CBA **VII §6(f)(5), 인쇄 205–206쪽**은 그해 비납세 MLE 계약이 모두 3시즌 이하이고 첫 시즌 **Salary+Unlikely Bonus 합계가 납세 MLE 이하**이며 다른 거래가 apron 초과를 막지 않는다면, apron을 넘기는 거래를 허용하고 **그 거래 때부터** 납세 MLE를 사용한 것으로 간주하는 전환 경로를 둔다. [NBA의 예외 설명](https://www.nba.com/news/free-agency-explained)도 Bird 재계약·최저급 계약 같은 초과 유발 거래를 예로 든다. 비납세 MLE를 썼다는 이름만으로 영구 hard cap이 확정되는 것은 아니다. 반대로 이 경로가 처음부터 납세 MLE 사용을 의미하지도 않는다.

[NBA의 2019–20 공식 캡 발표](https://pr.nba.com/nba-salary-cap-for-2019-20-season-set-at-109-140-million/)는 당시 납세 MLE `$5,718,000`과 cap `$109,140,000`을 공개했다. [NBA/NBPA의 2020–21 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)도 cap을 `$109,140,000`으로 동결했다. **2017 CBA §6(f)(2)의 전년 cap 변동률 공식이 2020–21 코로나 수정에서 이 항목에 그대로 적용된다면** 납세 MLE도 `$5,718,000`으로 유지된다. 같은 방식으로 이월된 기존 비납세 MLE `$9,258,000`과 2차 표의 apron 총액 `$138,928,000`도 이번 문서에서는 최종 리그 인증으로 쓰지 않는다. 2020 수정 합의의 해당 조항 원문/리그 예외 장부는 회수하지 못했으므로 이 값들은 규칙 이월 조건이다.

| 공개 입력 | 첫해 금액 | 보고 기간 | 출처 등급 |
|---|---:|---:|---|
| James Ennis III | `$3,300,000` | 1시즌 | [NBA 기사에 실린 동시대 1년 합의 보도](https://www.nba.com/news/nba-offseason-2020-nov-20-roundup)와 [선수 급여 이력](https://www.salaryswish.com/players/james-ennisiii). 구단의 11/25 재계약은 [공식 거래 연혁](https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf)에 있음; 정확 계약서는 아님 |
| Gary Clark | `$2,000,000` | 2시즌 `$4.1m` 보도 | [NBA 기사에 실린 동시대 2년 합의 보도](https://www.nba.com/news/nba-offseason-2020-nov-20-roundup)와 [선수 급여 이력](https://www.salaryswish.com/players/gary-clark). 구단의 11/23 재계약은 같은 공식 연혁; 계약 원문은 아님 |
| 위 두 건 합계 | `$5,300,000` | 둘 다 3시즌 이하라는 보고 | [2020-12 당시 MLE 배분표](https://www.hoopsrumors.com/2020/12/how-teams-are-using-202021-mid-level-exceptions.html)의 **2차 분류**. 2021-01~03 추가 사용·보너스 0 인증은 아님 |
| 납세 MLE 조건부 한도 | `$5,718,000` | 2020–21에 공식 동결 cap과 2017 CBA 공식을 이월 | 위 NBA 2019–20 발표 + 2020–21 발표 + CBA. 정확 2020 수정 조항은 미확인 |
| 두 보고 계약만 사용했을 때 차이 | `+$418,000` | `5,718,000−5,300,000` | 산술 여유. 다른 MLE 사용·unlikely 보너스가 있으면 감소 |

## 2. F2의 실제 경계

[당시 BAE 사용 추적](https://www.hoopsrumors.com/2020/12/how-teams-are-using-202021-bi-annual-exceptions.html)은 2020-12-31 현재 Orlando를 **사용하지 않은 팀**으로 표시한다. 이는 2021-03-25까지의 전수 부재나 리그 장부가 아니다. Orlando 공식 2020 거래 연혁은 위 두 재계약과 다른 일반 계약을 나열하지만, 예외 사용 방법·보너스·서명 후 수정 전체를 증명하지 않는다. CBA §8(e)(1)의 sign-and-trade **수취**, BAE 사용, 다른 금지 거래·추가 MLE 사용 여부를 아직 닫지 못했다. Clark의 3/25 송출은 2020년에 이미 사용한 `$2m` MLE 기록을 환불하지 않는다.

**조건부 추론:** 위 두 계약만 비납세 MLE 사용이고 추가 unlikely 보너스·다른 MLE 사용이 `$418,000` 여유를 넘지 않으며 두 계약 기간이 보고와 같고, BAE·sign-and-trade 수취 등 §6(f)(5)를 막는 사건이 없으며 2020 수정 규칙도 같다면, AJ의 Gordon 먼저 순서에서 캠프 전액 스트레스가 apron보다 `$76,411` 높게 나온 것만으로 **거래 불가능을 판정할 수 없다**. `$418,000`은 **MLE 재분류 자격의 금액 차이**이지 AJ의 `$76,411` **팀 급여 초과분을 상쇄하는 돈이 아니다**. 정확 조정 Team Salary가 실제로 apron을 넘게 하는 거래가 있다면 §6(f)(5)의 납세 MLE 전환 조건을 그 거래 시점에 확인해야 한다. 과거 캠프 계약의 가상 전액을 뒤늦게 더한 계산 자체는 전환 거래가 아니다. 실제 팀 급여가 apron 아래라면 전환 사건 자체가 발생하지 않을 수 있다.

이 법적 후보는 [AJ의 공개 급여 순서 화면](O15F14AJ_ORLANDO_TRADE_DAY_ORDER_SCREEN.md)에 **숨은 PASS를 추가하지 않는다**. AJ의 0보장 캠프 계약 연간 전액, Birch 전액, Teague 잠정 charge는 실제 3/25 원장이 아니며, 2020–21 정확 MLE·BAE·sign-and-trade 이력과 2020 수정 조항도 없다. 따라서 `hard_cap_trigger_verified=false`, `F2=HOLD`, F `0/5`·A `0/3`·K `0/4`, 시즌/픽·작가 최종 채택 없음. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`를 유지한다.

## 3. 다음에 필요한 원자료

1. 2020–21 수정 합의가 VII §6(f)(2)/(5)를 바꿨는지와 해당 시즌 공식 납세 MLE·apron 금액.
2. Orlando의 Ennis/Clark 원계약 기간·첫해 Salary 및 unlikely bonus, 추가 MLE 사용 및 BAE/수취 sign-and-trade 유무를 확인할 거래일 이전 장부.
3. 위 조건이 닫힌 뒤에만 AJ의 두 처리 순서 중 실제/대체 세계 적용 순서와 정확 중간 Team Salary·보너스/과거 부담을 결합한다. 발표 게시 순서를 리그 승인 순서로 바꾸지 않는다.
