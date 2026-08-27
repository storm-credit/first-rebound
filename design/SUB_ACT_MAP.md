# Sub-Act Map

- 상태: `NOT_STARTED`
- 목적: Act를 회차로 바로 쪼개지 않고, 인물과 세계의 상태가 실제로 변하는 중간 단위로 검증한다.

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
baseball_or_basketball_question:
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

`baseball_or_basketball_question` 필드명은 이 프로젝트에서 반드시 `basketball_question`으로 사용한다.

## 설계 규칙

- 주 장치 1개, 필요 시 보조 장치 1개만 선택
- 경기 결과만으로 종료하지 않고 관계·제도·자기인식 중 하나를 바꿈
- 성장 보상에는 훈련 시간, 출전 손실, 관계 마찰, 부상 위험 중 실제 비용이 따름
- 역사 사건을 건드리면 `simulation/CAUSALITY_MODEL.md`의 사건 ID를 연결
- 회차 수는 Sub-Act가 잠긴 뒤 배정
- 서술문·대사·장면 원고는 작성하지 않음

## 예정 순서

1. Act 1과 Act 10을 먼저 상세화해 시작/결말 대응 검증
2. Act 7의 2004 드래프트를 사실 연구와 함께 상세화
3. Act 3~6의 프렙/NCAA 자격과 성장 연결
4. Act 8~9의 팀·계약·우승창 시뮬레이션
5. 전체 Sub-Act 간 비용과 보상 간격 통합 검수
