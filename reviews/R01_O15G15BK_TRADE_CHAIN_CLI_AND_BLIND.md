# R01 — G15BK 거래 사슬 검증의 출처와 한계

- 기준: `research/O15G15BK_DET_DEN_BOL_MCGRUDER_FORBES_DEPENDENCY.md`; 정본/게이트 변경 0건.
- 프롬프트는 **날짜·선수 소유·완료/취소 구분**에 한정했다. 조사·출처 분석·저장소 검사·독립 반증을 각각 다른 질문으로 수행했다.

| 단계 | 실제 실행 및 결과 | 판정 한계 |
|---|---|---|
| Antigravity CLI 수집 | 절대 경로 `agy.exe -p ... --print-timeout 50s --output-format json`으로 Detroit 1/10·1/13과 NBA 거래 추적기 URL을 지정했다. `status=SUCCESS` 응답이었지만 `response=""`, `print timeout after 50s`여서 **본문 증거 0건**. | 실행·서비스 응답은 확인됐으나 수집 성공으로 세지 않는다. 구단 웹 본문은 Codex의 직접 NBA 검색/대조로 확인했다. |
| NotebookLM CLI 출처 제한 | 구단 두 URL과 NBA 추적기를 `source add --wait`에 넣었으나 반환된 신규 출처는 **추적기 1건**(`09d5fe7f-e379-4f8b-9dd5-ad45155ad675`)뿐이다. 그 출처만 `query notebook --source-ids ... --new-conversation`으로 질의해 1/19 Denver Forbes 취득·Bol/Dozier 송출, 1/10 Bol–McGruder의 공식 거래 목록 부재를 확인했다. | 목록 부재 자체가 의료 취소의 증거는 아니다. Detroit 구단 취소 기사와 NBA 보도를 별도로 대조했다. NotebookLM 답변은 정본 판정이 아니다. |
| Codex 저장소 검사 | G15AB의 Detroit McGruder 원역사 `23:38`과 G15BJ/BI의 Denver Forbes 명단·20분을 양방향으로 확인했다. [G15BK 검사기](../tools/check_o15g15bk_trade_chain.py)는 Bol을 Denver/Boston과 Detroit가 동시에 쓰지 않는 조건을 검사했다. G15AB·G15BI·G15BJ 기존 검사기도 재통과. | 기계 통과는 거래 합법성·의료·대체 경기 결과의 증명이 아니다. |
| Claude 도구 없는 문서 단독 반증 | 원장만 제공해 McGruder 이중 배치, `BLOCKED` 범위, 9월 Brooklyn 픽 의존성을 공격하도록 했다. `BLOCKED`가 **원형 Forbes 거래만** 가리키도록 문구를 좁혔고, G15AF의 Brooklyn 대체 거래 `HOLD`를 명시했다. | McGruder 관측 행 제거를 누락했다는 지적은 원장에 이미 제거가 적혀 있어 기각했다. Denver에서 원역사 Detroit 분을 재사용하지 않는 문구는 추가했다. “작가확정 0건”을 오해한 지적도 조건부 후보와 작가 승인 구분에 따라 기각했다. Claude의 사실 주장은 NBA 1차 출처로만 채택한다. |

잔여 검증: 대체 9/4 Brooklyn 거래·픽 보유, Bol 의료 통과 근거, 1/10 거래의 최종 실행과 급여·상대 동의, 1/19 원형 또는 새 Forbes 거래, 1/23 양 팀 표준/투웨이 자격과 분·공격 기회. 전부 `HOLD`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
