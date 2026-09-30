# Cleveland C2 공개 비용 — 도구 실행과 판정 범위

- 대상: [공개 비용 화면](../simulation/CLEVELAND_2020_21_C2_PAYROLL_SCREEN.md), 기준 `main` `634bb70`, 2026-09-30.
- 결과: `CODEX_REPRODUCTION_PASS / NLM_SHARED_DOCUMENT_ANALYSIS / INDEPENDENT_REBUTTAL_NOT_RUN`. F5·D1·G16/G17 완료가 아니다.

| 역할 | 실제 실행 | 유효 결과와 한계 |
|---|---|---|
| Antigravity 자료 수집 | 절대경로 `C:\Users\Storm Credit\AppData\Local\agy\bin\agy.exe`에 공식 Kabengele 구단 URL을 `read_url_content→view_file`로 읽도록 요청. 45초 제한, 대화 `29b843bc-f88e-4ed3-b8b0-ada4951abf10` | `status=SUCCESS`이지만 `response=""`; 본문 증거0건. 수집 `FAILED_NO_EVIDENCE`, 공식 날짜 재독 성공으로 표시하지 않음 |
| NotebookLM 공식 URL 추가 | 비정본 작업실 `303ffd55-e019-476a-9ae3-8dc0e32fe11f`에 같은 URL 추가 | `Could not add url source`; 직접 구단 원문 분석 실패 |
| NotebookLM 텍스트 추가 | Codex 비용 화면을 `--text`로 추가한 소스 `0f3c30c3-6ecb-4c78-bf62-39450e1ed3b5`, 대화 `d234b1c5-bfd3-4701-877f-5ceb8939dbfe` | 제목만 분석되어 수치 자료 부족이라고 반환. 이 소스·질의는 검산 성공에 포함하지 않음 |
| NotebookLM 파일 복구·연결 분석 | 같은 문서를 임시 UTF-8 txt 파일로 업로드한 소스 `6633d6f7-8bfd-45c3-9c2f-6cc4439dbcd5`. `source content`로 원문5,578자와 core/stress 숫자가 실제 들어간 것을 확인. 해당 소스 하나만 지정한 대화 `57126363-8fab-479b-ae35-ec2f16637e0a` | 15명 $98,368,133, 이전6의무 $29,833,941, likely 중복 없음, Kabengele +$43,119, 두 혜택0 증분을 연결. $7,497,017은 전체 한도 통과가 아닌 조건부 목록 차이라고 반환. **Codex 작성 문서의 재분석**이며 독립 금액 출처·원계약 검증이 아님 |
| NotebookLM 최종9의무 분석 | 파일 소스 `e0025eda-67f0-4ecb-8af9-740fd259e2a0`만 지정한 새 대화 `99308adc-14c3-4140-a5d2-cd045642c45f` | 추가 $628,594, 이전9의무 $30,462,535, 목록 $130,668,168→$130,711,287→$132,059,577과 tax/apron 차이 $567,423/$6,868,423을 확인. Ferrell 현금·Maker 현금차 미포함 때문에 전체 상한이 아님을 반환. 여전히 작성 문서 재분석이며 원계약 인증이 아님 |
| Codex 저장소/산술 | 15명 고유 이름·McGee 포함/Hartenstein·Varejão 제외, 이전6의무 ID 고유성, 기존 C2/거래 생략 결정, likely 포함 cap hit, 각 계약별 일할 반올림과 산출 재현 검사 | 자체 검사 범위 PASS. 공개 보고값의 진실성·전체 누락 비용·정확 리그 장부는 인증하지 않음 |
| Claude 문서 단독 반증 시도 | 기본 CLI 모델에 결과 문서만 전달하고 도구 사용 없이 현금/cap/tax/apron 혼동과 근거 없는 상한을 공격하도록 요청 | 55초 제한 및 후속 180초 재시도 모두 유효 응답 없음. `TIMEOUT / NOT_RUN` |
| 별도 source-blind | 유효한 별도 검수 결과 없음 | `NOT_RUN`; Claude 요청의 결과가 없으므로 검수 완료로 세지 않음 |

같은 보고 계약값을 여러 도구가 읽은 횟수는 독립 원자료 수가 아니다. NotebookLM은 문서 구조/수치 연결만 확인했고 2차 표를 직접 인증하지 않았다. Antigravity와 Claude 실패를 숨기거나 자동 fallback 결과를 그 도구 결과로 바꾸지 않는다.

후속 Codex 누락 검문은 Maker·Tucker +$628,594와 Ferrell 보고 cap 0/현금 $118,983을 입력 원장에 추가했다. 위 NotebookLM 분석은 추가 전 15명+6의무 문서의 분석이며, 추가 후 9의무는 위 새 대화에서 따로 분석했다. 원자료 인증을 대신하지 않는다.

종료 가능한 범위는 **새 비용 목록과 재현 도구의 내부 일관성**이다. 전체 R_CLE·정확 Team Salary·등록/건강·새 승패·Denver 시리즈는 HOLD, F PASS0/5·A0/3·K0/4, 7행 1완료·1진행·5대기/남은6. v0.30 PARTIAL·설계/원고 CLOSED.
