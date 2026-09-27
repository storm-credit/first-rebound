# R01 — O-15F14-AO 제한 독립 반증

- Claude CLI `haiku --restricted --tools ''`에 [AO 문서](../research/O15F14AO_DENVER_NNAJI_OTHER_PLAYOFF_STINTS.md)와 [네 구간 도구](../tools/build_denver_2021_playoff_nnaji_other_stints.py)만 주고 산술·역할·출처 등급·18구간 과장을 공격하게 했다. 첫 CLI 요청은 과제를 따르지 않아 검토로 계수하지 않고, 두 번째 요청만 아래에 사용한다.
- 받아들인 경계: Claude가 직접 받은 도구는 네 구간만 계산한다. 18구간은 별도 [종합 도구](../tools/build_denver_2021_playoff_selected_lineup_bridge.py)와 [JSON](../simulation/DENVER_2021_PLAYOFF_SELECTED_LINEUP_BRIDGE.json)에 의존하므로 Claude 검토를 그 전체의 독립 통과로 표시하지 않는다. Codex는 양쪽 도구를 실행해 18개 구간 합산·JSON 재현성을 확인했다.
- 기각한 문구: Claude는 NBA 공식 박스를 “1차 자료 검증됨”이라고 썼지만 URL을 직접 열지 않았다. 이번 Claude 실행의 범위는 **제공 텍스트와 코드 검토**다. NBA 박스/FOX HTML은 Codex가 따로 읽었다. 같은 시계를 보존한다는 조건에서 Nnaji가 선택 명단에 없으므로 382초의 원출전 슬롯 재배정이 필요하다는 추론은 유효하지만, 실제 감독 선택은 미확정이다.
- 결과: 26+137+135+84=382초, Bey 단독 3/4와 Hartenstein 4/4 K1 역할 검사에 산술 반례는 발견하지 못했다. 원본 경기책 독립 교차검증, 건강·등록·득점·시리즈 검증은 이 R01의 범위 밖이다. F5와 시즌 `HOLD`.
