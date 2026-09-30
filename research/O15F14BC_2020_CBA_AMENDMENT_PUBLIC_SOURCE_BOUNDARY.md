# O-15F14-BC — 2020–21 CBA 수정 공개 출처 경계

- 기준: `main` `3269700`, 2026-09-30 직접 대조. 판정: `PRESS_RELEASE_SCOPE_DELIMITED / AMENDMENT_TEXT_HOLD / F1_HOLD`.
- 질문: 2020–21 코로나 조정의 공개 NBA/NBPA 발표만으로 F1의 예외·Team Salary 조항을 정확히 적용할 수 있는가?

## 공식 출처가 실제로 말하는 것

| 출처 | 확인된 범위 | 말하지 않는 것 |
|---|---|---|
| [NBA·NBPA 2020-11-09 합의 발표](https://pr.nba.com/nba-nbpa-2020-21-season/) | 합의 원칙, 72경기, 2020–21 캡 `$109.140m`·세금선 `$132.627m`, 11/20 FA 협상 시작과 11/22 서명 시작 | 수정 CBA의 조문 전문, Article VII §6(m)(2)의 새 문구, Chicago의 개별 예외/권리 장부 |
| [NBA 이사회 2020-11-10 승인 발표](https://pr.nba.com/nba-board-of-governors-approves-adjustments-to-collective-bargaining-agreement/) | 이사회가 일부 조정안을 승인했고 11/18 드래프트·11/20 협상·11/22 서명·12/22 개막 일정을 공표 | 승인된 수정 조항의 전문이나 팀별 cap 계산서 |
| [NBPA 공개 2017 CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) | 코로나 수정 전의 Article VII §6(m)(2) 기본 규칙 | 2020년 수정의 적용 여부·수정 문구·실제 팀 신고값 |

**사실:** 위 두 보도자료는 발표된 날짜·캡 수치·일정을 확인하지만 Article VII §6(m)(2)에 실제 적용할 2020년 수정 조항 문구는 제시하지 않는다. 이사회 승인 발표는 그 자체로 NBPA 비준 문서나 양측이 체결한 수정 계약서도 아니다. **추론:** 이 보도자료만으로 F1의 2020–21 예외 조항을 확정 적용할 수 없다. **후보:** F1의 기존 급여/예외 상한 시험을 유지하되 수정 조항과 실제 `R`을 확보할 때까지 조건부로 둔다. **작가확정:** 신규 0건.

## V2 도구 경로와 한계

- **Codex 직접 대조:** 위 NBA 두 보도자료 및 2017 CBA의 문서 종류·포함 내용을 구분했다. 이번 웹 검색에서 공식 수정 전문을 확보하지 못했다는 것은 **공개 전문이 존재하지 않는다는 증명은 아니다**.
- **Anti-Gravity CLI 1.2.13:** `models` 서비스 조회는 성공. 공식 2020 수정 전문을 찾도록 한 읽기 전용 `search_web` 두 차례 뒤 70초 제한시간에 최종 답이 없어 `ATTEMPTED / NO_FINAL_EVIDENCE`다. 검색 호출 성공을 원문 확보로 세지 않는다.
- **NotebookLM CLI 0.11.5:** 비정본 First Rebound 검증 작업실 `303ffd55-e019-476a-9ae3-8dc0e32fe11f`에 11/09 NBA 발표를 출처 `629c7ba6-f8dd-43d9-9d82-49c9a6afd7a8`로 추가했다. 기존 2017 CBA 출처 `fb655448-b9dc-49ba-95ec-ff26ca9ed3f6`와 **이 두 출처만** 지정한 질의 `4b25188d-facc-4d5b-b41e-4e7ec9677f76`는 발표에 수정 전문이 없다고 답했다. 이는 지정 출처의 범위 확인이며 다른 공식 문서의 부재나 Team Salary PASS가 아니다.
- **Claude 문서 단독 반증:** [읽기 전용 검토](../reviews/R02_O15F14BC_F1_CLAUDE_DOCUMENT_REBUTTAL.md)는 보도자료가 수정 조항 문구를 제시하지 않는 점과 승인 발표의 법적 지위 표현을 좁히라고 지적했다. 원자료의 독립 재검색이나 F1 법률·급여 PASS가 아니다. 별도 source-blind는 `NOT_RUN`이다.

따라서 [F1 실행 패킷](../simulation/CHICAGO_2020_21_ADOPTION_READINESS.md)의 `R=null`, 정확 Team Salary·예외 수정 조항·거래 수취/송출 charge는 `HOLD`다. K1/L2 조건부 설계, F1~F5 최종 `0/5`, A1~A3 `0/3`, K 종료 `0/4` 및 7행 진행표 1완료·6미완료는 변하지 않는다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`를 유지한다.
