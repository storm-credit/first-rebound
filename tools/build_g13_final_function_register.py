"""Extend the preserved CP2 assignment snapshot with reviewed later functions."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import build_cp2_design_packets as base_builder
import build_a03_e1_final_episode_function as a03
import build_a03_e2_final_episode_function as a03_e2
import build_a03_e3_final_episode_function as a03_e3
import build_a04_e1_final_episode_function as a04_e1
import build_a04_e2_final_episode_function as a04_e2
import build_a04_e3_final_episode_function as a04_e3
import build_a04_e4_final_episode_function as a04_e4
import build_a04_e5_final_episode_function as a04_e5
import build_a05_final_function_batch as a05_batch
import build_a06_2020_21_finite_function_batch as a06_batch
import build_a07_finite_function_batch as a07_batch
import build_a08_finite_function_batch as a08_batch

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('control/G13_FINAL_FUNCTION_REGISTER.json')
MARKDOWN = OUTPUT.with_suffix('.md')
BASE = 'design/CP2_ACT_SUBACT_PACKET.json'
EXTENSION = str(a03.OUTPUT).replace('\\', '/')
SECOND_EXTENSION = str(a03_e2.OUTPUT).replace('\\', '/')
THIRD_EXTENSION = str(a03_e3.OUTPUT).replace('\\', '/')
FOURTH_EXTENSION = str(a04_e1.OUTPUT).replace('\\', '/')
FIFTH_EXTENSION = str(a04_e2.OUTPUT).replace('\\', '/')
SIXTH_EXTENSION = str(a04_e3.OUTPUT).replace('\\', '/')
SEVENTH_EXTENSION = str(a04_e4.OUTPUT).replace('\\', '/')
EIGHTH_EXTENSION = str(a04_e5.OUTPUT).replace('\\', '/')

def read(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))

def sha(root, path):
    return hashlib.sha256((root / path).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()

def build(root=ROOT):
    base = read(root, BASE)
    errors, old = base_builder.validate_final_functions(base, root=root)
    assert not errors, errors
    assert base['final_episode_functions_completed'] == len(old) == 19
    extra = read(root, EXTENSION)
    assert not a03.validate(extra, root=root), 'new function source-currentness failed'
    assert extra['episode_function_id'] == 'A03-EF-001'
    assert extra['final_function_order'] == 20
    assert extra['planned_allocation_slot'] == 91
    assert extra['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert extra['previous_function']['id'] == old[-1]['episode_function_id'] == 'A02-EF-010'
    assert extra['previous_function']['exact_full_exit'] == old[-1]['exit_state']
    assert extra['inter_act_bridge']['fictional_registration_completed_after_I3'] is True
    assert extra['inter_act_bridge']['I3_certification_retained'] is True
    assert extra['inter_act_bridge']['official_game_executed'] is False
    second = read(root, SECOND_EXTENSION)
    assert not a03_e2.validate(second, root=root), 'second function source-currentness failed'
    assert second['episode_function_id'] == 'A03-EF-002'
    assert second['final_function_order'] == 21 and second['planned_allocation_slot'] == 92
    assert second['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert second['previous_function']['id'] == extra['episode_function_id']
    assert second['previous_function']['exact_full_exit'] == second['entry_state'] == extra['exit_state']
    assert second['next_unit']['id'] == 'A03-F03'
    assert second['next_unit']['Texas_Tech_result_or_exact_box_prepaid'] is False
    third = read(root, THIRD_EXTENSION)
    assert not a03_e3.validate(third, root=root), 'third function source-currentness failed'
    assert third['episode_function_id'] == 'A03-EF-003'
    assert third['final_function_order'] == 22 and third['planned_allocation_slot'] == 93
    assert third['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert third['previous_function']['id'] == second['episode_function_id']
    assert third['previous_function']['exact_full_exit'] == third['entry_state'] == second['exit_state']
    assert third['whole_g13_complete'] is False and third['manuscript_allowed'] is False
    fourth = read(root, FOURTH_EXTENSION)
    assert not a04_e1.validate(fourth, root=root), 'fourth function source-currentness failed'
    assert fourth['episode_function_id'] == 'A04-EF-001'
    assert fourth['final_function_order'] == 23 and fourth['planned_allocation_slot'] == 145
    assert fourth['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert fourth['previous_function']['id'] == third['episode_function_id']
    assert fourth['previous_function']['exact_full_exit'] == fourth['entry_state'] == third['exit_state']
    assert fourth['public_history_bridge']['public_results_after_games_only'] is True
    assert fourth['cp2_provisional_entry_inherited_as_actual_belief'] is False
    assert fourth['whole_g13_complete'] is False and fourth['manuscript_allowed'] is False
    fifth = read(root, FIFTH_EXTENSION)
    assert not a04_e2.validate(fifth, root=root), 'fifth function source-currentness failed'
    assert fifth['episode_function_id'] == 'A04-EF-002'
    assert fifth['final_function_order'] == 24 and fifth['planned_allocation_slot'] == 146
    assert fifth['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert fifth['previous_function']['id'] == fourth['episode_function_id']
    assert fifth['previous_function']['exact_full_exit'] == fifth['entry_state'] == fourth['exit_state']
    assert fifth['whole_g13_complete'] is False and fifth['manuscript_allowed'] is False
    assert fifth['bounded_A04_S1_preparation_criterion_observed'] is True
    assert fifth['bounded_A04_S1_preparation_audit']['actual_sample_sent_to_evaluator_or_official_measurement_certified'] is False
    sixth = read(root, SIXTH_EXTENSION)
    assert not a04_e3.validate(sixth, root=root), 'sixth function source-currentness failed'
    assert sixth['episode_function_id'] == 'A04-EF-003'
    assert sixth['final_function_order'] == 25 and sixth['planned_allocation_slot'] == 147
    assert sixth['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
    assert sixth['previous_function']['id'] == fifth['episode_function_id']
    assert sixth['previous_function']['exact_full_exit'] == sixth['entry_state'] == fifth['exit_state']
    assert sixth['source_conditional_functions'] == ['A04-CF03', 'A04-CF04']
    assert sixth['local_blueprint']['CF03_first_attempt_is_prerequisite_not_separate_event'] is True
    assert sixth['whole_g13_complete'] is False and sixth['manuscript_allowed'] is False
    seventh = read(root, SEVENTH_EXTENSION)
    assert not a04_e4.validate(seventh, root=root), 'seventh function source-currentness failed'
    assert seventh['episode_function_id'] == 'A04-EF-004'
    assert seventh['final_function_order'] == 26 and seventh['planned_allocation_slot'] == 148
    assert seventh['previous_function']['id'] == sixth['episode_function_id']
    assert seventh['previous_function']['exact_full_exit'] == seventh['entry_state'] == sixth['exit_state']
    assert seventh['internal_order'] == ['C0', 'C1', 'C2']
    assert seventh['next_unit']['Asian_Games_nonparticipation_choice_prepaid_by_E4'] is False
    eighth = read(root, EIGHTH_EXTENSION)
    assert not a04_e5.validate(eighth, root=root), 'eighth function source-currentness failed'
    assert eighth['episode_function_id'] == 'A04-EF-005'
    assert eighth['final_function_order'] == 27 and eighth['planned_allocation_slot'] == 149
    assert eighth['previous_function']['id'] == seventh['episode_function_id']
    assert eighth['previous_function']['exact_full_exit'] == eighth['entry_state'] == seventh['exit_state']
    assert eighth['internal_order'] == ['S1', 'S2']
    assert eighth['next_unit']['rookie_minutes_or_starter_right_prepaid'] is False
    a05_paths = [str(p).replace('\\', '/') for p in a05_batch.OUTPUTS]
    a05_records = [read(root, path) for path in a05_paths]
    assert not a05_batch.validate_all(a05_records, root=root), 'A05 batch source-currentness failed'
    assert a05_records[0]['previous_function']['exact_full_exit'] == a05_records[0]['entry_state'] == eighth['exit_state']
    assert a05_records[0]['previous_function']['id'] == eighth['episode_function_id']
    assert [r['episode_function_id'] for r in a05_records] == [f'A05-EF-{i:03}' for i in range(1,5)]
    assert [r['source_conditional_functions'] for r in a05_records] == [['A05-CF01'], ['A05-CF02','A05-CF03'], ['A05-CF04','A05-CF05','A05-CF06'], ['A05-CF07','A05-CF08']]
    assert all(a05_records[i]['previous_function']['exact_full_exit'] == a05_records[i]['entry_state'] == a05_records[i-1]['exit_state'] for i in (1,2,3))
    assert a05_records[-1]['next_unit']['id'] == 'A06-S1'
    assert a05_records[2]['conditional_NBA_return']['selected_fictional_operating_condition_within_existing_rookie_role_line'] is True
    a06_path = str(a06_batch.OUTPUT).replace('\\', '/')
    a06 = read(root, a06_path)
    assert not a06_batch.validate(a06, root=root), 'A06 batch must be source-current'
    assert a06['status'] == 'FIVE_LOCAL_FINAL_FUNCTIONS_INDEPENDENTLY_REVIEWED'
    assert a06['independent_review_completed'] is True
    assert a06['previous_function']['exact_full_exit'] == a05_records[-1]['exit_state']
    a06_records=[]
    for i, row in enumerate(a06['functions']):
        assert row['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
        projected = dict(row, episode_function_id=row['id'], final_function_order=row['global_function_order'],
                         act='A06', whole_g13_complete=a06['whole_g13_complete'],
                         manuscript_allowed=a06['manuscript_allowed'], batch_record_pointer=f'/functions/{i}')
        a06_records.append(projected)
    assert [r['episode_function_id'] for r in a06_records] == [f'A06-EF-{i:03}' for i in range(1,6)]
    assert a06_records[0]['entry_state'] == a05_records[-1]['exit_state']
    assert all(a06_records[i]['entry_state'] == a06_records[i-1]['exit_state'] for i in range(1,5))
    all_records = old + [extra, second, third, fourth, fifth, sixth, seventh, eighth] + a05_records + a06_records
    extension_paths = [EXTENSION, SECOND_EXTENSION, THIRD_EXTENSION, FOURTH_EXTENSION, FIFTH_EXTENSION, SIXTH_EXTENSION, SEVENTH_EXTENSION, EIGHTH_EXTENSION] + a05_paths + [a06_path]*5
    for builder, act, first_order, first_slot in [(a07_batch,'A07',37,323),(a08_batch,'A08',40,383)]:
        path = str(builder.OUTPUT).replace('\\', '/')
        batch = read(root, path)
        assert not builder.validate(batch, root=root), f'{act} batch must be source-current'
        assert batch['status'] == 'THREE_LOCAL_FINAL_FUNCTIONS_INDEPENDENTLY_REVIEWED'
        assert batch['independent_review_completed'] is True and len(batch['functions']) == 3
        assert batch['previous_function']['id'] == all_records[-1]['episode_function_id']
        assert batch['previous_function']['exact_full_exit'] == all_records[-1]['exit_state']
        for i, row in enumerate(batch['functions']):
            assert row['id'] == f'{act}-EF-{i+1:03}'
            assert row['global_function_order'] == first_order+i
            assert row['planned_allocation_slot'] == first_slot+i
            assert row['status'] == 'FINAL_EPISODE_FUNCTION_LOCAL_COMPLETE'
            assert row['entry_state'] == all_records[-1]['exit_state']
            all_records.append(dict(row, episode_function_id=row['id'], final_function_order=row['global_function_order'],
                                    act=act, whole_g13_complete=batch['whole_g13_complete'],
                                    manuscript_allowed=batch['manuscript_allowed'], batch_record_pointer=f'/functions/{i}'))
            extension_paths.append(path)
    paths = base['final_episode_function_paths'] + extension_paths
    assert len(paths) == 42 and len(set(paths)) == 34
    assert len({(p,d.get('batch_record_pointer','')) for p,d in zip(paths,all_records)}) == 42
    assert [d['final_function_order'] for d in all_records] == list(range(1,43))
    slots = [d['planned_allocation_slot'] for d in all_records]
    assert len(slots) == len(set(slots)) == 42
    subacts = {s['id']: s for s in base['subacts']}
    acts = {a['id']: a for a in base['acts']}
    rows=[]
    for path,d in zip(paths,all_records):
        sid = d.get('primary_subact',d.get('subact'))
        assert sid in subacts and subacts[sid]['parent_act'] == d['act']
        assert acts[d['act']]['allocation_start'] <= d['planned_allocation_slot'] <= acts[d['act']]['allocation_end']
        assert d['whole_g13_complete'] is False and d['manuscript_allowed'] is False
        rows.append({'id':d['episode_function_id'],'path':path,'order':d['final_function_order'],
                     'planned_slot':d['planned_allocation_slot'],'act':d['act'],'subact':sid,
                     'exact_entry':d.get('entry_state',d.get('entry_after_fictional_bridge')),
                     'exact_exit':d['exit_state']})
        if 'batch_record_pointer' in d: rows[-1]['record_pointer']=d['batch_record_pointer']
        assert isinstance(rows[-1]['exact_entry'],str) and rows[-1]['exact_entry']
    per_act=dict(Counter(d['act'] for d in rows))
    assert per_act == {'A01':9,'A02':10,'A03':3,'A04':5,'A05':4,'A06':5,'A07':3,'A08':3}
    source_paths=['tools/build_g13_final_function_register.py',BASE,
                  'tools/build_cp2_design_packets.py','tools/build_a03_e1_final_episode_function.py',
                  'tools/build_a03_e2_final_episode_function.py',
                  'tools/build_a03_e3_final_episode_function.py',
                  'tools/build_a04_e1_final_episode_function.py',
                  'tools/build_a04_e2_final_episode_function.py',
                  'tools/build_a04_e3_final_episode_function.py',
                  'tools/build_a04_e4_final_episode_function.py',
                  'tools/build_a04_e5_final_episode_function.py',
                  'tools/build_a05_final_function_batch.py','tools/build_a06_2020_21_finite_function_batch.py',
                  'tools/build_a07_finite_function_batch.py','tools/build_a08_finite_function_batch.py',*paths]
    source_paths=list(dict.fromkeys(source_paths))
    return {
        'schema':'G13_CUMULATIVE_FINAL_FUNCTION_REGISTER_V1',
        'status':'SOURCE_CURRENT_LOCAL_FUNCTIONS_NOT_WHOLE_G13',
        'base_snapshot':{'path':BASE,'registered_functions':19,'preserved_without_edit':True},
        'extension_function_paths':extension_paths,
        'counts':{'registered_local_functions':42,'per_act':per_act,
                  'subacts_with_verified_local_function_route':len({d['subact'] for d in rows}),
                  'subacts_without_verified_local_function_route':42-len({d['subact'] for d in rows}),
                  'planned_allocation_slots':780,'unassigned_planned_slots':738,
                  'planned_slots_are_mandatory_new_events':False,'final_published_episode_count':None},
        'functions':rows,
        'historical_comparison_rule':'The preserved CP2/first-six audit snapshot remains19. This cumulative registry explicitly validates that prefix and the reviewed A03 extension, and is the current local assignment count. Whole exits and history locks are separate gates.',
        'a02_to_a03_exact_local_handoff_verified':True,
        'a03_e1_to_e2_exact_local_handoff_verified':True,
        'a03_e2_to_e3_exact_local_handoff_verified':True,
        'a03_e3_to_a04_e1_handoff_with_public_history_verified':True,
        'a04_e1_to_e2_personal_preparation_handoff_verified':True,
        'a04_e2_to_e3_single_coached_workout_handoff_verified':True,
        'a04_e3_to_e4_conditional_contact_handoff_verified':True,
        'a04_e4_to_e5_approved_summer_choice_handoff_verified':True,
        'a04_e5_to_a05_four_function_batch_handoff_verified':True,
        'a05_e4_to_a06_five_function_batch_handoff_verified':True,
        'a06_e5_to_a07_three_function_batch_handoff_verified':True,
        'a07_e3_to_a08_three_function_batch_handoff_verified':True,
        'a08_practice_route_does_not_certify_CF03_NBA_trial_or_whole_S2':True,
        'batch_record_resolution':'For a row with record_pointer, read its path then apply JSON Pointer to select that specific function; A06/A07/A08 each have multiple distinct records in one batch file.',
        'whole_subact_or_act_exit_promoted_by_this_register':False,
        'whole_g13_complete':False,'whole_g14_complete':False,'actual_context_packs':0,
        'manuscript_count':0,'manuscript_allowed':False,'design_gate':'CLOSED','author_locked':False,
        'source_rev_convention':'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256':{p:sha(root,p) for p in source_paths},
    }

def render(d):
    lines=['# G13 현재 국소 기능 누적 등록', '',
           '원 CP2의19개 등록 스냅샷을 보존하고 A03/A04의8개 producer·A05~A08 일괄 producer를 실제 검문하여 현재 누적42개를 연결한다. 전체 G13 완료나 출판42회차 확정이 아니다.', '',
           '- 현재 배정: A01 9·A02 10·A03 3·A04 5·A05 4·A06 5·A07 3·A08 3, 합계42. 기능 경로가 있는 소막24·없는 소막18. A06/A07/A08 기능은 파일과 각각의 JSON Pointer로 구분한다.',
           '- 원19개의 순서·계획slot·파일을 보존한다. A03-EF-001은 전역 순서20/계획slot91이며, 앞 막의 미사용 계획slot을 새 사건으로 채울 의무는 없다.',
           '- A02 E10 정확출구→별도 여름I3→가상 대학등록/연습 접근→A03 첫 연습/영상/좁은과제 선택을 연결했다. 공식경기·주전·분·신뢰·소막전체출구를 선지급하지 않는다.',
           '- A03 E1 정확출구→E2 다음 허용 연습의 두 박스아웃과 동료 공 확보를 연결한다. E2는 전역순서21/계획slot92이며 소막별 균등배정이나 실제 경기 기록을 뜻하지 않는다.',
           '- E2 정확출구→E3 Texas Tech의 검토된 가상11분 창·맡은 수비 선택·동료 공 확보 한 번을 연결한다. 전역순서22/계획slot93이다. 실제 포제션·대체 박스/점수·3월25일 우승·후속 프로평가는 인증하지 않는다.',
           '- E3 정확출구→별도3/31·4/2 공개 역사→A04 E1 개인 준비의 역할 증거/공격 미검증 자료를 연결한다. 전역순서23/계획slot145이며 공식 측정·구단 보드·지명·전체A03/A04 출구를 선지급하지 않는다.',
           '- A04 E1 정확출구→E2 빈 신체 항목표·숫자 없는 개인 예행·훈련 시간 비용을 연결한다. 전역순서24/계획slot146이며 공식 초청·측정·의료·워크아웃이나 전체S1 종료를 인증하지 않는다.',
           '- E2 정확출구→E3 첫 공격의 정지·개인 지도자의 한정 지시·무수비 단순 패스 재시도를 한 세션/한 기능으로 연결한다. 전역순서25/계획slot147이며 CF03/04를 별도 사건2개로 세지 않는다. NBA 평가·실전 숙련·CF05 연락·전체S1/Act를 인증하지 않는다.',
           '- E3 정확출구→E4 승인된 Chicago 진입 방향 뒤의 가상 안내·미확인 기관 항목 질문을 연결한다. 전역순서26/계획slot148이며 CF06 여름 선택·실제 서명·의료·주전 약속을 선지급하지 않는다.',
           '- E4 정확출구→E5 Chicago 준비를 택하는 승인된 여름 시간 선택을 연결한다. 전역순서27/계획slot149이며 이미 얻은 국가대표 자리를 포기한 사건이 아니다. A05 역할·분·성과는 미실행이다.',
           '- A04 E5 정확출구→A05의 네 기능군 R1 역할시도·R2 단 한 번의 밤샘/기회상실/다음준비·R3 별도 개발과 조건부 NBA 재시험·R4 2년차 약한손/조기이양을 연결한다. 전역순서28–31/계획slot157–160이다. 기존8인과를 네 기능으로 묶으며 새 날짜·개인분·경기결과·전체A05 출구를 확정하지 않는다.',
           '- A05 E4 정확출구→A06의 시작권/무볼·전진/숏롤 첫패스·Theis/Green 과제·선택된WAS승·IND패/다음과제 다섯 기능을 연결한다. 전역순서32–36/계획slot249–253이다. S2 시즌 실행을 재사용하며 개인 박스·임상·다음여름 계약·기술 완성을 선지급하지 않는다.',
           '- A06 E5 정확출구→A07 좁은 엘보 훈련 허용·두 수비 도착 조건의 실패/수정·좋은 표본과 실패를 함께 에이전트에게 넘기는 세 기능37–39/계획slot323–325를 연결한다. M1 조건부164행의 역할을 보존하며 날짜별 경기·효율·계약 답은 인증하지 않는다.',
           '- A07 E3 정확출구→A08 개인요구/동료 기능비용 질문·가상 훈련의 첫 반환 차단/안전재전개·이양 뒤 재관여 세 기능40–42/계획slot383–385를 연결한다. CF03 실제 NBA 시험/전체S2 및 계약·공동 에이스/전체Act는 HOLD로 남긴다.',
           '- 원 CP2/첫6 감사의19 계수는 과거 스냅샷이다. 현재 누적 계수는 이 등록기를 참조한다. 전체 역사·출구·Context Pack 게이트는 별도로 남는다.', '',
           '| 순서 | 기능 | 막/소막 | 계획slot |','|---|---|---|---|']
    lines += [f"| {r['order']} | {r['id']} | {r['act']}/{r['subact']} | {r['planned_slot']} |" for r in d['functions']]
    lines += ['', '전체G13/G14 미완료·실제Pack0·원고0·설계/원고CLOSED.', '']
    return '\n'.join(lines)

def validate(d,root=ROOT):
    try: expected=build(root)
    except (AssertionError,KeyError,ValueError,OSError,TypeError) as exc: return [f'source construction: {exc}']
    return [] if d==expected else ['cumulative register differs from validated prefix and extension']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true')
    args=p.parse_args();d=build()
    if args.write:
        (ROOT/OUTPUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (ROOT/MARKDOWN).write_text(render(d),encoding='utf-8')
    errors=validate(d)
    if args.check:
        saved=read(ROOT,OUTPUT);errors+=validate(saved)
        if (ROOT/MARKDOWN).read_text(encoding='utf-8-sig')!=render(saved): errors.append('Markdown not synchronized')
    print(json.dumps({'current':not errors,'counts':d['counts'],'errors':errors},ensure_ascii=False))
    if errors: raise SystemExit(1)

if __name__=='__main__': main()
