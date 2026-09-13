# O-15G11 자체 검토 — 조합 비용과 하위 구조

- 기반 main: `05664c8be869173f2736dfdb9e659b88f7be9d77`, PR #177.
- 판정: `CONDITIONAL_ROLE_AND_FUNCTION_CHECK_PASS / NOT_INDEPENDENT`.
- 검토 대상: [역할 문서](../simulation/CHICAGO_2021_22_ROLE_PLAN.md), [입력](../simulation/CHICAGO_2021_22_ROLE_PLAN_INPUTS.json), [결과](../simulation/CHICAGO_2021_22_ROLE_PLAN.json), [Sub-Act 권위](../design/CP2_ACT_SUBACT_PACKET.json).

## 검토한 문제와 결과

| 문제 | 확인 결과 |
|---|---|
| G3의 옛 후보를 그대로 사용해 G7과 충돌하는가 | G7 DB1의 10 Duarte/39 Wieskamp로 상속. 15자리와 G3 정상 분 보존 |
| 포지션 합계만 맞고 같은 선수가 동시에 두 자리를 채우는가 | 네 운용안·세 단독 공백의 7개 증명에서 5명 중복 0·포지션별 48·총 240 일치 |
| 누군가의 시간을 공짜로 늘리는가 | R21A 대비 모든 증감 합계 0. Carter 공백의 Bradley +16/Green +12 등 수혜자와 공여자 명시 |
| 전개 담당자·센터가 없는 시간을 숨기는가 | 정상안에는 LaMelo 또는 LaVine, 두 가드 공백 개별안에는 지정 대체자 동시 출전. 센터 이중 공백은 C24분 부족으로 HOLD |
| 조건부 조합을 실제 교대/건강 증명으로 과장하는가 | 순서 없는 시간 분해만 저장. 36분 및 Young C24는 설계 시험값, 실제 날짜/의료/효율/총 시즌 기록 null |
| 같은 선택을 여섯 하위 구간에 복제하는가 | 역할 요청·엘보 판단·평가·계약 비용·라이브 패스·공동 권한으로 분리, 각 2개 성공 기준과 실패 대응 연결 |
| 계약 금액이 농구 능력을 자동 보장하는가 | E2 합의/공동 에이스/플레이오프 진출은 미확정. 실제 연간 분과 QO는 이번 표에서 도출하지 않음 |
| 권한과 정본을 건드리는가 | 감독/코치·에이전트·의료 권한 분리. 실존 대사/내면 및 원고 0. Freeze·기존 Act 배분·나머지 36 Sub-Act 동일 |

## 실행 검증

- `python tools/build_chicago_2021_22_role_plan.py --check`: 7개 증명·센터 부족 경계, 파생 JSON byte 재현 PASS.
- `python -m unittest discover -s tools -p test_chicago_2021_22_role_plan.py`: 6개 PASS. 중복 선수·없는 포지션·분 불일치·비가용 선수·전개 담당자 제거·과거 후보/원문 변경·시즌 승격·부족 은폐 반례 포함.
- 기존 `test_cp2_design_packets.py`: 6개 PASS.
- `build_cp2_design_packets.py --check`에서 변경한 구조 원문의 STALE 2건을 먼저 확인했다. A07/A08의 6단위만 변경됐고 Act 수/기간/분량, 나머지 36단위, 5약속, 장기 원장이 보존됨을 대조한 뒤 두 설계 샘플의 해당 해시를 갱신했다. 재검사 PASS.
- 변경 문서의 로컬 상대 링크/JSON·`git diff --check`와 외부 반영 전 전체 tree 대조를 수행한다. 원격 CI는 실제 조회 결과를 별도 보고하며 로컬 검사로 대신하지 않는다.

서로 다른 도구로 검사했어도 같은 작업자의 자체 검토다. 전체 G16 독립 검수와 G17 작가 승인은 미실시다. D3 날짜별 가용성·시즌 생산성/성적, D1 정확 실행, D6 딥리드 및 후속 설계가 남는다. 전체 1완료·6진행/남은 6개, `v0.30 PARTIAL`·설계/원고 CLOSED 유지.
