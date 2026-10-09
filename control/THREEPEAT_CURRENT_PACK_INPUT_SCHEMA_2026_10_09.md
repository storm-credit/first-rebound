# 현재 삼연패 본편 Context Pack 입력 계약

상태: **첫 독립 검수의 3개 결함 수리 완료·독립 재검수 대기**. 이 문서는 입력 형식을 정의하며 작품의 선택·최종 회차·청사진을 승인하지 않는다. 실제 Pack은 0개이며 원고와 설계 게이트는 CLOSED, freeze는 v0.30 PARTIAL이다. 최초 입력과 실패 영수증은 Git `f528c1e0c7ebc1004c6da377d6e4ab7b9bc99a95`에 보존되며 이 세대의 입력 해시를 새 세대의 현재 입력 핀으로 바꾸지 않는다.

## 1. 적용 범위와 실행

별도 `tools/build_threepeat_actual_context_packs.py`는 현재 본편 M01–M09와 짧은 EPI를 순서대로 소비한다. 기존 LC1 컴파일러·14막/42소막·원111회차·146비트는 이력과 기능 처분의 근거로 보존한다. 새 컴파일러가 그 이전 구조의 전체 완성을 다시 요구하지 않는다. 40개 기능 묶음은 후보이며 **최종 N의 기본값이 아니다**. N은 별도의 최종 회차표와 개별 청사진이 확정된 뒤 양의 정수로 발급한다.

기본 실행은 입력만 검증하고 파일을 쓰지 않는다. `--write`만 실제 출력 생성을 요청하며 `--check`는 이미 존재하는 전체 출력을 읽어 검증한다. 현재는 아래 최종 입력이 발급되지 않았으므로 기본 실행도 명확한 오류와 종료 코드 2로 차단된다. 테스트의 입력·출력은 모두 TemporaryDirectory 안에만 만든다.

| 입력 | 요구 상태 |
|---|---|
| `control/THREEPEAT_CURRENT_PACK_SCOPE_AUTHORITY.json` | `LOCKED_CURRENT_PACK_SCOPE` |
| `canon/THREEPEAT_CURRENT_SELECTED_HISTORY_AND_EXIT_LOCK.json` | `LOCKED_CURRENT_SELECTED_HISTORY` |
| `design/THREEPEAT_FINAL_EPISODE_ALLOCATION.json` | `LOCKED_CURRENT_FINAL_EPISODE_FUNCTION_TABLE` |
| `control/THREEPEAT_CURRENT_EPISODE_BLUEPRINT_AUTHORITY.json` | `ACTUAL_CURRENT_BLUEPRINT_AUTHORITY` |

이 네 파일을 이번 작업에서 발급하지 않는다. 실제 출력 경로는 `context-packs/threepeat-actual`이다. 각 입력은 동일한 `scope_id`, 비어 있지 않은 `producer_id`, `manuscript_allowed=false`, `design_gate=CLOSED`, `freeze=v0.30 PARTIAL`을 가진다.

## 2. 현재 범위와 NBA 비중

범위 권위는 `active_unit_ids=[M01,...,M09,EPI]`, 실제로 모두 소비할 `required_exit_port_ids`, 현재 선택 자료의 `selected_scope_ref`를 제공한다. 해당 참조는 원 선택 자료의 JSON 객체를 직접 읽어 2023/2024/2025 Chicago 우승 목표·2025 본편 종결·2035 짧은 후일담을 확인한다. 원 선택 자료의 생성 시점 실행 대기는 새 청사진 승인을 뜻하지 않는다.

`category_policy`는 분모 `ALL_FINAL_EPISODES`, 하한 75·상한 85를 유지한다. `counted_categories`는 `NBA` 또는 명시적으로 승인된 `NBA`+`NBA_DRAFT` 중 하나이며, 드래프트 포함 여부를 40개 후보 묶음의 민감도에서 추정하지 않는다. 최소한 NBA/NBA_DRAFT/PRE_NBA/POST_NBA의 의미를 `category_definitions`에 쓴다. 실제 최종 행의 태그 의미는 독립 검수가 판단한다. 컴파일러는 숫자 비율과 승인 정책의 일치를 확인한다.

