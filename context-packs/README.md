# Context Pack Protocol

Context Pack은 회차 작업에 필요한 최소 문맥을 모은 **파생 산출물**이다. 정본이 아니며, 캐논을 몰래 변경할 수 없다. 설계 게이트가 닫힌 동안에는 회차 집필용 팩이 아니라 설계 검증용 샘플만 허용한다.

## 생성 시점

전체 Act/Sub-Act/회차 기능표와 역사 사건 원장이 잠긴 뒤 생성한다. 현재 상태에서는 실제 회차 팩을 만들지 않는다.

## 필수 구성

```yaml
pack_id:
target_episode_or_design_unit:
generated_at:
source_commit:
canon_version:
timeline_window:
pov_character:
entry_state:
episode_function:
act_question:
subact_question:
primary_narrative_device:
secondary_device_optional:
active_setup:
payoff_or_defer:
reader_expected_question:
do_not_explain_device: true
allowed_facts:
required_historical_events:
relationship_state:
physical_state:
basketball_constraints:
promises_to_pay:
forbidden_moves:
exit_state_required:
source_links:
integrity_status:
```

## 무결성 규칙

- 모든 사실에 원본 문서 링크와 버전이 있어야 함
- 현재 회차에서 활성화되지 않는 장치와 복선은 Pack에 넣지 않음
- Sub-Act 주 장치 1개와 선택 보조 1개 예산을 초과하지 않음
- Context Pack과 정본이 충돌하면 정본이 승리
- 사건 날짜와 선수 신체 상태가 연표와 일치
- 인물은 실제 권한 밖의 정보를 알거나 명령하지 않음
- 주인공이 접촉한 역사 사건은 시뮬레이션 ID를 포함
- 미검증 사실은 `HOLD`이며 원고 입력 금지
- 팩 생성 후 정본이 바뀌면 해당 팩은 `STALE` 처리

## Obsidian 연결

팩은 `[[canon/PROJECT_FREEZE]]`, 인물 정본, 세계 규칙, Act/Sub-Act, 사건 원장을 링크한다. 역링크는 탐색용이며 권위 관계를 바꾸지 않는다.
