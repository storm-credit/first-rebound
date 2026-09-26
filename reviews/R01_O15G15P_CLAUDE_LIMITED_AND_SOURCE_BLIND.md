# R01 O-15G15P — 2라운드 지명권 제한 반증과 결과물 단독 검수

- 대상: [G15P Orlando 33번 Herbert 권리 원장](../research/O15G15P_HERBERT_33_SECOND_ROUND_TENDER.md).
- 상태: `CLAUDE_LIMITED_RUN / SOURCE_BLIND_EDITORIAL_RUN`. 두 호출 모두 도구 없이 짧은 입력만 검토했다. CBA·NBA 원문 독립 수집 또는 G16 PASS가 아니다.

| 호출 | 출력 요지 | 판정 |
|---|---|---|
| Claude CLI Haiku 제한 반증 | Required Tender는 경력 RFA만의 제도이고, 새 2라운드 지명선수는 1라운드 rookie scale·그 cap hold를 따라야 한다고 주장. | **기각.** [2017 NBA–NBPA CBA Article I §1(ddd), Article X §4(a), Article VII §4(e)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)은 2라운드 Draft Rookie의 Required Tender와 **1라운드만**의 rookie scale hold를 명시적으로 구분한다. 원문과 상반된 모델 주장으로 ledger를 바꾸지 않는다. |
| Source-blind 첫 호출 | 최대 turn 수에 도달해 출력 없이 종료. | `NOT_RUN`으로 취급. |
| Source-blind 재호출, 결과물 요약만 입력 | 서명 미결 상태에서 선수 분을 배정할 수 없고, Orlando 기존 윙 깊이·오프시즌 이동 후 실제 역할을 정해야 한다고 지적. | **수용.** G15P의 서명 분기와 Orlando 윙 분 충돌 조건에 반영. New Orleans 쪽 빈 분·수비 역할도 별도 재계산 대상이다. |

Antigravity 타임아웃은 원문 확보 성공으로 세지 않았다. NotebookLM의 NBA 드래프트 결과와 SalarySwish 계약표는 Codex가 본 **같은 출처**이고, NotebookLM CBA 요약본의 누락은 전체 CBA 직접 대조로 보완했다. 신규 작가확정 0건, 원고·설계 게이트 `CLOSED`.
