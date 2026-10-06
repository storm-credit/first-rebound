# Context Pack Protocol

2026-09-30 [D1 S2 선택](../canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json)과 [운영 규칙](../control/CHICAGO_2020_21_D1_S2_PROTOCOL.md)을 설계 샘플 출처/해시에 연결한다. 검증 기준의 변경이며 allowed_facts·개별 건강·시즌의 승격이 아니다. 실제 회차 Pack0·설계/원고 CLOSED.

Context Pack은 회차 작업에 필요한 최소 문맥을 모은 **파생 산출물**이다. 정본이 아니며, 캐논을 몰래 변경할 수 없다. 설계/원고 게이트가 `CLOSED`인 동안에는 원고 작성과 실제 Pack의 집필 입력 사용을 금지한다. 다만 아래 생성 선행조건을 충족하면 G14의 **집필 전 생성·무결성 검증**을 위해 실제 회차 Pack을 만들 수 있다. 이때도 게이트 `CLOSED`와 `manuscript_allowed:false`를 유지한다. Pack 생성·검증을 집필 허가로 읽지 않는다.

## 생성 시점

전체 Act/Sub-Act/회차 기능표와 역사 사건 원장이 잠기고, 해당 구간의 `ACTUAL_VERIFIED` Blueprint와 현행 Canon을 확보한 뒤 생성한다. 이 선행조건을 삭제하거나 후보 Blueprint를 실제 Pack으로 컴파일하지 않는다. 현재는 G13 최종 회차 기능표와 역사 잠금이 미완료이므로 실제 회차 팩0·설계 검증용 샘플2를 유지한다.

G14 생성·검증은 `OPEN`의 선행조건이며 `OPEN`을 기다리는 단계가 아니다. G14 뒤의 G15/G16 전체 검수와 G17 사용자 명시 승인, 별도 게이트 개방 PR을 통과한 뒤에만 Pack을 원고 입력으로 사용할 수 있다. 따라서 `Pack→G14→OPEN→Pack` 순환이 발생하지 않는다. 이 순서 정리는 현재 Pack 생성 선행조건의 충족이나 원고 게이트 개방을 뜻하지 않는다.

## 필수 구성

현재 두 샘플의 최상위 경계:

```yaml
actual_episode_packs: 0
manuscript_allowed: false
author_locked: false
samples: [] # 아래 개별 샘플 구조 두 개
```

```yaml
pack_id:
target_episode_or_design_unit:
purpose: DESIGN_VALIDATION_ONLY_NOT_EPISODE_PACK # 현재 CP2 샘플 한정
manuscript_allowed: false
author_locked: false
generated_at:
source_commit:
source_revision: # 기반 커밋과 이후 파일 내용 해시를 구별
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
fact_evidence: # allowed_facts와 같은 순서의 claim/status/source_paths
information_boundary:
  mode: DESIGN_REVIEW_NO_IN_WORLD_ACCESS
  reviewer_loaded_claim_indexes: [] # 생성기가 fact_evidence의 모든 인덱스로 채움
  story_known_claim_indexes: []
  scene_segments: []
  access_witnesses: []
  relative_time_references: []
  exact_scene_date: null
  pov_author_locked: false
  narrative_access_status: HOLD
required_historical_events:
relationship_state:
physical_state:
hold_fields: # 미검증 항목 목록; fact_evidence.status와 별도
basketball_constraints:
promises_to_pay:
forbidden_moves:
exit_state_required:
source_links:
source_content_sha256: # source_links의 모든 경로를 파일 내용 SHA-256에 연결
integrity_status:
```

현재 샘플 파일의 최상위에는 `actual_episode_packs: 0`, `manuscript_allowed: false`, `author_locked: false`가 있어야 한다. `purpose`와 이 세 필드는 설계 검증용 샘플이라는 경계를 표시한다. 이 YAML은 실제 회차 Pack의 생성 허가나 완성된 범용 스키마가 아니다.

## 무결성 규칙

