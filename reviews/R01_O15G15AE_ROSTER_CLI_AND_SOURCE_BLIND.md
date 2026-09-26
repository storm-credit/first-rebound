# R01 — G15AE Detroit 8월 명단과 9월 거래 제한 검수

- 시작 권위 `main` `8aa6bb8`, 대상 [G15AE](../research/O15G15AE_DETROIT_AUGUST15_AND_SEPTEMBER_ASSET_BRIDGE.md). G16 전체 독립 검수나 G17 작가 확정이 아니다.
- **Codex 원자료:** [Detroit 8/12 구단 분석](https://www.nba.com/pistons/features/olynyk-deal-made-possible-stewarts-rapid-progress-opens-pistons-offense)과 [8/18 문답](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-august-18-2021)은 당시 표준 15명·Diallo RFA 미해결을 보여준다. 전원 이름/급여 명부가 아니므로 G15AE의 `15−3+3+1=16`은 명시된 동일 사건 가정의 **조건부 스트레스**다. [Brooklyn 9/4 발표](https://www.nba.com/nets/news/2021/09/04/brooklyn-nets-complete-trade-detroit-pistons)는 DET의 Okafor·Doumbouya와 BKN의 Jordan·2R 네 장·현금을 직접 확인한다. [NBA 선수 이동 원장](https://www.nba.com/news/nba-player-movement-2021)은 Jordan 원역사 방출만 확인하며 대체 급여 정산 근거가 아니다.
- **Antigravity CLI 1.2.11:** NBA [2021 offseason trade tracker](https://www.nba.com/news/2021-offseason-trade-tracker) `read_url_content`의 **기사 본문 접근 성공**, `num_turns=1`, 9/4 양 팀 선수·네 2R·현금 방향을 반환했다. 거래 원문의 독립 회수 한 건이며 대체 Nets 수락·급여 증명은 아니다.
- **NotebookLM CLI:** 기존 같은 NBA 거래 원장 `291dc747-80e1-40ca-99cc-b8e9f5aa889a`만 지정한 질의가 9/4 양방향 선수·픽·현금을 확인하고 개막 명단/대체 거래를 증명하지 못한다고 답했다. Antigravity와 **같은 NBA 원문**을 다시 분석한 것이므로 별도 독립 출처로 중복 계산하지 않는다.
- **Claude CLI source-blind:** G15AE 초안 텍스트만 입력한 제한 감사는 8/12 15명 개별 이름 미확인, Plumlee의 출발 15 포함 여부, 9월 거래로 8월 cap을 소급 해결할 위험, 10월 이탈 선수명 부재를 지적했다. Plumlee는 8/6 이적으로 출발 15명에서 제외됐다는 공식 거래 링크를 보강했다. 나머지 이름·급여/일자와 개막 로스터는 실제 `HOLD`이며, 문서가 9월 사건을 8/6 자금원으로 사용한 것은 아니므로 해당 지적은 **예방 경고**로 남긴다. Claude는 외부 원문을 직접 읽지 않았다.

**결과물 단독 맹점:** `16`은 실제 대체 8월 명단, CBA 위반, 10월 roster 판정이 아니다. 37번 지명권과 서명, 두-way/camp 계약과 표준계약을 분리한다. Nets 거래가 성립하더라도 네 2R·현금·Jordan 보장급여와 Brooklyn 수락 비용을 동반한다. 신규 작가확정 0건, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
