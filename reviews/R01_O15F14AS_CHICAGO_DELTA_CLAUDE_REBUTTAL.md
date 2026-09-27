# O-15F14-AS — Chicago 공개 급여 차액의 제한 독립 반박

- 대상: [15인 공개 급여 차액](../research/O15F14AS_CHICAGO_PUBLIC_ROSTER_DELTA.md)과 [F1 거래 직후 급여 범위](../simulation/CHICAGO_2020_21_TAX_BOUND.md).
- 판정: `NAMED_ROSTER_COMPARISON_VALID_AS_CONDITIONAL / F1_EXACT_EXECUTION_HOLD`.

## 반박에서 수용한 것

Claude CLI에 도구 접근 없이 AS의 수치·결론을 요약해 반례를 요청했다. CLI는 답했지만 저장소나 NBA 원문을 독립 조회하지 않았다. 가장 중요한 지적은 **이름 있는 15인의 원역사 대비 차액으로 명단 밖 부담 `R`의 상한을 증명할 수 없다**는 것이다. AS도 `R=null`로 두었으며, 원역사와 대체세계의 `R`이 같다는 근거를 제시하지 않았다. 따라서 공개 원역사 15인보다 최소 `$1,951,061` 낮다는 산술이 맞더라도 3/25 Chicago의 비납세 거래 자격이나 Theis/Green 정확 실행은 `HOLD`다.

Salary Sport의 보관 표와 대체 경로의 공개 계약 입력은 리그의 동시점 Team Salary 장부 두 건이 아니다. 일부 공통 선수의 계약 금액은 재사용되며, 원역사 보관 표의 작성 시각·포함 항목도 거래 승인 시각과 일치한다고 인증하지 않았다. 차액 검사는 **같은 급여 정의로 이름 있는 자리만 비교하는 조건부 검사**로 한정한다.

## 원문 대조 후 기각하거나 좁힌 것

Claude는 거래 **전** Team Salary를 먼저 확정하지 않으면 거래 후 비납세 분류를 쓰는 것이 순환적이라는 취지의 반례도 제시했다. 이 지적을 분류 규칙으로 채택하지 않는다. [2017 NBA–NBPA CBA Article VII §6(j)(1)(i), (iii)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)는 해당 팀의 **post-assignment Team Salary**가 Tax Level을 넘는지로 두 matching 갈래를 구분하고, 송출 선수의 **pre-trade Salary**와 수취 선수의 **post-assignment Salary**를 비교한다. 따라서 필요한 것은 거래 직후 팀 전체 부담과 각 계약의 적용 charge를 **같은 가상 거래**에 대해 계산하는 일이다. 거래 전 팀 전체 급여만으로 어느 갈래인지 결정하지 않는다. 조항은 실제 리그 승인서나 2020–21 수정 합의의 미공개 세부사항을 대신하지 않는다.

## 다음 증거의 정확한 형태

1. 2021-03-25 대체 Chicago의 거래 **직후** Team Salary에 들어가는 계약 외 모든 적용 항목의 닫힌 목록 또는 합계 상한. 기존 알려진 상단 `$127,017,028`을 쓸 때 비납세 증명에는 `R≤$5,609,972`가 필요하다. 4/16 원역사 dead money `$97,261`은 이 거래일 대체 값이 아니다.
2. 같은 거래에서 Chicago가 보낸 Gafford/Kornet과 받은 Theis/Green의 규정상 **pre-trade/post-assignment charge**, 다른 당사자의 수취·송출 구조와 2020–21 수정 규칙. 기본급 일치 시험의 `$175,985.75` 여유는 전체 charge 판정이 아니다.
3. 항목 1·2가 충족될 때만 §6(j)(1)의 해당 matching 갈래를 고르고 F1의 나머지 등록·픽/거래 순서를 결합한다. 원역사 급여 차액으로 `R`을 대체하거나, Claude의 잘못된 사전 팀 급여 요건을 새 게이트로 추가하지 않는다.

**검토 범위:** Claude는 논리 반례 제시자이며 원자료 재확인자나 별도 NBA 급여 출처가 아니다. Codex가 CBA 조항과 기존 산술을 직접 대조했다. Anti-Gravity·NotebookLM·별도 source-blind는 AS 차액에 대해 실행하지 않았다. 새 작가확정 0건, F `0/5`·A `0/3`·K `0/4`; 7개 매크로 중 1완료·1진행·5대기, 미완료 6개. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.
