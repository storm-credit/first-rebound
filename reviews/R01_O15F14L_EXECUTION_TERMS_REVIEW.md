# O-15F14-L 실행 조건 근거 자체 검토

- 상태: `PASS_WITH_EXACT_EXECUTION_HOLD / NOT_INDEPENDENT`.
- 대상: `CHICAGO_2020_21_EXECUTION_TERMS.md` 및 동명JSON, 출처 JSON.
- Hall: 2019 NBA 규약6.08과4명×직전3경기 부상 사유 미출전을 확인했다. May9 보고는 계약공지 후 발행이므로 사전 승인서로 쓰지 않는다. Porter·Carter·투웨이를4명에 넣지 않았다.
- 급여:8명 이력의 기본급과 인센티브를 분리했다. Clark 요약/유효계약 충돌, Fournier 시간기준 차이, Hall cash/cap0 문제를 보존했다.
- 산술: Gordon 양팀×2조건 통과. 알려지지 않은 trade bonus·hard cap은 포함 범위 밖이다. Chicago 납세 기준에서는 실패하므로 비납세 전제를 종료하지 않는다.
- 픽: 새 보호기간/2R 연도를 기존 미결 연결/종료와 구분했다. 실제 전달 결과를 대체세계 의무로 채택하지 않았다.
- 검증: 신규6개 PASS, JSON 재현 PASS, diff 공백 검사 PASS. 최초 테스트의 기대값 오기 수정 후 재검증했다.
- 보존: K1/L2 추천·H 방향 승인, author_locked=false·season_selected=false, v0.30 PARTIAL 및 설계/원고 CLOSED.
- 잔여: 팀 급여/예외 당일 장부·정확charge·픽 연결/종료·작가의 시즌/행정사건/추첨 채택. 네 K 묶음 모두 OPEN.
- 게시: blob/tree 대조·원격 CI 유무·main 동기화는 게시 실행에서 별도 확인한다.
