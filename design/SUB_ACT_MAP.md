# Sub-Act Map

- 상태: `NBA_LONG_RANGE_AUTHOR_SELECTION_HOLD / NOT_STARTED`
- 목적: Act를 회차로 바로 쪼개지 않고 인물과 세계의 상태가 실제로 변하는 중간 단위로 검증한다.

## Sub-Act 필수 필드

```yaml
sub_act_id:
parent_act:
time_and_place:
entry_state:
goal:
pressure:
primary_device:
secondary_device_optional:
basketball_question:
institutional_constraint:
relationship_in_play:
irreversible_choice:
cost:
exit_state:
historical_events_touched:
research_dependencies:
continuity_checks:
status:
```

## 설계 규칙

- E0는 2018 Draft로 잠겼다. NBA 장기 경로와 라이벌 팀을 선택하기 전에는 전체 Sub-Act를 확정하지 않음
- 주 장치 1개, 필요 시 보조 장치 1개만 선택
- 경기 결과만으로 종료하지 않고 관계·제도·자기인식 중 하나를 바꿈
- 성장 보상에는 훈련 시간, 출전 손실, 관계 마찰, 부상 위험 중 실제 비용이 따름
- 역사 사건을 건드리면 `simulation/CAUSALITY_MODEL.md`의 사건 ID를 연결
- 회차 수는 Sub-Act가 잠긴 뒤 배정
- 서술문·대사·장면 원고는 작성하지 않음

## NBA 장기 경로 선택 이후 예정 순서

1. 첫 Act와 최종 Act를 상세화해 시작/결말 대응 검증
2. 선택 드래프트 Act를 사실 연구와 함께 상세화
3. 프렙/NCAA 자격과 성장 연결
4. NBA 팀·계약·우승창·쇠퇴·은퇴 시뮬레이션
5. 전체 Sub-Act 비용과 보상 간격 통합 검수
