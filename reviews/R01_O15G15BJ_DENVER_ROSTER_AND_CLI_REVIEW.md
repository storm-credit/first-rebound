# R01 — G15BJ Denver 명단 자리·CLI 검토

- 대상: [G15BJ 원장](../research/O15G15BJ_DENVER_JAN23_ROSTER_SLOT_BRIDGE.md), [JSON](../simulation/O15G15BJ_DENVER_JAN23_ROSTER_SWAP.json), [검사기](../tools/check_o15g15bj_denver_roster.py). G16 전체 독립 검수 아님.
- 공식 직접 대조: [Denver 2022-01-23 경기 노트](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/01/nuggetsPistons.pdf) 1–2쪽, [NBA 2020 지명 결과](https://www.nba.com/news/2020-nba-draft-results-picks-1-60), [2021–22 거래 추적기](https://www.nba.com/news/2021-22-nba-trade-tracker), [CBA 101](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf), [당일 늦은 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf).

| 역할 | 수행·판정 | 제한 |
|---|---|---|
| Antigravity 수집 | 설치된 `agy.exe`를 실제 호출했다. PDF 1건은 웹 읽기 도구가 로컬 임시 파일을 만들었지만 명령·로컬 파일 도구 사용을 제한한 세션에서 본문을 추출하지 못했다고 명시했다. 재요청한 NBA 거래 추적기 **HTML 본문은 성공**: Denver Forbes, Boston Bol/Dozier, San Antonio Hernangómez·미래 2R·현금. | 이 NBA 표는 미래 픽 연도·원소유 팀과 현금액이 없다. CLI와 Codex가 **같은 NBA 페이지**를 읽었으므로 독립 원자료 두 건이 아니다. PDF 실패를 명단 수집 성공으로 세지 않는다. |
| NotebookLM 제한 분석 | 공식 Denver 경기 노트 PDF를 노트북 출처 `f755924d-b239-4f86-8b8d-deb8809efe1f`로 추가하고 CBA 101 `4e516c8c-d38b-4a27-8c70-1e05f8c5dced`만 지정했다. 대화 `4311aa1e-4e7a-486f-8917-ef613717cf73`: 15+2, Forbes/Cousins 날짜와 Bey 서명/거래 존속의 미증명을 분리했다. | “3년차 옵션 행사 여부”를 2022-01-23 Bey 계약 지속의 필요조건처럼 읽을 여지를 남겼다. 서명된 2020 신인 계약이라면 그날은 보장 **2년차**이며 3년차 옵션이 필요하지 않다고 CBA 원문으로 교정했다. |
| Codex 저장소 검사 | `check_o15g15bj_denver_roster.py`: 원역사 15+2의 중복 없음, Nnaji↔Bey 교체 후 15+2, X1/X2 교대 선수의 명단 포함과 비수신자 0분 명단 유지 통과. G15BI 교대 검사도 재통과. | 자리 수만 검증한다. 1/19 역산14는 다른 거래가 없다는 조건의 산술이며 실제 시간별 계약 장부가 아니다. 정확 cap/의료/경기 성과는 미검증. |
| Claude 도구 없는 반증 | 문서만 제공했을 때 “역사적 Nnaji21·Bey23”이라고 주장하며 급여식을 공격했다. | **기각.** [NBA 공식 2020 지명표](https://www.nba.com/news/2020-nba-draft-results-picks-1-60)는 Nnaji22·Bey19이고 프로젝트 정본은 Bey22·Nnaji24다. 한편 계약·후속 거래 불확실성 지적은 이미 명시된 HOLD와 일치한다. Claude는 외부 출처를 직접 확인하지 않았다. |

## 결과물 단독 맹점 검수

1. 15+2 **자리 수**가 맞아도 Bey의 서명, Forbes를 위한 3자 거래 수락, Cousins 10일 계약, Reed 투웨이 계약이 대체세계에서 생존했다는 뜻은 아니다.
2. Forbes 원역사 거래의 **미래 2R·현금**은 Denver/Boston/San Antonio 중 지급 주체와 정확 연도/조건을 추가로 회수해야 한다. 원역사 경기 노트는 선수만 적고, NBA 거래 추적기도 해당 필드를 닫지 않는다.
3. 같은 #22의 신인 기본급 중립은 **동일 서명 비율일 때의 식**이다. 실제 #22 2년차 금액·보너스, 팀급여·거래 매칭은 별도다.
4. 원역사 경기 전 JaMychal `Questionable`과 늦은 NBA 보고 `Available`은 시각이 다르다. 후자를 원역사의 최신 상태로 쓰되 대체세계 의료 허가는 아니다.

최종: `CONDITIONAL_ROSTER_SLOT_PARITY_PASS / EXACT_TRANSACTION_AND_GAME_HOLD`. 새 정본 승인 0건. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, G16/G17 미완료.