- 모든 사실에 원본 문서 링크와 버전이 있어야 함
- 설계 샘플의 각 `allowed_facts`는 `fact_evidence`에 같은 문구·순서로 매핑하고, 상태와 출처 경로를 별도 기록함. 허용 상태는 `CANON_FUNCTION`(이미 잠긴 기능), `CANDIDATE`(후보), `CONDITIONAL_RESULT`(조건부 계산 결과), `AUTHOR_MODELED_DESIGN`(지정 범위에서 이미 위임 선택된 설계)이다. 마지막 상태는 현재 생성기의 CP2-A06-S3 지정 주장과 해당 작가 선택 출처가 연결된 경우만 허용하며, 역사적 `FACT`나 전체 시즌 실행 승인을 뜻하지 않는다
- 각 `fact_evidence.source_paths`는 `source_links`에 존재하고 `source_content_sha256`에서 동일 경로의 내용 해시로 해석되어야 함. 해시는 해당 파일의 변조·구식 여부를 검사하며, 원자료의 진실성이나 주장에 대한 독립 검증까지 증명하지 않음
- 현재 회차에서 활성화되지 않는 장치와 복선은 Pack에 넣지 않음
- Sub-Act 주 장치 1개와 선택 보조 1개 예산을 초과하지 않음
- Context Pack과 정본이 충돌하면 정본이 승리
- 사건 날짜와 선수 신체 상태가 연표와 일치
- 인물은 실제 권한 밖의 정보를 알거나 명령하지 않음
- `pov_character`의 한 값은 시점 전환 승인이 아니다. S1 시점 전환은 장래 실제 회차 Pack에서 구간 경계·정보 접근 근거가 잠긴 뒤 별도 검증한다
- 주인공이 접촉한 역사 사건은 시뮬레이션 ID를 포함
- 미검증 항목은 샘플의 `hold_fields` 목록에 별도로 기록하며 원고 입력 금지. 이 `hold_fields` 목록과 `fact_evidence.status`는 다른 필드이며 HOLD를 허용 사실로 추가하지 않음
- 팩 생성 후 정본이 바뀌면 해당 팩은 `STALE` 처리

현재 CLOSED 게이트의 CP2 설계 샘플은 `tools/build_cp2_design_packets.py --check`로 **출처 내용 해시와 생성된 샘플 본문 자체**를 함께 대조한다. 이 검사는 실제 회차 팩의 생성 허가나 사실 승인으로 해석하지 않는다.

## 설계 검토자의 정보와 극중 지식

2026-10-01 두 설계 샘플에 `information_boundary`를 추가했다. 검토자는 `fact_evidence`를 모두 로드하지만 이것이 극중 인물이 아는 정보는 아니다. 현재 `story_known_claim_indexes`, `scene_segments`, `access_witnesses`, `relative_time_references`는 빈 배열이며 `exact_scene_date=null`, `pov_author_locked=false`, `narrative_access_status=HOLD`다. 최상위/샘플의 `author_locked=false`는 설계 샘플 자체가 작가확정이 아니라는 표시이고 `pov_author_locked=false`는 해당 회차 시점이 미승인이라는 별도 표시다. 출처로 연결한 이미 승인된 작가 선택을 취소하지 않는다. 생성기는 이 경계를 벗어난 샘플을 거절한다. 실제 회차 Pack0·원고0·G14 최종 HOLD다.

`assess_observed_access`는 별도 시험 도우미다. 입력된 **과거 관측 사건**의 사건일≤정보 취득일≤구간일과 접근 경로·소유자·출처 표지만 기계적으로 확인한다. 유효 날짜라도 입력의 진실성·출처 존재·POV 승인을 인증하지 않는다. 미확인/잘못된 날짜는 HOLD, 역전은 FAIL이며 성공 명칭도 `SUPPLIED_CLOCK_REPRODUCTION_PASS_NOT_NARRATIVE_CLEARANCE`다. 미래 계획·예측에는 적용하지 않는다. 실제 회차의 상대 시간 표현과 시점 전환은 승인된 회차 구간·POV·정보 경로를 확보한 뒤 별도 검사해야 한다.

## Obsidian 연결

팩은 `[[canon/PROJECT_FREEZE]]`, 인물 정본, 세계 규칙, Act/Sub-Act, 사건 원장을 링크한다. 역링크는 탐색용이며 권위 관계를 바꾸지 않는다.
