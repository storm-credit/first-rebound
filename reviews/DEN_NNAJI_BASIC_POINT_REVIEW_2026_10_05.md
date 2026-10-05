# Denver 원역사 신인 기본급·보너스 분기 후속

기준 main `259b5db` / PR417 이후. **공개 기본급 입력 보완**, 전체 비용 PASS는 아니다.

## 회수한 입력과 계산

[SalarySwish 계약 이력](https://www.salaryswish.com/players/zeke-nnaji)의 `ROOKIE SCALE CONTRACT Nov30 2020 / 2020–21` 행을 web 본문과 로컬 HTTP200으로 직접 읽었다. 기본급·cap hit·guaranteed 열은 각각2,379,840이다. [입력 원장](../research/DEN_NNAJI_2020_HISTORICAL_BASIC_POINT_2026_10_05.json)에 HTML 및 행 지문·출처 성격·역할을 보존했다. 공개 데이터 공급자의 계약 이력표이며 리그 계약 접수증이나 완전한 charge 인증이 아니다. 성과 보너스 열의0을 trade bonus 없음으로 바꾸지 않는다.

기존 #22 scale100%1,983,200과의 비율은120%다. 원역사 Denver에 남는 Nnaji22에만 이 공개 기본급 점을 적용한다. 대체세계에서 Orlando로 보내는 Nnaji24의 계약과 혼동하지 않는다. 대체 Denver의 Bey22는 미선택80~120% 전 구간을 보존한다.

| 기본급 차액 | 이전 입력 구간 | 현재 입력 구간 |
|---|---:|---:|
| Bey22 − Nnaji22 | −793,280~+793,280 | −793,280~0 |
| Hartenstein − McGee | −2,579,436 | −2,579,436 |
| 두 항목의 합 | −3,372,716~−1,786,156 | **−3,372,716~−2,579,436** |

[비교 생성기](../tools/build_den_f5_cost_comparator.py)와 [출력](../research/DEN_F5_COST_COMPARATOR_2026_10_05.json)은 역사 상한138,928,000과 이번 입력을 함께 읽는다. 대체 Bey 비율을 선택하지 않아도 `Gamma_Gordon + Gamma_Clark + DeltaOther ≤ 2,579,436`이면 기본급 차액으로 흡수된다. 세 상단은 아직null이며, 단순히 현재 표의 급여 합이 작다는 이유로 전체 비용을 인증하지 않는다.

## 별도 보너스 조사

[조사 원장](../research/DEN_GORDON_CLARK_BONUS_SCREEN_2026_10_05.json)에 실제 회수 범위를 기록했다.

- Josh Robbins의 2018-07-02 Orlando Sentinel 원보도는 옵션 없는4년 **합의**를 확인하지만 보장율·trade bonus 부재를 확인하지 않는다.
- Clark의 당시 보장 조건은 Keith Smith에 귀속한 Hoops Rumors 재인용 본문으로 회수했다. 원 트윗 본문 미회수와 구분한다.
- Pincus의 명시적인 `Trade Kickers: None`은 회수하지 못했다. 후대 Gordon 계약의3%나 성과 보너스0을2021 조건으로 역산하지 않았다.

공식2017 CBA XXIV2(a)(ii)의 잔여 기본급15%와 VII3(b)의 보호 비율 배분 규칙을 구분했다. 남은 연도가2020–21/2021–22뿐이라는 조건에서 전체 연간 기본급을 사용한 넓은 보너스 스크린은 Gordon5,181,818.25 + Clark615,000 =5,796,818.25다. 현재 기본급 절감 허용폭보다3,217,382.25 크므로 **이 넓은 경로만으로 종료할 수 없다**. 이는 실제 비용 초과·계약 불가능 판정이 아니다. 계약/보호/남은 기본급 근거를 좁히거나 다른 유효한 전체 구간 증명을 사용할 수 있다. 두 Gamma는 양 세계의 **차이**이므로 이 스크린을 검증된 차액으로 대입하지 않는다.

## 검수 및 역할

독립 Codex `/root/independent_finish_scope`는 실제 공개 계약 이력표를 읽고 기본급 입력의 한정 채택과 계산을 수용했다. 실제 변경 JSON/MD/생성기/S2/status와 넓은 보너스 스크린도 재검문했고 실질 결함 없이 수용했다. `--check --self-test` 통과·가짜 종료6종 거절·추가 법적 승격0이다. S2 원장 실행에서도 등록2 PASS/나머지10 HOLD·F/A/K0·시즌false·원고false를 확인했다.

이번 입력에 Antigravity/NotebookLM/Claude를 새로 실행하지 않았다. 직전 PR417의 Antigravity는 검색4단계 후 답변빈값, NotebookLM은 초기 파생 패킷 회수이며 이번 신인 입력의 분석으로 계수하지 않는다. 전체 source-blind는 미완료다.

**사실/보도:** 공개 기본급 행과 위 원보도·재인용의 명시 범위. **추론:** 차액 구간 및 조건부 넓은 스크린. **후보:** 전체 비공통 비용 차액을 닫는 비교 경로. **작가확정:** 기존 F5 승인만 사용, 신규0.

법적2완료/10HOLD·F0/5 A0/3 K0/4·최종회차0·실제Pack0·미완료 큰묶음6. freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0. freeze/gate의 내용과 이미 검수한 A01 원본 지문은 변경하지 않았다.
