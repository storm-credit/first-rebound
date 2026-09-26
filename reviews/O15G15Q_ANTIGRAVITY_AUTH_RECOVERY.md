# O-15G15Q — Antigravity CLI 인증 복구와 공식 본문 판독 확인

- 날짜: 2026-09-26. 시작점 `main` `319fcc0` / PR #200. 읽기·진단만 수행했고 정본/시즌/계약 선택은 바꾸지 않았다.
- 상태: `AGY_AUTH_RECOVERED / NBA_PAGE_BODY_VERIFIED`. 이 페이지는 [G15P](../research/O15G15P_HERBERT_33_SECOND_ROUND_TENDER.md)에서 Codex·NotebookLM도 이미 사용한 **같은 NBA 공식 출처**이므로 독립 자료 수를 늘리지 않는다.

## 실패 원인과 교차 진단

1. 설치된 CLI `agy.exe --version`은 `1.2.11`, `agy models`는 목록을 반환했다. 그러나 짧은 headless 요청은 시간 초과되고 실제 답변이 없었다. `--output-format json`의 한 실패 시도는 `status=SUCCESS`라도 `response=""`, `num_turns=0`이었다. 이 envelope만으로 성공 판정하지 않는다.
2. 해당 시각의 로컬 CLI 로그에는 `error getting token source: You are not logged into Antigravity`가 반복됐다. 로그의 인증 오류가 직접 관찰 근거이며, **왜 캐시된 로그인이 무효가 됐는지**는 확인되지 않았다. 모델 목록 조회만으로 agent turn 인증 성공을 추론할 수 없다.
3. [Antigravity 공식 headless 문서](https://antigravity.google/docs/cli/headless/)는 headless 실행이 캐시된 인증을 쓰고 먼저 대화형 `agy`로 로그인해야 한다고 설명한다. 실제 대화형 화면은 `currently not signed in` → `Signing in...` → 계정 표시로 바뀌었다. 비밀번호·토큰이나 자격증명 파일을 직접 다루지 않았다.
4. Claude CLI에 버전/모델 목록/타임아웃/로그 오류만 전달해 물었다. Claude도 **유효하지 않은 캐시 인증**을 주원인으로 보고 대화형 로그인과 재시험을 제안했다. Claude의 미검증 캐시 경로 추정은 사용하지 않았다.

## 복구 후 재현

| 확인 | 관측 | 판정 |
|---|---|---|
| headless 최소 응답 | `gemini-3.8-flash-low`가 `READY`를 반환; `status=SUCCESS`, `num_turns=1`, 출력 토큰 1 | agent turn 성공 |
| NBA 공식 URL | [2021 드래프트 결과](https://www.nba.com/news/2021-nba-draft-results-picks-1-60) 요청의 stream-json에서 `read_url_content`와 `view_file` 모두 `DONE` | 도구 단계 실제 실행 |
| 생성 본문 | AG가 만든 본문 파일의 HTML에서 `33. Magic draft Jason Preston (officially traded to the Clippers)` 및 `35. Pelicans draft Herbert Jones`를 직접 추출 | **이 URL의 본문 판독 성공** |

다른 NBA 페이지, PDF, MCP 서버 전체의 접근 성공까지 확대하지 않는다. 이후 수집은 `인증된 1턴 + 도구 단계 DONE + 저장 본문 확인 + 원문 위치` 네 가지를 확인하고, 실패 시 해당 URL을 `ACCESS_FAILED`로 둔다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 게이트 `CLOSED`, 신규 작가확정 0건 유지.
