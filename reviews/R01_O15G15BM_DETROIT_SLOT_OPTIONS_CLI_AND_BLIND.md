# R01 — G15BM 개막 자리 후보의 도구별 검증

- 대상: [G15BM](../research/O15G15BM_DETROIT_OPENING_SLOT_TWO_NAMED_OPTIONS.md); 신규 작가확정·정본/게이트 변경 0건.
- 역할 분리: Antigravity는 NBA 2021–22 규칙 수집 시도, NotebookLM은 공식 규칙 한 출처 분석, Codex는 G15AF 실명 집합의 변환 검산, Claude는 문서 단독 반증이다.

| 단계 | 실제 결과 | 채택/기각 범위 |
|---|---|---|
| Antigravity CLI | 절대 경로 `agy.exe`에서 NBA Communications의 2021–22 공식 규칙 한 URL을 지정했다. 헤드리스 환경에서 내부 `RunCommand`가 `command` 권한을 요구했고 프롬프트할 수 없어 **자동 거부**됐다. `status=SUCCESS`여도 `response=""`·본문 0건. | Antigravity 답변을 증거로 세지 않았다. 모든 도구를 자동 승인하는 옵션은 사용하지 않았다. Codex가 공식 원문을 직접 대조했다. |
| NotebookLM CLI | 공식 NBA Communications URL만 신규 출처 `50e03abb-8184-4b1b-a554-eb19099dd116`으로 수집됐다. Detroit 구단 문답 두 URL은 `source add` 결과에 없었다. 공식 출처 하나에 제한한 질의로 **15 표준+2 투웨이**, **50활동경기**, 투웨이 급여 0년차 최소급의 50%를 확인했다. | 32경기 **출전**은 50경기 **활동**을 증명하지 않는다고 분리. 구단 문답은 Codex가 NBA 페이지를 직접 대조했다. NLM 응답은 대체 명단 판정이 아니다. |
| Codex 저장소 검사 | [G15AF JSON](../research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json)을 읽는 [G15BM 검사기](../tools/check_o15g15bm_detroit_slot_options.py)가 원래 P0-B 개막 16을 다시 만들고 `A/B` 각각 표준15·투웨이2·G14 사용 10명 보존을 확인했다. 기존 G15AF 검사기도 통과했다. | 집합과 날짜별 후보 변환만 통과. Olynyk cap, 두 계약 효력, Garza 활동 경기, Pickett 권리, Lyles 착지·Bagley 거래는 통과하지 않았다. |
| Claude 문서 단독 반증 | 공통 Olynyk cap 미해소와 `A`의 50활동경기, `B`의 Bagley 원형 거래 파급을 강조했다. 원장에 **공통 HOLD 선행**, G14 사용 10명 실명, 기본 16표준+2투웨이 초과, 50경기 뒤 활동 중단 또는 별도 전환 자리를 더 명시했다. | “50경기면 표준 전환이 의무”는 과장: 추가 활동 명단 배치를 멈출 수도 있다. “Pickett이 떠나면 Garza+Smith 투웨이가 한 명이 된다”는 집합 오류. G14 10명에 Lyles/Garza가 들어갈 수도 있다는 지적은 이미 검증된 명단과 충돌해 기각. Claude의 우려는 별도 1차 출처 없이 사실로 채택하지 않았다. |

잔여 `HOLD`: 8/6 전체 Team Salary·권리/예외·통지 순서, Charlotte/Nets 상대 거래, 2021 DB1, `A` Garza 날짜별 50활동경기와 Pickett 수신자, `B` Lyles 다른 팀 착지·1/23 앞코트/2/10 Bagley 거래 재설계. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
