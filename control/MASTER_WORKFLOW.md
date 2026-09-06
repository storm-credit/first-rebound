# Master Workflow

중앙 두 저장소의 필요한 기능만 작품에 맞게 결합한 단계 권위 문서다. 실행 세부는 `control/ORCHESTRATOR_WORKFLOW.md`가 이 순서를 참조한다.

| 단계 | 작업 | 산출물 | 종료 조건 |
|---|---|---|---|
| 0 | Intent/Partial Freeze | 불변값·금지사항·미정 분리 | 사용자 요구와 충돌 없음 |
| 1 | Blindspot/Trap Scan | 위험·복제·시대 선택 오류 | 치명적 맹점에 소유자 지정 |
| E0 | Era/Title Selection | 시대 4안·연표 역산·제목 방향 | 사용자 `LOCKED` 승인 |
| 2 | Research Charter | 선택 시대 질문·출처 등급 | 주장별 검증 방식 존재 |
| 3 | Historical Baseline | 한국→프렙→NCAA→NBA 원역사 원장 | 연도·날짜·출처·확신도 |
| 4 | World/Character Model | 세계 규칙·인물·관계·신체 | 모든 선택의 제약 설명 |
| 5 | Ending/Theme | 결말 기능·주제·대가 | 시작과 결말의 변화축 연결 |
| 6 | House Style Lock | 작품 전체 단일 문체 규약 | 캐논·장르·가독성 기준 고정 |
| 7 | Narrative Device Budget | 역순 설계·복선·회수·장치 예산 | Act/Sub-Act 과밀 방지 |
| 8 | Reference Deep Read/Craft | 합법적 본문 표본과 기능 추출 | 모사 없는 KEEP/ADOPT/AVOID/RANGE |
| 9 | Causality Simulation | 접촉·파급·대안 사건 | 원역사 강제 복원 없음 |
| 10 | Master Architecture | 전체 시즌/커리어 곡선 | 결말까지 변화·비용 누적 |
| 11 | Act Map | Act 목표·압력·선택·장치 | Act 주 작법 1~2개 |
| 12 | Sub-Act Map | 하위 갈등과 장치·약속 | 주 장치 1 + 선택 보조 1 |
| 13 | Unity Review | Hoffman 통일성·과잉 장치·혼합 검수 | 좋은데 불필요한 재료 제거 |
| 14 | Episode Function Map | 회차별 약속·전환·후크 | 삭제 가능한 회차 0 |
| 15 | Context Pack Build | 회차별 최소 입력 묶음 | 활성 장치만 로드, 무결성 PASS |
| 16 | Independent/Traction Review | 맹점·현실성·연재 견인력 | BLOCKER/HOLD 0 |
| 17 | Gate Approval | 사용자 승인 | `DESIGN_GATE=OPEN` |

## 반복 루프

각 단계는 `질문 → 중요한 결정의 4안 → 맹점 훑기 → 선택 → 문서 반영 → 독립 확인 → 상태 갱신`으로 닫는다. 이미 답한 질문은 다시 묻지 않고 다음 결정을 실제로 막는 정보만 수집한다.
