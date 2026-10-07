"""Build five bounded A06 functions from selected 2020–21 season results."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a05_final_function_batch as previous_builder


ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_a06_2020_21_finite_function_batch.py'
PREVIOUS = 'design/A05_E4_FINAL_EPISODE_FUNCTION.json'
A05_AUDIT = 'design/A05_SUBACT_EXIT_AUDIT_2026_10_07.json'
CANDIDATES = 'design/A06_2020_21_CONDITIONAL_FUNCTIONS.json'
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
ROLES = 'simulation/CHICAGO_2020_21_ROLE_ARCHITECTURE.md'
REGISTER = 'control/CHICAGO_2020_21_D1_S2_REGISTER.json'
SCOPE = 'simulation/NBA_2020_21_WORKING_EXECUTION_SCOPE.json'
RESULTS = 'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json'
TRANSACTIONS = 'simulation/NBA_2020_21_APPROVED_TRANSACTION_EXECUTION_BRIDGE.json'
SUMMER = 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json'
OUTPUT = Path('design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.json')
SOURCES = (SELF, PREVIOUS, A05_AUDIT, CANDIDATES, CP2, ROLES, REGISTER,
           SCOPE, RESULTS, TRANSACTIONS, SUMMER)
CANDIDATE_MEANING_SHA256 = '85a07885f55c8215442d791092aad83d038c458a5ef032ba3ddc99a90eb11ad6'
MEANING_KEYS = ('id', 'subact', 'cause', 'choice', 'direct_cost', 'changed_state', 'next')


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def norm_sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def candidate_meaning_sha(rows):
    projection = [{key: row[key] for key in MEANING_KEYS} for row in rows]
    raw = json.dumps(projection, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


FUNCTIONS = (
    {
        'source_ids': ['A06-CF01', 'A06-CF02'], 'subact': 'A06-S1',
        'single_function': '다섯 선수의 공격 시작권을 나누고 공을 넘긴 뒤 자기 다음 위치를 만든다',
        'beats': [
            '전달받은 역할 설명과 허용된 코트 관측에서 LaMelo의 창출, LaVine의 득점 마무리, Coby의 기존 PG 시험, Markkanen의 공간, 자신의 수비·리바운드·제한 운반을 별개 과제로 확인한다.',
            'LaMelo가 시작하는 허용된 구간에서 자기 운반을 줄이고 공을 넘긴 뒤, 동료의 공격 공간을 막지 않는 컷·스크린 또는 리바운드 준비 위치로 이동한다. 동료의 수락·득점 결과는 미인증이다.',
        ],
        'exit': '주인공은 LaMelo가 시작하는 구간과 자기 제한 운반을 구분하고, LaVine의 득점·Coby의 PG 시험·Markkanen의 공간을 지우지 않는 다음 관여 위치로 실제 움직였다. 자기 운반 빈도와 다시 공 받기 쉬운 자리를 줄인 비용은 남지만 동료의 공격 성공이나 주전 권한을 얻은 것은 아니다.',
        'reader_question': '리바운드 뒤에는 어디까지 직접 전진하고 언제 첫 패스를 내야 할까',
    },
    {
        'source_ids': ['A06-CF03', 'A06-CF04'], 'subact': 'A06-S1',
        'single_function': '리바운드 뒤 짧은 전진·이양과 숏롤 첫 패스의 서로 다른 첫 벽을 시험한다',
        'beats': [
            '허용된 역할 반복에서 리바운드 뒤 열린 길로 짧게 전진하고 첫 벽이 서면 LaMelo 또는 기존 가드에게 공을 이양한다. 빠른 수비 앞 운반 오차는 그대로 기록한다.',
            '하프코트의 숏롤 위치에서는 보이는 도움수비와 동료 공간을 확인해 첫 단순 패스를 시도하지만 늦은 연결을 영상에서 대조한다. 패스 성공률·득점·상시 point forward 권한은 미정이다.',
        ],
        'exit': '주인공은 리바운드 뒤 열린 길의 짧은 전진과 첫 벽의 이양, 하프코트 숏롤의 첫 연결을 다른 과제로 시험했다. 자기 마무리 시간을 줄이고 늦은 패스를 드러낸 비용이 있으며, 빠른 수비와 두 번째 읽기에는 여전히 오류가 남는다. 세 코어의 공격 시작권을 혼자 대체하지 않는다.',
        'reader_question': 'Theis와 Green이 들어온 뒤 이름보다 수행 위치를 다시 확인할 수 있을까',
    },
    {
        'source_ids': ['A06-CF05'], 'subact': 'A06-S2',
        'single_function': '승인된 Theis·Green A의 합류 뒤 본인에게 전달된 역할 변화만 확인한다',
        'beats': [
            '선택된 2020–21 거래 실행 뒤 주인공에게 동료 구성과 한정 과제가 전달되는 가상 운영 조건에서, Theis·Green의 새 위치와 자신의 수비 복귀·리바운드·연결 책임을 묻는다.',
            '허용된 준비에서 바뀐 조합의 위치를 맞춰 보되 새 빅맨 이름만으로 자신의 판단 지연이나 팀의 모든 문제를 해결했다고 여기지 않는다. 프런트 비용·픽·리그 접수 내역은 자신의 정보가 아니다.',
        ],
        'exit': 'Theis·Green A는 선택된 시즌 실행의 동료 구성 변화로 남고, 주인공은 전달받은 수비·리바운드·연결 과제만 다시 확인했다. 자기 공격 반복 시간을 조합 준비에 쓰는 직접 비용을 지불했다. 승인된 거래 범위를 넘는 빅 영입·즉시 올인·새 법적 비용은 만들지 않는다.',
        'reader_question': '정규시즌 10위가 Washington의 한 경기 생존을 보장할까',
    },
    {
        'source_ids': ['A06-CF06'], 'subact': 'A06-S3',
        'single_function': '선택된 Washington 생존전에서 개인 공격 과시보다 맡은 수비·리바운드·연결을 먼저 수행한다',
        'beats': [
            '선택된 L2 Chicago@Washington 첫 승리 결과를 배경으로, 주인공은 가상 국소 역할 창에서 전달받은 수비 위치로 이동하고 가까운 상대와 바스켓 사이를 박스아웃한다. 그 뒤 동료가 공을 확보하는 것을 직접 본다.',
            '이 선택된 가상 행동과 팀의 이미 선택된 승리를 분리한다. 동료의 공 확보를 실제 역사 포제션·본인 공식 리바운드·승리의 단독 원인·정확 점수로 바꾸지 않는다.',
        ],
        'exit': 'Chicago의 선택된 Washington 원정 승리 안에서 주인공은 자기 공격을 최대화하기보다 맡은 수비 위치로 움직여 박스아웃했고, 동료가 공을 확보하는 한정 가상 수행을 직접 봤다. 이는 선택된 승리의 실제 역사 포제션이나 단독 승리 인과·개인 박스가 아니다. 승리는 다음 문턱의 진입일 뿐 본선 진출 보장이 아니다.',
        'reader_question': '첫 승리 뒤 Indiana의 다른 압박에 준비 시간을 다시 쓸 수 있을까',
    },
    {
        'source_ids': ['A06-CF07', 'A06-CF08'], 'subact': 'A06-S3',
        'single_function': '선택된 Indiana 패배 뒤 승패와 분리한 한정 수행 표본을 다음 준비로 넘긴다',
        'beats': [
            '첫 승리의 하이라이트를 더 보는 대신 허용된 Indiana 상대 영상과 자신의 수비·리바운드 과제를 준비하고, 선택된 다음 경기에서 맡은 좁은 역할을 다시 시험한다.',
            '선택된 Indiana 원정 패배 뒤 본인이 직접 본 늦은 첫 연결을 허용된 영상과 대조한다. 다음 훈련에는 첫 패스 시점 한 과제를 적고, 에이전트에게는 승패나 공식 효율 대신 자기 역할·한계의 한정 표본만 전달한다. 에이전트의 평가·계약 답은 미정이다.',
        ],
        'exit': 'Chicago의 선택된 Indiana 패배로 그 시즌 진출 기회는 끝났다. 주인공은 LaMelo와 나누는 시작권, 공 없는 관여, 첫 패스 시점의 부족을 관측했으며, 그중 첫 패스 시점 한 과제를 다음 훈련에 넘겼다. 에이전트에게도 한정 역할 표본과 미증명 부분을 분리해 전달했지만 새 계약·평가 결과는 받지 않았다. 이는 M1/G1A의 다음 여름 방향을 선지급하지 않는다.',
        'reader_question': '다음 여름 M1과 성장 코어 방향의 비용 속에서 어떤 역할을 계속 맡을까',
    },
)


def build(root=ROOT):
    previous = load(root, PREVIOUS)
    audit = load(root, A05_AUDIT)
    candidates = load(root, CANDIDATES)
    cp2 = load(root, CP2)
    register = load(root, REGISTER)
    scope = load(root, SCOPE)
    results = load(root, RESULTS)
    transactions = load(root, TRANSACTIONS)
    summer = load(root, SUMMER)
    role_text = (root / ROLES).read_text(encoding='utf-8-sig')
    expected_previous = previous_builder.build(root)[-1]
    assert previous == expected_previous, 'A05 E4 source-bound predecessor required'
    assert not previous_builder.validate_all([previous_builder.load(root, p) for p in previous_builder.OUTPUTS], root=root)
    assert previous['episode_function_id'] == 'A05-EF-004'
    assert previous['next_unit']['id'] == 'A06-S1'
    assert audit['counts']['subact_bounded_pass'] == 3 and audit['counts']['act_bounded_pass'] == 1
    assert audit['act_exit_row']['functional_exit_audit_result'] == 'PASS_BOUNDED_A05_ACT_OPERATING_EXIT'
    assert all(norm_sha((root / path).read_bytes()) == digest
               for path, digest in audit['source_sha256'].items()), 'A05 audit sources must remain current'
    assert candidates['status'] == 'EIGHT_CONDITIONAL_2020_21_CAUSAL_FUNCTIONS_NOT_FINAL_G13'
    assert len(candidates['functions']) == 8 and candidate_meaning_sha(candidates['functions']) == CANDIDATE_MEANING_SHA256
    assert all(row['selected_event'] is False and row['author_locked'] is False
               for row in candidates['functions'])
    assert candidates['allocation']['total_slots'] == 74
    assert candidates['season_selected'] is False, 'historical pre-S2 candidate snapshot must stay a snapshot'
    assert cp2['status'] == 'PROVISIONAL_FUNCTION_PACKET'
    subacts = {x['id']: x for x in cp2['subacts'] if x['id'] in {'A06-S1','A06-S2','A06-S3'}}
    assert len(subacts) == 3 and all(x['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY' for x in subacts.values())
    assert {key: subacts[key]['exit_state'] for key in subacts} == {
        'A06-S1': '각자 시작하는 공격을 구분',
        'A06-S2': 'Theis/Green A의 승인 범위 유지',
        'A06-S3': '진출 여부와 분리된 개인 수행 표본을 다음 훈련과 에이전트의 계약 평가에 넘김',
    }
    act = next(row for row in cp2['acts'] if row['id'] == 'A06')
    assert (act['choice'], act['cost'], act['exit_state']) == (
        'LaMelo의 창조와 LaVine의 득점을 살림',
        '온볼 기회와 빠른 승리 욕망',
        'K1/L2 잠정 탈락·2021 #10/#39')
    assert register['season_selected'] is True and len(register['k_closed']) == 4
    assert set(register['k_closed']) == {'K_HEALTH','K_REGISTRATION','K_TRANSACTIONS','K_METHOD_EVENTS'}
    assert scope['status'] == 'S2_FINITE_2020_21_EXECUTION_CLOSED'
    assert scope['finite_s2_execution_cleared'] is True and scope['season_selected'] is True
    assert scope['regular_record']['CHI'] == [31, 41]
    assert results['summary']['regular_games'] == 1080 and results['summary']['total_result_games'] == 1174
    assert next(row for row in results['standings'] if row['team'] == 'CHI')['seed'] == 10
    assert {(row['round'], row['pick'], row['origin'], row['control_holder'])
            for row in results['pick_control_snapshot']['rows'] if row['origin'] == 'CHI'
            and row['pick'] in (10, 39)} == {(1,10,'CHI','CHI'),(2,39,'CHI','CHI')}
    chi_playin = [g for g in results['games'] if g['phase'] == 'PLAY_IN' and 'CHI' in (g['home'], g['away'])]
    assert [(g['home'], g['away'], g['winner']) for g in chi_playin] == [('WAS','CHI','CHI'),('IND','CHI','IND')]
    assert all(g['classification'] == 'EXISTING_AUTHOR_SELECTED_RESULT_WORKING_EXECUTION' for g in chi_playin)
    assert transactions['status'] == 'APPROVED_DIRECTION_DATED_WORKING_EXECUTION_SUBSCOPE'
    f1 = next(row for row in transactions['events'] if row['id'] == 'F1_FIVE_PLAYER_ATOMIC')
    assert f1['date'] == '2021-03-25'
    assert {row['player'] for row in f1['movements'] if row['to'] == 'CHI'} == {
        'Daniel Theis', 'Javonte Green'}
    assert summer['selected']['route'] == 'G1A_PLUS_M1'
    assert summer['manuscript_allowed'] is False
    for phrase in ('LaMelo', 'LaVine', 'Coby White', 'Markkanen', '주인공', '첫 PG 시험 기회 유지'):
        assert phrase in role_text, phrase

    groups = []
    prior_exit = previous['exit_state']
    for index, spec in enumerate(FUNCTIONS, 1):
        source_rows = [candidates['functions'][int(s[-2:])-1] for s in spec['source_ids']]
        assert [r['id'] for r in source_rows] == spec['source_ids']
        assert all(r['subact'] == spec['subact'] for r in source_rows)
        row = {
            'id': f'A06-EF-{index:03}', 'global_function_order': 31 + index,
            'planned_allocation_slot': 248 + index, 'primary_subact': spec['subact'],
            'source_conditional_functions': spec['source_ids'],
            'status': 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE',
            'entry_state': prior_exit,
            'single_function': spec['single_function'],
            'unit_choice': [r['choice'] for r in source_rows],
            'direct_present_cost': [r['direct_cost'] for r in source_rows],
            'beats': [{'id': f'A06-R{index}-B{n}', 'action': action,
                       'classification': 'SELECTED_BOUNDED_FICTIONAL_ACTION_WITH_EXISTING_RESULT_BACKGROUND'}
                      for n, action in enumerate(spec['beats'], 1)],
            'exit_state': spec['exit'], 'reader_question_at_end': spec['reader_question'],
            'original_candidate_bounded_exit': source_rows[-1]['changed_state'],
            'published_episode_number': None, 'manuscript_word_count': None,
        }
        groups.append(row)
        prior_exit = row['exit_state']
    assert [g['global_function_order'] for g in groups] == [32,33,34,35,36]
    assert [g['planned_allocation_slot'] for g in groups] == [249,250,251,252,253]
    assert [g['primary_subact'] for g in groups] == ['A06-S1','A06-S1','A06-S2','A06-S3','A06-S3']
    assert [s for g in groups for s in g['source_conditional_functions']] == [f'A06-CF{i:02}' for i in range(1,9)]
    return {
        'schema': 'A06_2020_21_FINITE_FUNCTION_BATCH_V1',
        'status': 'FIVE_LOCAL_FINAL_FUNCTIONS_INDEPENDENTLY_REVIEWED',
        'independent_review_completed': True,
        'scope': 'Five bounded 2020-21 function records; no new season result selection or mandatory 74-episode obligation',
        'previous_function': {'id': previous['episode_function_id'], 'path': PREVIOUS,
                              'exact_full_exit': previous['exit_state']},
        'old_candidate_entry_projection': candidates['entry_from']['changed_state'],
        'old_candidate_entry_is_not_current_exact_E4_exit': True,
        'season_result_authority': {
            'historical_candidate_season_selected_false_is_old_snapshot': True,
            'current_s2_register_and_scope_season_selected': True,
            'Chicago_record': [31,41], 'Chicago_east_seed': 10,
            'L2_selected_sequence': ['CHI@WAS_WIN','CHI@IND_LOSS'],
            'selected_season_results_are_fictional_not_actual_boxes': True,
        },
        'five_player_usage_rights': {
            'LaMelo': 'initial second-unit creator then selected primary creation path; not an automatic copied Charlotte award',
            'LaVine': 'lead scorer and closing attack preserved',
            'Coby': 'initial PG trial and later secondary scoring/development preserved',
            'Markkanen': 'PF spacing and contract-year evaluation opportunity preserved; 2021 M1 is later selected direction',
            'protagonist': 'wing defense/rebound, limited direct carry and first pass; not permanent point forward',
        },
        'functions': groups,
        'subact_operating_exit_comparison': [
            {'subact':'A06-S1','cp2_exit':subacts['A06-S1']['exit_state'],
             'witnesses':['A06-EF-001','A06-EF-002'], 'review_result':'BOUNDED_PASS_SOURCE_CURRENT'},
            {'subact':'A06-S2','cp2_exit':subacts['A06-S2']['exit_state'],
             'witnesses':['A06-EF-003'], 'review_result':'BOUNDED_PASS_SOURCE_CURRENT'},
            {'subact':'A06-S3','cp2_exit':subacts['A06-S3']['exit_state'],
             'witnesses':['A06-EF-004','A06-EF-005'], 'review_result':'BOUNDED_PASS_SOURCE_CURRENT'},
        ],
        'act_operating_exit_comparison': {
            'cp2_choice': act['choice'],
            'cp2_cost': act['cost'],
            'cp2_exit': act['exit_state'],
            'witnesses': ['A06-EF-001','A06-EF-002','A06-EF-004','A06-EF-005'],
            'bounded_result': 'BOUNDED_PASS_SOURCE_CURRENT',
            'selected_season_exit': 'Chicago 31–41 / East 10; L2 Washington win then Indiana loss and elimination; frozen pre-optional-offseason control CHI 1R10 / CHI 2R39.',
            'literal_provisional_wording_is_historical_snapshot': True,
            'not_certified': 'Actual private June 22 holder, drafted player, individual box, all history, or whole G13 completion.',
        },
        'selected_summer_technical_problem': '첫 패스 시점의 지연',
        'agent_contract_evaluation_result_certified': False,
        'individual_L2_box_score_or_causal_winner_credit': False,
        'actual_private_medical_roster_or_team_receipt_certified': False,
        'new_award_championship_or_2022_choice': False,
        'new_final_functions_registered': 0,
        'planned_A06_slots': 74,
        'unassigned_slots_are_not_mandatory_new_events': True,
        'whole_A06_Act_complete': False,
        'bounded_A06_Act_operating_exit_pass': True,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'new_author_lock': False,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
        'source_hash_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256': {path: norm_sha((root / path).read_bytes()) for path in SOURCES},
    }


def render(data):
    lines = ['# A06 2020–21 유한 기능 5건', '',
             '**상태:** 국소 독립 검문 완료·중앙 등록 전. 기존 S2의 선택된 가상 시즌 결과를 사용하며 실제 개인 박스·의료·사적 접수를 인증하지 않는다.', '',
             f"- A05 정확 인계: {data['previous_function']['exact_full_exit']}",
             '- 10월 2일 조건부 문서의 `season_selected=false`는 과거 상태다. 현행 S2 유한 실행 원장의 `true`를 사용한다.',
             '- LaMelo 창출, LaVine 득점, Coby 개발, Markkanen 공간, 주인공 수비·리바운드·제한 운반을 보존한다. 2021 여름 M1은 다음 범위다.', '',
             '| 기능 | 소막·계획 슬롯 | 선택과 직접 비용 | 한정 출구 |', '| --- | --- | --- | --- |']
    for row in data['functions']:
        lines.append(f"| {row['id']} | {row['primary_subact']} / {row['planned_allocation_slot']} | {' / '.join(row['unit_choice'])}<br>비용: {' / '.join(row['direct_present_cost'])} | {row['exit_state']} |")
    lines += ['', '세 소막과 A06 Act의 **한정 운영 출구**는 독립 검문을 통과했다. CP2의 옛 ‘잠정’ 문구는 당시 상태이고, 현행 S2는 Chicago 31–41/동부10위·L2 Washington 승 뒤 Indiana 패배로 종료된다. #10/#39는 optional 2021여름 이동 전의 동결 권리틀이며 실제6월22일 보유자·지명선수 인증이 아니다.',
              'Washington 승리와 Indiana 패배는 기존 선택된 결과이며 주인공 개인 행동의 승패 단독 원인이 아니다. 첫 패스 시점은 다음 훈련의 한 과제일 뿐 기술 완성이나 계약 답이 아니다.',
              '중앙 등록 전 기능 증가0. 전체 A06/G13/G14, 실제 Context Pack, 원고는 미완료다. 새 수상·우승·2022 선택0, 설계/원고 게이트 `CLOSED`.', '']
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['A06 batch differs from source-bound current build']


def self_test(data):
    cases = [
        ('LaVine erased', lambda x: x['five_player_usage_rights'].update(LaVine='protagonist takes all closing shots')),
        ('L2 win becomes playoff berth', lambda x: x['functions'][3].update(exit_state='Chicago won Washington and secured the playoffs')),
        ('private medical certified', lambda x: x.update(actual_private_medical_roster_or_team_receipt_certified=True)),
        ('74 episodes mandatory', lambda x: x.update(unassigned_slots_are_not_mandatory_new_events=False)),
    ]
    for name, mutation in cases:
        changed = copy.deepcopy(data)
        mutation(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mutation in [
        ('A05 full exit changed', PREVIOUS, lambda x: x.update(exit_state='LaMelo entered and all teammates lost their roles')),
        ('same-ID A06 choice reversed', CANDIDATES, lambda x: x['functions'][4].update(choice='Theis/Green immediately solve every role and I approve the trade')),
        ('S2 falsely deselected', REGISTER, lambda x: x.update(season_selected=False)),
    ]:
        def altered(root, requested, path=path, mutation=mutation):
            source = original_load(root, requested)
            if str(requested).replace('\\', '/') == path:
                source = copy.deepcopy(source)
                mutation(source)
            return source
        with patch(__name__ + '.load', side_effect=altered):
            assert validate(data), name
    return len(cases) + 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / OUTPUT.with_suffix('.md')).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors += validate(saved)
        if (ROOT / OUTPUT.with_suffix('.md')).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'current': not errors, 'errors': errors,
                      'function_ids': [r['id'] for r in data['functions']],
                      'negative_controls': tested}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
