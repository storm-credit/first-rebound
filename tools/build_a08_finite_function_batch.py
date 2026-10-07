"""Build three bounded A08 function records without choosing the 2022 contract outcome."""

import argparse
import hashlib
import json
from pathlib import Path

import build_a07_finite_function_batch as previous_builder
import build_a07_a08_finite_function_preparation as preparation_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a08_finite_function_batch.py'
PREVIOUS = str(previous_builder.OUTPUT).replace('\\', '/')
PREPARATION = str(preparation_builder.OUTPUT).replace('\\', '/')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
CONDITIONAL = 'design/A08_2022_23_CONDITIONAL_FUNCTIONS.json'
OUTPUT = Path('design/A08_FINITE_FUNCTION_BATCH_2026_10_07.json')
SOURCES = (SELF, PREVIOUS, PREPARATION, CP2, CONDITIONAL)
SEMANTIC_SHA = 'fe72556676307039ab523e9148c20bd45944bc3b3af8cb6e4d9afe7f2367efc6'


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def sha(raw):
    normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def semantic_digest(cp2, candidate):
    core = {
        'act': [[x[k] for k in ('id', 'choice', 'cost', 'exit_state')]
                for x in cp2['acts'] if x['id'] == 'A08'],
        'subs': [[x[k] for k in ('id', 'entry_state', 'choice', 'cost', 'exit_state')]
                 for x in cp2['subacts'] if x['parent_act'] == 'A08'],
        'candidate': [[x[k] for k in ('id', 'subact', 'cause', 'entry_state', 'choice',
                                      'direct_cost', 'changed_state')]
                      for x in candidate['functions']],
    }
    raw = json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    preparation = load(root, PREPARATION)
    cp2 = load(root, CP2)
    candidate = load(root, CONDITIONAL)
    assert previous == previous_builder.load(root, previous_builder.OUTPUT)
    assert not previous_builder.validate(previous, root=root), 'A07 source-current required'
    assert previous['independent_review_completed'], 'A07 review required for A08 generation'
    assert preparation == preparation_builder.load(root, preparation_builder.OUTPUT)
    assert not preparation_builder.validate(preparation, root=root)
    assert preparation['independent_review_completed']
    assert [row['subact'] for row in preparation['representative_groups'][3:]] == ['A08-S1', 'A08-S2', 'A08-S3']
    assert semantic_digest(cp2, candidate) == SEMANTIC_SHA, 'A08 CP2/candidate meaning changed'
    cf = candidate['functions']
    assert [x['id'] for x in cf] == [f'A08-CF{i:02d}' for i in range(1, 6)]
    prior_exit = previous['functions'][-1]['exit_state']
    assert prior_exit == cf[0]['entry_state']
    functions = [
        {
            'id': 'A08-EF-001', 'global_function_order': 40, 'planned_allocation_slot': 383,
            'primary_subact': 'A08-S1', 'source_conditional_functions': ['A08-CF01'],
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'entry_state': prior_exit,
            'single_function': '자기 역할 요구와 필요한 동료 기능의 같은 예산 비용을 한 자료로 제시한다',
            'unit_choice': cf[0]['choice'], 'direct_present_cost': cf[0]['direct_cost'],
            'beats': [
                {'id': 'A08-R1-B1', 'action': '주인공은 A07의 좋은 시도와 막힌 반환을 함께 적은 자료에서 더 큰 자기 역할 요청과 연결·외곽·센터의 필요한 기능을 한 장에 나란히 놓는다. 새 기술 반복과 휴식에 쓸 일부 시간을 이 비교에 쓴다.', 'classification': 'SELECTED_FICTIONAL_OWN_ROLE_AND_TEAM_FUNCTION_COMPARISON'},
                {'id': 'A08-R1-B2', 'action': '그 자료를 가상 에이전트에게 건네고 공개 가능한 급여와 자기에게 실제 전달된 설명만으로 어느 기능을 포기해야 할지 묻는다. 에이전트에게 협상 질문을 맡길 뿐 프런트의 승인·다른 선수의 서명이나 정확 E2 가격을 받지 않는다.', 'classification': 'SELECTED_FICTIONAL_AGENT_QUESTION_NO_CONTRACT_RESULT'},
            ],
            'exit_state': cf[0]['changed_state'],
            'source_cp2_exit': '선수의 요구와 프런트의 계약 권한이 구분된 코어 유지 제안',
            'published_episode_number': None, 'manuscript_word_count': None,
        },
        {
            'id': 'A08-EF-002', 'global_function_order': 41, 'planned_allocation_slot': 384,
            'primary_subact': 'A08-S2', 'source_conditional_functions': ['A08-CF02', 'A08-CF03', 'A08-CF04'],
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'entry_state': None,
            'single_function': '첫 반환 차단 앞 각도 변경과 안전 재전개의 사용·중단 조건을 직접 시험한다',
            'unit_choice': [cf[i]['choice'] for i in (1, 2, 3)],
            'direct_present_cost': [cf[i]['direct_cost'] for i in (1, 2, 3)],
            'beats': [
                {'id': 'A08-R2-B1', 'action': '허용된 가상 훈련에서 첫 반환 길을 막는 수비를 보고 주인공은 공을 오래 잡지 않으려 짧게 드리블해 각도를 바꾼다. 첫 시도의 각도가 늦어 전달 경로가 닫힌다는 자기 관측을 남기며, 턴오버·득점은 정하지 않는다.', 'classification': 'SELECTED_FICTIONAL_LIVE_PRACTICE_ERROR_OBSERVED'},
                {'id': 'A08-R2-B2', 'action': '같은 과제를 다시 허용받은 좁은 훈련에서 그는 짧은 각도 변경 뒤 열린 가까운 수신자에게 공을 내보낸다. 이어 다른 반환 길도 닫힌 흐름에서는 무리한 패스를 멈추고 뒤쪽의 안전한 연결로 공을 되돌린다. 두 직접 동작은 가상 훈련 관측이며 패스 성공률·실제 NBA 경기 결정을 인증하지 않는다.', 'classification': 'SELECTED_FICTIONAL_BOUNDED_RETRY_AND_SAFE_RESET_OBSERVED'},
                {'id': 'A08-R2-B3', 'action': '주인공은 늦은 각도와 재시도 자료를 허용된 영상에서 대조하고, 다음 시험은 첫 반환이 실제 막힌 때로만 제한해 달라고 코치에게 요청한다. 더 많은 창조 기회를 즉시 요구하지 않는 비용을 감수한다.', 'classification': 'SELECTED_FICTIONAL_OWN_ERROR_REVIEW_NO_GENERAL_AUTHORITY'},
            ],
            'exit_state': '허용된 가상 훈련에서 첫 반환 차단 앞 늦은 각도 오류, 열린 수신자에게 짧게 내보낸 수정 시도와 다른 닫힌 길의 안전 재전개를 직접 수행했다. 원 A08-CF03의 실제 NBA 경기 시험은 미실행이고 압박 속 정확성·턴오버·상시 사용권은 아직 미증명이다.',
            'source_cp2_exit': '압박 속 라이브 패스의 사용/중단 조건을 가진 표본',
            'source_CF03_actual_NBA_game_trial_executed': False,
            'full_A08_S2_cp2_exit_certified': False,
            'published_episode_number': None, 'manuscript_word_count': None,
        },
        {
            'id': 'A08-EF-003', 'global_function_order': 42, 'planned_allocation_slot': 385,
            'primary_subact': 'A08-S3', 'source_conditional_functions': ['A08-CF05'],
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'entry_state': None,
            'single_function': '자기 짧은 공격과 이양 뒤 재관여를 같은 좁은 역할 안에서 선택한다',
            'unit_choice': cf[4]['choice'], 'direct_present_cost': cf[4]['direct_cost'],
            'beats': [
                {'id': 'A08-R3-B1', 'action': '가상 코치가 허용한 한정 팀 훈련에서 자신의 짧은 공격 창이 남는 첫 경우에는 주인공이 그 창을 시험한다. 다음 경우 동료에게 관측된 더 빠른 전개 창이 열리자 자기 슛을 더 시도할 기회를 줄이고 공을 넘긴다.', 'classification': 'SELECTED_FICTIONAL_TWO_CONDITIONS_NOT_NBA_USAGE_RIGHT'},
                {'id': 'A08-R3-B2', 'action': '그는 공을 보낸 뒤 멈추지 않고 다음 리바운드와 재관여 위치로 이동한다. 자기 이양·위치 이동만 직접 관측하고 동료의 득점·공동 에이스 지정·클로징 권한은 얻지 않는다.', 'classification': 'SELECTED_FICTIONAL_AFTER_PASS_REENGAGEMENT'},
            ],
            'exit_state': cf[4]['changed_state'],
            'source_cp2_exit': '경기별 공격 권한과 준비 책임을 함께 가지는 공동 에이스 후보',
            'published_episode_number': None, 'manuscript_word_count': None,
        },
    ]
    for i in range(1, len(functions)):
        functions[i]['entry_state'] = functions[i - 1]['exit_state']
    return {
        'schema': 'A08_FINITE_FUNCTION_BATCH_V1',
        'status': 'THREE_LOCAL_FINAL_FUNCTIONS_INDEPENDENTLY_REVIEWED', 'independent_review_completed': True,
        'previous_function': {'id': 'A07-EF-003', 'path': PREVIOUS, 'exact_full_exit': prior_exit},
        'functions': functions,
        'local_function_rows': 3,
        'A08_S2_actual_game_and_full_cp2_exit_hold': True,
        'A08_act_contract_authority_and_budget_exit_complete': False,
        'exact_E2_contract_price_acceptance_or_roster_receipt_certified': False,
        'co_ace_or_closing_authority_certified': False,
        'actual_NBA_2022_23_game_score_efficiency_or_winner_certified': False,
        'new_final_functions_registered': 0,
        'whole_A08_complete': False, 'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'manuscript_count': 0, 'manuscript_allowed': False,
        'author_locked': False, 'design_gate': 'CLOSED',
        'source_semantic_sha256': SEMANTIC_SHA,
        'source_hash_method': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {p: sha((root / p).read_bytes()) for p in SOURCES},
    }


