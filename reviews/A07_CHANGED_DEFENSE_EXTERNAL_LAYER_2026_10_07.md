# A07 새 외부 검증 레이어 실제 실행

입력은 고정된 가상 설계 사본이다. 세 도구의 응답 회수 여부를 실제 기록하며 원문 직접검문·정본 승인·전체 시즌 인증으로 계수하지 않는다.

|역할|실제 결과|
|---|---|
|Claude 상위판정 제거 반증|55.077초 PROCESS_TIMEOUT, stdout 0, 분석 미회수|
|Antigravity 새 WAS Bell2021 공식 출처 수집|55.063초 PROCESS_TIMEOUT; terminal SUCCESS 1개이나 response 비어 회수 false. 원문 인증 0|
|NotebookLM 텍스트 수입|11.099초 exit0; 최초 stdout JSON 파싱 실패. 중복 수입 없이 정확 제목의 source ID를 목록 1회 4.234초로 회수|
|NotebookLM source1개 분석|source de997619-ae30-4868-872c-a52b634c057f, query40/process55초; 55.032초 PROCESS_TIMEOUT, analysis_success false|

## 입력 및 수행 경계

- design/A07_CHANGED_DEFENSE_ROLE_EVALUATION_2026_10_07.json: `99aa206b5eaab09305596ba828fa718c801cf356a042ce07da20b9bc675d43ab`
- design/A07_CHANGED_DEFENSE_ROLE_EVALUATION_2026_10_07.md: `fbff2b04ddf53bad0384465dc9e2bec3ce06cd582b8ac681c0baec889c1b7d03`
- 업로드 사본 SHA: `41df8884022ea4ef36bf625e493c14dce738a2054dc3c774271b0b579f8a6454`. 원 MD에 가상 설계 사본이라는 안내를 붙였다.
- source import 1회, query 1회, Claude 1회, Antigravity 1회. source ID 복구 목록 조회만 추가했다.
- Claude에는 상위 status·root 판정·출구 인증을 제거하고 행동·가시 관측·비용·혼합자료 전달만 제공했다.
- Antigravity의 terminal SUCCESS 문자열은 비어 있는 답변이나 원문 열람의 성공을 보증하지 않는다.
- 지정 NLM 사본만 분석 대상으로 삼았다. 실행 시점 사본이며 후속 status 변경이 자동 동기화되지 않는다.
- 원 CLI/RPC/계정 로그·stderr 원문은 보관하지 않았으며 안전한 상태·지문·자료 ID만 남겼다.
- 재로그인·설정 변경·실패 호출 반복 0. 분석 미회수는 기존 독립 직접검문을 취소하거나 새 무한 게이트를 만들지 않는다.
- 새 정본·원장·producer·Pack·원고 변경 0. PROJECT_FREEZE v0.30 PARTIAL, 설계·원고 CLOSED.

## 실행 파일

- [Claude](A07_CHANGED_DEFENSE_CLAUDE_BLIND_2026_10_07.json)
- [Antigravity](A07_LAYER_ANTIGRAVITY_WAS_BELL_2026_10_07.json)
- [NLM 등록](A07_CHANGED_DEFENSE_NLM_SOURCE_REGISTRATION_2026_10_07.json)
- [NLM 분석](A07_CHANGED_DEFENSE_NLM_ANALYSIS_2026_10_07.json)
