# R01 O-15G15M — Claude 제한 반증과 결과 단독 편집 검수

- 대상: [G15M Bacon·1R cap hold 원장](../research/O15G15M_BACON_GUARANTEE_AND_ROOKIE_CAP_HOLD.md).
- 상태: `LIMITED_REASONING_REVIEW / SOURCE_BLIND_EDITORIAL_RUN`; 계약서·CBA 원문을 Claude가 독립 수집한 감사나 G16 통과가 아니다.

| 호출 | 목적·입력 차단 | 결과 | 판정 |
|---|---|---|---|
| Claude CLI Haiku, 도구 없음, 2턴 | Bacon 조기/후기 방출과 Mobley3 120% hold 주장에 논리 비약이 있는지 요청 | 검토 대신 검토 준비와 재질문만 출력 | `NOT_RUN`; 성공으로 세지 않음 |
| 새 짧은 반증 호출, 도구 없음, 2턴 | Bacon의 원계약 동일·8/8 waiver와 Mobley3 미서명 1R hold 두 문장만 제시 | waiver **요청/통과**와 보호급여 의무의 성립 조건을 더 명시하라고 지적. CBA 적용 시점/선수 자격도 확인 필요라고 표시 | 유효한 날짜·비용 조건을 본문에 추가. 2017 CBA §4(e)(1)과 실제 #3 Mobley 지명은 Codex가 NBA/NBPA 원문으로 확인했으므로 Claude의 ‘미확인’은 Claude에게 원문을 주지 않은 범위 표시다. |
| 새 결과 요약만 준 source-blind 호출, 도구 없음, 2턴 | 앞 출처·계산 없이 최종 요약만 제시해 독자 혼동 지점을 요청 | Bacon `−1`과 Mobley 미서명 `0`이 다른 사건인지, waiver 전 보호액과 방출 뒤 dead charge `0`의 연결이 불명확하다고 지적 | G15M의 **자리와 급여의 인과** 문단으로 구분·조건을 보강. |

Claude 호출들은 원자료를 재검증하지 않았다. NBA 공식 거래일, NBPA의 2017 CBA, 비공식 계약 보호액의 출처 등급을 본문에서 유지한다. 신규 작가확정 0건, 원고·설계 게이트 `CLOSED`.
