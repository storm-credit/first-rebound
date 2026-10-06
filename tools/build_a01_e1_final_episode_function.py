"""Build and verify A01's first final *function*, without producing prose or a Pack.

The completion is local to one function. Source hashes and exact reconstruction
protect the recorded editorial decision; they cannot certify unwritten scenes.
"""

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

import check_a01_opening_blueprint as blueprint_check


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_E1_FINAL_EPISODE_FUNCTION.json')
MARKDOWN = Path('design/A01_E1_FINAL_EPISODE_FUNCTION.md')
SOURCES = (
    'tools/build_a01_e1_final_episode_function.py',
    'canon/STORY_BIBLE.md',
    'design/A01_OPENING_BLUEPRINT.json',
    'design/A01_FIRST_TRIAL_BLUEPRINT.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'design/A01_OPENING_EPISODE_BOUNDARY.md',
    'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
    'research/A01_KOREA_2015_SCHOOL_TRIAL_BOUNDARY.md',
)
BOUNDARY_TRACE_PATHS = (
    'design/A01_OPENING_BLUEPRINT.json',
    'design/A01_FIRST_TRIAL_BLUEPRINT.json',
    'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/STORY_BIBLE.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
)
OPENING_SEMANTIC_SHA256 = '2748c10af38120d10da36b090db4056a9b32a8e945be7ab21a36fb2b3d37d4ed'
TRIAL_SEMANTIC_SHA256 = 'be9dd623fb75b4489a2658602e95e8f91bccb8520cde7451048c2d11e1a05b6b'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def semantic_sha(data):
    projected = {k: v for k, v in data.items() if k != 'source_rev_sha256'}
    return hashlib.sha256(json.dumps(projected, sort_keys=True,
                                     ensure_ascii=False, separators=(',', ':'))
                           .encode('utf-8')).hexdigest()


