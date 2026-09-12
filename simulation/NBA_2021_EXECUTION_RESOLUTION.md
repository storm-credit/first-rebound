# O-15F14-L — 픽 종료·McGee 예외·Chicago 잔여 항목 회수

- 기준: PR #165, main `32a2b738c57981cf4892d61627827d0d1190f51d`.
- 사실 권위: [출처 원장](../research/NBA_2021_EXECUTION_RESOLUTION_SOURCES.json). 조건부 분기·산술: [동명 JSON](NBA_2021_EXECUTION_RESOLUTION.json).
- 판정: `REPORTED_TERMS_RECOVERED / EXACT_EXECUTION_HOLD`. 미래 결과·계약 채택은 하지 않았다.

## 1. Gordon 후행 픽의 마지막 보호 연도와 종료

[SalarySwish의 Gordon 거래 이력](https://www.salaryswish.com/trades/players/aaron-gordon)은 후행 1R의 2025~27 top5 보호와 모두 미전달일 때 의무 소멸을 기재한다. 이 필드는 이전 [자산 연결](NBA_2021_ASSET_CHAIN.md)의 ‘종료 미확보’를 보도 회수 수준에서 대체한다. 선행 1R 전달이 늦어지는 연결은 [후대 CBS 보도](https://www.cbssports.com/nba/news/which-traded-nba-future-first-round-picks-hold-the-most-value-ranking-all-47-that-have-changed-hands/)와 대조했다.

| 선행 1R 실제 전달을 가정한 연도 | Gordon 첫 검토 연도 | 조건부 후행 처리 |
|---:|---:|---|
| 2023 | 2025 | 최종 6~30이면 전달, 1~5이면 다음 해, 2027까지 보호되면 보고상 소멸 |
| 2024 | 2026 | 동일 보호 규칙을 2026~27에 적용 |
| 2025 | 2027 | 그해 최종 6~30이면 전달, 1~5이면 보고상 소멸 |
| 선행이 2R로 전환 | 미확정 | 선행 1R 전달로 간주하거나 2027을 자동 지정하지 않음 |

이 표는 미래 성적을 선택하지 않는 분기 시험이다. 선행의 2025·2026 2R 전환과 후행의 소멸은 서로 다른 의무다. 최종 실제 2025 순번, 실제 Hampton 대가, 거래 요약의 Clark 금액은 입력하지 않았다. Nnaji24 대가 방향은 기존 승인을 유지한다. 소유권·우선권 전부를 검증한 것도 아니다.

## 2. McGee의 픽과 독립된 수취 예외

[ESPN의 2021년 3월 25일 보도](https://www.espn.co.uk/nba/story/_/id/31133711/sources-denver-nuggets-acquiring-javale-mcgee-cleveland-cavaliers)는 2023 DEN 2R의 top46 보호와 2027 DEN 2R의 무보호를 명시한다. [FearTheSword의 동시대 보도](https://www.fearthesword.com/2021/3/25/22350288/cavs-deal-javale-mcgee-to-nuggets)도 일치한다. 공식 공지에 없던 2027 보호 필드를 이제 보도 근거로 채울 수 있다. 2023이 보호됐을 때의 종료·이월 문구는 여전히 미확보다. 무기재를 자동 소멸로 해석하지 않는다.

[Hartenstein](https://www.salaryswish.com/players/isaiah-hartenstein)·[McGee](https://www.salaryswish.com/players/javale-mcgee)의 공개 기본급을 사용한 시험은 다음과 같다.

| 수취 경로 | 계산 | 판정 |
|---|---:|---|
| Hartenstein만 outgoing으로 합산 | $1,620,564 × 175% + $100,000 = $2,935,987 | McGee $4,200,000보다 $1,264,013 부족 |
| 기존 Grant TPE에 McGee 전액 수취 | 보고 명목액 $9,500,000 − $4,200,000 = $5,300,000 | 다른 사용·정확 가용액이 확인되면 적용 가능한 별도 경로 |

[NBA 예외 목록](https://www.nba.com/news/trade-exceptions-what-they-are-and-why-they-matter)은 이 예외의 출처를 뒷받침한다. 최초 발행은 2021-03-16, 페이지 수정은 2022-09-22다. 금액은 반올림 보도값이므로 정확 원장액으로 채택하지 않았다. [동시대 거래 기사](https://bleacherreport.com/articles/2938141-nuggets-updated-roster-salary-cap-after-reported-javale-mcgee-trade)에서도 같은 예외 사용을 확인했다.

Hartenstein을 보낸 급여를 기존 Grant 예외에 더하지 않는다. Gordon 거래의 matching도 이 예외와 합치지 않는다. Denver의 [후반 apron 시험](BOSTON_DENVER_2020_21_PAYROLL.md)은 별도 팀 한도이며, 예외가 있다는 이유로 면제되지 않는다. 보도 경로는 회수했지만 대체세계의 정확 TPE 잔액은 null이다. 코드는 수취액 전액이 예외의 본체 금액 안에 드는지 보수적으로 시험하며 CBA의 추가 거래 허용액을 사용하지 않는다. 이 전액 충족 시험의 false를 거래 불법 판정으로 사용하지 않는다.

## 3. Chicago의 오래된 비용과 캠프 방출 구분

[Asik 급여 제거 보도](https://www.hoopsrumors.com/2019/06/bulls-receive-cap-relief-for-omer-asik.html)는 2019–20의 $3m에 관한 자료다. 해당 수치를 2020–21 잔액으로 가산하거나 현재 R에서 다시 차감하지 않는다.

캠프 3명 [Vonleh](https://www.salaryswish.com/players/noah-vonleh)·[Norvell](https://www.salaryswish.com/players/zach-norvelljr)·[Shittu](https://www.salaryswish.com/players/simisola-shittu)의 공개 표시는 보장 0이다. 기존 연간 전액 시험 $4,372,601과 실제 정산액은 다른 값이다. 부상 정산·분쟁 등의 전체 금액을 확인한 것은 아니다.

[2017 CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)의 I 1(cc)/(hhhh), VII 4(a)(2)/(d)를 연결하면 계약 완료 선수와 waiver로 해제된 선수는 구분된다. 따라서 **이 캠프 방출 자체에서 새로운 Veteran Free Agent 보류액이 생긴다고 가산하지 않는다.** 이는 조항을 적용한 해석이며 기존 권리·방출 급여·별도 합의까지 없다고 인증한 것이 아니다. 앞서 처리한 타팀 계약 3건과 빈자리 부담을 재차 차감하지 않는다. [Chicago R 원장](CHICAGO_2020_21_RESIDUAL_COMPONENTS.md)의 실제 합계는 계속 null이다.

## 4. 종료 범위와 검증

새로 회수한 필드는 후행 보호 종료, McGee 2027 보호와 수취 예외, 과거 비용의 시즌 구분이다. 계산 5개 검사는 보호 경계·종료, 선행 전환 오용, 2R 미확인 종료, 예외 분리·정확 가용액, 미채택/미확정 보존을 점검한다. 조건부 예시를 미래 결과로 저장하지 않는다.

신규 5개 PASS·JSON 재현·diff 검사, 자체 검토 `NOT_INDEPENDENT`. 네 K 묶음 전체 종료는 0이고 `author_locked=false`, `season_selected=false`, v0.30 PARTIAL·설계/원고 CLOSED다. 남은 정확 필드는 [채택 준비 색인](CHICAGO_2020_21_ADOPTION_READINESS.md)에서 최신 확보분과 함께 관리한다.