정책은 `selection_source_ref`가 가리키는 **선택된** `EPISODE_CATEGORY_POLICY` 객체의 `policy`와 정확히 같아야 한다. 정책 객체에는 `selection_source_ref`를 다시 넣지 않아 순환을 피한다. EPI의 회차는 POST_NBA다. 드래프트 제외 비율은 별도 진단값으로 출력하며 추가 통과 기준으로 만들지 않는다. 최종 N 또는 정책 선택이 없으면 생성할 수 없다.

## 3. 결과에 영향을 주는 선택의 원 자료 조인

범위 권위의 `consequential_choice_requirements`와 역사의 `consequential_choices`는 같은 ID 집합이다. 현재 사용 범위의 두 필수 선택은 다음과 같다.

| ID | 종류 | 실제 처리 |
|---|---|---|
| `C01_CALENDAR` | `CALENDAR_AVAILABILITY` | 공적 출전·훈련·여행·병역이 실제 사용 창에 주는 달력 영향을 선택한 해법으로 해소해야 한다. 금메달 자동 선택을 요구하지 않는다. |
| `EARLY_REWARD_IMPLEMENTATION` | `EARLY_CAREER_REWARD` | 초반 보상 방향을 선택한 해법으로 해소해야 한다. 특정 개인상을 강제하지 않는다. |

각 사용 선택은 `use_mode=USED`, `status=RESOLVED_SELECTED`, 비어 있지 않은 `used_port_ids`, 원 선택 객체의 `selection_source_ref`, 원 객체와 동일한 `resolution`을 가진다. 원 객체는 `selected=true`, `status=SELECTED_FICTIONAL_USED_RESOLUTION`, `authority_class=AUTHOR_SELECTED` 또는 `DELEGATED_SELECTED`, 동일한 `choice_id`/`kind`, 비어 있지 않은 해법, `unresolved_used_dependencies=[]`를 직접 제공한다. 기존 선택을 후행 표준 객체로 소비할 때도 실제 author/delegated 선택의 내용과 독립 검수 범위를 보존해야 한다. 형식만 채운 생산자 객체가 새 선택을 만들지는 않는다.

달력 객체는 추가로 `used_calendar_status=SELECTED_RESOLVED`, 실제 선택에 종속된 포트를 포함하는 `covered_exit_port_ids`를 제공한다. selected 플래그만 true인 채 달력 HOLD가 남아 있거나 원 자료가 UNSELECTED/CANDIDATE/HOLD/selected=false이면 독립 검수 해시를 새로 만들어도 거절한다. 포트→선택과 선택→포트 연결을 양쪽으로 확인한다. 청사진의 사용 선택도 같은 레지스트리와 포트에 연결한다.

미사용 MVP/FMVP는 별도 선택 행을 `use_mode=NOT_USED`, `status=NOT_USED`, `used_port_ids=[]`로 둘 수 있고 결과가 null이어도 전체 생성의 장애물이 아니다. 단 `effect_kind=PERSONAL_AWARD_MAX_SALARY` 주장은 그 청사진에 선언된 `requires_selected_choice_ids`를 통해 실제 선택된 `PERSONAL_AWARD` 자료를 소비해야 한다. 미사용 null을 HigherMax 근거로 바꿀 수 없다.

## 4. 현재 역사와 최종 회차표

현재 역사는 `current_used_scope_complete=true`와 모든 `finite_used_exit_ports`를 제공한다. 각 포트는 `port_id`, 현재 `unit_id`, `status=SELECTED_RESOLVED`, 구체적인 `entry_state`/`changed_action`/`durable_cost`/`exit_state`, 원 사용 자료 `source_refs`, 사용 선택 ID를 가진다. 이전17개 NBA 시즌의 세계 전체 인증을 대신 요구하지 않는다.

`unit_exits`는 M01–M09/EPI 각 1행이다. 각 행의 진입·출구·포트 소유·다음 막 ID와 다음 진입이 서로 맞아야 한다. EPI의 다음 막과 진입은 null이다. 최종 회차표는 `final_episode_count=N`, 1~N 연속 정수 `episode`, 막 순서와 전체 막 사용을 제공한다. Boolean과 부동소수점 회차 번호는 금지한다.

