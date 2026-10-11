# Antigravity NBA 공식 수집 회수 진단

기준 main `db73633c54d1d0b28ea2d65664aef2a4de69bea0`. [실행·원문 대조 영수증](ANTIGRAVITY_NBA_OFFICIAL_READER_DIAGNOSTIC_2026_10_12.json).

| 실행 | 응답 회수 | 실제 수집 판정 |
|---|---|---|
| PR548의 기존 JSON 실행 재관측 | SUCCESS이나 빈 답 | 수집 실패 이력 유지 |
| stream-json·120초·격리 작업 폴더로 HTML 읽기 | 최종 UNVERIFIED 회수 | 37,499바이트 자료에 기사 body 없음 |
| 같은 게시물의 작은 공식 API 읽기 | 최종 답 회수·종료0·38.358초 | 필요한 날짜 세 항목 수집, 전체 기사 미완료 |

공식 [게시물](https://pr.nba.com/nba-all-star-voting-tissot-2022/)과 [게시물 API](https://pr.nba.com/wp-json/wp/v2/posts?slug=nba-all-star-voting-tissot-2022)의 id14270·원 게시물 link를 대조했다. 실제 Antigravity 저장 자료를 회수해 Codex의 직접 HTTP 자료와 정확한 앞부분 일치를 확인했다. 투표 종료는 **2022년1월22일 자정 ET**, 선발 발표 **1월27일**, 리저브 발표 **2월3일**이다. 이 날짜들은 이미 설계에서 사용하던 공식 기준이며 새 수상 선택이 아니다.

## 실제 원인 증거와 한계

- 큰 HTML의 직접 HTTP 자료에는 body가 있으나 Antigravity 자료는 body 전에 끝난다. JavaScript가 반드시 필요하거나 원 서버가 잘랐다는 모델 추정은 원인으로 확정하지 않는다.
- 작은 API 직접 응답은17,359바이트이며 JSON 배열 앞에188자의 HTML 발췌가 섞여 있다. 그 뒤 배열은 실제로 완전하게 파싱된다. 전체 응답이 정상 JSON이라고 보고하지 않는다.
- Antigravity 저장 자료는4,889바이트이며 `content.rendered` 도중에 끝난다. 필요한 세 날짜와 자정 ET는 그 안에 있고, 완전한 원문의 기사 내용에서도 일치한다. **세 항목 확인은 성공, 기사 전체 확인은 실패**다.
- 이 한 자료의 부분 수집 성공을 모든 MCP 통신·다른 출처·로그인 상태의 성공으로 확대하지 않는다. 관측 길이를 전역 고정 제한값으로 해석하지 않는다.
- raw 로그와 저장 자료는 Temp에 보존하고 JSON 영수증에는 지문·경로·한정 판정만 남겼다. NotebookLM·Claude·독립 에이전트는 이번에 실행하지 않았다.

프롬프트는 공식 자료 읽기만 허용했다. 새 개인상·득표·금메달·원고·Pack·게이트 선택은0이며 v0.30 PARTIAL/CLOSED를 유지한다. 다음 실행은 실제로 확인한 작은 공식 본문을 우선하고, 필요한 조항이 수집 범위 밖이면 미확인으로 남긴다. 같은 실패를 조건 없이 다시 실행하지 않는다.
