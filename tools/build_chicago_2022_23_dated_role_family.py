"""Published82-date, new-roster regulation role candidate; not a health/result adoption."""
from __future__ import annotations
import argparse,copy,csv,hashlib,io,json,re
from collections import Counter
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_23_dated_role_family.py'
OUT='simulation/CHICAGO_2022_23_DATED_ROLE_FAMILY.json'
MD=OUT.replace('.json','.md')
BASELINE='ee0ff822aa127f8263cc69e03ba2a7184053e22e'
ROOKIE='simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json'
CAL='simulation/CHICAGO_2022_23_PUBLISHED_CALENDAR.csv'
PROV='simulation/NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE.json'
M1='simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json'
AUTH='control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md'
PINS={'simulation/CHICAGO_2022_ROOKIE_SELECTED_EXECUTION.json': '3c06967cf8c7171f815819efd3b4a71fb88ac77db3ae8798b34afeeeae93ce1c', 'simulation/CHICAGO_2022_23_PUBLISHED_CALENDAR.csv': 'bd78708fb1d58e4decede3723bd14829863d395366d30d202565e3c7f7729f4b', 'simulation/NBA_2022_23_PUBLISHED_CALENDAR_PROVENANCE.json': 'b0ed4235d17653b1272636f8197cb9eca3daacc1e279a157376f9ae227496e78', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca', 'control/DELEGATED_CONTINUATION_SCOPE_2026_10_07.md': '91cc2246afefca1d8fe8c0274440e80f5d87a91edd5e4faf097201e03e0bfc2d'}
EXPECTED_ROOKIE_SHA='3c06967cf8c7171f815819efd3b4a71fb88ac77db3ae8798b34afeeeae93ce1c'
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
PACERS=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-fy22-whole-20261007/pacers2022.pdf')
TEAM_PDF=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-2022-23-calendar-20261007/league_byteam.pdf')
STD=['Lauri Markkanen','Alex Caruso','LaMelo Ball','Coby White','Chris Duarte','Javonte Green','Joe Wieskamp','Tony Bradley','Denzel Valentine','Wendell Carter Jr.','Protagonist','Zach LaVine','Thaddeus Young','Tomas Satoransky','Walker Kessler']
TW=['Devon Dotson','Tyler Cook']
ALIASES={'Markkanen':'Lauri Markkanen','Caruso':'Alex Caruso','LaMelo_pick4':'LaMelo Ball','Coby':'Coby White','LaVine':'Zach LaVine','Carter':'Wendell Carter Jr.','Young':'Thaddeus Young','Satoransky':'Tomas Satoransky','Green':'Javonte Green'}
POSITION_ORDER=['PG','SG','SF','PF','C']
OLD_POS={'PG':{'LaMelo_pick4':32,'Coby':10,'Caruso':6},'SG':{'LaVine':34,'Coby':8,'Caruso':6},'SF':{'Protagonist':28,'Caruso':6,'Chris Duarte':14},'PF':{'Markkanen':32,'Protagonist':4,'Young':12},'C':{'Carter':28,'Young':8,'Tony Bradley':12}}
POS={'PG':{'LaMelo Ball':32,'Coby White':10,'Alex Caruso':6},'SG':{'Zach LaVine':34,'Coby White':8,'Alex Caruso':6},'SF':{'Protagonist':28,'Alex Caruso':6,'Chris Duarte':14},'PF':{'Lauri Markkanen':32,'Protagonist':4,'Thaddeus Young':12},'C':{'Wendell Carter Jr.':28,'Thaddeus Young':2,'Tony Bradley':6,'Walker Kessler':12}}
EXPECTED_MINUTES={'Alex Caruso':18,'Chris Duarte':14,'Coby White':18,'LaMelo Ball':32,'Lauri Markkanen':32,'Protagonist':32,'Thaddeus Young':14,'Tony Bradley':6,'Walker Kessler':12,'Wendell Carter Jr.':28,'Zach LaVine':34}
ELIGIBILITY={'PG':['LaMelo Ball','Coby White','Alex Caruso','Tomas Satoransky'],'SG':['Zach LaVine','Coby White','Alex Caruso','Chris Duarte','Denzel Valentine'],'SF':['Protagonist','Chris Duarte','Alex Caruso','Joe Wieskamp','Javonte Green','Denzel Valentine'],'PF':['Lauri Markkanen','Protagonist','Thaddeus Young','Javonte Green'],'C':['Wendell Carter Jr.','Thaddeus Young','Tony Bradley','Walker Kessler']}
NAMES=dict(zip(['Atlanta','Boston','Brooklyn','Charlotte','Chicago','Cleveland','Dallas','Denver','Detroit','Golden State','Houston','Indiana','LA Clippers','L.A. Lakers','Memphis','Miami','Milwaukee','Minnesota','New Orleans','New York','Oklahoma City','Orlando','Philadelphia','Phoenix','Portland','Sacramento','San Antonio','Toronto','Utah','Washington'],['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']))

def norm(s):return s.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
def text(p):return norm((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def physical():
    for p,h in PINS.items():assert sha(p)==h,'Pinned source changed: '+p
    return {p:json.loads(text(p)) for p in [ROOKIE,PROV,M1]}
def source_inputs():return physical()
def assert_sources(s):
    assert s==physical(),'Source loader objects differ from pinned physical snapshots'
    assert sha(ROOKIE)==EXPECTED_ROOKIE_SHA
    r=s[ROOKIE]['working_execution'];items=r['registered_contracts']
    assert [x['player'] for x in items if x['roster_type']=='STANDARD']==STD
    assert [x['player'] for x in items if x['roster_type']=='TWO_WAY']==TW
    assert len(items)==len({x['player'] for x in items})==17
    assert r['selected_rookie_route']['id']=='R1_WAIVE_STANLEY_KEEP_BRADLEY'
    k=next(x for x in r['selected_board_rows'] if x['pick']==18)
    assert k['player']=='Walker Kessler' and k['participation']['public_prospect_identity']['position']=='C'
    assert r['Ellis_selected_rights_path']['STD_added']==r['Ellis_selected_rights_path']['TW_added']==0
    assert all(x['holder']=='CHI' and x['exclusive_current_UPC_claim'] for x in items)
    assert s[ROOKIE]['limits']['root_canonical_adoption_recorded'] is False
    assert s[ROOKIE]['limits']['independent_review_completed'] is False
    assert s[PROV]['derived_text_sha256'][CAL]==sha(CAL)
    assert s[PROV]['verification']['Chicago_games']==82
    old=next(x for x in s[M1]['rows'] if x['state']=='NORMAL')
    assert old['position_minutes']==OLD_POS and len(old['unordered_regulation_blocks'])==11
    assert old['player_minutes']['Protagonist']==32 and old['player_minutes']['Markkanen']==32

def dates(s):
    rows=list(csv.DictReader(io.StringIO(text(CAL))))
    assert len(rows)==82 and len({x['calendar_key'] for x in rows})==82
    assert [int(x['team_game_number']) for x in rows]==list(range(1,83))
    assert sum(x['home']=='CHI' for x in rows)==sum(x['away']=='CHI' for x in rows)==41
    assert [x['published_date'] for x in rows]==sorted(x['published_date'] for x in rows)
    assert len({x['published_date'] for x in rows})==82
    assert rows[0]['published_date']=='2022-10-19' and rows[-1]['published_date']=='2023-04-09'
    for r in rows:
        assert (r['home']=='CHI')!=(r['away']=='CHI')
        assert r['opponent']==(r['away'] if r['home']=='CHI' else r['home'])
        assert all(r[k]=='' for k in ['actual_NBA_game_id','actual_played_date','alternate_date_selected','alternate_result_selected'])
    return rows

def primary(s,cal):
    import fitz
    info=[]
    for p,h,pages,url,role in [
      (CBA,'66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a',[412,413],'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','XXIX_ACTIVE_MIN12_INACTIVE_AND_TW_BASELINE_NOT_EXTRA8_SIDELINE_PLAYERS'),
      (PACERS,'9b33b46bfe88d495a54ad21894fd67eb3b376aff048589a1e609eb82e79b3625',[165],'https://cdn.nba.com/teams/uploads/sites/1610612754/2022/10/2022-23-Pacers-Media-Guide-compressed.pdf','TEAM_OFFICIAL_2022_ACTIVE12_15_DRESSED_ELIGIBLE_AVAILABLE8_TW50_PARAGRAPHS_ONLY'),
      (TEAM_PDF,'e7d774794df47fe54887ff9505471ebed12f1a740a692ecc6096fb104ac927ad',[5],'https://pr.nba.com/wp-content/uploads/sites/46/2022/08/2022-23-NBA-Schedule-By-Team-8-17-22.pdf','NBA_ORIGINAL_PUBLISHED_CHI82_DATE_OPPONENT_FACTS_NOT_PLAYED_IDS')]:
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h
        d=fitz.open(p);ts={n:norm(d[n-1].get_text()) for n in pages}
        if p==CBA: assert 'twelve (12)' in ts[412] and 'minimum of eight (8)' in ts[412]
        if p==PACERS:
            plain=' '.join(ts[165].split())
            assert 'no fewer than 12 and no more than 15' in plain and 'more than 50 games during the 2022-23' in plain
        if p==TEAM_PDF:
            assert 'SUBJECT TO CHANGE' in ts[5]
            matches=list(re.finditer(r'(?m)^(\d{1,2})\n(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\n(\d{1,2}/\d{1,2}/\d{2})\n([^\n]+)\n([^\n]+)',ts[5]))
            assert len(matches)==82
            direct={}
            for m in matches:
                away=m[4].startswith('at ');name=m[4][3:] if away else m[4]
                opp=NAMES[name];date=datetime.strptime(m[3],'%m/%d/%y').date().isoformat()
                direct[int(m[1])]=(date,opp,opp if away else 'CHI','CHI' if away else opp)
            assert {int(x['team_game_number']):(x['published_date'],x['opponent'],x['home'],x['away']) for x in cal}==direct
        info.append({'url':url,'cache_path':str(p),'raw_sha256':h,'role':role,'PDF1based_text_LF_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest() for n,t in ts.items()}})
    return info

def role_template(s):
    old=next(x for x in s[M1]['rows'] if x['state']=='NORMAL')
    expanded=[]
    # New ordered candidate, not an adoption of last season's unordered chronology.
    # Preserve all other position occupants; donate Bradley6C and Young6C.
    for i,b in enumerate(old['unordered_regulation_blocks']):
        pos={p:ALIASES.get(n,n) for p,n in b['positions'].items()}
        partitions=[(int(b['minutes']),pos['C'])]
        if i==1:partitions=[(2,'Walker Kessler')]
        if i==8:partitions=[(2,'Walker Kessler')]
        if i==9:partitions=[(4,'Walker Kessler'),(6,'Tony Bradley')]
        if i==10:partitions=[(4,'Walker Kessler'),(2,'Thaddeus Young')]
        for minutes,center in partitions:
            a=copy.deepcopy(pos);a['C']=center;expanded.append((minutes,a,i))
    blocks=[];clock=0
    # Two24-minute cycles preserve the vector without a32-minute continuous PG stint.
    expanded=[(minutes//2,pos,i,cycle) for cycle in [1,2] for minutes,pos,i in expanded]
    for minutes,pos,i,cycle in expanded:
        end=clock+minutes*60
        blocks.append({'start_second':clock,'end_second':end,'duration_seconds':minutes*60,'positions':pos,'players':[pos[p] for p in POSITION_ORDER],'modeled_half_cycle':cycle,'old_M1_block_reference':M1+'#/rows/0/unordered_regulation_blocks/'+str(i),'new_order_is_fictional_candidate_not_actual_substitutions':True})
        clock=end
    pm=Counter()
    for b in blocks:
        for n in b['players']:pm[n]+=b['duration_seconds']
    positive=sorted(pm);active=positive+['Tomas Satoransky']
    return {'id':'H22_NORMAL_KESSLER12_REG48','classification':'NEW_FICTIONAL_ROLE_AND_AVAILABILITY_RECOMMENDATION_NOT_ADOPTED',
      'registered_STANDARD':STD,'registered_TWO_WAY':TW,'STANDARD_working_available_for_nomination':STD,
      'active_STANDARD':active,'inactive_STANDARD':[n for n in STD if n not in active],
      'positive_performers':positive,'zero_minute_active':['Tomas Satoransky'],
      'TW_active':[],'TW_other_roster':TW,'Ellis_registered_or_converted':False,
      'availability_recommendation':'No new sustained major absence for retained15STANDARD in this candidate; clinical status is not a historical fact',
      'modeled_absent':[],'clinical_status_for_all17':{n:None for n in STD+TW},
      'zero_minutes_reason':'Working coach rotation/nomination, not a diagnosis; TW NBA participation not selected',
      'position_eligibility_design_only':ELIGIBILITY,'position_minutes':POS,
      'player_seconds':dict(sorted(pm.items())),'player_minutes':{n:v//60 for n,v in sorted(pm.items())},
      'starters':[blocks[0]['positions'][p] for p in POSITION_ORDER],
      'ordered_regulation_blocks':blocks,'elapsed_seconds':clock,'team_player_seconds':sum(pm.values()),
      'working_clock_policy':'Two24minute cycles, half of each donor-adjusted M1 block in each cycle; regulation coverage witness, not actual or optimal NBA tactical substitutions',
      'game_ready_dressed_eligible_available_minimum':8,'side_bench_extra_eight_after_oncourt_five_required':False,
      'Kessler_C_seconds_donors':{'Tony Bradley':360,'Thaddeus Young':360},
      'Kessler_position_source_pointer':ROOKIE+'#/working_execution/selected_board_rows/17/participation/public_prospect_identity',
      'Kessler_new_NBA_productivity':{'mechanism':'EXPLICIT_NEW_FICTIONAL_BPM_PROXY_ONLY','proposed_center':-1,'range':[-3,1],'chosen_point':None,'actual_rookie_NBA_BPM_or_future_performance_copied':False,'source':'Author modeled development sensitivity; NBA prospect positionC supports role identity, not a BPM estimate'},
      'incumbent_productivity_parameters':'Named separate source-supported/modeled evaluation inputs to be joined later; minutes preserve M1 roles, not past or future BPM values',
      'source_registry_canonical_adoption_inherited':False,'H22_adopted':False,
      'medical_active_list_or_tactical_success_certificate':False,'results_or_OT_selected':False}

def assert_template(t,s):
    assert t['id']=='H22_NORMAL_KESSLER12_REG48' and t['classification']=='NEW_FICTIONAL_ROLE_AND_AVAILABILITY_RECOMMENDATION_NOT_ADOPTED'
    assert t['registered_STANDARD']==STD and t['registered_TWO_WAY']==TW
    assert t['STANDARD_working_available_for_nomination']==STD and t['modeled_absent']==[]
    assert t['position_minutes']==POS and t['position_eligibility_design_only']==ELIGIBILITY
    assert t['player_minutes']==EXPECTED_MINUTES and t['player_seconds']=={n:m*60 for n,m in EXPECTED_MINUTES.items()}
    assert t['positive_performers']==sorted(EXPECTED_MINUTES)
    assert t['active_STANDARD']==sorted(EXPECTED_MINUTES)+['Tomas Satoransky']
    assert len(t['active_STANDARD'])==12 and len(set(t['active_STANDARD']))==12
    assert t['inactive_STANDARD']==[n for n in STD if n not in t['active_STANDARD']]
    assert len(t['inactive_STANDARD'])==3 and set(t['active_STANDARD'])|set(t['inactive_STANDARD'])==set(STD)
    assert not set(t['active_STANDARD'])&set(t['inactive_STANDARD'])
    assert t['zero_minute_active']==['Tomas Satoransky'] and not t['TW_active'] and t['TW_other_roster']==TW
    assert t['Ellis_registered_or_converted'] is False and t['clinical_status_for_all17']=={n:None for n in STD+TW}
    assert t['Kessler_C_seconds_donors']=={'Tony Bradley':360,'Thaddeus Young':360}
    assert t['Kessler_position_source_pointer']==ROOKIE+'#/working_execution/selected_board_rows/17/participation/public_prospect_identity'
    assert t['elapsed_seconds']==2880 and t['team_player_seconds']==14400
    assert t['working_clock_policy']=='Two24minute cycles, half of each donor-adjusted M1 block in each cycle; regulation coverage witness, not actual or optimal NBA tactical substitutions'
    assert t['game_ready_dressed_eligible_available_minimum']==8 and t['side_bench_extra_eight_after_oncourt_five_required'] is False
    assert len(t['ordered_regulation_blocks'])==26
    old=next(x for x in s[M1]['rows'] if x['state']=='NORMAL')['unordered_regulation_blocks']
    expected_indices=[0,1,2,3,4,5,6,7,8,9,9,10,10]*2
    expected_durations=[360,60,60,60,180,60,60,60,60,120,180,120,60]*2
    expected_centers=['Wendell Carter Jr.','Walker Kessler','Wendell Carter Jr.','Wendell Carter Jr.','Wendell Carter Jr.','Wendell Carter Jr.','Wendell Carter Jr.','Wendell Carter Jr.','Walker Kessler','Walker Kessler','Tony Bradley','Walker Kessler','Thaddeus Young']*2
    pc={p:Counter() for p in POSITION_ORDER};minutes=Counter();clock=0
    for bi,b in enumerate(t['ordered_regulation_blocks']):
        assert b['start_second']==clock and b['end_second']-clock==b['duration_seconds']>0
        assert type(b['start_second']) is int and type(b['end_second']) is int and type(b['duration_seconds']) is int
        assert b['duration_seconds']==expected_durations[bi] and b['modeled_half_cycle']==1+bi//13
        assert b['old_M1_block_reference']==M1+'#/rows/0/unordered_regulation_blocks/'+str(expected_indices[bi])
        rawpos=old[expected_indices[bi]]['positions']
        expectedpos={p:ALIASES.get(n,n) for p,n in rawpos.items()};expectedpos['C']=expected_centers[bi]
        assert b['positions']==expectedpos,'Returned clock positions differ from direct source and named donor policy'
        assert list(b['positions'])==POSITION_ORDER and b['players']==[b['positions'][p] for p in POSITION_ORDER]
        assert len(set(b['players']))==5 and set(b['players'])<=set(t['active_STANDARD'])
        assert b['new_order_is_fictional_candidate_not_actual_substitutions'] is True
        for p,n in b['positions'].items():
            assert n in ELIGIBILITY[p];pc[p][n]+=b['duration_seconds'];minutes[n]+=b['duration_seconds']
        clock=b['end_second']
    assert clock==2880 and dict(sorted(minutes.items()))==t['player_seconds']
    assert {p:{n:v//60 for n,v in c.items()} for p,c in pc.items()}==POS
    assert all(sum(c.values())==2880 for c in pc.values())
    assert t['starters']==['LaMelo Ball','Zach LaVine','Protagonist','Lauri Markkanen','Wendell Carter Jr.']
    assert t['Kessler_new_NBA_productivity']=={'mechanism':'EXPLICIT_NEW_FICTIONAL_BPM_PROXY_ONLY','proposed_center':-1,'range':[-3,1],'chosen_point':None,'actual_rookie_NBA_BPM_or_future_performance_copied':False,'source':'Author modeled development sensitivity; NBA prospect positionC supports role identity, not a BPM estimate'}
    assert all(t[k] is False for k in ['source_registry_canonical_adoption_inherited','H22_adopted','medical_active_list_or_tactical_success_certificate','results_or_OT_selected'])

def dated_rows(cal):
    return [{'team_game_number':int(x['team_game_number']),'published_date':x['published_date'],'calendar_key':x['calendar_key'],'home':x['home'],'away':x['away'],'opponent':x['opponent'],'original_venue_note':x['original_venue_note'],
      'template':'H22_NORMAL_KESSLER12_REG48','role_pointer':OUT+'#/role_template','roster_contract_pointer':ROOKIE+'#/working_execution/registered_contracts','published_csv_pointer':CAL+'#row'+x['team_game_number'],
      'working_date_adopted':False,'H22_state_selected_for_date':False,'registration_family_canonical_adoption':False,'actual_NBA_game_id':None,'actual_played_date':None,'result':None,'overtime_periods':None,
      'regulation_elapsed_seconds':2880,'regulation_team_seconds':14400,'named_15STD_2TW_condition_only':True,'actual_clinical_or_active_list_certified':False} for x in cal]

def assert_dates(rows,cal):
    assert len(rows)==82
    for r,c in zip(rows,cal):
        assert r['team_game_number']==int(c['team_game_number'])
        for k in ['published_date','calendar_key','home','away','opponent','original_venue_note']:assert r[k]==c[k]
        assert r['template']=='H22_NORMAL_KESSLER12_REG48' and r['regulation_elapsed_seconds']==2880 and r['regulation_team_seconds']==14400
        assert r['role_pointer']==OUT+'#/role_template' and r['roster_contract_pointer']==ROOKIE+'#/working_execution/registered_contracts'
        assert r['published_csv_pointer']==CAL+'#row'+c['team_game_number']
        assert all(r[k] is False for k in ['working_date_adopted','H22_state_selected_for_date','registration_family_canonical_adoption','actual_clinical_or_active_list_certified'])
        assert all(r[k] is None for k in ['actual_NBA_game_id','actual_played_date','result','overtime_periods'])

def build():
    s=source_inputs();assert_sources(s);cal=dates(s);p=primary(s,cal)
    t=role_template(s);assert_template(t,s);rs=dated_rows(cal);assert_dates(rs,cal)
    return {'id':'CHICAGO_2022_23_DATED_ROLE_FAMILY','baseline_main':BASELINE,'status':'82_PUBLISHED_DATE_ROLE_AND_HEALTH_RECOMMENDATION_REVIEW_PENDING_NOT_SELECTED',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8BOMstrip;CRLF/CRtoLF','primary':p,
      'pending_registration_source_status':s[ROOKIE]['classification'],'source_registry_canonical_adoption':False,
      'policy':{'H22_recommendation':'SUSTAINED_MAJOR_ABSENCE_NOT_ADDED_IN_NEW_FICTIONAL_NORMAL_MODEL','H22_adopted':False,'date_adoption':False,'regulation_only':True,'source_old58_24_or_old_clinical_absences_copied':False,'historical_results_or_OT_imported':False,'size_domain_active':[12,15],'nominated_STANDARD':12,'TW_active_count_over_all82_hypothetical_assignments':0,'no_new_transactions_or_TW_conversions':True},
      'role_template':t,'dated_rows':rs,
      'summary':{'published_date_keys':82,'named_standard':15,'named_two_way':2,'positive_players':11,'active_standard':12,'inactive_standard':3,'clock_template_blocks':len(t['ordered_regulation_blocks']),'hypothetical_dated_blocks':82*len(t['ordered_regulation_blocks']),'hypothetical_dated_five_player_cells':82*len(t['ordered_regulation_blocks'])*5,'total_regulation_team_minutes_if_all82_adopted':19680,'executed_H22_date_selections':0},
      'prospective_exposure_not_official_GP_GS':{'if_same_candidate_is_adopted_all82_player_minutes':{n:m*82 for n,m in EXPECTED_MINUTES.items()},'official_GP_or_GS_certified':False,'Coby_2023_starter_and_LaMelo_extension_award_inputs_selected':False},
      'same_financial_family_source':{'cost_pointer':ROOKIE+'#/working_execution/cost','normal_before_D23':162976941,'apron_before_D23':164614941,'new_UPC_salary_or_transaction_selected_by_this_role_leaf':False,'N23':None,'A23':None,'whole_FY22_cost_after_D23':None},
      'primary_scope_limits':['Pacers2022guide active12–15/dressed-eligible-available8/TW50 paragraphs only; its separate waiver/injured-list summaries are not used as new waiver authority','Published keys/date/opponent verified on originalNBA byteamPDF5; they are not NBAplayedIDs and are SUBJECTTOCHANGE','Kessler positionC from pendingreviewedboard publicprospect identity; no futureNBA box/BPM/rimdefense success copied','Named registered17 and July11RSC source pending rootcanonical adoption; this leaf does not fabricate source independent flags'],
      'next_finite_inputs':['Root independent review and H22/date/ordered working coach plan adoption under existing delegation','Named opponent changed rosters and simultaneous240minute clock for each chosen publisheddate','Current fictional/source-supported productivity ports including proposed Kessler interval; no actualfuture rookieBPM copied','Explicit regulation/noOT or additional OT clock/result/standing/2023QO and extension statistic model; not auto-derived clinicalcerts'],
      'certification':{'independent_review_completed':False,'H22_selected':False,'source_registry_canon_selected':False,'all82_game_results_selected':False,'actual_clinical_registration_or_GP_GS_certified':False,'new_contract_pick_or_important_career_outcome_selected':False,'whole_2022_23_or_macro3_complete':False,'central_REGISTER_promoted':False},
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','Pack_count':0,'manuscript_allowed':False}

def render(j):
    mins='\n'.join('| '+n+' | '+str(m)+' |' for n,m in EXPECTED_MINUTES.items())
    return '''# Chicago 2022–23 82날짜 역할·가용성 후보

공식 사전발표82키를 현재 신인 선택 생산기의15STD+2TW와 묶는다. 원등록 snapshot3c06967c는 아직 root canonical adoption/독립완료false인 입력이므로, 이 산출물도 실제 채택·H22 선택·날짜 선택을 false로 둔다. 최신 source 상태를 지문과 함께 보존한다.

## 새 H22 제안과 명단

15STANDARD에 새 지속 중대결장을 추가하지 않는 NORMAL 가상 권고다. 과거58/24, 실제 후대 부상, 2021임상 모델을 복사하지 않는다. 후보 운영상 명명15명은 nomination에 가용하되 실제17명 임상상태는 모두null이다. 양수11명과 Satoransky0분 bench로12STANDARD active, Green/Wieskamp/Valentine은3STANDARD inactive다. inactive/0분은 부상이라는 뜻이 아니다. Devon Dotson/Tyler Cook은TW명단만 보존하고 NBA active/분0, Ellis는미수락권리로 남긴다. 새TW3/표준전환/수취팀/거래를 만들지 않는다.

## 같은 48분 시계

| 선수 | 경기당 후보 분 |
|---|---:|
'''+mins+'''

기존 M1 NORMAL의 PG/SG/SF/PF 분배를 유지한다. C에서 Bradley의12중6, Young의8중6을 신인 Kessler에게 주므로 Carter28/Bradley6/Young2/Kessler12다. Young은 PF12를 더해총14. 성장코어 P32/LaMelo32/Mark32/LaVine34/Carter28 및 Caruso18/Duarte14/Coby18을 보존한다. 부모의 반복훈련·실제골대보호 성공·미래효율은 이 분배의 사실 근거로 주장하지 않는다.

두24분 주기에 각구간을 절반씩 나눈26개 순서 있는 가상 구간, 연속0..2880초, 매구간 PG/SG/SF/PF/C와5고유선수, 각포지션48분·팀240분을 검산한다. 원M1의 unordered11구간을 새순서 후보로 표현하되 실제NBA교대 인증으로 승격하지 않는다. 시작5인은LaMelo/LaVine/P/Mark/Carter다. 같은 템플릿을82행의 참조로 묶어 큰시계복제를 피하고 총분19680은 전행 채택을 가정한 exposure일 뿐 선택시즌 결과가 아니다.

Kessler 신규 생산성은 명시적 fictionBPM 중심권고−1/범위−3..1/선택점null. 실제 Utah 신인BPM·수상·블록·box를 가져오지 않는다. 다른 선수 생산성도 별도평가 입력 포트이며 분 보존을 효율 보존이라고 말하지 않는다. Coby GP/GS·LaMelo 연장성과 조건을 공식 기록으로 확정하지 않는다.

## 날짜와 법적 범위

NBA 원ByTeam PDF5의82행을 CSV 날짜·상대·명목홈/원정에 직접 대조한다. Oct19 MIA부터Apr9 DET까지41홈/41원정. Jan19는DET명목홈이지만 Paris의AccorArena라는 원노트를 보존하며 Detroit일반홈우위를 자동 적용하지 않는다. PUBLISHED키는생산된문서키이고 NBA gameid·실제경기일·승자·점수·OT는null이다. 발표원문 SUBJECTTOCHANGE를 유지한다.

원CBA XXIX와 official Pacers2022guide PDF165의active12–15/경기준비·출장자격·가용8/TW50 문단을 좁게 사용한다. 이번12STD 명명후보는3inactive/11양수와1가용reserve를 가져 경기준비·출장자격·가용최소8을 충족한다. court5외별도벤치8을 요구하는 해석은 아니다. 그 가이드의 다른 waiver·injured-list 요약은이번등록의새근거로사용하지 않는다. 원등록 가족의 비용 normal162,976,941/apron164,614,941를 참조할 뿐 새비용·N23/A23·사적정확영수증을 만들지 않는다.

다음은 root의한정가용/날짜/코치계획채택, 상대 명명명단과동시시계, 생산성·OT/결과모델이다. 명명된 source/role공백으로 남기고 실제사적의료·장부 전수를새완료요건으로 요구하지 않는다.

| 대그룹 | 상태 |
|---|---|
| 1 | 완료 보존 |
| 2 | S2 완료 보존 |
| 3 | 82날짜 역할·가용성 후보 준비, 결과 미선택 |
| 4 | 선행시즌 의존성 |
| 5 | 진행 |
| 6 | 진행·Pack0 |
| 7 | 미완료·CLOSED |

미완료5 / 6번까지4. v0.30 PARTIAL·원고0·중앙/Git 변경0.
'''

def validate(j):
    errors=[]
    try:
        s=physical();assert_sources(s);assert_template(j['role_template'],s);assert_dates(j['dated_rows'],dates(s))
        assert j==build(),'Saved artifact differs from source-bound reconstruction'
    except (AssertionError,ValueError,KeyError) as e:errors.append(str(e) or 'Semantic assertion rejected')
    return errors

def self_test():
    base=build();checks=[]
    def reject(label,helper,bad):
        try:
            with patch(__name__+'.'+helper,return_value=bad):build()
        except AssertionError:checks.append(label);return
        raise AssertionError('FALSE_PASS '+label)
    t=copy.deepcopy(base['role_template']);t['player_seconds']['Walker Kessler']+=60;t['player_seconds']['Tony Bradley']-=60;reject('same_total_Kessler_donor_changed','role_template',t)
    t=copy.deepcopy(base['role_template']);t['active_STANDARD'][-1]='Keon Ellis';reject('unregistered_Ellis_active','role_template',t)
    t=copy.deepcopy(base['role_template']);t['TW_active']=['Devon Dotson'];reject('TW_participation_added','role_template',t)
    t=copy.deepcopy(base['role_template']);t['ordered_regulation_blocks'][0]['players'][4]='Protagonist';reject('same_clock_duplicate_player','role_template',t)
    t=copy.deepcopy(base['role_template']);t['clinical_status_for_all17']['Walker Kessler']='CERTIFIED_HEALTHY';reject('actual_rookie_clinical_certificate','role_template',t)
    t=copy.deepcopy(base['role_template']);t['Kessler_new_NBA_productivity']['chosen_point']=3.5;reject('future_actual_rookie_BPM_imported','role_template',t)
    t=copy.deepcopy(base['role_template']);t['ordered_regulation_blocks'][0]['old_M1_block_reference']=M1+'#/rows/0/unordered_regulation_blocks/1';reject('wrong_source_clock_pointer','role_template',t)
    rows=copy.deepcopy(base['dated_rows']);rows[44]['original_venue_note']='Detroit home arena';reject('Paris_venue_erased','dated_rows',rows)
    rows=copy.deepcopy(base['dated_rows']);rows[0]['result']='CHI';reject('historical_or_selected_winner_added','dated_rows',rows)
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();j=build()
    if a.write:(ROOT/OUT).write_text(dump(j),encoding='utf-8');(ROOT/MD).write_text(render(j),encoding='utf-8')
    errors=[]
    if a.check:
        errors=validate(json.loads(text(OUT)))
        if text(MD)!=render(j):errors.append('Markdown not current')
    tests=self_test() if a.self_test else []
    print(dump({'current':not errors,'errors':errors,'summary':j['summary'],'negatives':tests,'H22_selected':False}))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
