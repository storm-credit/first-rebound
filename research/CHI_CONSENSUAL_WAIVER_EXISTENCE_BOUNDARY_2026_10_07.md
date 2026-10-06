# Chicago — 합의 면제의 존재와 실제 매칭 통과 경계

2026-10-07 / main `76cd80b` / **조건부 수학 증인, 법적 행 승격0**. [증인 JSON](CHI_CONSENSUAL_WAIVER_EXISTENCE_BOUNDARY_2026_10_07.json).

[원 2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)의 VII§7(d)(3), PDF248/인쇄226은 선수와 양도 구단이 거래 보너스 전부 또는 일부의 면제를 합의하도록 허용한다. 연결 heading `(d) Other`는 PDF247이다. VII3(b)의 보너스 Salary 배분과 VII6(j)의 매칭 요건은 그대로 적용한다.

기존 원보너스 모델 구간을 Theis γT∈[0,750,000], Green γG∈[0,227,697.15]로 유지한다. 법규상 합의할 수 있는 수학 변수 q를 다음처럼 놓으면 매칭 가능한 후보가 존재한다.

```text
q = max(0, γT + γG − 175,985.75)
qT = min(γT, q)
qG = q − qT
0 ≤ qT ≤ γT, 0 ≤ qG ≤ γG
6,517,981 + γT + γG − q ≤ 6,693,966.75
```

이는 **모든 원보너스 값에 대해 합의 가능한 면제량이 존재한다**는 `∀γ∃q` 증명이다. 모든 실제 면제 선택이 통과한다는 `∀γ∀q` 증명이나 선수의 승낙 보증이 아니다. JSON의9경계 조합을 Decimal로 계산했으며 최대 후보 면제 합계801,711.40이다. 이는 실제 지급·위법·면제 금액이 아니다. Theis/Green을 동시 합산하므로 양수 Green 보너스를 최저급 예외로 우회하지 않는다.

S2는 전체 허용 입력이 통과해야 한다. 현재 허용 입력에는 면제 없는 경우도 남아 있고 기존 무면제 상단 반례가 보존된다. **현재 CHI_MATCHING_RULE은 HOLD**다. 실제 보너스·면제·선수 승낙·Boston 합의·새 작가 financial 선택은 모두null이다. 이 조건부 경로를 소개한 것으로 검증 기준을 바꾸거나 재승인을 받은 것으로 처리하지 않는다.

조항은 면제한 기존 계약의 extension/renegotiation을 거래6개월 뒤 또는 원래 가능일 중 늦은 날까지 막는다. 3/25 기준6개월 경계는9/25다. 만료 뒤 새 FA 계약은 기존 계약 연장과 구분하지만, 정확 2021 계약을 자동 통과시키지 않는다. 후속 계약·급여 경로에서 이 제한을 검문해야 한다.

새 동시대 Causeway Street 기사와3/29로redirect된 BI 자료는 완전한 pretrade kicker 목록이 아니다. 선수 누락으로 Γ0을 만들지 않는다. [NotebookLM 원 CBA 분석](../reviews/D1_TRADE_PROOF_TRANSFER_NLM_2026_10_06.json)은 회수됐으나 잘못 쓴7(e)(3)을7(d)(3)으로 정정하고, 비납세 공식의 누락된max 분기와 사적 Exhibit4 필수 인증 요구를 기각했다. 수정 거래에 원거래 승인을 그대로 복사할 수 없다는 논리 반례만 원문·산술로 확인했다. NLM 출력 자체는 사실 인증 권위가 아니다.

법적10PASS/2HOLD·F법적3/5·A0/3·K0/4·시즌미확정·미완료큰묶음6·v0.30 PARTIAL·설계/원고 CLOSED·원고0.