def render(data):
    lines = ['# A08 2022–23 세 대표 국소 기능', '',
             'A07의 제한 역할 자료를 받되 2022 E2 계약 결과와 공동 에이스 권한은 선지급하지 않는다. 기존 5개 조건부 인과 후보를 세 소막의 기능으로 묶는다.', '']
    for row in data['functions']:
        lines += [f"## {row['id']} · {row['primary_subact']}", '',
                  f"- 입력: {row['entry_state']}", f"- 기능: {row['single_function']}"]
        lines += [f"- {beat['id']}: {beat['action']}" for beat in row['beats']]
        lines += [f"- 출구: {row['exit_state']}", '']
    lines += ['계획 슬롯 383–385는 출판 회차가 아니며 남은 57슬롯을 새 사건으로 채우지 않는다. '
              'EF-002는 훈련의 오류·수정 기능이다. 원 CF03의 NBA 실경기 시험과 A08-S2 전체 출구는 아직 미실행이다. '
              '세 국소 기능은 A08 Act의 실제 계약 권한·예산 출구를 완결하지 않는다.',
              '', '세 국소 기능의 독립 검문 완료·중앙 등록 전 상태다. 전체 A08/G13/G14·실제 Context Pack·원고 미완료, 설계·원고 게이트 `CLOSED`.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        return [] if data == build(root) else ['A08 batch differs from source-bound build']
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
        print(json.dumps({'current': not errors, 'errors': errors, 'functions': len(saved['functions'])}))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
