"""Select the bounded film-review response to A03's first practice failure."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a03_college_entry_working_model as entry_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A03_CF01_ROLE_RESPONSE_WORKING_MODEL_2026_10_07.json')
MARKDOWN = OUTPUT.with_suffix('.md')
ENTRY = str(entry_builder.OUTPUT).replace('\\', '/')
CANDIDATES = 'design/A03_CONDITIONAL_EPISODE_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
SCOPE = 'control/COLLEGE_ARC_SCOPE_GATE.md'
SOURCES = ('tools/build_a03_cf01_role_response_working_model.py', ENTRY,
           CANDIDATES, CP2, SCOPE)


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def read_bytes(root, path):
    return (root / path).read_bytes()


def norm_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def build(root=ROOT):
    entry = load(root, ENTRY)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    assert entry == entry_builder.load(root, entry_builder.OUTPUT), 'entry differs from validated producer input'
    assert not entry_builder.validate(entry, root=root), 'A03 entry source-currentness failed'
    assert entry['status'] == 'SELECTED_ROUTINE_FICTIONAL_ENTRY_AND_FIRST_PRACTICE_MODEL_INDEPENDENTLY_REVIEWED'
    assert entry['independent_review_completed'] is True
    assert entry['new_sequence'][-1]['id'] == 'A03-R1'
    assert '동료가 빈 공간을 메워야 했다' in entry['first_local_trial_exit']
    assert entry['limits']['selected_I3_full_qualifier_or_compliance_revoked_here'] is False
    assert entry['limits']['2017_18_official_college_game_or_box_score_completed'] is False
    assert entry['limits']['A03_S1_whole_exit_completed'] is False
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    s1 = next(row for row in cp2['subacts'] if row['id'] == 'A03-S1')
    assert s1['choice'] == '우승팀 소속이라는 이름 대신 자신이 수행할 수 있는 좁은 벤치 역할을 맡는다'
    assert s1['cost'] == '자기 쇼케이스'
    assert s1['exit_state'] == '제한된 역할을 수락'
    assert candidates['status'] == 'THREE_CONDITIONAL_FUNCTIONS_NOT_FINAL_G13'
    assert candidates['final_episode_functions'] == 0
    f01 = candidates['functions'][0]
    assert (f01['id'], f01['subact'], f01['function']) == ('A03-F01', 'A03-S1', '초기 실패')
    assert {key: f01[key] for key in ('entry', 'pressure', 'choice', 'cost', 'changed_state', 'next', 'causal_link')} == {
        'entry': '프렙의 신체 우위를 대학 출전 기회로 바로 환산하려는 기대',
        'pressure': '자신의 대인수비와 팀 도움수비 연결이 충돌하는 제한 출전 과제',
        'choice': '영상으로 자신이 동료에게 넘긴 부담을 확인하고 다음 훈련의 제한 역할을 수락',
        'cost': '출전 보상 없이 영상·역할 훈련에 시간을 쓰며 학업 의무도 유지',
        'changed_state': '불만은 남지만 다음 기회 전에 수행할 과제를 구분',
        'next': 'A03-F02',
        'causal_link': '제한 역할 수락을 반복 행동으로 확인해야 신뢰의 근거가 생김',
    }
    assert f01['status'] == 'CONDITIONAL_EPISODE_FUNCTION_CANDIDATE'
    assert '대표 경기 기능 | 3개' in read_bytes(root, SCOPE).decode('utf-8-sig')

    response = [
        {'id': 'V1', 'source_event': 'A03-R1 first supervised practice failure',
         'authorized_access': 'Protagonist sees only the permitted team-practice clip showing his late help-position move and the teammate covering that space.',
         'observable_action': 'He identifies the assigned help-space cue he missed in his own movement.',
         'not_accessed': 'Private coach grading, teammates’ inner thoughts, actual 2017 Villanova film or a real-game possession.'},
        {'id': 'V2', 'source_event': 'V1 observed own late cue',
         'choice': 'He accepts a bounded next supervised reserve-forward task: check the agreed help-space cue and preserve the connection with the teammate before chasing his own showcase.',
         'direct_present_cost': 'He uses the permitted practice debrief and task-assignment time on his visible mistake and next limited task instead of seeking a personal showcase; existing academic duties continue.',
         'observed_result': 'The task is accepted, but the next repetition, teammate trust and game minutes have not yet been observed.',
         'new_punishment_injury_or_school_cost_event': False},
    ]
    exit_state = (
        '주인공은 허용된 연습 영상에서 자신이 도움 위치로 늦게 움직여 동료가 빈 공간을 메운 모습을 확인했다. '
        '그는 출전 분을 요구하는 대신 다음 허용 훈련의 좁은 도움 위치·동료 연결 과제를 맡겠다고 선택하고, '
        '이번 연습의 영상 검토·다음 과제 확인 시간을 자기 과시 대신 쓴다. 다음 역할 훈련의 수행·반복 성공·동료 신뢰·공식 출전은 아직 관측되지 않았다.'
    )
    return {
        'schema': 'A03_CF01_ROLE_RESPONSE_WORKING_MODEL_V1',
        'status': 'SELECTED_ROUTINE_ROLE_RESPONSE_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'review_scope': 'ONE_FILM_OBSERVATION_AND_ONE_LIMITED_ROLE_CHOICE_ONLY',
        'scope': 'A03_S1_FIRST_FAILURE_FILM_RESPONSE_AND_BOUNDED_TASK_CHOICE_ONLY',
        'evidence_classes': {'prior_registration_and_failure': 'VALIDATED_FICTIONAL_DESIGN',
                             'V1_V2': 'NEW_ROUTINE_FICTIONAL_DESIGN_SELECTION',
                             'real_college_film_or_coach_grade': 'NOT_CERTIFIED'},
        'prior_exact_entry_trial_exit': entry['first_local_trial_exit'],
        'prior_selected_I3_full_qualifier_retained': True,
        'response': response,
        'selected_design_exit_state': exit_state,
        'CP2_S1_bounded_exit_candidate_supported': True,
        'CP2_S1_whole_exit_or_final_episode_function_certified': False,
        'next_candidate': {'id': 'A03-F02', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'causal_need': 'Repeat the accepted role in an observed permitted opportunity before teammates can rely on it.',
                           'repeat_success_or_minutes_increase_prepayment': False},
        'limits': {'formal_college_game_or_box_score_claimed': False,
                   'real_2017_college_practice_or_private_film_certified': False,
                   'existing_I3_certification_revoked': False,
                   'new_roster_counter_or_starter_guarantee': False,
                   'new_representative_games': 0,
                   'A03_three_representative_function_cap_changed': False,
                   'A03_S2_trust_or_repeated_success_completed': False,
                   'academic_work_completed_by_film': False,
                   'new_academic_life_cost_event_added': False,
                   'whole_college_season_completed': False},
        'author_locked': False, 'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: norm_sha(read_bytes(root, p)) for p in SOURCES},
    }


def render(data):
    rows = ['# A03 첫 역할 실패 뒤 영상·제한 과제 선택', '',
            '**범위:** 원고가 아닌 가상 팀의 국소 역할 설계. 첫 연습 실패를 자신의 영상 접근과 제한 과제 선택으로 잇는다.', '',
            f"- 상태: `{data['status']}`",
            f"- 정확 진입: {data['prior_exact_entry_trial_exit']}", '',
            '| 단계 | 보이는 행동과 선택 | 정보 경계 |', '| --- | --- | --- |']
    for step in data['response']:
        rows.append(f"| {step['id']} | {step.get('observable_action', step.get('choice'))} | {step.get('not_accessed', step.get('observed_result'))} |")
    rows += ['', f"- 국소 출구: {data['selected_design_exit_state']}",
             '- 이번 허용 연습의 영상 검토·다음 과제 확인 시간을 자기 과시 대신 사용하는 비용이다. 다음 역할 훈련은 아직 하지 않았고 학업 의무는 남으며 새 학업·생활 처분 사건도 만들지 않는다.',
             '- 이미 선택된 여름 full qualifier/compliance를 취소하지 않는다. 실제 사적 NCAA 기록·실존 팀 영상·공식 경기·박스스코어는 인증하지 않는다.',
             '- A03-F02 반복 수행·동료 신뢰·출전 확대는 다음 후보이며, 현재 A03 최종 회차 기능이나 소막 전체 출구로 계수하지 않는다.',
             '- 대표 기능3·새 대표 경기0·전체 G13/G14 미완료·원고0·게이트 `CLOSED`.', '']
    return '\n'.join(rows)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['role response differs from source-bound selected design']


def self_test(data):
    changes = [
        ('game certification', lambda x: x['limits'].update(formal_college_game_or_box_score_claimed=True)),
        ('I3 revoked', lambda x: x['limits'].update(existing_I3_certification_revoked=True)),
        ('teammate trust prepaid', lambda x: x['limits'].update(A03_S2_trust_or_repeated_success_completed=True)),
        ('real clip certified', lambda x: x['limits'].update(real_2017_college_practice_or_private_film_certified=True)),
        ('whole S1 prepaid', lambda x: x.update(CP2_S1_whole_exit_or_final_episode_function_certified=True)),
    ]
    for name, mut in changes:
        changed = copy.deepcopy(data)
        mut(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mut in [
        ('R1 failure reversed', ENTRY, lambda x: x.update(first_local_trial_exit='첫 대학 공식 경기에서 완벽히 수비해 선발로 뛰었다')),
        ('F01 choice made showcase', CANDIDATES, lambda x: x['functions'][0].update(choice='영상 없이 출전 분을 요구하고 즉시 선발이 된다')),
        ('F01 same-key cost made injury', CANDIDATES, lambda x: x['functions'][0].update(cost='영상·역할 훈련 대신 부상으로 석 달 결장한다')),
        ('S1 exit made championship', CP2, lambda x: next(y for y in x['subacts'] if y['id']=='A03-S1').update(exit_state='우승 MVP가 됨')),
    ]:
        def changed_load(root, requested, path=path, mut=mut):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mut(source)
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
    return len(changes) + 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors, 'negative_controls': tested,
                      'status': data['status']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
