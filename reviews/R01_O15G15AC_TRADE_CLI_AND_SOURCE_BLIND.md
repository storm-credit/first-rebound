# R01 — G15AC Plumlee 거래의 CLI·제한 맹점 검수

- 시작 권위 `main` `dfe3dd5`, 대상 [G15AC](../research/O15G15AC_PLUMLEE_2021_DRAFT_ASSET_COLLISION.md). G16 독립 검수·G17 작가확정이 아니다.
- **Codex 공식 원자료:** [Charlotte 2021-08-06 구단 공지](https://www.nba.com/hornets/press-releases/charlotte-hornets-acquire-mason-plumlee-and-draft-rights-jt-thor)의 DET→CHA Plumlee+Thor 권리, CHA→DET Koprivica 권리를 직접 확인했다. [NBA 드래프트 1~60](https://www.nba.com/news/2021-nba-draft-results-picks-1-60)의 원역사 30 Aldama/37 Thor/57 Koprivica/58 Sims와 저장소 DB1~DB4의 제안 30 Thor/37 Aldama/57 Koprivica/58 Huff를 별개로 대조했다. `selected_scenario=null`·추가 거래 false를 확인했다.
- **NotebookLM CLI:** 구단 발표 URL 새 출처 추가는 `Could not add url source`로 실패했다. 대신 기존 NBA 공식 드래프트 결과 출처 `0e91cdd3-d925-436e-971d-ce802b31a349`만 지정한 대화 `0552c5fb-bb5b-42d3-9360-893b52edbdc9`가 원역사 30/37/57/58 및 공식 양도 대상만 반환했다. 구단 발표를 NotebookLM이 분석한 것으로 표시하지 않는다. 같은 NBA 원문의 재질의는 새 독립 출처가 아니다.
- **Antigravity CLI:** 구단 발표 본문 읽기 요청은 40초 `print timeout`, `num_turns=0`·응답 본문 0건이다. CLI `status=SUCCESS`를 근거 확보로 세지 않는다.
- **Claude CLI 제한 source-blind:** New York에 놓인 DB1 Koprivica 권리를 Charlotte가 그대로 보낼 수 없고 추가 거래/선택이 필요하다는 지적은 **유효**하다. 그러나 Plumlee가 Charlotte→Detroit로 들어온다는 주장과 원역사 거래가 먼저 이뤄져야 G14 Detroit에 Plumlee가 있다는 주장은 **공식 거래 방향의 역전**이므로 기각한다. DB1에서 Detroit가 37번 Thor를 이미 소유했다는 주장도 **DET37 Aldama·UTA30 Thor**와 충돌한다. 이 모델의 추가 인과 사슬은 채택하지 않는다.

**결과물 단독 맹점:** P0 거래 미실행만으로 2022-01-23 Detroit 보유·건강을 확정하지 않는다. P1은 원역사 상대의 수락 이유, 현재 자산, 픽 37/57/58, Plumlee 급여와 두 팀 명단을 다시 계산해야 한다. 원역사 Charlotte의 Plumlee/Thor 수취가 사라지면 Charlotte 장기 커리어 상대 변화도 검토한다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.
