"""Prepare finite A09-A14 function scope without deciding future season outcomes."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a09_a14_bounded_function_preparation.py'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
FREEZE = 'canon/PROJECT_FREEZE.md'
STORY = 'canon/STORY_BIBLE.md'
CONDITIONAL = {
    'A09': 'design/A09_2023_24_CONDITIONAL_FUNCTIONS.json',
    'A10': 'design/A10_2024_25_CONDITIONAL_FUNCTIONS.json',
    'A11': 'design/A11_2025_26_CONDITIONAL_FUNCTIONS.json',
    'A12': 'design/A12_2026_27_CONDITIONAL_FUNCTIONS.json',
    'A13': 'design/A13_2027_28_CONDITIONAL_FUNCTIONS.json',
    'A14': 'design/A14_2028_35_CONDITIONAL_FUNCTIONS.json',
}
OUTPUT = Path('design/A09_A14_BOUNDED_FUNCTION_PREPARATION_2026_10_07.json')
SOURCES = (SELF, CP2, FREEZE, STORY, *CONDITIONAL.values())
SEMANTIC_SHA = '3587c896ae7a0cfd235c590b424f4cf1349a6288613ebbc48b6d7b016991825a'
LOCAL_SCOPE = {
    'A09-S1': '허가·보험·캠프의 서로 다른 권한자에게 자기 준비와 일정 질문을 전달하는 루틴은 설계 가능. 참가 승인 자체는 별도.',
    'A09-S2': '허용된 팀 훈련의 역할 공유·실패 뒤 행동만 국소 관측 가능. 실제 대표팀 명단·대회 결과는 별도.',
    'A09-S3': 'NBA 복귀 준비와 본인 부하 조정 루틴만 선설계 가능. 실제 복귀 경기/분은 별도.',
    'A10-S1': '짧은 자기 공격 창과 막힌 뒤 다음 선택을 허용 훈련에서 시험 가능. 실전 첫 옵션 권한은 별도.',
    'A10-S2': 'LaVine과 기회비용을 드러내는 제한 훈련 대조 가능. 클로징 재배정은 별도.',
    'A10-S3': '우승창에 필요한 미완 과제의 자기 관측은 가능. 진출·우승 결과는 별도.',
    'A11-S1': '무볼 재배치와 수비 출력 유지의 제한 과제는 관측 가능. MVP·시즌 통계는 별도.',
    'A11-S2': '두 팀의 역할·비용 구조 비교는 공개/허용 자료 한정 가능. 상대팀 속마음·결승 결과는 별도.',
    'A11-S3': '실패 원인 후보 정리는 가능하나 특정 파이널 패배의 시점·상대·시리즈는 미선택.',
    'A12-S1': '유지할 사람과 기능의 비용 비교안은 가능. 개별 실거래·동의는 별도.',
    'A12-S2': '속도와 책임을 나누는 훈련 과제는 관측 가능. 실제 라인업·승패는 별도.',
    'A12-S3': '다음 대결에 필요한 부족한 기능 정리는 가능. 재대결 진출은 선인증하지 않음.',
    'A13-S1': '상대의 정답을 알아도 막기 어려운 조건을 제한 과제로 재현 가능. 파이널 특정 경기 아님.',
    'A13-S2': '자기 슛과 더 나은 동료 위치의 선택을 연습 가능. 결말 실제 수신자·상대·시즌은 미선택.',
    'A13-S3': '파이널 7차전 수비→리바운드→전진→더 나은 동료에게 패스→동료 결승 득점·팀 승리는 잠긴 기능. 정확 좌표는 미선택.',
    'A14-S1': '성공 뒤 공격 시작의 출력 배분과 달라진 동료 조합의 위치·첫 연결을 제한 과제로 시험 가능. 추가 우승·미래 건강·시즌기록은 별도.',
    'A14-S2': '출력 감소를 수용한 짧은 역할·판단의 국소 과제는 설계 가능. 계약액·건강은 별도.',
    'A14-S3': 'Chicago 원클럽에서 후배에게 준비 습관을 남기고 은퇴하는 기능은 고정 방향. 정확 은퇴 연차·마지막 계약은 미선택.',
}


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def semantic_digest(cp2, packets):
    ids = tuple(CONDITIONAL)
    core = {
        'acts': [[x[k] for k in ('id', 'choice', 'cost', 'exit_state')]
                 for x in cp2['acts'] if x['id'] in ids],
        'subs': [[x[k] for k in ('id', 'parent_act', 'entry_state', 'choice', 'cost', 'exit_state')]
                 for x in cp2['subacts'] if x['parent_act'] in ids],
        'functions': [[x[k] for k in ('id', 'subact', 'cause', 'choice', 'direct_cost', 'changed_state')]
                      for p in packets.values() for x in p['functions']],
    }
    return hashlib.sha256(json.dumps(core, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def build(root=ROOT):
    cp2 = load(root, CP2)
    packets = {key: load(root, path) for key, path in CONDITIONAL.items()}
    assert semantic_digest(cp2, packets) == SEMANTIC_SHA, 'CP2 or 27 candidates changed meaning'
    freeze = (root / FREEZE).read_text(encoding='utf-8-sig')
    story = (root / STORY).read_text(encoding='utf-8-sig')
    assert 'NBA 파이널 7차전 마지막 국면에서 주인공은 수비에 성공하고 결정적 리바운드를 잡는다.' in freeze
    assert '동료의 결승 득점으로 팀이 승리한다.' in freeze
    assert 'Chicago Bulls 원클럽 프랜차이즈 경로' in freeze
    assert 'Chicago 원클럽 프랜차이즈' in story
    assert sum(len(p['functions']) for p in packets.values()) == 27
    acts = [x for x in cp2['acts'] if x['id'] in CONDITIONAL]
    subacts = [x for x in cp2['subacts'] if x['parent_act'] in CONDITIONAL]
    assert len(acts) == 6 and len(subacts) == 18
    assert set(LOCAL_SCOPE) == {x['id'] for x in subacts}
    groups = []
    for sub in subacts:
        aid = sub['parent_act']
        candidates = [x for x in packets[aid]['functions'] if x['subact'] == sub['id']]
        assert candidates
        assert all(not x['selected_event'] and not x['author_locked'] for x in candidates)
        groups.append({
            'subact': sub['id'], 'act': aid, 'candidate_ids': [x['id'] for x in candidates],
            'cp2_choice': sub['choice'], 'cp2_cost': sub['cost'], 'cp2_exit': sub['exit_state'],
            'bounded_next_observation_scope': LOCAL_SCOPE[sub['id']],
            'local_final_function_selected': False, 'whole_subact_exit_certified': False,
        })
    return {
        'schema': 'A09_A14_BOUNDED_FUNCTION_PREPARATION_V1',
        'status': 'INDEPENDENTLY_REVIEWED_SIX_ACT_EIGHTEEN_SUBACT_SCOPE_NOT_SELECTED',
        'independent_review_completed': True,
        'acts': [{'id': x['id'], 'window': x['window'], 'planned_units': x['planned_units'],
                  'source_choice': x['choice'], 'source_cost': x['cost'], 'source_exit': x['exit_state']}
                 for x in acts],
        'groups': groups, 'source_conditional_candidate_count': 27,
        'locked_function_boundaries': {
            'Finals_Game7_defense_rebound_forward_pass_teammate_winning_score_team_win': True,
            'Chicago_one_club_retirement_function': True,
            'exact_season_opponent_score_receiver_or_retirement_year_locked': False,
        },
        'important_unselected_outcomes': ['H2 정확 연도·상대·패배', 'AW2 추가 수상·우승',
                                          'RC1 결말 수신자', 'NM1 메달·복무',
                                          '2035 정확 은퇴 좌표·마지막 계약'],
        'seventeen_season_all_games_required_for_this_preparation': False,
        'new_final_functions_registered': 0, 'new_author_locks': 0,
        'whole_A09_A14_complete': False, 'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED', 'source_semantic_sha256': SEMANTIC_SHA,
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A09–A14 대표 기능 범위 준비', '',
             '원 CP2 6막·18소막과 조건부 인과 27개를 빠짐없이 연결했다. 이 표 자체는 최종 기능이나 전체 시즌 결과가 아니다.', '',
             '|소막|기존 후보|다음 좁은 관측 범위|', '|---|---|---|']
    for row in data['groups']:
        lines.append('|{}|{}|{}|'.format(row['subact'], ', '.join(row['candidate_ids']),
                                         row['bounded_next_observation_scope']))
    lines += ['', '파이널 7차전 수비→리바운드→전진→더 나은 동료에게 패스→동료 결승 득점·팀 승리와 '
              'Chicago 원클럽 은퇴는 이미 잠긴 기능이다. 정확 시즌·상대·수신자·2035 은퇴 좌표는 선택하지 않는다.',
              '', '17시즌 전경기 계산을 이 범위표의 신규 게이트로 만들지 않는다. 실제 기능·Context Pack·원고는 0개 늘었고 설계·원고 게이트는 `CLOSED`다.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['future function preparation differs from source-bound build']
    except (AssertionError, KeyError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / OUTPUT.with_suffix('.md')).write_text(render(data), encoding='utf-8')
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors = validate(saved)
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8') != render(saved):
            errors.append('Markdown differs')
        print(json.dumps({'current': not errors, 'errors': errors,
                          'acts': len(saved['acts']), 'subacts': len(saved['groups'])}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