각 최종 회차 행과 개별 청사진은 다음 값을 정확히 공유한다: `episode`, `unit_id`, `category`, `episode_function`, `action_choice`, `durable_cost`, `state_change`, `entry_state`, `exit_state_required`, `consumed_exit_port_ids`, `consequential_choice_ids`. 각 막의 첫 진입과 마지막 출구는 현재 역사와 같다. 최종 회차 전체의 포트 합집합이 요구 포트를 빠짐없이 소비해야 한다. 다른 막의 포트를 회차에 붙일 수 없다. 같은 포트의 내부 과정이 여러 회차에 걸칠 수 있으나 그 의미·밀도·인물 비용은 최종표의 독립 검수 대상이다.

## 5. 실제 개별 청사진과 정보 접근

권위 파일의 `episode_authorities`는 정확히 N개의 정수 회차와 `qualified_status=ACTUAL_VERIFIED`, 청사진 `path/source_sha256/json_pointer`를 가진다. 묶음 문서 상태는 `ACTUAL_VERIFIED_CURRENT_BLUEPRINT_BUNDLE`, 개별 객체는 `ACTUAL_VERIFIED`여야 한다. 개별 객체도 Boolean/float가 아닌 정확한 정수 `episode`와 현재와 같은 `scope_id`를 가져야 한다. 후보와 문서상 검수 완료 플래그를 실제 개별 청사진으로 승격하지 않는다.

청사진에는 구체적인 `timeline_window`, `unit_question`, 1~2개 `primary_devices`, `setup_to_plant`, `payoff_to_consume`, `reader_question`, `relationship_state`, `physical_state`, `basketball_goal`, `forbidden_changes`가 필요하다. 실제 사용 미해소 종속은 `unresolved_used_dependencies=[]`가 되어야 한다. 이 문서가 새 학업 증서·개인 임상 기록·모든 NBA 박스의 현실 인증을 요구하지 않는다.

`information_boundary`는 `LOCKED_SELECTED_SCENE_ACCESS`, 현재 POV, 구체적인 `clock_basis`, 검수된 시계 순서와 실제 `scene_segments`/`access_witnesses`를 제공한다. 장면은 고유 ID·증가하는 유한 시계·POV·해당 장면의 claim 인덱스를 가진다. POV가 바뀌면 승인 여부와 화면 경계 표식이 필요하다.

각 witness는 존재하는 장면 ID, 그 장면 POV와 같은 owner, 같은 장면 시계, 획득 시계, 구체적 방법과 그 장면에 속한 claim 인덱스만 가진다. 관측 사건 시계 ≤ 획득 시계 ≤ 장면 시계다. CURRENT_PLAN과 EXPLICIT_INFERENCE는 관측 FACT가 아니며 주장과 witness의 temporal_kind가 같아야 한다. 모든 장면 지식은 witness가 뒷받침하고 모든 claim은 실제 장면에 사용된다. Boolean/NaN/Infinity 시계, 존재하지 않는 장면·다른 인물·다른 장면 claim을 붙인 witness는 거절한다.

주장의 status는 CANON_FUNCTION/AUTHOR_MODELED_DESIGN/FACT/INFERENCE다. FACT는 temporal_kind가 OBSERVED_EVENT여야 하며 `primary_source_body_verified=true`, INFERENCE는 `inference_visible=true`가 필요하고 모두 원 출처를 가진다. CURRENT_PLAN을 FACT로 내보낼 수 없다. 공개된 향후 일정의 발표를 아는 사실은 관측한 발표 사건으로 표현하며 향후 경기가 이미 일어났다는 관측으로 바꾸지 않는다. 이 표시는 공급된 자료와 검수 범위의 선언이며 컴파일러가 원문의 진실이나 인물의 사적 인지 사실을 별도로 인증한다는 뜻이 아니다.

## 6. 원 출처와 독립 검수

참조는 repository 내부 상대 경로·정규화 UTF8 LF SHA256을 사용한다. JSON의 루트 포인터는 빈 문자열이다. `/`는 빈 문자열 키, `~0`/`~1`만 허용하며 배열 인덱스는 0 또는 선행0 없는 양의 정수다. `-1`, `01`, `-`, 잘못된 tilde escape는 금지한다. 중복 JSON 키와 비유한 숫자도 거절한다.

