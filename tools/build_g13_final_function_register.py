"""Extend the preserved CP2 assignment snapshot with reviewed later functions."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import build_cp2_design_packets as base_builder
import build_a03_e1_final_episode_function as a03

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('control/G13_FINAL_FUNCTION_REGISTER.json')
MARKDOWN = OUTPUT.with_suffix('.md')
BASE = 'design/CP2_ACT_SUBACT_PACKET.json'
EXTENSION = str(a03.OUTPUT).replace('\\', '/')

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
    all_records = old + [extra]
    paths = base['final_episode_function_paths'] + [EXTENSION]
    assert len(paths) == len(set(paths)) == 20
    assert [d['final_function_order'] for d in all_records] == list(range(1,21))
    slots = [d['planned_allocation_slot'] for d in all_records]
    assert len(slots) == len(set(slots)) == 20
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
    assert per_act == {'A01':9,'A02':10,'A03':1}
    source_paths=['tools/build_g13_final_function_register.py',BASE,
                  'tools/build_cp2_design_packets.py','tools/build_a03_e1_final_episode_function.py',*paths]
    return {
        'schema':'G13_CUMULATIVE_FINAL_FUNCTION_REGISTER_V1',
        'status':'SOURCE_CURRENT_LOCAL_FUNCTIONS_NOT_WHOLE_G13',
        'base_snapshot':{'path':BASE,'registered_functions':19,'preserved_without_edit':True},
        'extension_function_paths':[EXTENSION],
        'counts':{'registered_local_functions':20,'per_act':per_act,
                  'subacts_with_verified_local_function_route':len({d['subact'] for d in rows}),
                  'subacts_without_verified_local_function_route':42-len({d['subact'] for d in rows}),
                  'planned_allocation_slots':780,'unassigned_planned_slots':760,
                  'planned_slots_are_mandatory_new_events':False,'final_published_episode_count':None},
        'functions':rows,
        'historical_comparison_rule':'The preserved CP2/first-six audit snapshot remains19. This cumulative registry explicitly validates that prefix and the reviewed A03 extension, and is the current local assignment count. Whole exits and history locks are separate gates.',
        'a02_to_a03_exact_local_handoff_verified':True,
        'whole_subact_or_act_exit_promoted_by_this_register':False,
        'whole_g13_complete':False,'whole_g14_complete':False,'actual_context_packs':0,
        'manuscript_count':0,'manuscript_allowed':False,'design_gate':'CLOSED','author_locked':False,
        'source_rev_convention':'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256':{p:sha(root,p) for p in source_paths},
    }

def render(d):
    lines=['# G13 현재 국소 기능 누적 등록', '',
           '원 CP2의19개 등록 스냅샷을 보존하고 해당 producer19개와 A03의 새 기능 producer를 실제 검문하여 현재 누적20개를 연결한다. 전체 G13 완료나 출판20회차 확정이 아니다.', '',
           '- 현재 배정: A01 9·A02 10·A03 1, 합계20. 기능 경로가 있는 소막7·없는 소막35.',
           '- 원19개의 순서·계획slot·파일을 보존한다. A03-EF-001은 전역 순서20/계획slot91이며, 앞 막의 미사용 계획slot을 새 사건으로 채울 의무는 없다.',
           '- A02 E10 정확출구→별도 여름I3→가상 대학등록/연습 접근→A03 첫 연습/영상/좁은과제 선택을 연결했다. 공식경기·주전·분·신뢰·소막전체출구를 선지급하지 않는다.',
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
