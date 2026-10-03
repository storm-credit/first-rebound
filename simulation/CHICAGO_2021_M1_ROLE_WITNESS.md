# Chicago 2021 M1 정상 가용일 5인 조합 증인

**조건부 수학 검산. 실제 분·경기·교대·건강·등록·계약 통과가 아니다.**

[승인된 M1](../canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json)과 [G1A 방향](../canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json)의 Markkanen PF32·Caruso SF4분 감소를, [기존 구판 R21A](CHICAGO_2021_22_ROLE_PLAN_INPUTS.json)의 5인 검산과 구분했다. 구판은 보존한다.

## 배분과 시계

| 자리 | 조건부 분 합계 |
|---|---|
| PG | LaMelo32 + Coby10 + Caruso6 =48 |
| SG | LaVine34 + Coby8 + Caruso6 =48 |
| SF | 주인공28 + Duarte14 + Caruso6 =48 |
| PF | Markkanen32 + 주인공4 + Young12 =48 |
| C | Carter28 + Young8 + Bradley12 =48 |

주인공32·Markkanen32·Caruso18분. 기존 대비 주인공 SF+4/PF−4, Markkanen PF+4, Caruso SF−4이고 다른 선수의 총분은 같다. [JSON의11개 조합](CHICAGO_2021_M1_ROLE_WITNESS.json)은 매 조합5명이 서로 다르고 LaMelo 또는 LaVine 한 명 이상이 남는 **순서 없는** 48분/240팀분 성립 증인이다. 저장 합계도 조합과 일치해야 한다.

## 검산이 인증하지 않는 것

- Duarte/Wieskamp 정확 지명·Caruso/Bradley 수락·전체15명 명단은 여전히 후보/조건이다.
- Markkanen M1 작품 방향은 선택됐지만 정확 신고·급여 전체·계약 실행 인증과 별개다.
- 모든 사용 선수가 적법하게 등록되고 가용하다는 조건은 증명하지 않았다. 정상일 조합을 건강/82경기/선발/QO 기준 충족으로 환산하지 않는다.
- 2분 단위·행 순서는 수학적 구성이다. 실제 교대, 첫5명, 공격 효율, 선수 만족도, 연장 유무를 선택하지 않는다.
- 배분0인 비교 명단 선수도 비용과 권리를 갖는다. Caruso4분 감소는 급여4분 비례 감액이 아니다.

검사: `python -B tools/check_chicago_2021_m1_role_witness.py`.
음성 대조: 5인 중복·분/배분 변경·창조자 부재·합계 위조·출처 삭제·포지션 위반·실제 사건/계약 승격을 거부한다. [테스트](../tests/test_chicago_2021_m1_role_witness.py).

2026-10-04 작업 시작 시점 상태: F0/5·A0/3·K0/4·법적12HOLD·최종 회차 기능0·실제Pack0. 현재 전역 판정은 [프로젝트 상태](../PROJECT_STATE.md)와 [게이트](../control/DESIGN_GATE.md)가 우선한다. PROJECT_FREEZE v0.30 PARTIAL·설계/원고CLOSED·원고0.

`LaMelo_pick4`는 [freeze의 v0.30 O-15E2](../canon/PROJECT_FREEZE.md)에서 작가가 이미 고른 2020 Chicago4순위의 식별자다. 미선택2021 Duarte/Wieskamp와 다른 권위이며 이번에 재선택하지 않는다.