이번 컴파일러는 실제 현재 파일의 bytes만 읽는다. 직접 참조에 `source_snapshot_commit`, `source_snapshot_commits`, `snapshot_commit`, `source_epoch`, `epoch`를 선언하면 지원하지 않는 세대 참조로 명시적으로 거절한다. 이를 무시한 채 live 파일을 그 Git 세대의 자료라고 읽지 않는다. 과거 입력·실패·영수증의 세대 메타데이터는 보존하며, 실제 팩의 현재 typed claim은 해당 범위로 이미 채택된 고정 자료의 현재 핀을 소비한다. 원 자료 자체를 복제하거나 과거 검수 해시를 현재 승인 해시로 바꾸는 절차가 아니다.

MD/CSV/UTF8 텍스트는 새 JSON 사본 없이 `format=UTF8_TEXT`, `json_pointer=""`, 명시적 `text_locator`로 읽는다. locator는 `WHOLE_TEXT` 또는 1부터 시작하는 정수 `LINE_RANGE`(start_line/end_line)다. 선택적으로 `expected_text`를 직접 대조한다. 텍스트 본문을 선택 권위의 JSON 객체로 해석하지 않는다. 선택·정책·범위 권위는 JSON 객체여야 한다. 원 PDF 등 binary는 기존 typed evidence receipt의 필요한 필드만 참조하며 raw PDF SHA를 UTF8 정규화 SHA와 혼동하지 않는다.

독립 영수증은 `ACCEPTED_CURRENT_THREEPEAT_PACK_INPUTS`, `independent_review_completed=true`, 모든 입력·청사진·실제로 사용한 출처의 정확한 `reviewed_artifacts_sha256`, 공급된 `reviewer_id`를 제공한다. reviewer ID는 입력 및 청사진의 producer ID와 달라야 한다. 파일 digest는 사람의 신원을 암호학적으로 증명하지 않는다.

권위 파일과 영수증의 상호 해시 순환은 `reviewed_authority_payload_sha256`으로 피한다. 이는 권위 파일에서 `independent_review` 키만 제외한 나머지 객체를 `ensure_ascii=false`, `sort_keys=true`, 구분자 `(',',':')`, NaN 금지로 JSON 직렬화한 UTF8 bytes의 SHA256이다. 영수증의 실제 파일 SHA는 권위 파일이 핀한다. 두 개의 다른 기준을 ordinary whole-file SHA라고 부르지 않는다.

완전히 위조된 선택 객체와 검수자 신원 전체를 해시만으로 식별한다는 주장은 하지 않는다. 이 컴파일러는 공급된 권위의 조인·출처/시점/타입·검수 범위와 변경 여부를 검사한다. 실제 작가 위임과 독립 의미 검수는 저장소의 별도 책임이다.

## 7. 출력 보호와 현재 결과

모든 입력을 먼저 검증하고 출력 전체를 preflight한다. 오래되거나 다른 내용의 기존 Pack·예상하지 않은 파일/디렉터리·경로 이탈을 발견하면 첫 새 파일도 쓰지 않는다. 파일은 exclusive create로 만들며 기존 같은 bytes는 재사용하고 덮어쓰지 않는다. 쓰기 도중 실패하면 이번 호출에서 막 생성한 파일을 제거한다. 시스템의 다른 프로세스와 모든 상황에서 원자적이라는 주장은 하지 않는다.

현재 보호 테스트 26개는 최초23개를 유지하고 개별 청사진 번호·범위, 명시된 지원하지 않는 세대, FACT+CURRENT_PLAN의 실제 실패 반례 3종을 추가한다. 기존 검수 범위는 격리된 가변 N/9막, 선택 HOLD 세탁, 미사용 개인상과 HigherMax, 유한 출구 누락, 최종 N/정책/드래프트 분류, stale/producer review, 후보/OPEN/device, RFC6901, 시계·ghost witness, 원 MD/CSV, JSON 중복/overflow, 전체 출력 사전 대조와 부분 IO 복구다. 실제 Pack/청사진/원고 생성이나 G13/G14 통과를 인증하지 않는다. 후행 총괄·독립 공격 재검수가 끝나기 전에는 **수리본 독립 수락 0**이다.
