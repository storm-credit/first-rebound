# Antigravity 단일 공식 URL 회수 시험 — 2026-10-07

[기계 기록](NARROW_COLLECTION_RECOVERY_2026_10_07.json). Antigravity CLI `1.3.0`에 [공식 Headless 문서](https://antigravity.google/docs/cli/headless/) 한 URL만 요청했다. `gemini-3.8-flash-low`, `--effort low`, `--output-format stream-json`, 내부 제한 `90s`, 외부 제한 `105s`, `--mode` 미지정. 설정·인증·설치는 변경하지 않았다.

**응답 회수 성공:** 72.703초에 종료코드 0, 단일 `SUCCESS` 결과의 응답 169자와 별도의 agent_response 조각 169자를 받았다. 응답에는 요청 URL과 문서의 `text`·`json`·`stream-json` 형식이 모두 나타났다. 이전 50초 다중 검색의 빈 `SUCCESS`와 달리 최종 응답을 실제로 회수했다.

**본문 증거는 제한적:** `read_url_content` 완료 이벤트에는 `output` 필드가 없고, 이어진 `view_file` 완료 출력은 모두 동일한 24자 길이·해시였으며 한 번은 `ERROR`였다. 출력 원문은 보존하지 않았으므로 이것으로 전체 문서 본문 열람을 인증할 수 없다. CLI의 최종 답변은 독립 원문 증거가 아니며, 위 형식 명칭은 별도로 [공식 문서](https://antigravity.google/docs/cli/headless/)에서 대조했다. NBA 원자료 수집·정본 승격은 이 시험에서 0이다.

[수정한 파서](../tools/parse_antigravity_stream.py)는 기본 반환 형식을 유지한다. `safe_capture=True`일 때만 최대 4,096자의 `agent_response.text_delta`를 **부분 응답**으로 분리하고, 도구 출력은 유형·길이·SHA-256만 남긴다. 부분 응답과 도구 `DONE`은 빈 최종 답변을 회수 성공으로 승격시키지 않는다. [테스트](../tests/test_antigravity_stream.py)는 기본 호환성, 빈/중복/오류 결과, 부분 응답, 본문 비보존을 확인한다.
