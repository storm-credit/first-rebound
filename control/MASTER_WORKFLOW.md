# Master Workflow

중앙 두 저장소의 필요한 기능만 작품에 맞게 결합한 단계 권위 문서다. 실행 세부는 `control/ORCHESTRATOR_WORKFLOW.md`가 이 순서를 참조한다.

| 단계 | 작업 | 산출물 | 종료 조건 |
|---|---|---|---|
| 0 | Intent/Partial Freeze | 불변값·금지사항·미정 분리 | 사용자 요구와 충돌 없음 |
| 1 | Blindspot/Trap Scan | 위험·복제·시대 선택 오류 | 치명적 맹점에 소유자 지정 |
| E0 | Era/Title Selection | 시대 4안·연표 역산·제목 방향 | 사용자 `LOCKED` 승인 |
| 2 | Research Charter | 선택 시대 질문·출처 등급 | 주장별 검증 방식 존재 |
| 3 | Historical Baseline | 한국→프렙→NCAA→NBA 원역사 원장 | 연도·날짜·출처·확신도 있음 |
| 4 | World/Character Model | 세계 규칙·인물·관계·신체 | 모든 선택의 제약 설명 가능 |
| 5 | Ending/Theme | 결말 기능·주제·대가 | 시작과 결말의 변화축 연결 |
| 6 | Causality Simulation | 접촉·파급·대안 사건 | 강제 복원 없이 결과 계산 가능 |
| 7 | Reference/House Style | 합법적 본문 표본과 단일 문체 규약 | 모사가 아닌 KEEP/ADOPT/AVOID/RANGE |
| 8 | Master Architecture | 전체 시즌/커리어 곡선 | 결말까지 변화·비용 누적 |
| 9 | Act Map | Act 목표·압력·선택·상태 변화 | Act마다 주 방법 1~2개 |
| 10 | Sub-Act Map | 하위 갈등과 주/보조 장치 | 각 Sub-Act 종료 상태 명확 |
| 11 | Unity Review | 인과·주제·POV·역할 통합 | 모순과 중복 없음 |
| 12 | Episode Function Map | 회차별 약속·전환·후크 | 모든 회차가 구조적 기능 보유 |
| 13 | Context Pack Build | 회차별 최소 입력 묶음 | 출처·버전·연속성 검사 통과 |
| 14 | Independent Review | 맹점·정의·현실성·견인력 | BLOCKER/HOLD 0 |
| 15 | Gate Approval | 사용자 승인 | `DESIGN_GATE=OPEN` |

## 반복 루프

각 단계는 `질문 → 중요한 결정의 4안 → 맹점 훑기 → 선택 → 문서 반영 → 독립 확인 → 상태 갱신`으로 닫는다. 이미 답한 질문은 다시 묻지 않고, 다음 결정을 실제로 막는 정보만 수집한다.
