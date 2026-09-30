# Context Pack Protocol

2026-09-30 [D1 S2 선택](../canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json)과 [운영 규칙](../control/CHICAGO_2020_21_D1_S2_PROTOCOL.md)을 설계 샘플 출처/해시에 연결한다. 검증 기준의 변경이며 allowed_facts·개별 건강·시즌의 승격이 아니다. 실제 회차 Pack0·설계/원고 CLOSED.

Context Pack은 회차 작업에 필요한 최소 문맥을 모은 **파생 산출물**이다. 정본이 아니며, 캐논을 몰래 변경할 수 없다. 설계 게이트가 닫힌 동안에는 회차 집필용 팩이 아니라 설계 검증용 샘플만 허용한다.

## 생성 시점

전체 Act/Sub-Act/회차 기능표와 역사 사건 원장이 잠긴 뒤 생성한다. 현재 상태에서는 실제 회차 팩을 만들지 않는다.

## 필수 구성

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
required_historical_events:
relationship_state:
physical_state:
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
- 설계 샘플의 각 `allowed_facts`는 `fact_evidence`에 같은 문구·순서로 매핑하고, 상태와 출처 경로를 별도 기록함. 현재 허용 상태는 `CANON_FUNCTION`(이미 잠긴 기능), `CANDIDATE`(후보), `CONDITIONAL_RESULT`(조건부 계산 결과)뿐이다. 어느 상태도 개별 NBA 사건의 무조건적 `FACT`나 작가확정을 뜻하지 않는다
- 각 `fact_evidence.source_paths`는 `source_links`에 존재하고 `source_content_sha256`에서 동일 경로의 내용 해시로 해석되어야 함. 해시는 해당 파일의 변조·구식 여부를 검사하며, 원자료의 진실성이나 주장에 대한 독립 검증까지 증명하지 않음
- 현재 회차에서 활성화되지 않는 장치와 복선은 Pack에 넣지 않음
- Sub-Act 주 장치 1개와 선택 보조 1개 예산을 초과하지 않음
- Context Pack과 정본이 충돌하면 정본이 승리
- 사건 날짜와 선수 신체 상태가 연표와 일치
- 인물은 실제 권한 밖의 정보를 알거나 명령하지 않음
- `pov_character`의 한 값은 시점 전환 승인이 아니다. S1 시점 전환은 장래 실제 회차 Pack에서 구간 경계·정보 접근 근거가 잠긴 뒤 별도 검증한다
- 주인공이 접촉한 역사 사건은 시뮬레이션 ID를 포함
- 미검증 사실은 `HOLD`이며 원고 입력 금지
- 팩 생성 후 정본이 바뀌면 해당 팩은 `STALE` 처리

현재 CLOSED 게이트의 CP2 설계 샘플은 `tools/build_cp2_design_packets.py --check`로 **출처 내용 해시와 생성된 샘플 본문 자체**를 함께 대조한다. 이 검사는 실제 회차 팩의 생성 허가나 사실 승인으로 해석하지 않는다.

## Obsidian 연결

팩은 `[[canon/PROJECT_FREEZE]]`, 인물 정본, 세계 규칙, Act/Sub-Act, 사건 원장을 링크한다. 역링크는 탐색용이며 권위 관계를 바꾸지 않는다.
