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

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('control/G13_FINAL_FUNCTION_REGISTER.json')
MARKDOWN = OUTPUT.with_suffix('.md')
BASE = 'design/CP2_ACT_SUBACT_PACKET.json'
EXTENSION = str(a03.OUTPUT).replace('\\', '/')
SECOND_EXTENSION = str(a03_e2.OUTPUT).replace('\\', '/')
THIRD_EXTENSION = str(a03_e3.OUTPUT).replace('\\', '/')
FOURTH_EXTENSION = str(a04_e1.OUTPUT).replace('\\', '/')

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
    all_records = old + [extra, second, third, fourth]
    paths = base['final_episode_function_paths'] + [EXTENSION, SECOND_EXTENSION, THIRD_EXTENSION, FOURTH_EXTENSION]
    assert len(paths) == len(set(paths)) == 23
    assert [d['final_function_order'] for d in all_records] == list(range(1,24))
    slots = [d['planned_allocation_slot'] for d in all_records]
    assert len(slots) == len(set(slots)) == 23
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
        assert isinstance(rows[-1]['exact_entry'],str) and rows[-1]['exact_entry']
    per_act=dict(Counter(d['act'] for d in rows))
    assert per_act == {'A01':9,'A02':10,'A03':3,'A04':1}
    source_paths=['tools/build_g13_final_function_register.py',BASE,
                  'tools/build_cp2_design_packets.py','tools/build_a03_e1_final_episode_function.py',
                  'tools/build_a03_e2_final_episode_function.py',
                  'tools/build_a03_e3_final_episode_function.py',
                  'tools/build_a04_e1_final_episode_function.py',*paths]
    return {
        'schema':'G13_CUMULATIVE_FINAL_FUNCTION_REGISTER_V1',
        'status':'SOURCE_CURRENT_LOCAL_FUNCTIONS_NOT_WHOLE_G13',
        'base_snapshot':{'path':BASE,'registered_functions':19,'preserved_without_edit':True},
        'extension_function_paths':[EXTENSION, SECOND_EXTENSION, THIRD_EXTENSION, FOURTH_EXTENSION],
        'counts':{'registered_local_functions':23,'per_act':per_act,
                  'subacts_with_verified_local_function_route':len({d['subact'] for d in rows}),
                  'subacts_without_verified_local_function_route':42-len({d['subact'] for d in rows}),
                  'planned_allocation_slots':780,'unassigned_planned_slots':757,
                  'planned_slots_are_mandatory_new_events':False,'final_published_episode_count':None},
        'functions':rows,
        'historical_comparison_rule':'The preserved CP2/first-six audit snapshot remains19. This cumulative registry explicitly validates that prefix and the reviewed A03 extension, and is the current local assignment count. Whole exits and history locks are separate gates.',
        'a02_to_a03_exact_local_handoff_verified':True,
        'a03_e1_to_e2_exact_local_handoff_verified':True,
        'a03_e2_to_e3_exact_local_handoff_verified':True,
        'a03_e3_to_a04_e1_handoff_with_public_history_verified':True,
        'whole_subact_or_act_exit_promoted_by_this_register':False,
        'whole_g13_complete':False,'whole_g14_complete':False,'actual_context_packs':0,
        'manuscript_count':0,'manuscript_allowed':False,'design_gate':'CLOSED','author_locked':False,
        'source_rev_convention':'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256':{p:sha(root,p) for p in source_paths},
    }

def render(d):
    lines=['# G13 현재 국소 기능 누적 등록', '',
           '원 CP2의19개 등록 스냅샷을 보존하고 해당 producer19개와 A03/A04의 새 기능 producer4개를 실제 검문하여 현재 누적23개를 연결한다. 전체 G13 완료나 출판23회차 확정이 아니다.', '',
           '- 현재 배정: A01 9·A02 10·A03 3·A04 1, 합계23. 기능 경로가 있는 소막10·없는 소막32.',
           '- 원19개의 순서·계획slot·파일을 보존한다. A03-EF-001은 전역 순서20/계획slot91이며, 앞 막의 미사용 계획slot을 새 사건으로 채울 의무는 없다.',
           '- A02 E10 정확출구→별도 여름I3→가상 대학등록/연습 접근→A03 첫 연습/영상/좁은과제 선택을 연결했다. 공식경기·주전·분·신뢰·소막전체출구를 선지급하지 않는다.',
           '- A03 E1 정확출구→E2 다음 허용 연습의 두 박스아웃과 동료 공 확보를 연결한다. E2는 전역순서21/계획slot92이며 소막별 균등배정이나 실제 경기 기록을 뜻하지 않는다.',
           '- E2 정확출구→E3 Texas Tech의 검토된 가상11분 창·맡은 수비 선택·동료 공 확보 한 번을 연결한다. 전역순서22/계획slot93이다. 실제 포제션·대체 박스/점수·3월25일 우승·후속 프로평가는 인증하지 않는다.',
           '- E3 정확출구→별도3/31·4/2 공개 역사→A04 E1 개인 준비의 역할 증거/공격 미검증 자료를 연결한다. 전역순서23/계획slot145이며 공식 측정·구단 보드·지명·전체A03/A04 출구를 선지급하지 않는다.',
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
