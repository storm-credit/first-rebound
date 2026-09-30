# D1 S2 이행 — 검증 범위

- 기준: `main e5e8661`, [실제 작가 선택](../canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json).
- 대상: [프로토콜](../control/CHICAGO_2020_21_D1_S2_PROTOCOL.md), [초기 검문 원장](../control/CHICAGO_2020_21_D1_S2_REGISTER.json), [검사기](../tools/check_chicago_d1_s2.py).
- 등급: `CODEX_SELF_REVIEW / INDEPENDENT_REVIEW_NOT_RUN`. 도구 검사 성공은 원자료 인증이 아니다.

## 확인

1. 선택된 것은 S2 기준 한 개다. H00/H10/H01/H11, 거래일 R 상한·정확 차지, K1/L2 시즌·추첨을 잠그지 않았다.
2. null/무한 상한, 한도 횡단, 근거/전수 범위 미확인, 누락된 1R→2R 전환 분기에는 통과를 주지 않는다. 검증된 구간 하한이 한도를 넘으면 FAIL이다. 작위적인 잔액 상한은 검수자의 `source_verified` 인증을 받을 수 없다.
3. Boston/Orlando·Denver/Cleveland 비용을 각 팀/일자별 필드로 나눴다. 기준선이 있다고 실제 하드캡이 발생한 것은 아니며, 적용 규칙·전수 구성도 별도 요구한다.
4. S0 시기 정확 실행 수와 S2 법적 필드 수는 구분한다. 초기 F는 모두 HOLD, A0/3·K0/4다. CLOSED/원고 불허를 변경하지 않았다.
5. 현재 설계 샘플의 출처 해시가 DESIGN_GATE 변경으로 2건 STALE임을 잡았다. S2 결정/규칙을 생성기의 출처에 추가하고 두 샘플을 재생성했다. allowed_facts·신체 상태·시즌 결과는 승격하지 않았으며 실제 회차 Pack은0이다.

## 실행 결과

- `check_chicago_d1_s2.py --self-test`: null/상한/분기 누락 등 부정 통제와 초기 원장 검사 PASS.
- `build_cp2_design_packets.py --check`, CP2 변조/경계 11개 테스트: PASS.
- JSON·변경 문서의 로컬 링크·`git diff --check`: PASS.
- 새 Antigravity 원자료·NotebookLM 분석·Claude 반증·source-blind: **NOT_RUN**. 앞서 급여 화면의 NotebookLM 분석과 Claude 시간 초과를 이 규칙 문서의 독립 검수로 재사용하지 않는다.

G16/G17을 충족하는 전체 독립 검수는 남았다. 7행 1완료·2번 진행·3번 조건부 선행·4~7 대기, 미완료6. freeze PARTIAL·설계/원고 CLOSED.
