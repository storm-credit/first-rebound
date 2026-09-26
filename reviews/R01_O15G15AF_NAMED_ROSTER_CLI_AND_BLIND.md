# R01 — G15AF 실명 명단·개막 연결 제한 검수

- 시작 권위 `main` `0d76e75`, 대상 [G15AF](../research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md). G16 전체 독립 검수 또는 G17 승인이 아니다.
- **Codex 직접 조사:** [NBA 드래프트 당시 프로필](https://www.nba.com/draft/2021/team-profiles/detroit-pistons)의 11 계약자/5 FA는 8월 12일 명부 자체가 아니다. [Detroit 8/12 기사](https://www.nba.com/pistons/features/olynyk-deal-made-possible-stewarts-rapid-progress-opens-pistons-offense)의 15명 관측, [8/18 문답](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-august-18-2021)의 McGruder 재서명과 Diallo RFA, 공식 이동/거래/전환 기록을 연결해 15명을 **추론 재구성**했다. 원역사 개막 15명은 이름별 사건에서 나오며 10/20 독립 계약 명부는 아직 미회수다.
- **Antigravity CLI 1.2.11:** 이번 NBA 드래프트 프로필 URL에 `read_url_content`를 실제 실행하고 `status:SUCCESS`, `num_turns=1`을 받았지만 저장된 결과는 Next.js 셸이며 `Under Contract` 선수 본문이 없었다. **해당 URL의 AG 증거 0건.** 앞선 G15AE에서 NBA 거래 원문을 읽은 성공을 이 URL로 확대하지 않는다.
- **NotebookLM CLI:** 같은 NBA 드래프트 프로필을 작업실 `303ffd55-e019-476a-9ae3-8dc0e32fe11f`에 소스 `3ee5e7c6-42de-4d64-a679-5a464842c774`로 추가하고 그 소스 한정 질의를 완료했다. 11 계약자와 Diallo 등 5 FA를 반환하며 드래프트 스냅샷만으로 8월/10월 명부를 증명할 수 없다고 답했다. Codex와 **같은 NBA 원문**이므로 별도 독립 출처가 아니다.
- **Claude CLI source-blind:** 완성 초안만 입력한 무도구 제한 검수가 Jordan 방출 일자, 대체 Nets 거래 가정, Suggs와 Aldama의 지명권·서명 기준, G15AB 연결 설명을 문제 삼았다. 유효한 명료화로 Jordan 사건을 **9/4 뒤·9/9 전**으로 한정하고, Patrick/Kira/Suggs 표준 서명은 가정·Aldama 미서명도 가정이며 Nets 거래는 실행 증거가 없음을 문서에 명시했다. “Jordan 이탈이 8/12–8/19 사이일 수 있어 16명이 위반”이라는 지적은 **Jordan의 Detroit 취득 자체가 9/4**이고 8월 16도 캠프 전 집합이어서 기각했다. Claude는 외부 원문을 읽지 않았고 원자료 독립 감사가 아니다.
- **기계 검증:** `python tools/check_o15g15af_detroit_roster.py` 통과. 원역사 `15→16→15→14→15`, P0-B 엄격 동일 사건 가정 `16→17→16→15→16`, 이름의 중복/없는 선수 제거 없음. 이 검사는 가정의 성립과 CBA·cap 적법성을 보증하지 않는다.

**결과물 단독 맹점:** 8월 12일 실명 15명은 여러 공식 출처를 결합한 재구성이다. 캠프 초청·투웨이·지명권은 표준 15명과 구분한다. 개막 16명은 실제 대체역사의 위반 판정이 아니라 **Nets 거래까지 동일하게 옮긴 반사실 시험**이다. 이 시험에서조차 실명 이탈 1명과 8/6 Olynyk 별도 cap 경로가 없다. 신규 작가확정 0건, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
