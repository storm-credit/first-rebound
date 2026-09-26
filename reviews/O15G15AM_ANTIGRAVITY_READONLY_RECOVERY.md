# O-15G15AM — Antigravity headless 공식 기사 읽기 복구

- 시작 권위: `main` `47fe648` (PR #222 병합). 검증 레이어의 **도구 실행 기록**이며 새 NBA 시나리오나 작가확정이 아니다.
- Antigravity CLI `1.2.11`, 절대 실행 경로 사용. 기존 G15AL의 URL 요청은 `RunCommand` headless 허가 거절과 빈 최종 답변으로 끝났다. 이 실패 기록을 성공으로 소급 변경하지 않는다.
- [Google 공식 headless 문서](https://www.antigravity.google/docs/cli/headless/)는 headless 모드에서 명령 권한을 대화형으로 받을 수 없으며 거절되어도 결과 상태가 `SUCCESS`일 수 있음을 명시한다. [공식 권한 문서](https://antigravity.google/docs/permissions?tab=cli)는 `~/.gemini/antigravity-cli/settings.json`의 세밀한 허용 규칙을 설명한다.

## 재시험

1. 사용자 설정의 기존 `permissions.allow`에 `read_url(*)`가 있는 것만 확인했다. 전역 설정을 수정하거나 모든 명령 자동 허용 옵션을 사용하지 않았다.
2. 공식 [NBA 2021–22 캡 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season) URL을 지정하고 `read_url_content`와 `view_file`만 사용하며 `run_command`를 호출하지 말라는 별도 프롬프트로 `--output-format stream-json` 실행.
3. 이벤트 순서에서 `read_url_content ACTIVE→DONE`, `view_file ACTIVE→DONE`, 최종 `status=SUCCESS`·`denied_actions=null` 확인. `RunCommand` 이벤트 없음.
4. Antigravity가 저장한 원문 파일의 기사 텍스트에서 **Salary Cap `$112.414 million`**과 **room mid-level `$4.910 million`** 구절을 Codex가 다시 직접 판독했다. Antigravity 답변의 동일 수치는 이 저장 본문과 일치한다.

판정은 **`AG_DIRECT_NBA_ARTICLE_READ_SUCCESS`**. 로그인 재진행 없이 공개 NBA 기사 읽기는 작동한다. 이는 G15AJ/AI/AH가 이미 사용한 **같은 공식 기사**의 새 접근 경로이므로 독립 원자료가 늘어난 것은 아니다. Detroit 계약 원장, NBA PDF, 다른 동적 기사까지 모두 읽힌다는 뜻도 아니다. 다음 Antigravity 자료수집은 먼저 읽기 전용 도구로 시도하고, stream-json 도구 이벤트와 저장 본문을 확인해 성공/실패를 판정한다. NotebookLM 출처 제한 분석과 Codex 원문·저장소 감사, Claude 문서 단독 반증의 역할은 그대로다. G16/G17 및 설계/원고 게이트 `CLOSED` 유지.
