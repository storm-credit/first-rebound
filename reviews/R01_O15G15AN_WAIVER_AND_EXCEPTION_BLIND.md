# R01 O-15G15AN — source-blind 웨이버/예외 분기 검토

- 입력: [G15AN 문서](../research/O15G15AN_DETROIT_WAIVER_AND_EXCEPTION_BRANCHES.md) 텍스트만 Claude CLI `haiku --restricted --tools '' --max-turns 1`에 전달. 원문 링크·PDF·JSON 열람 없음. 독립 사실 확인으로 계수하지 않는다.
- 시작 권위 `main` `806a007`; 신규 작가확정 0건, 설계/원고 게이트 `CLOSED`.

| 지적 | 판정 |
|---|---|
| `$5m−$925,258=$4,074,742`, 네 Olynyk 직전 잔여값 | 계산 오류 지적 없음. Codex [검사기](../tools/check_o15g15an_detroit_waiver_branches.py)의 G15AL 교차 계산으로 별도 검산. |
| 웨이버 요청·48시간·미청구 계약 종료는 다르고, 재정 책임과 cap 차지 제거 시점도 구분해야 함 | 수용·유지. 2017 CBA 원문은 전자와 재정 책임을 확인하지만 후자의 8/6 실제 장부 처리는 `HOLD`. |
| 프로필 11+5로 완전한 권리/계약을 증명할 수 없음 | 수용·유지. NBA 8/2 자료의 Cook을 프로필이 빠뜨리는 반례와 날짜별 Smith QO 변경을 본문에 둠. |
| P0-B에서 McGruder 구계약 유지/방출 중 실제 사건 선택이 필요 | 수용·유지. 구계약 잔류는 **조건부 반증 분기**이며, 원역사 재계약·P0-B 실제 실행으로 승격하지 않음. |
| 정확 접수 시각, 예외 포기, 모든 FA Amount, 전체 Team Salary 부족 | 수용·유지. 다음 회수 항목이며 문서 완결 주장 없음. |

Claude는 네 분기 산술·날짜 표현에서 구체 오류를 찾지 못했다. 이것은 실제 캡 적격성 PASS가 아니다. Antigravity 팀 기사 본문 실패, NotebookLM 공식 두 소스 분석 성공, Codex 원문 대조 및 G16/G17 미완료를 [검증 레이어 기록](../control/RESEARCH_VERIFICATION_LAYER_V2.md)과 같이 분리한다.

**후속 정정 G15AP:** 이 검토도 Lee FA Amount가 빠진 초안에 대한 당시 기록이다. 네 분기 중 인원과 미충원 차지에 의존한 숫자는 [G15AP](../research/O15G15AP_SABEN_LEE_HOLD_AND_SEQUENCE_CORRECTION.md) 및 수정된 G15AN 표가 우선한다.