def source_json(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    opening = source_json(root, 'design/A01_OPENING_BLUEPRINT.json')
    trial = source_json(root, 'design/A01_FIRST_TRIAL_BLUEPRINT.json')
    packet = source_json(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    selected = source_json(root, 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json')
    boundary = (root / 'design/A01_OPENING_EPISODE_BOUNDARY.md').read_text(encoding='utf-8-sig')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    a01 = next(a for a in packet['acts'] if a['id'] == 'A01')
    a01_s1 = next(s for s in packet['subacts'] if s['id'] == 'A01-S1')
    assert semantic_sha(opening) == OPENING_SEMANTIC_SHA256, 'opening narrative projection changed'
    assert semantic_sha(trial) == TRIAL_SEMANTIC_SHA256, 'trial handoff projection changed'
    assert opening['status'] == trial['status'] == 'ACTUAL_VERIFIED'
    assert [b['id'] for b in opening['beats']] == ['B1', 'B2', 'B3', 'B4']
    assert sum(len(b['claims']) for b in opening['beats']) == 5
    assert opening['exit_state'] == trial['entry_state']
    assert a01['planned_units'] == 36 and a01['allocation_start'] == 1
    assert a01['allocation_end'] == 36 and packet['status'] != 'FINAL_EPISODE_OUTLINE'
    assert a01_s1['parent_act'] == 'A01' and a01_s1['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert selected['selected']['style']['route'] == 'S1'
    assert opening['information_boundary']['pov_style_direction'] == 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY'
    assert 'E1, 감독의 방과 후 조건부 체험 제안에서 끝낸다' in boundary
    for path in BOUNDARY_TRACE_PATHS:
        current_digest = sha((root / path).read_bytes())
        line = rf'^\| \[{re.escape(path)}\]\([^)]*\) \| `{current_digest}` \|$'
        assert re.search(line, boundary, re.MULTILINE), f'stale E1 boundary trace: {path}'
    assert '농구 입문 동기' in story and '관중석' in story
    assert all(b['claims'][0]['evidence_class'].startswith('AUTHOR_LOCKED_CANON_')
               for b in opening['beats'])

    beats = []
    for beat in opening['beats']:
        beats.append({
            'id': beat['id'],
            'function_event': beat['event'],
            'relative_time': beat['relative_time'],
            'claims': [{k: c[k] for k in ('claim', 'evidence_class', 'source_path',
                                         'source_anchor', 'protagonist_access',
                                         'other_person_access', 'unknown')}
                       for c in beat['claims']],
        })
    result = {
        'schema': 'A01_FINAL_EPISODE_FUNCTION_V1',
        'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
        'authority_scope': 'ONE_G13_FUNCTION_ONLY_NOT_FULL_G13_OR_AUTHOR_LOCK',
        'episode_function_id': 'A01-EF-001',
        'act': 'A01',
        'subact': 'A01-S1',
        'editorial_boundary': 'E1',
        'final_function_order': 1,
        'planned_allocation_slot': 1,
        'published_episode_number': None,
        'published_episode_title': None,
        'manuscript_word_count': None,
        'slot_accounting': {
            'a01_planned_slots': 36,
            'assigned_final_function_slots': 1,
            'remaining_planned_slots': 35,
            'allocation_is_final_series_episode_count': False,
        },
        'final_episode_functions_completed': 1,
        'single_function': opening['single_function'],
        'entry_state': opening['entry_state'],
        'exit_state': opening['exit_state'],
        'direct_present_cost': opening['direct_present_cost'],
        'reader_question_at_end': opening['next_question'],
        'internal_order': ['B1', 'B2', 'B3', 'B4'],
        'beats': beats,
        'next_unit': {
            'beat_id': 'T1',
            'function_event': trial['beats'][0]['event'],
            'entry_state': trial['entry_state'],
            'is_in_this_function': False,
            'handoff_to_blueprint': 'design/A01_FIRST_TRIAL_BLUEPRINT.json',
        },
        'information_access': copy.deepcopy(opening['information_boundary']),
        'school_authority': {
            'coach_conditional_offer': 'AUTHOR_LOCKED_CANON_EVENT',
            'offer_is_immediate_team_selection': False,
            'acceptance_completed': False,
            'training_attendance_completed': False,
            'school_permission_certified': False,
            'attendance_or_supplement_execution_certified': False,
            'attendance_disposition_certified': False,
        },
        'unassigned_details': {
            'school_name': None,
            'grade': None,
            'exact_date': None,
            'ball_path': None,
            'coach_private_thought': None,
            'individual_scene_pov': None,
            'exact_dialogue': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
        'source_semantic_projection_sha256': {
            'opening': OPENING_SEMANTIC_SHA256,
            'first_trial': TRIAL_SEMANTIC_SHA256,
        },
        'verification_limits': [
            'Function order and one planned slot are editorial placement, not a published chapter number or final series length.',
            'ACTUAL_VERIFIED source Blueprints establish local locked events; individual scene execution and administrative permission remain unverified.',
            'Exact school identity, date, grade, dialogue, movement and coach private thought are not assigned.',
            'Source/hash/structure checks cannot prove narrative quality or a finished whole G13.',
        ],
        'whole_g13_complete': False,
        'whole_g14_complete': False,
        'actual_context_packs': 0,
        'g15_complete': False,
        'g16_complete': False,
        'g17_complete': False,
        'author_locked': False,
        'new_author_decisions': 0,
        'manuscript_count': 0,
        'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }
    return result


def render(data):
    rows = ['| 순서 | 기존 정본 Beat | 기능상 역할 |', '| --- | --- | --- |']
    for i, beat in enumerate(data['beats'], 1):
        rows.append(f"| {i} | {beat['id']} | {beat['function_event']} |")
    return '\n'.join([
        '# A01 첫 최종 회차 기능 — E1',
        '',
        '이 문서는 **회차 기능 설계**다. 원고·대사·장면 문장이 아니다. 기존 잠긴 사건 B1–B4를 첫 기능의 순서와 종료점에 배치했다.',
        '',
        f"- 기능 ID: `{data['episode_function_id']}` / A01-S1 / 기능 순서 1 / A01 계획 배분 슬롯 1",
        '- A01 계획 슬롯 36개 중 1개 기능 배정, 계획상 잔여 35개. 36은 확정 출판 회차 수가 아니다.',
        '- 국소 최종 회차 기능 완료 **1**. G13 전체·G14·실제 Pack·G15–G17·원고 허가는 완료되지 않았다.',
        '',
        '## 기능과 경계',
        '',
        f"- 시작: {data['entry_state']}",
        f"- 단일 기능: {data['single_function']}",
        f"- 현재 직접 비용: {data['direct_present_cost']}",
        f"- 끝: {data['exit_state']}",
        f"- 남기는 독자 질문: {data['reader_question_at_end']}",
        '',
        *rows,
        '',
        '다음 T1의 첫 체험 진입은 이 기능 밖이다. B4 끝 상태와 T1 시작 상태는 문자 단위로 일치한다.',
        '',
        '## 정보 접근과 학교 권한',
        '',
        '- S1 주인공 밀착 3인칭의 기능 단계 정보 경계를 적용한다. 주인공은 자신의 지각·회피·공 반응과 실제 전달된 제안까지만 안다. 감독의 비공개 평가·속마음은 접근하지 않는다. 개별 장면 POV는 아직 인증하지 않았다.',
        '- 감독은 방과 후 조건부 체험을 제안한다. 수락, 첫 훈련 참여, 수업·보충·시간 준수 이행, 출결 처분, 선수 선발과 학교 허가는 완료로 표시하지 않는다.',
        '- 학교명·학년·정확한 날짜·공 이동·구체 대사·감독 내면은 새로 배정하지 않았다.',
        '',
        '## 검증 범위',
        '',
        '- 사건과 주장 4 Beat/5개는 [오프닝 Blueprint](A01_OPENING_BLUEPRINT.json)의 잠긴 정본 범위를 그대로 사용한다. [E1 경계](A01_OPENING_EPISODE_BOUNDARY.md)의 편집 선택을 첫 기능에 반영한다.',
        '- JSON의 `source_rev_sha256`와 별도 검사기는 원본 현재성, 한 기능의 배치·경계·권한 제한을 검증한다. 문장 품질이나 전체 설계 완료를 인증하지 않는다.',
        '- `published_episode_number/title`, 분량, 개별 장면은 미정이다. 정본 사건 추가 0, 작가 잠금 0, 실제 Context Pack 0, 원고 0.',
        '- 설계/원고 게이트 `CLOSED`, `manuscript_allowed:false`.',
        '',
    ])


def validate(data, root=ROOT, currentness=True):
    errors = []
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError) as exc:
        return [f'source construction: {exc}']
    if data != expected:
        errors.append('record differs from current source-bound function')
    if currentness:
        for unit in ('opening', 'first-trial', 'first-contribution'):
            _, unit_errors = blueprint_check.check(root=root, unit=unit)
            errors.extend(f'{unit}: {e}' for e in unit_errors)
    return errors


def self_test(data):
    mutations = [
        ('different beat', lambda d: d['beats'][2].update(function_event='새 농구 묘기')),
        ('wrong slot', lambda d: d.update(planned_allocation_slot=2)),
        ('false completion', lambda d: d.update(whole_g13_complete=True)),
        ('manuscript gate', lambda d: d.update(manuscript_allowed=True)),
        ('administrative promotion', lambda d: d['school_authority'].update(school_permission_certified=True)),
        ('private thoughts', lambda d: d['information_access']['not_available_to_protagonist_without_new_access'].clear()),
        ('false SHA', lambda d: d['source_rev_sha256'].update({'canon/STORY_BIBLE.md': '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate, currentness=False), name
    return len(mutations)


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
        try:
            saved = source_json(ROOT, OUTPUT)
            errors.extend(validate(saved))
            if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
                errors.append('Markdown not synchronized')
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f'missing or invalid artifact: {exc}')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'function': data['episode_function_id'], 'local_complete': 1,
                      'planned_slots_remaining': 35, 'negative_controls': tested,
                      'current': not errors, 'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
