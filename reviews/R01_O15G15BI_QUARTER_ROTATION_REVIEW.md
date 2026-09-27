# R01 — G15BI 쿼터 교대 산술·자료 경계 검토

- 범위: [G15BI 조건부 교대](../research/O15G15BI_DENVER_QUARTER_ROTATION_WITNESS.md)와 [JSON](../simulation/O15G15BI_DENVER_QUARTER_ROTATION.json). `G16` 독립 시즌 검수가 아니다.
- 설계/원고 게이트 `CLOSED`, `PROJECT_FREEZE v0.30 PARTIAL`, 정본 승격 0건.

| 단계 | 수행·결과 | 증거 경계 |
|---|---|---|
| Antigravity 자료 수집 | 설치된 `agy.exe`로 [공식 NBA 경기 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)의 명단 제한 조회를 요청. headless 세션의 `RunCommand` 권한이 자동 거부돼 빈 응답. CLI의 `status=SUCCESS`는 **자료 회수 성공이 아니다**. | 이번 단계 신규 증거 0건. 기존 G15Z의 공식 경기 출처와 Codex 직접 조회를 유지한다. 무제한 권한 우회는 하지 않았다. |
| NotebookLM 출처 제한 분석 | 기존 공식 [2022-01-23 19:30 ET 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf) 한 출처 `c8189748-40fd-473a-afcc-f7cc35b396dd`만 지정한 대화 `fdc0a3aa-84d3-42c5-9f38-b1b8bbd9c2bc`. 원역사 DEN Will Barton과 JaMychal Green이 `Available`, Jeff Green·Hyland 등은 `Out`이라고 반환. 계약·대체세계 등록·PF16분은 보고서로 판단할 수 없다고 명시. | Codex가 PDF 4쪽을 직접 대조했다. `Available`은 원역사 부상 보고 상태일 뿐 2022 대체세계 경기 분 배정의 증명이 아니다. 보고서에 Bey가 없다는 사실도 별도 대체 DEN 계약의 부정 증거가 아니다. |
| Codex 저장소 검사 | `python tools/check_o15g15z_denver_lineup.py`와 `python tools/check_o15g15bi_denver_quarters.py` 통과. X1/X2 각각 4쿼터 5인 중복0·240 선수분·최장 연속12분·G15Z 기준 최대차 64초. | 계약·의료·PF 적합성·실제 경기 교대·상대 전술을 검증하지 않는다. |
| Claude 결과물 단독 반증 | 도구 없는 `haiku`에 후보 JSON만 제공했다. 선수별 분 합계와 최장 연속 12분에 구체 반례를 제시하지 않았다. | 답변은 **24개 2분 칸을 48칸으로 오기**했고, “5명 서로 다름”을 실제 포지션 적합성 통과처럼 표현했다. 두 진술은 기각한다. 독립 NBA 출처 검증이나 G16 대체가 아니다. |

## 결과물 자체의 맹점

1. **유일한 수신자처럼 보이는 문제:** X1과 X2는 한 경기의 두 후보이지 함께 뛰는 11인 로테이션이 아니다. 다른 수신자는 각 분기에서 0분이다.
2. **원역사 분 복사의 문제:** 2분 칸 설계는 공식 박스의 개인분과 최대 64초 차이로 가깝지만 실제 Denver 교체 시각을 재구성하지 않았다. Nnaji의 득점·슛을 RX에게 이전하지 않는다.
3. **휴식과 출전 허가의 문제:** 최장 연속12분은 산술 상한이다. 무릎·피로·파울·매치업과 2021–22 계약/등록은 별도다. X2 Bey의 PF, X1 JaMychal의 원역사 DNP 변경에 비용이 남는다.

결론: `QUARTER_ROTATION_MATH_PASS / ROSTER_AND_REAL_GAME_HOLD`. D1 2020–21 정확 시즌과 D3 2021–22 실경기/장기 시즌 선택은 여전히 열려 있다.
