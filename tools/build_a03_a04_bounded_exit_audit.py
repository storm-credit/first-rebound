"""Audit existing college and draft witnesses without adding a scene or episode."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_a03_a04_bounded_exit_audit.py'
OUT='design/A03_A04_BOUNDED_EXIT_AUDIT_2026_10_07.json'
CP2_CONSUMED_MEANING_SHA='12aeccd49af3e1d35c1efcc42805334f7569ca1e214603257880fd87ae23e42b'
SOURCES=[SELF,'design/CP2_ACT_SUBACT_PACKET.json','design/A03_COLLEGE_ENTRY_WORKING_MODEL_2026_10_07.json',
 *[f'design/A03_E{i}_FINAL_EPISODE_FUNCTION.json' for i in range(1,4)],
 'design/A03_POST_TOURNAMENT_HISTORY_BRIDGE_2026_10_07.json',
 'design/A04_S1_EXTERNAL_PRESENTATION_EXIT_ADDENDUM_2026_10_07.json',
 'design/A04_S1_EXTERNAL_PRESENTATION_WORKING_MODEL_2026_10_07.json',
 'design/A04_S2_S3_OPERATING_EXIT_AUDIT_2026_10_07.json','canon/CAREER_TIMELINE.md']
def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def load(p):return json.loads(text(p))
def build():
 cp=load(SOURCES[1]);sub={r['id']:r for r in cp['subacts']}
 submeaning=[{k:r[k] for k in ['id','entry_state','choice','cost','exit_state']} for r in cp['subacts'] if r['parent_act'] in ['A03','A04']]
 actmeaning=[{k:r[k] for k in ['id','choice','cost','exit_state']} for r in cp['acts'] if r['id'] in ['A03','A04']]
 digest=hashlib.sha256(json.dumps({'subacts':submeaning,'acts':actmeaning},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
 assert digest==CP2_CONSUMED_MEANING_SHA,'Reviewed original choice/cost/exit criteria changed; labels cannot be inherited'
 e=[load(f'design/A03_E{i}_FINAL_EPISODE_FUNCTION.json') for i in range(1,4)]
 assert [r['episode_function_id'] for r in e]==['A03-EF-001','A03-EF-002','A03-EF-003']
 assert e[1]['entry_state']==e[0]['exit_state'] and e[2]['entry_state']==e[1]['exit_state']
 bridge=load(SOURCES[6]);presentation=load(SOURCES[8]);addendum=load(SOURCES[7])
 assert bridge['previous_function']['exact_full_exit']==e[2]['exit_state']
 assert bridge['official_public_sequence'][0]['title_won_on_this_date'] is False
 assert presentation['independent_review_completed'] is True
 assert presentation['new_final_episode_functions']==0 and presentation['NBA_club_submission_or_grade'] is False
 assert addendum['dimensions']['literal_present_to_external_evaluation']=='PASS_FICTIONAL_NON_NBA_OBSERVER_RECEIVES_AND_SEES_LIMITS'
 assert '32~36경기, 선발 0회' in text('canon/CAREER_TIMELINE.md')
 rows=[
 {'id':'A03-S1','result':'BOUNDED_PASS','witness':['A03-EF-001'],'reason':'가상 등록·제한 연습 뒤 더 많은 분 대신 좁은 도움 위치 과제를 수락하고 영상·준비 시간을 지불한다. 우승팀 소속이면 개인능력이 충분하다는 옛 진입을 믿음으로 상속하지 않는다.'},
 {'id':'A03-S2','result':'HOLD_ONE_OBSERVABLE_TEAMMATE_ASSIGNMENT','witness':['A03-EF-002','A03-EF-003'],'reason':'두 연습의 동료 공 확보와 Texas Tech의 맡은 수비 수행은 있다. 그러나 원 출구의 동료가 맡기는 기능을 직접 보여 주는 다음 좁은 요청/재배정 관측은 현재 세 기능에 명시되지 않았다. 이를 팀 속마음이나 시즌 전체 무오류로 증명할 필요는 없다.'},
 {'id':'A03-S3','result':'BOUNDED_PASS_RETROSPECTIVE_A04_HANDOFF','witness':['A03-EF-003','A03_POST_TOURNAMENT_HISTORY_BRIDGE','A04_S1_EXTERNAL_PRESENTATION'],'reason':'Texas Tech 한정 기여·4/2 이후 기존 우승팀 소속·미증명 개인 공격을 분리한 자료가 이후 비공식 외부 상담자에게 제시되었다. E3 또는3/25 당시 프로평가 완료로 소급하지 않는다. 실제 스카우트등급·주인공 우승MVP·후속포제션은 인증하지 않는다.'},
 {'id':'A04-S1','result':'BOUNDED_PASS','witness':['A04_S1_EXTERNAL_PRESENTATION_EXIT_ADDENDUM'],'reason':'개인 준비와 별도 비공식 외부 제시를 합쳐 표본·약점 노출을 관측했다. 공식 NBA접수·의료·순번은 아니다.'},
 {'id':'A04-S2','result':'BOUNDED_PASS','witness':['A04-EF-004','A04_S2_S3_OPERATING_EXIT_AUDIT'],'reason':'승인 Chicago 방향의 가상 준비 안내에서 일반 절차와 기관이 아직 확인하지 않은 항목을 구분했다. 계약 서명이나 주전 약속은 받지 않았다.'},
 {'id':'A04-S3','result':'BOUNDED_PASS','witness':['A04-EF-005','A04_S2_S3_OPERATING_EXIT_AUDIT'],'reason':'이미 승인된 Chicago 루키 여름 준비를 택하고 아시안게임 경로를 추진하지 않는다. 실제 확보한 국가대표 자리를 포기했다고 바꾸지 않는다.'}]
 for row in rows:
  row['original_choice']=sub[row['id']]['choice'];row['original_cost']=sub[row['id']]['cost'];row['original_exit']=sub[row['id']]['exit_state']
 return {'schema':'A03_A04_BOUNDED_EXIT_AUDIT_V1','status':'INDEPENDENTLY_REVIEWED_BOUNDED_EXIT_AUDIT','baseline_main':'e8070d14e7cfa43eab17c7e1cf62c5cbc71bba85',
 'rows':rows,'counts':{'subacts':6,'bounded_pass':5,'specific_hold':1,'new_functions':0,'new_slots':0},
 'act_results':{'A03':'HOLD_ONE_OBSERVABLE_TEAMMATE_ASSIGNMENT','A04':'HOLD_INSTITUTIONAL_CONTRACT_DEVELOPMENT_RESPONSIBILITY_WITNESS'},
 'A04_finite_gap':'가상 안내를 받은 E4/E5는 실제 기관이 계약·개발 책임을 맡았다는 운영 관측과 다르다. 승인된 Chicago 1R 표준계약 방향 안에서 정확순번/사적급여를 확정하지 않는 적법 계약가족·소속등록/개발과제 전달 증인이 필요하다. 새주전/보장분은 필요없다.',
 'time_firewall':'A03-S3 자료의 외부 제시 완료 증인은 이후 A04에서 관측된다. A03-E3 출구나4/2 이전에 NBA평가를 미리 받았다는 사건이 아니다.',
 'college_relative_order':{'chain':['2017 summer I3/I4','A03-EF-001','A03-EF-002','A03-EF-003 2018-03-25'], 'basis':'E1 receives cleared college entry; E2 exact entry equals E1 exit; E3 exact entry equals E2 exit. The two practices precede the anchored tournament window by this existing narrative partial order.','new_exact_practice_date_or_schedule_receipt_required':False},
 'scope':'Existing local choices and observable exits only; college scope gate and completed public sources are preserved; no forty-game reopening or private receipt prerequisite.',
 'peer_review_completed':True,'whole_G13_complete':False,'whole_G14_complete':False,'actual_context_packs':0,'new_author_lock':False,'manuscript_allowed':False,'design_gate':'CLOSED',
 'source_sha256':{p:hashlib.sha256(text(p).encode()).hexdigest() for p in SOURCES}}
def render(o):
 lines=['# A03·A04 한정 출구 대조','',o['status'],'','기존 대학·드래프트 기능과 이후 관측을 대조한다. 새 회차·슬롯·원고를 만들지 않는다.','', '| 소막 | 판정 | 직접 증인과 한계 |','|---|---|---|']
 lines += [f"| {r['id']} | {r['result']} | {r['reason']} |" for r in o['rows']]
 lines += ['', 'A03 전체에는 동료의 다음 좁은 수비 요청/재배정 관측1건이 남는다. A04 전체에는 안내와 구별되는 기관의 계약·개발 책임 운영 증인이 남는다.', '',o['time_firewall'],'',o['A04_finite_gap'],'', '한정 소막5PASS/1HOLD·전체 두Act 미완료. [전체7행 현황](WORLD_BIBLE_COMPLETION_ROADMAP.md)과 [현재기능등록](../control/G13_FINAL_FUNCTION_REGISTER.md)을 참조한다. 미완료큰묶음5·6번까지4·v0.30 PARTIAL·실제Pack0·원고0·설계/원고CLOSED.','']
 return '\n'.join(lines)
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');args=a.parse_args();o=build()
 if args.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/OUT[:-5]).with_suffix('.md').write_text(render(o),encoding='utf8')
 if args.check:assert load(OUT)==o;assert text(OUT[:-5]+'.md')==render(o)
 print(json.dumps(o['counts']))
if __name__=='__main__':main()
