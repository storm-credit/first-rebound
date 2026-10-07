"""Four selected Miami dates using reviewed legal family; direct physical sources, no ancestor builds."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from datetime import date,timedelta
from unittest.mock import patch
import argparse,csv,hashlib,io,json
import fitz
import build_nyk_2021_keeper_and_chicago_selected_results as base
import build_chicago_detroit_2021_two_date_selected_bpm_results as det
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_mia_2021_keeper_and_chicago_selected_results.py'
OUT='simulation/CHICAGO_MIAMI_2021_22_SELECTED_KEEPER_RESULTS.json';MD=OUT[:-5]+'.md'
BASELINE='d111ddb9a0246345b1c04784404c829bf3202576'
PINS={**base.PINS,base.SELF:'61eb21ed98b1c4020bce85062db5bb7b988de9ba9cf213116b52f54575d9b397'}
need=base.need;sha=base.sha;text=base.text;physical=base.physical
IDS=('0022100296','0022100394','0022100922','0022101164')
CLOSURE='research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json'
ATOM='research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json'
PINS.update({CLOSURE:'3007e4a2407a02e97998826c3cb8ee352ac2a75353b3c8c5822c16aa55fdbb48',ATOM:'719b2ff19583d6373a2c165988c9fc55b298fce3728dc8763df2d3f327357278'})
STANDARD=('Bam Adebayo','Dewayne Dedmon','Duncan Robinson','Gabe Vincent','Jimmy Butler','KZ Okpala','Kyle Lowry','Markieff Morris','Max Strus','Omer Yurtseven','P.J. Tucker','Tyler Herro','Udonis Haslem','Victor Oladipo')
TWO_WAY=('Caleb Martin','Marcus Garrett')
ROLE_MINUTES={'PG':{'Kyle Lowry':30,'Gabe Vincent':18},'SG':{'Duncan Robinson':26,'Tyler Herro':22},'SF':{'Jimmy Butler':26,'Tyler Herro':8,'Max Strus':14},'PF':{'P.J. Tucker':26,'Markieff Morris':14,'Jimmy Butler':8},'C':{'Bam Adebayo':34,'Dewayne Dedmon':14}}
ROLE_FIXED=deepcopy(ROLE_MINUTES)
STARTERS={'PG':'Kyle Lowry','SG':'Duncan Robinson','SF':'Jimmy Butler','PF':'P.J. Tucker','C':'Bam Adebayo'}
ROLE_SHA='af366fd2b6e7ad2ece233d47f0cca92e8b39b74ec4c2f92a21d74180f6c28bf4'
POLICY={'selected_contract_route':'REUSE_ROOT_REVIEWED_MIA14STD2TW_LOWRY_ATOM_AND_PUBLIC_GAMMA_APRON_FAMILY','no_duplicate_Lowry_atom':True,'new_trade':False,'new_contract_price_bonus_or_exception':False,'availability':'Oladipo workingabsent onfourdates, no actualmedical/foreignreceipt certificate; Lowry/Butler/Bam/Morris10positive operationalavailable; no automatichistoricalthumb/surgery/Jokiccontact/protocol imported; zeroreserve clinicalnull','TW_regular_activation':0,'new_TW_conversion':False,'whole_private_or_actual_receipts':False}
POLICY_FIXED=deepcopy(POLICY)

def direct(root,p):
    t=(root/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
    return json.loads(t)if p.endswith('.json')else list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else t
def sources(root):return {p:physical(root,p)for p in PINS}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def support(src):
    need(hashlib.sha256(base.CBA.read_bytes()).hexdigest()==base.CBA_SHA,'CBA raw changed')
    d=fitz.open(base.CBA);pages=(216,240,241,286)
    tx={n:d[n-1].get_text().replace('\r\n','\n').replace('\r','\n')for n in pages}
    cl=src[CLOSURE];at=src[ATOM]
    need(cl['selected_MIA_apron_legal_family_complete']and cl['selected_route_feasible_under_reported_contract_family']and not cl['actual_NBA_approval_or_contract_receipt_certified'],'Reviewed legal scope changed')
    need(cl['source_sha256'][ATOM]==PINS[ATOM]and cl['cba_raw_sha256']==base.CBA_SHA,'Legal source relationship changed')
    need(cl['cba_page_text_sha256']=={str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()},'Consumed CBA source changed')
    h=at['MIA_roster_handoff'];need(tuple(h['opening_2021_10_25_standard'])==STANDARD and tuple(h['opening_2021_10_25_two_way'])==TWO_WAY and h['standard_count']==14 and h['two_way_count']==2 and h['MIA_owned_2021_draft_picks']==0,'Reviewed named roster source changed')
    need(set(cl['public_contract_rows'])==set(STANDARD),'Reviewed14 public contract rows changed')
    w=cl['six_category_apron_witness'];need(w['reported_salary_plus_known_adjustments_usd']==136439559 and w['slack_before_any_extra_unreported_obligation_usd']==6562441 and w['reported_apron_usd']==143002000,'Consumed legal price interval changed')
    need(at['selected_atom']['fictional_NPC_direction_selected']and at['selected_atom']['ordered_actions'][2]=='One consented simultaneous assignment sends Dragic and Precious to Toronto and Lowry to Miami','Named prior atom changed')
    return {'source_existing_reviewed_family':CLOSURE,'atom_source':ATOM,'new_original_contract_collection':False,'CBA':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(base.CBA),'raw_sha256':base.CBA_SHA,'normalized_fitz_page_sha256':{str(n):hashlib.sha256(t.encode()).hexdigest()for n,t in tx.items()}},'source_scope':'Reuse reviewed21raw/public14price/currentbonus/sixcategory route, no new private absence or earlier ancestor revalidation'}

def contracts(cl):
    return [{'player':p,'route':'RETAIN_SELECTED_REVIEWED_PUBLIC_UPC_FAMILY','public_price_bonus_row':deepcopy(cl['public_contract_rows'][p]),'all_original_and_prior_Gamma_preserved':True,'new_contract_selected_here':False,'actual_receipt':None}for p in STANDARD]

def assert_contracts(rows,cl):
    need(POLICY==POLICY_FIXED and len(rows)==14 and {r['player']for r in rows}==set(STANDARD),'Returned registration/authority altered')
    for r in rows:need(r=={'player':r['player'],'route':'RETAIN_SELECTED_REVIEWED_PUBLIC_UPC_FAMILY','public_price_bonus_row':cl['public_contract_rows'][r['player']],'all_original_and_prior_Gamma_preserved':True,'new_contract_selected_here':False,'actual_receipt':None},'Returned reviewed contract price/Gamma altered')

def role_blocks():
    rem={r:{p:m//2 for p,m in ps.items()}for r,ps in ROLE_MINUTES.items()};roles=list(rem);out=[]
    for i in range(24):
        if i==0:a=deepcopy(STARTERS)
        else:
            total=Counter()
            for ps in rem.values():total.update(ps)
            forced={p for p,v in total.items()if v==24-i}
            def find(k,a):
                if k==5:return a if forced<=set(a.values())else None
                r=roles[k]
                for p in sorted(rem[r],key=lambda p:(p not in forced,-rem[r][p],p)):
                    if rem[r][p]>0 and p not in a.values():
                        b=find(k+1,{**a,r:p})
                        if b:return b
                return None
            a=find(0,{})
        need(a is not None,'Five-player role matching unavailable')
        for r,p in a.items():need(rem[r].get(p,0)>0,'Role remainder invalid');rem[r][p]-=1
        out.append({'start_second':i*120,'end_second':(i+1)*120,'seconds':120,'positions':a})
    need(all(v==0 for ps in rem.values()for v in ps.values()),'Role minutes incomplete');return out

def assert_roles(blocks):
    need(ROLE_MINUTES==ROLE_FIXED and digest(blocks)==ROLE_SHA,'Selected chronology changed');seconds=Counter();rs={r:Counter()for r in ROLE_FIXED}
    for i,b in enumerate(blocks):
        need((b['start_second'],b['end_second'],b['seconds'])==(i*120,(i+1)*120,120)and len(set(b['positions'].values()))==5,'Clock/identity invalid')
        for r,p in b['positions'].items():seconds[p]+=120;rs[r][p]+=120
    need(dict(rs)=={r:Counter({p:m*60 for p,m in ps.items()})for r,ps in ROLE_FIXED.items()}and sum(seconds.values())==14400,'Role/source budget changed');return seconds

def build(root=ROOT):
    src=sources(root)
    for p,h in PINS.items():need(sha(root/p)==h and src[p]==direct(root,p),'Returned physical source differs '+p)
    raw=support(src);cl=src[CLOSURE];at=src[ATOM];rows=contracts(cl);assert_contracts(rows,cl);standard=list(STANDARD)
    need(not any(x['conditional_final_draft_rights_holder']=='MIA'for x in src[base.DRAFT]['selected_rows']),'Miami source draft holder changed')
    blocks=role_blocks();seconds=assert_roles(blocks);active=sorted(set(seconds)|{'Udonis Haslem','Omer Yurtseven'});inactive=sorted(set(standard)-set(active));need(len(active)==12 and len(inactive)==2 and set(active)<=set(standard)and 'Victor Oladipo'in inactive,'Dated active nomination changed')
    r={'blocks':blocks,'player_seconds':dict(seconds),'active':active};prepared=[];names=set()
    for gid in IDS:
        g=next(x for x in src[det.CAL]if x['game_id']==gid);h=next(x for x in src[base.HEALTH]['selected_dates']if x['game_id']==gid);need(g['opponent']=='MIA'and(g['date'],g['home'],g['away'])==(h['date'],h['home'],h['away']),'Exact date/state changed')
        c=next(x for x in src[base.CHI]['rows']if x['game_id']==gid and x['state']==h['selected_chicago_state']);need(c['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI health altered')
        pair=base.paired(c,r);joint=base.assert_pair(c,r,pair);joint['MIA']=joint.pop('NYK')
        for b in pair:b['MIA']=b.pop('NYK')
        need(set(joint['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive inactive')
        need(not(set(joint['MIA'])&set(joint['CHI'])),'Actor shared across teams')
        for ps in joint.values():names.update(ps)
        prepared.append((g,h,pair,joint))
    need(src[base.AUTH]['selected']['selected_date_rows']['sha256']==PINS[base.HEALTH],'Selected authority changed')
    rates=det.expected_ratings({det.BPM:src[det.BPM]},names-{'Coby','Dewayne Dedmon'})
    need(not any(x['nba_player']=='Dewayne Dedmon'for x in src[det.BPM]),'Dedmon source n0 changed')
    rates['Dewayne Dedmon']={'exact_fraction':'0','method':'SELECTED_FICTIONAL_EB_N0_NEUTRAL_LIMIT','historical_BPM':None,'observed_minutes':None,'selected_pseudo_observation_minutes':0,'source_row_exists':False,'actual_ability_zero_certified':False,'fictional_working_coefficient_selected':True,'source_boundary':'MissingMarch25NBArow, selectedneutraln0prior not pastcareer ability zero or currenthealth certificate; no later2021/22 stats imported'}
    if 'Coby'in names:rates['Coby']=det.expected_ratings({det.BPM:src[det.BPM]},{'Coby White'})['Coby White']
    for p in set(rates)&set(src[det.OUT]['player_ratings']):need(rates[p]==src[det.OUT]['player_ratings'][p],'Shared selected singleBPM changed')
    games=[]
    for g,h,pair,joint in prepared:
        impact={t:sum(Fraction(rates[p]['exact_fraction'])*sec/2880 for p,sec in ps.items())for t,ps in joint.items()};y=(date.fromisoformat(g['date'])-timedelta(days=1)).isoformat();back={t:any(x['date']==y and t in(x['home'],x['away'])for x in src[det.LEAGUE])for t in joint};home=2 if g['home']=='CHI'else-2;fatigue=Fraction(1,2)*(int(back['MIA'])-int(back['CHI']));margin=impact['CHI']-impact['MIA']+home+fatigue;need(margin!=0,'Separate OT required for tie')
        games.append({'game_id':g['game_id'],'date':g['date'],'home':g['home'],'away':g['away'],'CHI_state':h['selected_chicago_state'],'MIA_active':active,'MIA_inactive':inactive,'simultaneous_segments':pair,'player_seconds':{t:dict(sorted(ps.items()))for t,ps in joint.items()},'team_BPM_per100':{t:float(v)for t,v in impact.items()},'home_effect_CHI_per100':home,'back_to_back':back,'fatigue_effect_CHI_per100':float(fatigue),'exact_CHI_minus_MIA_impact_fraction':str(margin),'CHI_minus_MIA_impact_per100':float(margin),'selected_regulation_winner':'CHI'if margin>0 else'MIA','score':None,'overtime_selection':None})
    return {'id':'CHICAGO_MIAMI_2021_22_SELECTED_KEEPER_RESULTS','baseline_main':BASELINE,'status':'SELECTED_REVIEWED_MIA_LEGAL_FAMILY_FOUR_RESULTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_support':raw,'selected_policy':deepcopy(POLICY),'lawful_contract_family':rows,'selected_registration':{'standard':standard,'TW':list(TWO_WAY),'STD':14,'TW_count':2,'active':active,'inactive':inactive,'TW_NBA_nominations':[],'zero_minutes_not_clinical_absence':True,'all_original_waived_camp_stretch_FA_unsigned_exception_Gamma_retained':True},'selected_role_minutes':deepcopy(ROLE_FIXED),'selected_role_blocks':blocks,'selected_ratings':rates,'selected_games':games,'reviewed_apron_source_reused':{'source':CLOSURE,'adjusted_TeamSalary':136439559,'apron':143002000,'family_slack':6562441,'old_Gamma_private_zero_certified':False,'selected_new_contract_delta_here':0,'applies_at_selected_dates_if_no_new_intervening_cost_event':True},'interval':'Only Nov27/Dec11/Feb28/Apr2 same namedfamily no selected intervening contract/roster/cost event, not original COVID/thumb/contact calendar','butterfly_handoff':['LowryMIA/DragicPreciousTOR priorselectedatom carried, no secondassignment or new fees. MarkieffMIA andCalebMIA TW cannot duplicate formerLAL/CHA UPC.','TuckerMIA selectedbeforeBKN? currentclosed14 controls; no currentMIL keeper retention automatically added. NoMIA2021draft rights/tender selected.','No BjelicaGSW/NunnLAL/IguodalaGSW/ArizaLAL contracts restoredhere; sourceexpired/remove priorGamma stillretained.','Oladipo workingabsent on4dates; Bam/Morris/Butler operatingavailable separatefiction, no automatichistoricalthumb/Jokiccontact/protocolmedicalcertificate.','No laterKZOKC/Garrettwaiver/Highsmithstandard event automatically imported; preservedTW2 not NBAactivated.'],'summary':{'selected_games':4,'CHI_wins':sum(g['selected_regulation_winner']=='CHI'for g in games),'MIA_wins':sum(g['selected_regulation_winner']=='MIA'for g in games),'STD':14,'TW':2,'active_each':12,'positive_each':10,'blocks_each':24,'clock_seconds_each':2880,'team_player_seconds_each':14400},'certification':{'selected_fictional_lawful_NPC_family':True,'selected_dated_working_health_and_results':True,'independent_review_completed':False,'actual_private_receipts_medical_or_exact_price_certified':False,'whole_private_teamcost':False,'new_author_lock':False,'whole82_or_macro3':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}}

def markdown(d):
    a=['# Miami · 네 날짜 선택 결과','','이미 검문된 Miami 법적 가족을 직접 소비한 감독·건강·단일 BPM 결과. 독립 검문 대기.','','|날짜|키|CHI 상태|승자|CHI 영향/100|','|---|---|---|---|---|']
    for g in d['selected_games']:a.append(f"|{g['date']}|{g['game_id']}|{g['CHI_state']}|{g['selected_regulation_winner']}|{g['CHI_minus_MIA_impact_per100']:.9f}|")
    a+=['','[검문된 apron 가족](../research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json)과 [선택된 Lowry 원자거래](../research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json)를 물리 JSON source필드로 직접소비한다. 21raw/14가격/원Gamma/6범주 전체를다시수집하거나새UPC·가격·예외를선택하지않는다. 136,439,559/apron143,002,000/여유6,562,441의공개가족·추가의무여유조건은유지되며실제private원장이0이라는증명은아니다.','',
    '14STD2TW를그대로유지하고 현재LowryMIA/DragicPreciousTOR 소유/원fee·bonus·term을두번째양도하지않는다. Herro원2021bonus5,000 포함 등14가격행을exactjoin한다. MarkieffMIA와CalebMIA TW가다른LAL/CHA 기존UPC와동시중복될수없다. TW는캡제외와cash보상이별개이고이번활성0/새conversion0. MIA권리2021draft0·Tender0,원남은한STD자리강제충원하지않는다.','',
    'usual5 Lowry/Robinson/Butler/Tucker/Bam. Lowry30/Vincent18/Robinson26/Herro30/Butler34/Strus14/Tucker26/Morris14/Bam34/Dedmon14=240. PG Lowry30/Vincent18,SG Robinson26/Herro22,SF Butler26/Herro8/Strus14,PF Tucker26/Morris14/Butler8,C Bam34/Dedmon14. 양수10+Haslem/Yurtseven active12, inactiveOladipo/Okpala2. 원수학fixture가아닌선택감독24개2분블록과CHI동시시계/포지션/선수초 직접검문.','',
    'Oladipo는4날짜작업부재, 나머지양수선수는개별작업가용성선택이며임상·백신·실수락인증은아니다. 원Bam12월thumb/Morris11월Jokic접촉/Butler프로토콜사건을독립상대세계에자동복사하지않는다. 실제MIA전82경기건강이나다른날짜역할불변을확정하지않는다. 원KZOKC/Garrettwaiver/Highsmith표준계약도새선택이아니다.','',
    'Dedmon은March25원행부재의가상EB n0중립0이며과거커리어능력0·현재실력인증이아니다. 현재CHI Mark32/Caruso18/P32·날짜별선택건강, 동일단일March25 EB/BPM·홈2·연전.5,원역사점수·OT자동복사0. score/OTnull,새stat/honors/우승경로선택0.','',
    '## 7행 진행','','|번호|작업|상태|','|---|---|---|','|1|2020 드래프트 연쇄|완료|','|2|2020–21|완료|','|3|2021–23|MIA4 결과 작업선택·독립검문 대기|','|4|장기 커리어|미완|','|5|결말·구조|미완|','|6|집필 규격·Pack|현행 기능등록기 참조·Pack0|','|7|통합·최종 승인|CLOSED|','',
    '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 남은 큰묶음5,6번까지4. v0.30 PARTIAL/CLOSED/원고0. whole82/wholemacro3/실제기관·의학·사적비용인증false.','']
    return '\n'.join(a)

def validate(d,root=ROOT):
    try:return []if d==build(root)else['Saved IND differs from physical source-bound construction']
    except(ValueError,KeyError,StopIteration)as e:return[str(e)]
def self_test():
    controls=[];old=contracts
    def wrong(cl):
        x=old(cl);next(r for r in x if r['player']=='Markieff Morris')['actual_receipt']=True;return x
    with patch(__name__+'.contracts',wrong):
        try:build()
        except ValueError:controls.append('RETURNED_ACTUAL_UPC_RECEIPT')
        else:raise AssertionError('FalsePASS actual receipt')
    loader=physical
    def wrongsource(root,p):
        x=loader(root,p)
        if p==CLOSURE:x['public_contract_rows']['Tyler Herro']['reported_likely_usd']=0
        return x
    with patch(__name__+'.physical',wrongsource):
        try:build()
        except ValueError:controls.append('RETURNED_PHYSICAL_BONUS_REMOVAL')
        else:raise AssertionError('FalsePASS bonus')
    return controls

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');a.add_argument('--self-test',action='store_true');v=a.parse_args();d=build()
    if v.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if v.check:need(direct(ROOT,OUT)==d and text(ROOT/MD)==markdown(d),'IND currentness stale')
    print(json.dumps({'current':True,'summary':d['summary'],'games':[{k:g[k]for k in('game_id','date','CHI_state','selected_regulation_winner','CHI_minus_MIA_impact_per100')}for g in d['selected_games']],'writer_controls':self_test()if v.self_test else None},ensure_ascii=False))
if __name__=='__main__':main()
