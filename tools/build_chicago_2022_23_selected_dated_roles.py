"""Consume root-reviewed H22 recommendation without rewriting its pending snapshot."""
from __future__ import annotations
import argparse,copy,hashlib,json
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_23_selected_dated_roles.py'
OUT='simulation/CHICAGO_2022_23_SELECTED_DATED_ROLES.json'
MD=OUT.replace('.json','.md')
CANON='canon/DELEGATED_CHICAGO_2022_23_HEALTH_ROLES_2026_10_08.json'
FAMILY='simulation/CHICAGO_2022_23_DATED_ROLE_FAMILY.json'
REVIEW='reviews/CHICAGO_2022_23_DATED_ROLE_FAMILY_ROOT_INDEPENDENT_REVIEW_2026_10_08.json'
ROOKIE_CANON='canon/DELEGATED_2022_DRAFT_AND_CHICAGO_ROOKIE_DECISION_2026_10_08.json'
AUTH='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
PINS={'simulation/CHICAGO_2022_23_DATED_ROLE_FAMILY.json': 'db2d4456e11d0d6c96ef1181f68e43ad34a5c17d1c656a934326864c9579a719', 'reviews/CHICAGO_2022_23_DATED_ROLE_FAMILY_ROOT_INDEPENDENT_REVIEW_2026_10_08.json': '51da4f6eacff419f081f6e888b2b361e2f918659676d742c9be4f110d16847a7', 'canon/DELEGATED_2022_DRAFT_AND_CHICAGO_ROOKIE_DECISION_2026_10_08.json': 'a32dfc265a7250bc89df366c14b43444645438675674f4be66feda2b6a053eba', 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md': '91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d'}
BASELINE='ee0ff822aa127f8263cc69e03ba2a7184053e22e'

def norm(s):return s.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def text(p):return norm((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def data_sha(x):return hashlib.sha256(dump(x).encode()).hexdigest()
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned source changed: '+p
    return {p:json.loads(text(p)) for p in [FAMILY,REVIEW,ROOKIE_CANON]}
def inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Supplied source differs from pinned physical snapshot'
    f=s[FAMILY];r=s[REVIEW];c=s[ROOKIE_CANON]
    for p,h in f['source_sha256'].items():assert sha(p)==h,'Reviewed family upstream source changed: '+p
    for p,h in r['source_sha256'].items():assert sha(p)==h,'Review evidence changed: '+p
    assert r['verdict']=='ACCEPTED_82_DATE_ROLE_AVAILABILITY_RECOMMENDATION_NOT_RESULTS'
    assert r['independent_review_completed'] is True and r['current_source_certified'] is True
    assert f['summary']['published_date_keys']==82 and f['summary']['clock_template_blocks']==26
    assert f['certification']['H22_selected'] is False and f['certification']['source_registry_canon_selected'] is False
    assert c['selected']['Chicago_first']==[18,'Walker Kessler'] and c['selected']['Chicago_second']==[57,'Keon Ellis']
    assert c['selected']['route']=='R1_WAIVE_STANLEY_KEEP_BRADLEY'
    assert c['selected']['registration']=={'STANDARD':15,'TWO_WAY':2}
    assert c['review_acceptance']['canonical_adoption_recorded_here'] is True
    assert c['selected']['normal_family_upper_before_D23']==162976941
    assert c['selected']['apron_family_upper_before_D23']==164614941
    assert f['role_template']['Kessler_new_NBA_productivity']['chosen_point'] is None
    assert f['role_template']['Kessler_new_NBA_productivity']['range']==[-3,1]

def decision(s):
    f=s[FAMILY]
    return {'id':'DELEGATED_CHICAGO_2022_23_HEALTH_ROLES_2026_10_08','baseline_main':BASELINE,
      'classification':'AUTHOR_DELEGATED_WORKING_HEALTH_CALENDAR_AND_ROLE_SELECTION',
      'authority':AUTH,'selection_instruction':'Root explicit adoption after independent82date/clock/nomination review on2026-10-08; existing health/season delegation, no new human permission',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8BOMstrip;CRLF/CRtoLF',
      'selected':{'H22':'NORMAL_NO_NEW_SUSTAINED_MAJOR_ABSENCE_IN_WORKING_MODEL','date_keys':82,
        'calendar':'Official published Chicago82 dates adopted as working dates, not physical played history',
        'role_template':'H22_NORMAL_KESSLER12_REG48','ordered_coach_schedule':True,
        'registered_STANDARD':f['role_template']['registered_STANDARD'],'registered_TWO_WAY':f['role_template']['registered_TWO_WAY'],
        'active_STANDARD':f['role_template']['active_STANDARD'],'inactive_STANDARD':f['role_template']['inactive_STANDARD'],
        'position_minutes':f['role_template']['position_minutes'],
        'player_minutes':f['role_template']['player_minutes'],'Kessler_new_fiction_BPM_point':-1,
        'Kessler_sensitivity_range':[-3,1],'TW_active_game_count':0},
      'source_snapshot_policy':'Original candidate/source pendingflags preserved; this separate canon records the new delegated adoption',
      'review_acceptance':{'independent_recommendation_review_completed':True,'review':REVIEW,
        'new_consumer_peer_review_completed':False},
      'boundaries':{'actual_private_health_NBA_roster_filings_or_box_stats_certified':False,
        'official_GP_GS_or_total_minutes_certified':False,'Coby_2023_ordinary_QO_starter_branch_selected':False,
        'LaMelo_award_or_extension_and_MVP_year_selected':False,'new_contract_price_or_franchise_move_selected':False,
        'results_all82_or_OT_adopted':False,'new_D23_cost_N23':None,'new_D23_cost_A23':None,
        'whole_2022_23_or_macro3_complete':False,'new_human_author_lock':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}

def selected_template(s):
    t=copy.deepcopy(s[FAMILY]['role_template'])
    t['classification']='AUTHOR_DELEGATED_WORKING_ROLE_AND_H22_SELECTED_NOT_ACTUAL_HISTORY'
    t['H22_adopted']=True;t['source_registry_canonical_adoption_inherited']=True
    t['Kessler_new_NBA_productivity']['chosen_point']=-1
    t['adoption_source']=CANON+'#/selected';t['source_candidate_pointer']=FAMILY+'#/role_template'
    return t

def selected_rows(s):
    rows=copy.deepcopy(s[FAMILY]['dated_rows'])
    for i,r in enumerate(rows):
        r['working_date_adopted']=True;r['H22_state_selected_for_date']=True
        r['registration_family_canonical_adoption']=True;r['role_pointer']=OUT+'#/selected_role_template'
        r['source_candidate_row_pointer']=FAMILY+'#/dated_rows/'+str(i)
        r['adoption_source']=CANON+'#/selected'
    return rows

def assert_selected(t,rows,s):
    old=s[FAMILY]['role_template'];expected=copy.deepcopy(old)
    expected['classification']='AUTHOR_DELEGATED_WORKING_ROLE_AND_H22_SELECTED_NOT_ACTUAL_HISTORY'
    expected['H22_adopted']=True;expected['source_registry_canonical_adoption_inherited']=True
    expected['Kessler_new_NBA_productivity']['chosen_point']=-1
    expected['adoption_source']=CANON+'#/selected';expected['source_candidate_pointer']=FAMILY+'#/role_template'
    assert t==expected,'Selected template differs from reviewed source plus explicit root adoption'
    assert t['clinical_status_for_all17']=={n:None for n in t['registered_STANDARD']+t['registered_TWO_WAY']}
    assert len(rows)==len(s[FAMILY]['dated_rows'])==82
    for i,(r,o) in enumerate(zip(rows,s[FAMILY]['dated_rows'])):
        e=copy.deepcopy(o);e['working_date_adopted']=True;e['H22_state_selected_for_date']=True
        e['registration_family_canonical_adoption']=True;e['role_pointer']=OUT+'#/selected_role_template'
        e['source_candidate_row_pointer']=FAMILY+'#/dated_rows/'+str(i);e['adoption_source']=CANON+'#/selected'
        assert r==e,'Selected date row differs from source clock/date and allowed adoption delta'
        assert r['result'] is None and r['overtime_periods'] is None and r['actual_NBA_game_id'] is None
        assert r['regulation_team_seconds']==14400

def assert_decision(d,s):
    t=s[FAMILY]['role_template']
    assert d['id']=='DELEGATED_CHICAGO_2022_23_HEALTH_ROLES_2026_10_08'
    assert d['classification']=='AUTHOR_DELEGATED_WORKING_HEALTH_CALENDAR_AND_ROLE_SELECTION'
    assert d['authority']==AUTH and d['source_sha256']=={**PINS,SELF:sha(SELF)}
    assert d['selected']=={'H22':'NORMAL_NO_NEW_SUSTAINED_MAJOR_ABSENCE_IN_WORKING_MODEL','date_keys':82,
        'calendar':'Official published Chicago82 dates adopted as working dates, not physical played history',
        'role_template':'H22_NORMAL_KESSLER12_REG48','ordered_coach_schedule':True,
        'registered_STANDARD':t['registered_STANDARD'],'registered_TWO_WAY':t['registered_TWO_WAY'],
        'active_STANDARD':t['active_STANDARD'],'inactive_STANDARD':t['inactive_STANDARD'],
        'position_minutes':t['position_minutes'],'player_minutes':t['player_minutes'],
        'Kessler_new_fiction_BPM_point':-1,'Kessler_sensitivity_range':[-3,1],'TW_active_game_count':0},'Delegated selection differs from exact root instruction and reviewed named family'
    assert d['review_acceptance']=={'independent_recommendation_review_completed':True,'review':REVIEW,'new_consumer_peer_review_completed':False}
    assert d['selected']['H22']=='NORMAL_NO_NEW_SUSTAINED_MAJOR_ABSENCE_IN_WORKING_MODEL'
    assert d['selected']['Kessler_new_fiction_BPM_point']==-1 and d['selected']['Kessler_sensitivity_range']==[-3,1]
    assert d['selected']['position_minutes']==s[FAMILY]['role_template']['position_minutes']
    assert d['selected']['player_minutes']==s[FAMILY]['role_template']['player_minutes']
    assert d['selected']['TW_active_game_count']==0 and d['selected']['date_keys']==82
    assert all(d['boundaries'][k] is False for k in ['actual_private_health_NBA_roster_filings_or_box_stats_certified','official_GP_GS_or_total_minutes_certified','Coby_2023_ordinary_QO_starter_branch_selected','LaMelo_award_or_extension_and_MVP_year_selected','new_contract_price_or_franchise_move_selected','results_all82_or_OT_adopted','whole_2022_23_or_macro3_complete','new_human_author_lock'])
    assert d['boundaries']['new_D23_cost_N23'] is None and d['boundaries']['new_D23_cost_A23'] is None

def build():
    s=inputs();assert_sources(s);d=decision(s);assert_decision(d,s)
    t=selected_template(s);rs=selected_rows(s);assert_selected(t,rs,s)
    out={'id':'CHICAGO_2022_23_SELECTED_DATED_ROLES','baseline_main':BASELINE,
      'status':'AUTHOR_DELEGATED_82DATE_H22_ROLE_ADOPTED_CONSUMER_PEER_REVIEW_PENDING_NOT_RESULTS',
      'source_sha256':{**PINS,SELF:sha(SELF),CANON:data_sha(d)},'hash_convention':'UTF8BOMstrip;CRLF/CRtoLF',
      'adoption':{'canon':CANON,'source_candidate_pending_flags_preserved':True,'role_recommendation_review':REVIEW,'rookie_registry_adoption':ROOKIE_CANON},
      'selected_role_template':t,'dated_rows':rs,
      'summary':{**s[FAMILY]['summary'],'executed_H22_date_selections':82,'working_published_date_adoptions':82,'results_selected':0,'overtime_periods_selected':0,'official_GP_GS_records_certified':0},
      'regulation_exposure':{'player_minutes_if_all82_regulation_blocks_executed':copy.deepcopy(s[FAMILY]['prospective_exposure_not_official_GP_GS']['if_same_candidate_is_adopted_all82_player_minutes']),
        'Coby_fourth_year_regulation_minute_lower_bound':1476,'Coby_total_minutes_including_OT':None,'Coby_official_GP_GS':None,
        'Coby_under2000_total_minutes_proved':False,'Coby_starter_exclusion_or_QO_amount_selected':False,
        'LaMelo_awards_extension_MVP_or_title_outcomes':None,
        'working_minutes_not_actual_private_box_certificate':True},
      'preserved_financial_family':copy.deepcopy(s[FAMILY]['same_financial_family_source']),
      'remaining_finite_inputs':['Changed opponent named contracts/availability/clock on each workingdate','Incumbent productivity evaluation ports and optional sensitivity; Kessler point−1 isfiction, rangepreserved','Explicit whole-gameOT/result/standing/playoff and2023GP/GS/QO/extension inputs; not copied from historicalbox','NewD23 N23/A23 and following2023contracts/CBAboundary remain separate'],
      'certification':{'independent_recommendation_review_completed':True,'new_consumer_independent_review_completed':False,
        'H22_and82_working_date_role_selected':True,'actual_medical_NBA_active_receipts_box_GP_GS_certified':False,
        'all82_results_or_OT_selected':False,'new_important_contract_or_franchise_MVP_title_selected':False,
        'whole_2022_23_or_macro3_complete':False,'central_REGISTER_promoted':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}
    return d,out

def render(j):
    return '''# Chicago 2022–23 선택된 날짜·H22·코치 역할

독립검문된 역할 후보를 기존위임으로 채택한 별도 소비자다. 원후보의 pending flags는 작성시점 이력으로 남기고, 새 canon에 H22 NORMAL·공식발표82날짜·순서 있는 역할계획의 선택을 기록한다. 신인·명단 정본채택은 별도 draft/rookie canon을 소비한다. 이번 소비자 자체 독립검문은 pending이다.

15STD+2TW, active12STANDARD/3inactive·양수11명, TW NBA active0. P32/LaMelo32/Mark32/LaVine34/Carter28, Caruso18/Coby18/Duarte14, Young14/Bradley6/Kessler12. 두24분 주기의26구간을82행에서참조하고 PG/SG/SF/PF/C 각각48분·5고유선수·총240분을 유지한다. 임상17명 모두null, 원실제부상58/24와 미래NBA교대를복사하지 않는다. 0분/비활성은임상결장인증이아니다.

Kessler의 새 fictionBPM −1점을 선택하고 민감도−3..1을 보존한다. 실제신인BPM·실제골대보호성과·득점·우승·계약가치를인증하지않는다. Jan19 DET명목홈/Paris원노트는그대로라서 Detroit일반홈우위를자동복사하지않는다. PUBLISHED키는NBA실경기ID가아니다.

## 결과·통계·비용 경계

82규정시간 분계획만채택한다. 결과·점수·OT는전부null이며 전체경기가noOT라고선택하지않는다. Coby4년차 규정시간 하한18×82=1476은작업모델의하한이다. 추가OT분·공식GP/GS가없으므로2000분미만/스타터제외/QO금액을확정하지않는다. LaMelo연장award·MVP/title선택도없다.

원급여예약 normal162,976,941/apron164,614,941와원Γ를유지한다. 신규계약/픽양도나할인을생성하지않고N23/A23은null이다. 다음은상대명명명단·같은날240분시계·생산성입력과명시OT/결과,2023통계/계약/CBA경계다. 실제의료·영수증을새완료요건으로요구하지않는다.

| 대그룹 | 상태 |
|---|---|
| 1 | 완료 보존 |
| 2 | S2 완료 보존 |
| 3 | 82날짜 H22·역할 선택, 결과/OT 미선택 |
| 4 | 선행시즌 의존성 |
| 5 | 진행 |
| 6 | 진행·Pack0 |
| 7 | 미완료·CLOSED |

미완료5 / 6번까지4. v0.30 PARTIAL·원고0·중앙/Git변경0.
'''

def validate(d,j):
    errors=[]
    try:
        s=physical();assert_sources(s);assert_decision(d,s);assert_selected(j['selected_role_template'],j['dated_rows'],s)
        expected_d,expected_j=build();assert d==expected_d and j==expected_j,'Stored adoption differs from source-bound reconstruction'
    except (AssertionError,KeyError,ValueError) as e:errors.append(str(e) or 'Semantic assertion rejected')
    return errors

def self_test():
    d,b=build();tests=[]
    def reject(label,helper,bad):
        try:
            with patch(__name__+'.'+helper,return_value=bad):build()
        except AssertionError:tests.append(label);return
        raise AssertionError('FALSE_PASS '+label)
    t=copy.deepcopy(b['selected_role_template']);t['player_seconds']['Walker Kessler']+=60;t['player_seconds']['Tony Bradley']-=60;reject('same_total_Kessler_Bradley_exchange','selected_template',t)
    t=copy.deepcopy(b['selected_role_template']);t['clinical_status_for_all17']['Walker Kessler']='REAL_HEALTHY';reject('actual_clinical_certificate','selected_template',t)
    rs=copy.deepcopy(b['dated_rows']);rs[0]['result']='CHI';reject('winner_generated_without_result_inputs','selected_rows',rs)
    rs=copy.deepcopy(b['dated_rows']);rs[44]['original_venue_note']='Detroit ordinary arena';reject('Paris_note_erased','selected_rows',rs)
    dd=copy.deepcopy(d);dd['boundaries']['Coby_2023_ordinary_QO_starter_branch_selected']=True;reject('regulation1476_used_for_QO_selection','decision',dd)
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();d,j=build()
    if a.write:(ROOT/CANON).write_text(dump(d),encoding='utf-8');(ROOT/OUT).write_text(dump(j),encoding='utf-8');(ROOT/MD).write_text(render(j),encoding='utf-8')
    errors=[]
    if a.check:
        errors=validate(json.loads(text(CANON)),json.loads(text(OUT)))
        if text(MD)!=render(j):errors.append('Markdown not current')
    tests=self_test() if a.self_test else []
    print(dump({'current':not errors,'errors':errors,'H22_selected':True,'working_dates':82,'results_selected':0,'OT_selected':0,'negatives':tests}))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
