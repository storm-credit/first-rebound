"""Audit the first six CP2 Sub-Act exits and two adjacent Act handoffs."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_cp2_finite_function_coverage as finite_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_A02_SUBACT_EXIT_AUDIT_2026_10_07.json')
MARKDOWN = Path('design/A01_A02_SUBACT_EXIT_AUDIT_2026_10_07.md')
CP2 = 'design/CP2_ACT_SUBACT_PACKET.json'
FINITE = str(finite_builder.OUTPUT).replace('\\', '/')
BRIDGE = 'research/A01_A02_PREP_TRANSITION_AUTHORITY_BOUNDARY_2026_10_07.json'
COLLEGE = 'design/A02_CF10_COLLEGE_TRANSITION_WORKING_MODEL_2026_10_07.json'
SKILL = 'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md'

ASSESSMENTS = {
    'A01-S1': {
        'cp2_exit': '참여와 회피가 분리됨',
        'cp2_choice_anchor': '기본 준비',
        'cp2_cost_anchor': '즉시 칭찬',
        'witness_ids': ['A01-EF-001', 'A01-EF-002'],
        'action_anchor': '첫 훈련에 들어갔고 같은 학년 라이벌에게',
        'cost_anchor': '첫 훈련에 실제 쓴 시간',
        'reason': '회피 중의 제안은 수락이 아니었고, 다음 기능에서 실제 체험에 들어가 완패했다. 참여 행동과 종전 회피가 분리됐다.',
        'boundary': '다음 훈련 복귀는 S2이며 기술 숙련·생활 전면 교정은 이 출구의 요구가 아니다.',
        'result': 'HOLD_CP2_CHOICE_AND_COST_NOT_OBSERVED_IN_S1',
        'specific_gap': 'E1–E2에는 농구부가 맡긴 기본 준비를 실제 해 보거나 즉시 칭찬을 포기하는 선택이 확정되어 있지 않다. 첫 훈련 진입·완패만으로 그 CP2 선택/비용까지 인증하지 않는다.',
    },
    'A01-S2': {
        'cp2_exit': '재능 밖 의무를 처음 인식',
        'cp2_choice_anchor': '맡은 준비 시간',
        'cp2_cost_anchor': '정해진 시간',
        'witness_ids': ['A01-EF-003', 'A01-EF-004', 'A01-EF-005', 'A01-EF-006'],
        'action_anchor': '게임 한 판을 더 시작하지 않고 이번 한 번 맡은 공 준비에 참여했다',
        'cost_anchor': '한 판 더 이어갈 즉시 재미와 승부 기회',
        'reason': '재참여·팀 기여 뒤 위치 학습과 공동 준비를 거쳐, 한 판 더 게임할 기회를 미루고 맡은 공 준비를 했다.',
        'boundary': '한 번의 준비 선택은 반복 수면·출석·게임 통제나 팀 전원의 신뢰 완성을 증명하지 않는다.',
    },
    'A01-S3': {
        'cp2_exit': '외부 환경 선택의 주체가 됨',
        'cp2_choice_anchor': '미국행 이유',
        'cp2_cost_anchor': '익숙한 서열',
        'witness_ids': ['A01-EF-007', 'A01-EF-008', 'A01-EF-009'],
        'action_anchor': '프렙 이동 방향의 준비를 계속하겠다고 직접 밝혔다',
        'cost_anchor': '익숙한 국내 신체 우위와 관계 안에만 남는 쉬운 선택',
        'reason': '미국 환경을 비교하고 국내 기록·미국 권한의 미답을 구별한 뒤, 미답을 떠안은 채 기존 프렙 방향을 본인이 밝혔다.',
        'boundary': '의사표명 자체는 가상 F1–F6 기관 절차·실제 학교 도착이나 개인 실물 증명을 대신하지 않는다.',
    },
    'A02-S1': {
        'cp2_exit': '소속 자격을 책임짐',
        'cp2_choice_anchor': '도움을 요청',
        'cp2_cost_anchor': '학습 시간',
        'witness_ids': ['A02-EF-001', 'A02-EF-002', 'A02-EF-003'],
        'action_anchor': '다음 허용 하루에는 스스로 일어나 의무 스터디홀과 허용 기본 훈련을 먼저 맞춘',
        'cost_anchor': '즉시 게임을 시작하고 계속할 자유',
        'reason': '학업 도움을 요청하고 게임으로 지원 시간 한 번을 잃은 뒤, 다음 허용 하루에는 자기 기상·스터디홀·기본 훈련을 먼저 수행했다.',
        'boundary': '책임을 보이는 한 하루의 기능적 출구다. 전체 졸업·NCAA 자격·장기 생활 습관 통과는 아니다.',
    },
    'A02-S2': {
        'cp2_exit': '새 역할의 반복 과제',
        'cp2_choice_anchor': '윙의 기본 과제',
        'cp2_cost_anchor': '포지션 자존심',
        'witness_ids': ['A02-EF-004', 'A02-EF-005', 'A02-EF-006'],
        'action_anchor': '코너 패스가 시작될 때 복귀를 시도했지만',
        'cost_anchor': '자기의 늦은 복귀를 드러내는 영상 대조와 한 번의 수정 시도',
        'reason': '코너 복귀 지연을 보고, 별도 허용 훈련에서 위치·공 확인과 영상 대조 후 같은 과제의 복귀를 다시 시도했다.',
        'boundary': '반복 과제를 특정한 출구이며 제때 복귀·실전 성공·윙 기술 숙련은 아니다.',
    },
    'A02-S3': {
        'cp2_exit': 'Villanova 입학/역할 경로 연결',
        'cp2_choice_anchor': '반복 수행과 학사 준비',
        'cp2_cost_anchor': '안정성',
        'witness_ids': ['A02-EF-007', 'A02-EF-008', 'A02-EF-009', 'A02-EF-010'],
        'action_anchor': '2017년 봄 늦은 Villanova 체육장학금 오퍼와 입학 승인을 전달받고',
        'cost_anchor': '익숙한 프렙 역할을 한 번 더 과시할 허용 훈련·평가 시간',
        'reason': '프렙의 제한 역할 반복·학업 별도 수행·공식 절차 질문 뒤 가상 Villanova 영입·입학, 학교 졸업·성적표와 후순위 준비가 이어졌다.',
        'boundary': '여름 EC/compliance는 A02 회차 밖 별도 기관 연결이고, A03 등록·대학 첫 출전은 아직 미실행이다.',
    },
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def read_exact(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def cost_text(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)


def build(root=ROOT):
    finite = load(root, FINITE)
    cp2 = load(root, CP2)
    bridge = load(root, BRIDGE)
    college = load(root, COLLEGE)
    for path, observed in ((FINITE, finite), (CP2, cp2), (BRIDGE, bridge), (COLLEGE, college)):
        assert observed == read_exact(root, path), 'input differs from filesystem source: ' + path
    assert not finite_builder.validate(finite, root=root), 'finite 42-row source/currentness failed'
    assert finite['counts']['registered_local_functions_total'] == 19
    assert finite['counts']['subacts_with_registered_local_function_route'] == 6
    assert finite['counts']['whole_subact_exits_audited'] == 0
    assert finite['whole_g13_complete'] is False and finite['manuscript_allowed'] is False
    assert [s['id'] for s in cp2['subacts'][:6]] == list(ASSESSMENTS)
    subacts = {s['id']: s for s in cp2['subacts']}
    rows = {r['subact_id']: r for r in finite['subact_rows']}
    loaded_functions = {}
    source_paths = {'tools/build_a01_a02_subact_exit_audit.py', FINITE, CP2, BRIDGE, COLLEGE, SKILL}
    results = []
    for sid, config in ASSESSMENTS.items():
        subact, coverage = subacts[sid], rows[sid]
        assert subact['exit_state'] == config['cp2_exit'], sid
        assert config['cp2_choice_anchor'] in subact['choice'], sid
        assert config['cp2_cost_anchor'] in subact['cost'], sid
        assert coverage['registered_function_ids'] == config['witness_ids'], sid
        assert coverage['whole_subact_exit_audited'] is False, sid
        witnesses = []
        for fid, path in zip(coverage['registered_function_ids'], coverage['registered_function_paths']):
            item = load(root, path)
            assert item == read_exact(root, path), 'loaded final function differs from validated file: ' + path
            assert item['episode_function_id'] == fid, sid
            assert item.get('primary_subact', item.get('subact')) == sid, fid
            assert item['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
            assert item['manuscript_allowed'] is False and item['whole_g13_complete'] is False
            loaded_functions[fid] = item
            source_paths.add(path)
            witnesses.append({
                'function_id': fid, 'source_path': path,
                'exact_entry': item.get('entry_state', item.get('entry_after_fictional_bridge')),
                'choice_or_function': item.get('unit_choice', item['single_function']),
                'direct_present_cost': item['direct_present_cost'],
                'exact_exit': item['exit_state'],
            })
        last = loaded_functions[config['witness_ids'][-1]]
        assert config['action_anchor'] in last['exit_state'], sid
        assert config['cost_anchor'] in cost_text(last['direct_present_cost']), sid
        assert coverage['last_registered_exact_exit'] == last['exit_state'], sid
        audit_result = config.get('result', 'PASS_BOUNDED_CP2_FUNCTIONAL_EXIT')
        results.append({
            'subact_id': sid, 'cp2_entry_state': subact['entry_state'],
            'cp2_choice': subact['choice'], 'cp2_cost': subact['cost'],
            'cp2_exit_state': subact['exit_state'],
            'function_witnesses': witnesses,
            'last_exact_exit': last['exit_state'],
            'observed_action_cost_authority_reason': config['reason'],
            'bounded_not_claimed': config['boundary'],
            'cp2_exit_phrase_observed': True,
            'cp2_choice_and_cost_observed_within_own_function_route': audit_result == 'PASS_BOUNDED_CP2_FUNCTIONAL_EXIT',
            'specific_gap': config.get('specific_gap'),
            'exit_audit_result': audit_result,
            'actual_real_case_or_broad_habit_certified': False,
        })
    assert len(loaded_functions) == 19
    a01_last = loaded_functions['A01-EF-009']
    a02_first = loaded_functions['A02-EF-001']
    a02_last = loaded_functions['A02-EF-010']
    a01_contribution = loaded_functions['A01-EF-003']
    assert '농구를 계속할 이유가 생긴다' in a01_contribution['exit_state']
    assert a02_first['entry_previous_full_exit'] == a01_last['exit_state']
    assert a02_first['intervening_fictional_authority_outcomes'] == ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
    assert '학교에 도착했지만' in a02_first['entry_after_fictional_bridge']
    fpath = bridge['fictional_transition_working_path']
    assert fpath['status'] == 'ROUTINE_FICTIONAL_AUTHORITY_OUTCOMES_SELECTED_WITHIN_LOCKED_MOVE_INDEPENDENTLY_REVIEWED'
    assert [x['id'] for x in fpath['steps']] == ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
    assert fpath['A01_E9_intent_is_not_any_of_F1_to_F6'] is True
    assert fpath['historical_real_person_or_real_school_case_certified'] is False
    assert fpath['steps'][2]['authority'] == 'fictional prep designated school official and SEVIS'
    assert fpath['steps'][3]['authority'] == 'U.S. consular decision in the fictional case'
    assert fpath['steps'][4]['authority'] == 'U.S. border admission in the fictional case'
    assert bridge['manuscript_allowed'] is False and bridge['whole_g13_complete'] is False
    assert college['status'] == 'ROUTINE_COLLEGE_TRANSITION_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED'
    assert college['entry_state'] == loaded_functions['A02-EF-009']['exit_state']
    i1, i2, i3, i4 = college['institutional_sequence']
    assert [i['id'] for i in (i1, i2, i3, i4)] == ['I1', 'I2', 'I3', 'I4']
    assert i1['scope'] == i2['scope'] == 'A02_S3'
    assert i1['offer_in_fiction'] and i1['admission_in_fiction']
    assert i2['graduation_in_fiction'] and i2['final_transcript_sent_in_fiction']
    assert i3['scope'] == 'INTER_ACT_INSTITUTIONAL_BRIDGE_NOT_A02_EPISODE_DATE'
    assert i3['eligibility_center_academic_and_athletics_certified_in_fiction']
    assert i3['villanova_compliance_confirmed_in_fiction']
    assert i3['actual_private_ncaa_decision_or_villanova_record_certified'] is False
    assert i4['enrollment_or_first_game_executed_here'] is False
    assert a02_last['next_unit']['enrollment_or_official_college_game_executed_here'] is False
    assert a02_last['next_unit']['summer_bridge_executed_as_A02_beat'] is False
    a01, a02 = cp2['acts'][:2]
    assert a01['exit_state'] == '팀에 다시 나올 이유를 얻음'
    assert a02['exit_state'] == '프렙 졸업과 NCAA 진입 근거'
    a03_s1 = subacts['A03-S1']
    assert a03_s1['entry_state'] == '우승팀 소속을 자기 실력과 혼동'
    handoffs = [
        {'from_act': 'A01', 'to_act': 'A02',
         'from_exact_exit': a01_last['exit_state'],
         'bridge_evidence': ['A01 E9 intention', 'F1 school acceptance', 'F2 guardian/funding',
                             'F3 school-issued I-20', 'F4 visa', 'F5 border admission',
                             'F6 provisional placement and adviser', 'A02 E1 arrived-school entry'],
         'to_exact_entry': a02_first['entry_after_fictional_bridge'],
         'handoff_audit_result': 'PASS_FICTIONAL_AUTHORITY_BRIDGE',
         'boundary': 'E9 의사만으로 도착을 인증하지 않는다. 가상 F1–F6와 실제 사람·학교 서류 인증은 분리한다.'},
        {'from_act': 'A02', 'to_act': 'A03',
         'from_exact_exit': a02_last['exit_state'],
         'bridge_evidence': ['I1 spring fictional offer/admission', 'I2 May–June graduation/final transcript',
                             'I3 selected summer EC/compliance inter-act bridge'],
         'to_cp2_provisional_entry': a03_s1['entry_state'],
         'to_exact_entry': None,
         'handoff_audit_result': 'HOLD_A03_ENROLLMENT_AND_FIRST_FUNCTION_NOT_EXECUTED',
         'specific_missing_action': 'I3 뒤 가상 대학 등록과 A03-S1 첫 국소 기능의 실제 진입·제한 로스터 역할 연결. I4는 현재 미실행.',
         'boundary': 'A02-S3의 경로 연결과 여름 기관 선택을 대학 첫 경기·출전 안정성으로 바꾸지 않는다.'},
    ]
    s1_alignment_candidate = {
        'status': 'WORKING_OPERATIONAL_ALIGNMENT_CANDIDATE_NOT_APPLIED',
        'target': 'A01-S1 provisional CP2 choice and cost only',
        'preserve_exact': ['A01-S1 entry/exit', 'A01 whole Act exit', 'A01-S2 and S3',
                           'all 19 existing final function records', 'original CP2 packet'],
        'proposed_operational_choice': '주인공은 체육관에 남을 명분과 자존심 때문에 감독이 제안한 첫 조건부 체험에 실제 들어간다.',
        'proposed_operational_cost': '첫 훈련에 쓴 시간에는 과제 없이 체육관에 머무를 수 없고, 동갑 비교에서 기술·판단·위치선정의 부족을 드러내는 완패를 겪는다.',
        'exact_support': ['A01-EF-001 conditional trial offer', 'A01-EF-002 T1 entry and T2 defeat',
                          'A01-EF-002 direct present cost'],
        'meaning_shift_to_review': '원 CP2의 즉시 칭찬 포기·농구부 기본 준비를 S1에서 실행했다고 소급하지 않는다. S1은 회피에서 참여로, S2는 맡은 기본 준비의 책임으로 나뉘어 관측되는 현재 19기능의 단계다.',
        'new_event_or_extra_episode_required': False,
        'currently_fills_s1_hold': False,
        'author_locked': False,
    }
    acts = [
        {'act_id': 'A01', 'cp2_exit_state': a01['exit_state'],
         'evidence_function_ids': ['A01-EF-003', 'A01-EF-005', 'A01-EF-006', 'A01-EF-009'],
         'functional_exit_audit_result': 'PASS_BOUNDED_ACT_EXIT',
         'reason': 'E3의 실제 다음 훈련 복귀·리바운드/아웃렛 뒤 라이벌만이 아닌 계속할 이유가 생기고, E5/E6에서 맡은 준비로 그 이유를 시험했다.',
         'not_claimed': '게임 생활 전체 교정·실제 학교 출결 해결·프렙 도착을 Act 안에서 인증하지 않는다.'},
        {'act_id': 'A02', 'cp2_exit_state': a02['exit_state'],
         'evidence_function_ids': ['A02-EF-007', 'A02-EF-008', 'A02-EF-009', 'A02-EF-010'],
         'functional_exit_audit_result': 'PASS_FICTIONAL_GRADUATION_AND_NCAA_ENTRY_BASIS',
         'reason': 'E10의 가상 프렙 졸업·최종 성적표와 별도 여름 I3 full-qualifier/compliance 선택이 NCAA 진입의 근거를 이루지만 A02 회차의 여름 사건은 아니다.',
         'not_claimed': '대학 등록·실전 출전·정확 과목/점수·실제 NCAA 학생 기록 인증은 아니다.'},
    ]
    source_hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                     for p in sorted(source_paths)}
    return {
        'schema': 'A01_A02_SUBACT_EXIT_AUDIT_V1',
        'status': 'BOUNDED_FIRST_SIX_SUBACT_AUDIT_WITH_ONE_CP2_CHOICE_HOLD_AND_ONE_HANDOFF_HOLD',
        'scope': 'FIRST_SIX_CP2_FUNCTIONAL_EXITS_NOT_WHOLE_G13_OR_PUBLISHED_EPISODE_SCHEDULE',
        'counts': {'subact_exits_audited': 6, 'subact_bounded_pass': 5,
                   'subact_specific_hold': 1,
                   'act_exits_audited': 2, 'act_bounded_pass': 2,
                   'adjacent_act_handoffs_audited': 2, 'handoff_pass': 1,
                   'handoff_hold': 1, 'remaining_subact_rows_without_final_route': 36,
                   'remaining_subact_exits_not_fully_audited': 37,
                   'registered_local_functions_reused': 19,
                   'new_episode_functions_added': 0,
                   'planned_780_slots_are_mandatory_new_events': False},
        'subact_exit_rows': results, 'act_exit_rows': acts, 'act_handoffs': handoffs,
        's1_provisional_alignment_candidate': s1_alignment_candidate,
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': source_hashes,
        'mechanical_limits': [
            'Source-current record equality and anchored action/cost text guard provenance and false promotion; they cannot certify the literary meaning of a whole Act or scene.',
            'Five bounded SubAct routes pass; S1 participation/avoidance is visible but its CP2 basic-preparation choice and immediate-praise cost are not certified by E1–E2. Two bounded Act exits do not make 42 SubActs or G13 complete.',
            'The A01→A02 fictional institution bridge is selected; real school/student documents are not certified.',
            'A02→A03 remains a specific hold until college enrollment and A03-S1 exact entry are implemented after the summer certification bridge.',
        ],
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'manuscript_count': 0, 'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def render(data):
    lines = ['# A01·A02 여섯 소막 출구와 두 막 인계 감사', '',
             '**상태:** 앞 여섯 소막 중 5건은 좁은 기능 출구를 충족한다. A01-S1의 참여/회피 분리는 관측됐으나 CP2의 기본 준비 행동과 즉시 칭찬 비용은 미관측이므로 HOLD다. A01/A02 막 출구 2건을 좁게 검문했고 A02→A03 실제 진입도 HOLD다. 전체 G13·실제 회차 편성·원고 허가는 아니다.', '',
             '| 소막 | CP2 출구 | 관측 행동·비용·권한의 근거 | 남기는 경계 | 판정 |',
             '| --- | --- | --- | --- | --- |']
    for row in data['subact_exit_rows']:
        lines.append(f"| {row['subact_id']} | {row['cp2_exit_state']} | {row['observed_action_cost_authority_reason']} | {row['bounded_not_claimed']} | `{row['exit_audit_result']}` |")
    for row in data['subact_exit_rows']:
        if row['specific_gap']:
            lines.append(f"\n**{row['subact_id']} 정확한 빈칸:** {row['specific_gap']}")
    proposal = data['s1_provisional_alignment_candidate']
    lines.extend(['', '### A01-S1 잠정 CP2 표현의 국소 정렬 후보', '',
                  f"- 선택 표현: {proposal['proposed_operational_choice']}",
                  f"- 비용 표현: {proposal['proposed_operational_cost']}",
                  f"- 의미 검토: {proposal['meaning_shift_to_review']}",
                  '- 이는 운영 표현 후보이며 아직 S1 HOLD를 해소하거나 원 CP2·E1/E2·전체 기능·작가 잠금을 바꾸지 않는다.'])
    lines.extend(['', '## 막 출구와 인계', ''])
    for act in data['act_exit_rows']:
        lines.append(f"- {act['act_id']} `{act['functional_exit_audit_result']}`: {act['reason']} {act['not_claimed']}")
    for h in data['act_handoffs']:
        lines.append(f"- {h['from_act']}→{h['to_act']} `{h['handoff_audit_result']}`: {h['boundary']}")
        if h.get('specific_missing_action'):
            lines.append(f"  - 남은 정확 행동: {h['specific_missing_action']}")
    lines.extend(['', '## 범위와 다음 작업', '',
                  '- 국소 기능 19개를 재사용했고 새 회차 기능은 만들지 않았다. 기능 경로가 아직 없는 36소막과 A01-S1의 구체 빈칸 1건, 합계 37소막 출구가 미완이다. 다음 36소막은 기존 조건부 단위63을 실제 선택·비용·출구 연쇄로 투영해야 한다.',
                  '- 여름 NCAA/대학 compliance는 가상 기관 연결 경로로 선택됐지만 A02 회차의 여름 사건이 아니다. 실제 사람의 사적 학업·입학 문서와 NCAA 결정 원본을 인증하지 않는다.',
                  '- A03 등록·제한 로스터 진입과 첫 기능의 정확 진입이 남아 있다. 계획780슬롯을 새 사건780개로 채우지 않는다.',
                  '- 출구의 source-current/anchor 기계검문은 의미 전체를 인증하지 않는다. 전체 G13/G14·Context Pack·원고는 미완료, 설계/원고 게이트는 `CLOSED`.', ''])
    return '\n'.join(lines)


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError, ValueError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['audit differs from source-bound six-exit comparison']


def self_test(data):
    changes = [
        ('candidate cannot silently fill S1 hold', lambda d: d['s1_provisional_alignment_candidate'].update(currently_fills_s1_hold=True)),
        ('prepay A01 S1 choice and cost', lambda d: d['subact_exit_rows'][0].update(exit_audit_result='PASS_BOUNDED_CP2_FUNCTIONAL_EXIT', specific_gap=None)),
        ('prepay A03 handoff', lambda d: d['act_handoffs'][1].update(handoff_audit_result='PASS')),
        ('hide S1 one-day limit', lambda d: d['subact_exit_rows'][3].update(bounded_not_claimed='full lifetime habit cured')),
        ('invent 780 mandatory events', lambda d: d['counts'].update(planned_780_slots_are_mandatory_new_events=True)),
        ('claim whole G13', lambda d: d.update(whole_g13_complete=True)),
        ('claim actual Pack', lambda d: d.update(actual_context_packs=1)),
        ('open manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in changes:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, path, mutate in [
        ('E3 team reason removed', 'design/A01_E3_FINAL_EPISODE_FUNCTION.json',
         lambda x: x.update(exit_state='팀에 다시 나올 이유는 없다')),
        ('E10 admission replaced by automatic play', 'design/A02_E10_FINAL_EPISODE_FUNCTION.json',
         lambda x: x.update(exit_state='대학에 자동 등록하고 첫 공식 경기에 선발 출전했다')),
        ('F3 coach issues I-20', BRIDGE,
         lambda x: x['fictional_transition_working_path']['steps'][2].update(authority='basketball coach')),
        ('I3 summer certification made A02 event', COLLEGE,
         lambda x: x['institutional_sequence'][2].update(scope='A02_S3')),
    ]:
        def changed_load(root, requested_path):
            source = original_load(root, requested_path)
            if requested_path == path:
                source = copy.deepcopy(source)
                mutate(source)
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
    return len(changes) + 4


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors.extend(validate(saved))
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'counts': data['counts'], 'negative_controls': tested,
                      'current': not errors, 'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
