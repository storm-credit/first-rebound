"""Build two editorial working boundaries; all concrete new actions remain candidates.

This is not a scene, final episode, Context Pack, school authorization, or canon lock.
Repository hashes strip a UTF-8 BOM and normalize CRLF/CR to LF.
"""
from pathlib import Path
from copy import deepcopy
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE_MAIN = '7e3949604a5158ae314dcff54c05bf81bf6b4d63'
OUT = ROOT / 'design/A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.json'
MD = OUT.with_suffix('.md')
SKILL = Path('C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md')
SOURCES = (
    'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/A01_OPENING_EPISODE_BOUNDARY.md',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'design/CP2_PROMISE_LEDGER.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
    'canon/PROJECT_FREEZE.md',
    'control/DESIGN_GATE.md',
    'context-packs/README.md',
    'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.json',
    'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.md',
)


def normalized(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def readj(path):
    return json.loads(normalized(ROOT / path))


def digest(path):
    return hashlib.sha256(normalized(path).encode('utf-8')).hexdigest()


def build():
    contribution = readj(SOURCES[0])
    functions = readj(SOURCES[1])
    cf = {row['id']: row for row in functions['functions']}
    parent = readj(SOURCES[3])
    act = next(row for row in parent['acts'] if row['id'] == 'A01')
    subact = next(row for row in parent['subacts'] if row['id'] == 'A01-S2')
    authority = readj(SOURCES[7])
    if contribution['status'] != 'ACTUAL_VERIFIED':
        raise ValueError('C3 must be the verified local core input, not a candidate replacement')
    if act['planned_units'] != 36 or cf['A01-CF07']['next'] != 'A01-CF08':
        raise ValueError('preserved A01 allocation/CF07 to CF08 chain changed')
    if cf['A01-CF08']['next'] != 'A01-CF09':
        raise ValueError('game-reward test must remain the following CF09')
    if any(cf[k]['selected_event'] is not False for k in ('A01-CF07', 'A01-CF08')):
        raise ValueError('source concrete-event authority changed; review before regeneration')
    if authority['selected']['style']['route'] != 'S1':
        raise ValueError('source style route changed')
    # State labels are Korean editorial descriptions, not prose or realized events.
    transition = (
        '기본 학습을 시도할 작업 범위를 정했고 기술 완성·반복 성공은 미선택이다. '
        '다음 팀 준비 약속의 구체 작업과 수행 결과는 후보로 남는다.'
    )
    holds = ['exact_date', 'school_permission', 'school_name', 'teacher_authorization',
             'class_attendance_completion', 'academic_supplement_completion',
             'attendance_disposition', 'team_membership', 'athletic_registration',
             'concrete_action_selection', 'drill_format', 'duration', 'named_teammate',
             'observable_result', 'individual_scene_pov', 'episode_number']
    info = {
        'global_style': 'S1', 'scope': 'DESIGN_REVIEW_INFORMATION_RULES_NOT_SCENE_POV_CERTIFICATE',
        'possible_in_world_access': ['자신이 실제 수행한 행동', '자신이 직접 본 공·위치·동료 행동',
                                     '실제로 전달받은 과제·시간 조건'],
        'not_yet_observed': ['어떤 구체 과제를 전달받았는지', '누가 어떤 준비를 대신 맡았는지',
                             '준비 수행 뒤 누구의 부담이 얼마나 줄었는지'],
        'forbidden_access': ['감독·라이벌·동료의 비공개 생각', '미전달 학교 결정',
                             '장래 기술 완성·성공', '팀원 전원의 신뢰'],
        'story_known_claim_indexes': [], 'scene_segments': [], 'access_witnesses': [],
        'exact_scene_date': None, 'individual_scene_pov_verified': False,
    }
    boundaries = [
        {
            'id': 'A01-LEARNING-WB', 'source_function': 'A01-CF07', 'subact': 'A01-S2',
            'status': 'WORKING_EDITORIAL_BOUNDARY_CONCRETE_EVENT_CANDIDATE',
            'entry_state': contribution['exit_state'],
            'source_function_entry_summary': cf['A01-CF07']['entry_state'],
            'entry_summary_is_exact_handoff': False,
            'single_function': '첫 팀 기여를 반복할 준비 과제로 좁히며 기본 학습 시도의 범위를 정한다',
            'working_boundary_selection': 'C3 뒤 기본 과제를 시도하는 범위까지만 다루고 반복 성공·기술 완성 전에 끝낸다',
            'action_candidates': [
                {'id': 'L-A', 'status': 'CANDIDATE', 'action': '박스아웃·위치선정·패스 중 한 기본 과제를 먼저 시도하는 좁은 단위',
                 'advantage': '첫 성공과 학습의 차이를 하나의 관측 과제로 분리할 수 있다',
                 'cost': '첫 성공을 다시 과시할 시간을 기본 과제 시도에 사용한다',
                 'missing': '세 과제 중 어느 것을 택할지·지시·시도 동작·관측 결과는 미선택'},
                {'id': 'L-B', 'status': 'CANDIDATE', 'action': '세 기본 과제를 연결한 반복 훈련 범위',
                 'advantage': '첫 기여의 연속 행동과 준비 항목의 관계를 함께 다룰 수 있다',
                 'cost': '학습 항목이 늘어나면 단일 기능과 관측 결과가 흐려질 수 있다',
                 'missing': '연결 드릴·과제 순서·시도 결과·기간은 미선택'},
            ],
            'editorial_recommendation': 'L-A', 'concrete_action_selected': False,
            'current_cost_class': 'CANDIDATE_DIRECT_TIME_OPPORTUNITY_NOT_REALIZED_COST',
            'exit_state': transition, 'next_boundary': 'A01-TEAM-PREPARATION-WB',
            'required_before_event_promotion': ['기본 과제의 실제 행동', '전달 또는 관측 경로',
                                               '성공·실패를 선지급하지 않는 관측 결과', '학교 참여 조건의 필요한 범위'],
            'excluded': ['C1/C2/C3 재실행', '완패 다음날 재방문 재작성', '새 완패나 부상',
                         '반복 성공·숙련 완료', '감독의 천재 인증', '게임 포기 사건'],
            'source_claims': [{'classification': 'AUTHOR_LOCKED_CANON',
                              'claim': '첫 성공은 박스아웃·위치선정·패스 학습을 시작할 증거이지 기술 완성이 아니다',
                              'path': 'canon/STORY_BIBLE.md', 'section': '농구 입문 동기 / 3단계 셋째 항목'},
                             {'classification': 'CANDIDATE', 'claim': cf['A01-CF07']['choice'],
                              'path': SOURCES[1], 'section': 'A01-CF07'}],
        },
        {
            'id': 'A01-TEAM-PREPARATION-WB', 'source_function': 'A01-CF08', 'subact': 'A01-S2',
            'status': 'WORKING_EDITORIAL_BOUNDARY_CONCRETE_EVENT_CANDIDATE',
            'entry_state': transition,
            'source_function_entry_summary': cf['A01-CF08']['entry_state'],
            'entry_summary_is_exact_handoff': False,
            'single_function': '맡은 준비에 다시 참여하는 후보 행동과 동료 부담의 관측 조건을 분리한다',
            'working_boundary_selection': '구체 준비 약속과 수행의 범위까지 다루며 게임 충돌 시험·생활 전체 개선 전에 끝낸다',
            'action_candidates': [
                {'id': 'P-A', 'status': 'CANDIDATE', 'action': '팀 공동 훈련 도구의 준비·정리 중 맡은 일을 다시 수행하는 범위',
                 'advantage': '누가 대신 준비해야 하는지와 수행 뒤 남은 일을 관측할 수 있다',
                 'cost': '칭찬이나 승부가 없는 준비 시간에 참여한다',
                 'missing': '도구·작업·약속 시각·대신 맡을 동료·실제 부담 감소는 미선택'},
                {'id': 'P-B', 'status': 'CANDIDATE', 'action': '기본 훈련 반복에서 동료에게 연결하는 준비 역할을 맡는 범위',
                 'advantage': '학습과 팀의 다음 반복에 필요한 행동을 연결할 수 있다',
                 'cost': '자기 성공을 보여 주는 차례와 준비 역할의 시간 관계를 따로 확인해야 한다',
                 'missing': '훈련 형식·역할·차례·동료·관측 가능한 결과는 미선택'},
            ],
            'editorial_recommendation': 'P-A', 'concrete_action_selected': False,
            'current_cost_class': 'CANDIDATE_DIRECT_TIME_OPPORTUNITY_NOT_REALIZED_COST',
            'exit_state': '팀 준비 약속·수행·동료 부담을 확인할 작업 범위를 정했다. 구체 사건과 생활 개선은 확정하지 않았고 CF09의 게임 보상 시험은 다음 후보로 남는다.',
            'next_boundary': None, 'next_source_function': 'A01-CF09',
            'burden_observation_required': {
                'alternative_burden_holder': None, 'preparation_task': None,
                'observable_before': None, 'observable_after': None,
                'reduced_burden_certified': False,
                'rule': '누군가 대신 떠안는 준비와 수행 뒤 줄어든 일을 관측할 입력 없이 팀 부담 감소를 사실로 쓰지 않는다',
            },
            'required_before_event_promotion': ['맡은 준비 작업·약속의 전달 경로', '본인 수행',
                                               '대신 맡을 동료와 전후 관측', '필요한 참여·권한 조건'],
            'excluded': ['패배 다음날 자존심 복귀 재작성', 'CF09 게임 보상 충돌 선지급',
                         '학교 출결·수면 전체 개선', '미국 프렙 자율 루틴', '동료 전원의 신뢰'],
            'source_claims': [{'classification': 'AUTHOR_LOCKED_CANON_FOUNDATION_EVENT_DETAIL_HOLD',
                              'claim': '팀에 필요한 경험은 반복돼야 학교에 오는 이유가 라이벌 밖으로 확장된다',
                              'path': 'canon/CHARACTER_RESPONSIBILITY_ARC.md', 'section': '세 번의 문턱 / 한국 고교'},
                             {'classification': 'CANDIDATE', 'claim': cf['A01-CF08']['choice'],
                              'path': SOURCES[1], 'section': 'A01-CF08'}],
            'promise_link': {'id': 'P2', 'role': 'PLANT_ACTION_CANDIDATE', 'ledger_position': 'A01-S2',
                             'silence_length_or_on_page_payoff_certified': False},
        },
    ]
    for row in boundaries:
        row.update(exact_date=None, episode_number=None, allocation_slot=None,
                   school_permission_certified=False, individual_scene_pov_verified=False,
                   realized_event_verified=False, actual_result=None, author_locked=False)
    return {
        'schema_version': 1, 'date_local': '2026-10-07',
        'status': 'TWO_WORKING_BOUNDARIES_CONCRETE_ACTIONS_CANDIDATE_REVIEW_PENDING',
        'purpose': 'EDITORIAL_DESIGN_VALIDATION_ONLY_NOT_EPISODE_BLUEPRINT_OR_CONTEXT_PACK',
        'source_main': BASELINE_MAIN,
        'source_hash_convention': 'SHA256_UTF8_NO_BOM_LF_NORMALIZED',
        'source_sha256': {f: digest(ROOT / f) for f in SOURCES},
        'common_skill': {'path': SKILL.as_posix(), 'sha256': digest(SKILL),
                         'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SKILL.parents[2], text=True).strip(),
                         'sections': ['7', '8', '13', '19', '21', '22']},
        'parent_scope': {'act': 'A01', 'subact': 'A01-S2', 'act_question': act['question'],
                         'subact_question': subact['basketball_question'],
                         'primary_device': subact['primary_device'], 'secondary_device': subact['secondary_device']},
        'authority': {'existing_local_core_input': SOURCES[0], 'existing_E1_preserved': SOURCES[2],
                      'concrete_new_training_event_authority': None,
                      'health_season_style_delegation_does_not_lock_new_training_events': True,
                      'working_editorial_scope_selected': True, 'concrete_actions_selected': False},
        'classification': {'canon_fact': '기존 입문·첫 기여·학습 한계·책임 성장의 작품 정본만',
                           'inference': '기본 학습과 팀 준비를 서로 다른 작업 경계로 좁히는 편집 판단',
                           'candidate': 'L-A/L-B/P-A/P-B 구체 행동과 그 비용·관측 결과',
                           'new_author_lock': '없음'},
        'boundaries': boundaries, 'information_boundary': info,
        'hold_fields': {key: None for key in holds},
        'school_constraints': ['제안·참여·소속·등록·대회 자격은 서로 다른 사건',
                               '감독은 출결 불이익을 삭제하지 못함',
                               '체험 조건의 학업 보충과 법정 기초학력 프로그램 수료를 동일시하지 않음',
                               '제안일과 체험일·새 경계 날짜의 관계는 미선택',
                               '기존 학교 원문·개별 허가 미인증을 그대로 보존'],
        'counts': {'working_boundaries_added': 2, 'concrete_action_candidates': 4,
                   'new_local_core_blueprints_verified': 0, 'A01_existing_allocation_slots': 36,
                   'A01_allocation_slots_consumed': 0, 'final_episode_functions_added': 0,
                   'actual_context_packs_added': 0, 'new_author_locks': 0, 'manuscript_count': 0},
        'global_episode_assignment': False, 'actual_episode_pack': False,
        'school_execution_cleared': False, 'full_design_complete': False,
        'author_locked': False, 'manuscript_allowed': False,
        'design_gate': 'CLOSED', 'freeze': 'v0.30 PARTIAL',
        'tools_executed_in_this_packet': {'Antigravity': 'NOT_RUN', 'NotebookLM': 'NOT_RUN', 'Claude': 'NOT_RUN'},
        'review_scope': 'SELF_SOURCE_AND_HANDOFF_CHECK_ONLY_INDEPENDENT_REVIEW_PENDING',
    }


def validate(data):
    rows = data['boundaries']
    if len(rows) != 2 or rows[0]['entry_state'] != readj(SOURCES[0])['exit_state']:
        raise ValueError('exact C3 handoff required')
    if rows[0]['exit_state'] != rows[1]['entry_state'] or rows[0]['next_boundary'] != rows[1]['id']:
        raise ValueError('exact boundary handoff required')
    if any(row['concrete_action_selected'] or row['realized_event_verified'] or row['author_locked'] for row in rows):
        raise ValueError('concrete event promotion forbidden')
    if rows[1]['burden_observation_required']['reduced_burden_certified'] is not False:
        raise ValueError('unobserved teammate burden cannot be certified')
    if any(value is not None for value in data['hold_fields'].values()):
        raise ValueError('unselected event/permission/date fields must remain null')
    if any(row['exact_date'] is not None or row['episode_number'] is not None or row['allocation_slot'] is not None for row in rows):
        raise ValueError('date/episode/allocation not selected')
    for key in ('A01_allocation_slots_consumed', 'final_episode_functions_added',
                'actual_context_packs_added', 'new_author_locks', 'manuscript_count'):
        if data['counts'][key] != 0:
            raise ValueError('count promotion forbidden')
    if data != build():
        raise ValueError('source reconstruction or authority boundary mismatch')
    return True


def render(data):
    a, b = data['boundaries']
    lines = ['# A01 첫 기여 뒤 학습·팀 준비의 작업 경계2개', '',
             '2026-10-07 / [입력 JSON](A01_LEARNING_AND_TEAM_PREPARATION_BOUNDARIES.json) / '
             '[생성·검문기](../tools/build_a01_learning_preparation_boundaries.py).', '',
             '**편집 경계2개를 선택했다. 구체 행동4개는 비교 후보이며 실제 사건·학교 이행·최종 회차·Pack 인증은 아니다.**', '',
             '기존 E1과 첫 체험·첫 기여3 Blueprint는 수정하지 않는다. C3 뒤 A01-CF07→CF08만 구체화하고 '
             '패배 다음날 재방문을 다시 작성하지 않는다. A01 36슬롯 소모0·최종 회차 추가0·실제 Pack0·새 작가 잠금0·원고0이다.', '',
             '## 상위 질문과 권위', '', f"- Act/SubAct 질문: {data['parent_scope']['act_question']}.",
             '- A01-S2 주 장치 PLANT_AND_PAYOFF·보조 장치 없음. P2는 CF08 후보 연결만 유지한다.',
             '- 건강·시즌·S1 위임은 새로운 훈련 사건의 작가 확정 권한으로 읽지 않는다.',
             '- 사실은 기존 작품 정본, 추론은 편집 범위, 후보는 구체 행동·관측 결과로 구분한다.', '',
             '## 두 경계의 실제 작업 범위', '',
             '| 경계 | 포함할 범위 | 끝내는 곳·다음 압력 |', '|---|---|---|',
             f"| CF07 학습 | {a['working_boundary_selection']} | 구체 과제·관측 결과는 후보로 남기고 CF08에 연결 |",
             f"| CF08 준비 | {b['working_boundary_selection']} | 동료 부담의 전후 관측이 필요하며 CF09 게임 시험은 다음 |", '',
             '### C3의 정확한 인계', '', a['entry_state'], '',
             'CF07 기존 entry_state는 요약이므로 위 문자열을 대신하지 않는다. 첫 기여를 다시 실행하지 않고 '
             '학습 과제가 생긴 이유만 입력받는다.', '',
             '### CF07→CF08 작업 인계', '', a['exit_state'], '',
             '이 문자열은 편집 설계 상태다. 실제 학습 성공이나 준비 수행 결과가 발생했다는 서술이 아니다.', '',
             '## 구체 행동의 비교 후보', '',
             '| 후보 | 행동 범위 | 판단·직접 비용 | 미선택 입력 |', '|---|---|---|---|']
    for row in data['boundaries']:
        for candidate in row['action_candidates']:
            lines.append(f"| {candidate['id']} | {candidate['action']} | {candidate['advantage']}. {candidate['cost']} | {candidate['missing']} |")
    lines += ['', '편집 권고는 L-A·P-A이다. 두 권고 모두 구체 행동 선택·사건 잠금은 아니다. '
              '학습 과제 한 개와 팀 준비 부담을 관측할 수 있는 좁은 후보를 먼저 검문할 수 있다는 판단이다.', '',
              '## 남은 입력과 모순 검문', '',
              '- 학습: 어느 기본 과제를 실제로 시도하는지·전달 경로·시도 행동·관측 결과가 남는다. '
              '첫 성공을 반복 성공·기술 완성·라이벌 추월로 바꾸지 않는다.',
              '- 준비: 맡은 작업·약속 전달·수행·대신 맡을 동료·전후 관측이 남는다. '
              '부담 감소를 관측하지 않고 팀 신뢰가 생겼다고 쓰지 않는다.',
              '- CF08은 동료를 준비에 계산할 수 있는 조건이고, 완료된 자존심 복귀와 다른 기능이다. '
              'CF09 게임 보상 충돌·수면·학교생활 개선을 앞당기지 않는다.',
              '- 감독은 출결 불이익을 삭제하지 않는다. 체험 제안·참여·소속·등록·대회 자격, '
              '학업 보충과 법정 프로그램 수료를 구분한다. 날짜·학교·허가·조건 이행은 null/HOLD다.', '',
              '## S1 정보 접근', '',
              '전역 S1 방향은 보존한다. 실제 수행·직접 관측·전달된 과제만 장래 접근 후보다. '
              '감독·라이벌·동료의 내면, 미전달 학교 결정, 미래 성공·전원 신뢰는 금지한다. '
              '구체 관측 사건·장면·날짜·개별 POV 인증은 아직 없으므로 story_known_claim_indexes는 빈 배열이다.', '',
              '## 출처·재현·계수', '',
              f"기준 main `{data['source_main']}`. 공통 writing skill `{data['common_skill']['revision']}` "
              '§§7·8·13·19·21·22를 적용했다. JSON은13개 원본과 공통 스킬의 SHA256을 '
              'UTF-8 BOM 제거·CRLF/CR→LF 정규화로 연결한다. 기존 입력의 파일 존재를 실행 권위로 읽지 않는다.', '',
              '자체 검문은 C3/두 경계의 정확 인계·출처 재구성·학교/날짜/사건/계수 승격 금지에 한정한다. '
              '독립 검문은 대기다. Antigravity·NotebookLM·Claude는 이번 산출물에서 NOT_RUN이며, '
              '과거 실행을 새 수집 성공으로 계수하지 않는다.', '',
              '`python -B -X utf8 tools/build_a01_learning_preparation_boundaries.py --check --self-test`', '',
              'Freeze v0.30 PARTIAL·설계/원고 CLOSED. 최종 회차 배치와 역사 원장이 잠기기 전 실제 Context Pack을 만들지 않는다.']
    return '\n'.join(lines) + '\n'


def self_test():
    base = build()
    validate(base)
    for label in ('handoff', 'action', 'burden', 'permission', 'episode', 'count', 'source', 'access'):
        data = deepcopy(base)
        if label == 'handoff': data['boundaries'][0]['entry_state'] += '이미 숙련했다'
        elif label == 'action': data['boundaries'][0]['concrete_action_selected'] = True
        elif label == 'burden': data['boundaries'][1]['burden_observation_required']['reduced_burden_certified'] = True
        elif label == 'permission': data['hold_fields']['school_permission'] = True
        elif label == 'episode': data['boundaries'][1]['episode_number'] = 2
        elif label == 'count': data['counts']['A01_allocation_slots_consumed'] = 2
        elif label == 'source': data['source_sha256'][SOURCES[0]] = '0' * 64
        elif label == 'access': data['information_boundary']['story_known_claim_indexes'] = [0]
        try: validate(data)
        except ValueError: continue
        raise AssertionError(f'false promotion accepted: {label}')
    return 8


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    validate(data)
    body = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    markdown = render(data)
    if args.check:
        if normalized(OUT) != body or normalized(MD) != markdown:
            raise ValueError('saved boundary artifacts stale or modified')
    else:
        OUT.write_text(body, encoding='utf-8', newline='\n')
        MD.write_text(markdown, encoding='utf-8', newline='\n')
    tests = self_test() if args.self_test else 0
    print(json.dumps({'status': 'SOURCE_AND_HANDOFF_REPRODUCTION_PASS_NOT_EVENT_PROMOTION',
                      'working_boundaries': 2, 'concrete_action_candidates': 4,
                      'negative_tests': tests, 'final_episodes_added': 0,
                      'actual_context_packs': 0, 'manuscript_count': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
