# R01 — G15Z 도구 조사·제한 반증·결과물 단독 맹점 검수

- 시작 권위: `main` `310d846`; 검토 대상: [G15Z](../research/O15G15Z_DENVER_FIVE_MAN_AND_BEY_CONTRACT_BRIDGE.md). 새 정본 선택이나 G16 독립 검수 아님.
- **Antigravity CLI:** 설치 절대경로 `agy.exe` 1.2.11, `gemini-3.8-flash-low`의 NBA [Free Agency explained](https://www.nba.com/news/free-agency-explained) 직접 읽기 요청이 `SUCCESS`와 `Accessed body: Yes`를 반환했다. 3·4년차 옵션 문장을 회수했고 Codex가 같은 NBA 본문과 대조했다. 응답의 광범위한 거래/방출 설명은 이 문서의 사실 근거로 사용하지 않았다. 이 URL 1건의 본문 성공을 다른 NBA 자료 접근 성공으로 확대하지 않는다.
- **NotebookLM CLI:** 기존 공식 [NBA CBA 101](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) 출처 `4e516c8c-d38b-4a27-8c70-1e05f8c5dced`만 지정한 새 대화 `2d67d914-4b9d-4397-ae00-9e314d1dc739`에서 2년 보장+3·4년차 옵션과 서명/등록 구분을 반환했다. Codex가 PDF I.D.(5), I.R.(1)을 직접 확인했다. 두 CLI의 대답은 같은 NBA 규칙 계열이므로 서로 독립 원자료 2건으로 세지 않는다.
- **Codex 기계검증:** `python tools/check_o15g15z_denver_lineup.py`에서 X1/X2 각자 5인 중복 0·자리별48:00·팀240:00·선수별 분 일치를 통과했다. 검증기의 역할은 JSON이 주장한 분 산술에 한정된다.
- **Claude CLI 제한 반증:** 도구 없는 `haiku`에 JSON과 독립적으로 동일한 구간·신인 계약 조건만 제공했다. 5인 중복 없음과 계약 조건의 한계를 확인했다. 단, “Morris가 Denver PG인지 불명확하며 Marcus Morris일 수 있다”는 지적은 **기각**한다. 공식 [Denver 2022-01-23 경기 노트](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/01/nuggetsPistons.pdf)는 #11 Monte Morris를 가드로 적고, [해당 NBA 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)는 Morris `29:51`을 기록한다. 모델의 의심을 사실로 올리지 않는다. Claude의 “매 12초 구간” 표현도 검사 구간의 정확한 기술이 아니므로 채택하지 않는다.

## 결과물만 보고 한 맹점 검수

| 질문 | 판정 |
|---|---|
| 같은 선수가 동시에 두 자리인가? | JSON 검증 통과. Campazzo와 Rivers의 서로 다른 자리 사용은 시간상 분리된다. |
| 누구의 실제 역할을 공짜로 받았나? | Nnaji의 16:45를 이름 있는 수신자에게 시험했지만 Nnaji의 득점/FGA는 옮기지 않았다. X1의 Bey 0분, X2의 JaMychal 0분은 각각 설명 부채로 남았다. |
| 이 스케줄로 실제 경기가 가능한가? | **미검증.** 긴 연속 출전, 쿼터 휴식, 포지션 적합성과 계약·건강이 남았다. 수학 통과를 경기 설계 PASS로 승격하지 않는다. |
| 원역사 결과가 침입했나? | 승패·점수·실제 교체 시각을 선택하지 않았다. Detroit의 Bey30:42도 Denver에 복사하지 않았다. |

최종 범위는 `ABSTRACT_FIVE_MAN_MATH_PASS / REAL_ROTATION_HOLD / CONTRACT_HOLD`다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, G16/G17 미완료.
