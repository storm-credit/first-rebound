# R01 O-15G15N — 계약 산술 제한 반증과 결과 단독 맹점 검수

- 대상: [G15N Orlando 공통 계약 비용](../research/O15G15N_ORLANDO_COMMON_2021_22_CONTRACT_CHARGES.md).
- 상태: `LIMITED_ARITHMETIC_REVIEW / SOURCE_BLIND_EDITORIAL_RUN`. Claude에 NBA/CBA 원문을 독립 수집시키지 않았다. G16 독립 감사 또는 작가 승인과 다르다.

| 호출 | 입력 범위 | 결과와 처리 |
|---|---|---|
| Claude CLI Haiku, 도구 없음, 2턴 | 8개 charge 숫자, Cole/Okeke 인센티브, #24 2년차 스케일과 원역사 #22 금액만 제공 | `8명 $84,477,366`, `#24 ×120% $2,303,040` 산술 오류 없음. 그러나 **#24가 원역사 #22 Nnaji 의무를 부담한다**는 방향의 제안은 대체 드래프트 픽 차이를 지우므로 기각. 120%는 가능한 최대액 중 **조건부 계약 시험**이라고 본문에 명시. |
| 별도 source-blind 편집 호출, 도구 없음, 2턴 | 출처와 앞 판단 없이 결과 요약만 제공 | 8계약+2계약의 합산 구조, #24 비용 발생 조건과 10계약 합계에서의 제외 여부가 독자에게 모호할 수 있다고 지적. 본문에 `8+2=10`과 2020년 서명·2021–22 유효·120% 가정, Nnaji 미포함을 명시. |

계약표와 NBA 공식 분류는 Codex·NotebookLM이 확인한 같은 원문 계보이며 Claude가 별도 증거를 회수하지 않았다. 숫자 자체의 최종 대체 Team Salary 판정은 `HOLD`, 신규 작가확정 0건, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
