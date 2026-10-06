# Antigravity CLI 응답 회수 진단 — 2026-10-07

범위: CLI 응답 회수만 진단했다. 설정·로그인·설치·권한은 변경하지 않았고, 기존 소설/NBA 근거의 사실성을 인증하지 않았다.

## 실제 확인

- 설치된 `agy.exe`는 현재 **1.3.0**이다. 종전 1.2.11 기록은 당시 버전이다. `agy models`가 모델 목록을 반환했고 `gemini-3.8-flash-low`가 목록에 있었다.
- 새 단일 테스트: `gemini-3.8-flash-low`, `--effort low`, `--print-timeout 30s`, `--output-format stream-json`, 도구 금지 짧은 프롬프트, `--mode` 지정 없음. **25.72초, 종료코드 0, 결과 1개 `SUCCESS`, 최종 `AGY_OK`, agent_response 조각 연결 `AGY_OK`, 도구 호출 0**. CLI·모델·인증·stream 출력 경로는 동작한다.
- [최근 미회수 기록](PLAYOFF_PREEXISTING_HEALTH_AG_2026_10_07.json): `search_web` 상태 갱신 11개가 있었고 마지막은 `ACTIVE`; 터미널 duration 49.981초는 내부 `50s` 제한에 거의 붙었다. `SUCCESS`라고 표시됐으나 `response=""`, 외부 60초 프로세스 제한도 넘었다. **자료 회수 0**으로 다루는 것이 맞다.
- [성공한 도구 사용 사례](ANNUAL_CALENDAR_AG_2026_10_06.json)는 도구 4단계 후 비어 있지 않은 응답이 돌아왔다. 반면 [긴 빈 응답 사례](CHI_ANNUAL_EXCEPTIONS_AG_2026_10_05.json)도 있어, 모든 실패를 50초 제한 하나로 단정할 수 없다. `--mode plan`이 원인이라는 증거도 없다.

## 원인 경계와 실행 방법

[공식 Headless 문서](https://antigravity.google/docs/cli/headless/)는 `step_update`가 도구 진행과 `agent_response.text_delta`를, 마지막 `result.response`가 최종 답변을 담는다고 설명한다. 또한 `--print-timeout`은 응답 대기 상한이다. 현재 [파서](../tools/parse_antigravity_stream.py)는 도구 이름·상태와 최종 응답만 보존하고 `tool_info.output` 및 부분 `text_delta`를 저장하지 않는다. 기존 원시 스트림도 보존되지 않아 **옛 검색 본문이 숨겨져 있었는지 사후 확인할 수 없다**. 도구 `DONE`은 본문 취득이나 검증 완료가 아니다.

다음 수집은 질문/공식 URL **하나씩** 실행하고 50초에 연속 검색을 몰아넣지 않는다. 내부 제한은 실제 소요보다 여유 있게 두되 외부 제한은 그보다 조금 길게 설정하고, 실패하면 최대 한 번만 범위를 좁혀 재시도한다. `exit=0`·단일 terminal·`SUCCESS`·**비어 있지 않은 최종 응답**을 모두 확인한다. 빈 `SUCCESS`는 `EMPTY_RESPONSE/HOLD`로 처리한다. 출처의 사실은 별도 공식 본문 확인 전까지 정본에 반영하지 않는다. 인증과 설치 경로는 [공식 설치 문서](https://antigravity.google/docs/cli/install)의 Windows 경로와 부합하며 재로그인 근거는 없다.

후속 수리와 단일 URL 시험 결과는 [NARROW_COLLECTION_RECOVERY_2026_10_07.md](NARROW_COLLECTION_RECOVERY_2026_10_07.md)에 기록했다. 최종 답변 회수는 성공했지만, 도구 출력 메타데이터만으로 공식 페이지 본문 전체 접근을 인증하지 않는다.
