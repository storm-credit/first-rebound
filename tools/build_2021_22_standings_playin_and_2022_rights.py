"""Joint selected records -> source-rule seeds -> six fictional play-ins -> typed2022 rights.

No ancestor builds; no historical seed, draw, player or owner copied. Draft ties
and the four lottery draws remain explicit finite parameters.
"""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
from copy import deepcopy
from unittest.mock import patch
import argparse,hashlib,json,fitz
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2021_22_standings_playin_and_2022_rights.py'
OUT='simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json';MD=OUT[:-5]+'.md'
GLOBAL='simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json'
GLOBALTOOL='tools/build_2021_22_global_selected_regular_results.py'
PRIMARY='research/NBA_2022_STANDINGS_AND_DRAFT_PRIMARY_OBSERVATIONS_2026_10_07.json'
RIGHTS='research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json'
FILES=(GLOBAL,GLOBALTOOL,PRIMARY,RIGHTS)
PINS={'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '93264d2dff86a58ad10ca6975315c6c2167961f94f2517b6f5f79fa3113f2af8', 'tools/build_2021_22_global_selected_regular_results.py': '98d0ad39c771cf75724e37d9f85bdd1450bc393bcf1ddc6d627d757efec01b61', 'research/NBA_2022_STANDINGS_AND_DRAFT_PRIMARY_OBSERVATIONS_2026_10_07.json': '165e240a765ac07d98253b348654022978ef7e034c90bcfbd874694cd19dfda6', 'research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json': 'bf8087a89af09a817c0a3eb5d4df906a906575a56016c873912db00eccdca9db'};MEANING={'simulation/NBA_2021_22_GLOBAL_SELECTED_REGULAR_RESULTS.json': '48d257db6ab6986a3acc1b5d8095ebdd8a9712fce3f06b93133a91c4d7740718', 'tools/build_2021_22_global_selected_regular_results.py': 'a9c0ec939d2d3040090da77213abf61fe3f8c6cdb4f93543354e059469e25ca3', 'research/NBA_2022_STANDINGS_AND_DRAFT_PRIMARY_OBSERVATIONS_2026_10_07.json': '676777036162a994aff6dbff69d5e7cdcd599d033329e59e52782755e7676e1e', 'research/CHICAGO_2022_NAMED_DRAFT_RIGHTS_COST_REFINEMENT_2026_10_07.json': '3517d47b6c788e8670506aea8797e90f1bcc625e3a0f80daf7f9cb77b3d4adec'}
DIVISIONS={'Atlantic':['BOS','BKN','NYK','PHI','TOR'],'Central':['CHI','CLE','DET','IND','MIL'],'Southeast':['ATL','CHA','MIA','ORL','WAS'],'Northwest':['DEN','MIN','OKC','POR','UTA'],'Pacific':['GSW','LAC','LAL','PHX','SAC'],'Southwest':['DAL','HOU','MEM','NOP','SAS']}
CONF={t:('EAST'if d in ('Atlantic','Central','Southeast')else 'WEST')for d,ts in DIVISIONS.items()for t in ts}
DIV={t:d for d,ts in DIVISIONS.items()for t in ts}
POLICY={'new_playin_lawful_contract_and_operational_family':'Extend retained live/selected legalUPC/allGamma/no-new-event family April11–15 within salaryyear2021–22. Source generation April10 endpoint remains historical scope, not silently rewritten.',
 'CHI_playin_state':'COBY_OUT continues source lastApr10 operational absence; new five-day delegated working health choice, no medical claim or return invented.',
 'others':'Use last regular selected role/active family. All active participants STANDARD; no TW postseason activation/newUPC.',
 'method':'Same March25 EB/BPM+home2+B2Bhalf. New scores/OT absent. Not probability calibration or actual future ability.',
 'second_round_tied_order_reverse_first':True,'independent_second_round_draw':False,'draft_tie_draw_selected':False,'lottery_draw_selected':False,'all2022_control60_certified':False,
 'exact_Chicago_second_swap_exercise_selected':False,'new_author_lock_or_title':False}
FIXED=deepcopy(POLICY)
def need(x,m):
    if not x:raise AssertionError(m)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def direct(root,p):return json.loads(text(root/p))if p.endswith('.json')else text(root/p)
def physical(root,p):return direct(root,p)
def sources(root):
    need(POLICY==FIXED,'Continuation policy changed')
    out={}
    for p in FILES:
        need(sha(root/p)==PINS[p],'Source stale: '+p)
        v=physical(root,p);need(v==direct(root,p)and digest(v)==MEANING[p],'Returned source changed: '+p);out[p]=v
    raw=next(s for s in out[PRIMARY]['source_observations'] if s['id']=='BYLAWS2019_DRAFT_ORDER')
    p=Path(raw['cache_path'])
    need(hashlib.sha256(p.read_bytes()).hexdigest()==raw['raw_sha256'],'Draft-order raw source changed')
    with fitz.open(p) as doc:
        for page,h in raw['PDF1based_text_sha256'].items():
            need(hashlib.sha256(doc[int(page)-1].get_text().encode()).hexdigest()==h,'Draft-order page changed')
        need('inverse order' in doc[86].get_text() and 'second round' in doc[86].get_text(),'Draft tied reverse relation absent')
    return out
def pct(team,opponents,rows):
    games=[g for g in rows if team in(g['home'],g['away'])and (g['away']if g['home']==team else g['home'])in opponents]
    need(len(games)>0,'No games for tie criterion')
    return Fraction(sum(g['selected_regulation_winner']==team for g in games),len(games))
def resolve(group,rows,division_winners,trace,scope):
    if len(group)==1:return group
    criteria=['head_to_head','division_winner','same_division_record','conference_record']if len(group)==2 else ['division_winner','head_to_head_group','same_division_record','conference_record']
    for criterion in criteria:
        if criterion=='same_division_record'and len({DIV[t]for t in group})!=1:continue
        values={}
        for t in group:
            if criterion=='division_winner':values[t]=Fraction(int(t in division_winners))
            elif criterion.startswith('head_to_head'):values[t]=pct(t,set(group)-{t},rows)
            elif criterion=='same_division_record':values[t]=pct(t,set(DIVISIONS[DIV[t]])-{t},rows)
            else:values[t]=pct(t,{u for u in CONF if CONF[u]==CONF[t]and u!=t},rows)
        trace.append({'scope':scope,'group':list(group),'arity':len(group),'criterion':criterion,'values':{t:str(v)for t,v in values.items()}})
        buckets=defaultdict(list)
        for t,v in values.items():buckets[v].append(t)
        if len(buckets)>1:
            # Apply partial separation, then restart each unresolved group at its
            # appropriate two-team/multi-team first criterion.
            return [t for v in sorted(buckets,reverse=True)for t in resolve(sorted(buckets[v]),rows,division_winners,trace,scope)]
    raise AssertionError('Current tie needs later eligible-postseason/points/draw input: '+repr(group))
def rankings(globalv):
    rows=globalv['rows'];records=globalv['team_records'];trace=[];leaders=[]
    for d,ts in DIVISIONS.items():
        mx=max(records[t]['wins']for t in ts);group=sorted(t for t in ts if records[t]['wins']==mx)
        leaders.append(resolve(group,rows,set(),trace,'DIVISION:'+d)[0])
    seeds={}
    for c in ('EAST','WEST'):
        buckets=defaultdict(list)
        for t in records:
            if CONF[t]==c:buckets[records[t]['wins']].append(t)
        order=[t for w in sorted(buckets,reverse=True)for t in resolve(sorted(buckets[w]),rows,set(leaders),trace,c)]
        seeds[c]=[{'seed':i+1,'team':t,'wins':records[t]['wins'],'losses':records[t]['losses']}for i,t in enumerate(order)]
    return seeds,leaders,trace
def assert_rankings(seeds,leaders,trace,g):
    need(len(leaders)==6 and set(leaders)<=set(CONF),'Division leader domain')
    # Direct current-source checks of the only tied seed family. This guard
    # consumes source winners/ratios independently of returned resolve().
    tied={'LAC','LAL','PHX'};rows=g['rows']
    need(all(g['team_records'][t]['wins']==64 for t in tied),'Current64-tie source changed')
    need(all(pct(t,tied-{t},rows)==Fraction(1,2)for t in tied),'Current group H2H changed')
    need(pct('LAC',set(DIVISIONS['Pacific'])-{'LAC'},rows)==Fraction(11,16),'PacificLAC numerator changed')
    need(all(pct(t,set(DIVISIONS['Pacific'])-{t},rows)==Fraction(10,16)for t in ('LAL','PHX')),'Pacific remaining tie changed')
    need(pct('PHX',{t for t in CONF if CONF[t]=='WEST'}-{'PHX'},rows)==Fraction(42,52)and pct('LAL',{t for t in CONF if CONF[t]=='WEST'}-{'LAL'},rows)==Fraction(41,52),'Remaining two-way conference ratio changed')
    need('LAC'in leaders and [r['team']for r in seeds['WEST']][1:4]==['LAC','PHX','LAL'],'Returned partial tie/restart changed')
    need(any(r['scope']=='WEST'and r['arity']==2 and set(r['group'])=={'LAL','PHX'}and r['criterion']=='head_to_head'for r in trace),'Partial two-way did not restart')
    for c,rs in seeds.items():
        need(len(rs)==15 and len({r['team']for r in rs})==15 and all(CONF[r['team']]==c for r in rs),'Seed ownership/domain changed')
        need([r['seed']for r in rs]==list(range(1,16)),'Seed numbering changed')
        need(all((r['wins'],r['losses'])==(g['team_records'][r['team']]['wins'],g['team_records'][r['team']]['losses'])for r in rs),'Returned seed record differs')
        need(all(rs[i]['wins']>=rs[i+1]['wins']for i in range(14)),'Seed record order changed')

def playin_game(key,day,home,away,g,played):
    views={}
    for t in (home,away):
        if t=='CHI':template='CHI:COBY_OUT'
        else:
            last=max((r for r in g['rows']if t in(r['home'],r['away'])),key=lambda r:r['date']);template=last['team_date_models'][t]['template']
        v=g['shared_role_templates'][template]
        need(set(v['positive_player_seconds'])<=set(v['active'])<=set(v['registration']['standard']),'Play-in participant is not source standard active')
        views[t]={'template':template,'active':v['active'],'positive_player_seconds':v['positive_player_seconds'],'new_operational_continuation_selected':True,'actual_medical_receipt':False}
    rates=g['selected_productivity_inputs'];sums={t:sum(Fraction(rates[p]['fraction'])*n/2880 for p,n in v['positive_player_seconds'].items())for t,v in views.items()}
    # No scheduled day immediately before Apr12/13/15 has the same team. This
    # is checked rather than inherited from the original observed games.
    prior={'2022-04-12':'2022-04-11','2022-04-13':'2022-04-12','2022-04-15':'2022-04-14'}[day]
    back={t:(t,prior)in played for t in views};m=sums[home]-sums[away]+2+Fraction(int(back[away])-int(back[home]),2)
    need(m!=0,'Play-in exact proxy tie')
    return {'id':key,'date':day,'home':home,'away':away,'team_models':views,'exact_home_margin':str(m),'winner':home if m>0 else away,'loser':away if m>0 else home,'back_to_back':back,'score':None,'overtime':None,'actual_receipt':False}
def assert_playin(r,key,day,home,away,g,played):
    need((r['id'],r['date'],r['home'],r['away'])==(key,day,home,away),'Returned play-in identity changed')
    totals={}
    for t in (home,away):
        k='CHI:COBY_OUT'if t=='CHI'else max((q for q in g['rows']if t in(q['home'],q['away'])),key=lambda q:q['date'])['team_date_models'][t]['template']
        v=g['shared_role_templates'][k];expected={'template':k,'active':v['active'],'positive_player_seconds':v['positive_player_seconds'],'new_operational_continuation_selected':True,'actual_medical_receipt':False}
        need(r['team_models'][t]==expected,'Returned play-in role/health/class altered')
        totals[t]=sum(Fraction(g['selected_productivity_inputs'][p]['fraction'])*n for p,n in v['positive_player_seconds'].items())/2880
    need(not any(r['back_to_back'].values()),'Unexpected play-in B2B')
    m=totals[home]-totals[away]+2
    need(r['exact_home_margin']==str(m)and(r['winner'],r['loser'])==((home,away)if m>0 else(away,home)),'Returned play-in outcome changed')
    need(r['score']is None and r['overtime']is None and r['actual_receipt']is False,'Actual play-in certificate promoted')

def build(root=ROOT):
    src=sources(root);g=src[GLOBAL];need(g['summary']['league_games']==1230 and g['summary']['original_CHI_results_conserved']==82,'Global source domain changed')
    obs=src[PRIMARY];need(obs['calendar_projection']=={'regular_end':'2022-04-10','seven_eight':'2022-04-12','nine_ten':'2022-04-13','final':'2022-04-15','playoffs_begin':'2022-04-16','lottery':'2022-05-17','draft':'2022-06-23'},'Primary calendar projection changed')
    seeds,leaders,trace=rankings(g);assert_rankings(seeds,leaders,trace,g)
    played={(t,r['date'])for r in g['rows']for t in(r['home'],r['away'])};matches=[];final={}
    for conf,rows in seeds.items():
        ts={r['seed']:r['team']for r in rows};q=[]
        for phase,day,h,a in [('78','2022-04-12',ts[7],ts[8]),('910','2022-04-13',ts[9],ts[10])]:
            key=conf+':'+phase;r=playin_game(key,day,h,a,g,played);assert_playin(r,key,day,h,a,g,played);q.append(r);played.update((t,day)for t in(h,a))
        r=playin_game(conf+':FINAL','2022-04-15',q[0]['loser'],q[1]['winner'],g,played);assert_playin(r,conf+':FINAL','2022-04-15',q[0]['loser'],q[1]['winner'],g,played);q.append(r);matches.extend(q)
        final[conf]=[{'seed':r['seed'],'team':r['team']}for r in rows[:6]]+[{'seed':7,'team':q[0]['winner']},{'seed':8,'team':r['winner']}]
    eligible=set(t for rs in final.values()for t in[r['team']for r in rs]);lottery=sorted(set(CONF)-eligible,key=lambda t:(g['team_records'][t]['wins'],t))
    need(len(lottery)==14 and len(eligible)==16 and len(matches)==6,'Postseason/lottery partition changed')
    def draft_buckets(teams,offset,round_number):
        groups=defaultdict(list)
        for t in teams:groups[g['team_records'][t]['wins']].append(t)
        out=[];index=offset
        for w in sorted(groups):
            ts=sorted(groups[w]);out.append({'wins':w,'origins':ts,'possible_pre_draw_ranks':list(range(index,index+len(ts))),'same_record_draft_drawing_required':len(ts)>1 and round_number==1,'first_round_tie_order_parameter_reference':('FIRST_TIE_'+str(w)) if len(ts)>1 else None,'second_round_tied_order_is_reverse_first':len(ts)>1 and round_number==2,'independent_second_round_draw':False});index+=len(ts)
        return out
    first=draft_buckets(eligible,15,1);second=draft_buckets(set(CONF),31,2)
    chi_first=next(r['possible_pre_draw_ranks']for r in first if 'CHI'in r['origins'])
    second_ranges={t:r['possible_pre_draw_ranks']for r in second for t in r['origins']}
    claims=src[RIGHTS]['positive_claim_bridge'];need(claims[0]['id']=='CHI2022_FIRST'and claims[0]['count_upper']==1 and claims[1]['id']=='CHI2022_COMPOSITE_SECOND'and claims[1]['count_upper']==1,'Named Chicago cardinality/source claims changed')
    rights={'CHI_first':{'origin':'CHI','holder_before_new_offseason_assignment':'CHI','qualified_for_playoffs':True,'pick_rank_domain':chi_first,'exact_rank':None,'same_record_peer':'GSW','coupled_first_second_rank_pairs':[[17,48],[18,47]],'new_pick_assignment':False},'CHI_second':{'count':1,'origin_domains':{t:second_ranges[t]for t in ('CHI','DET','LAL')},'original_2018_CHI_DET_exchange_preserved':True,'original_2019_LAL_comparison_exchange_preserved':True,'comparison_function':'If applicableWASexchange exercised, compare LAL against more favorableCHI/DET; otherwise preserve post2018 right. Existingpriority/eligibility limits unchanged.','second_tied_order_reverse_first':True,'independent_second_draw':False,'exact_exercise_flags':None,'exact_final_origin_rank_holder':None,'all_three_original_claims_conserved_not_added_or_deleted':True},'lottery_top4':'Four distinct draws among the14 modeled nonplayoff origins; exact draw unselected, original2022ORL/OKC/HOU/SAC order not copied.','full60_current_control_claim_map':'Remaining named portfolio consumer; originalhistorical2022holders not blindly copied.'}
    need(chi_first==[17,18]and second_ranges['CHI']==[47,48]and second_ranges['DET']==[32]and second_ranges['LAL']==[54,55,56,57],'Derived current Chicago rank domains changed')
    return {'id':'NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS','baseline_main':'d74ffd6efcdb18a07285a23ea7a59a014400c32b','status':'SELECTED_WORKING_SEEDS_SIX_PLAYIN_RESULTS_AND_TYPED2022_CHI_RIGHTS_INDEPENDENT_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_provenance':deepcopy(obs),'selected_policy':deepcopy(POLICY),'conference_seeds':seeds,'division_winners':leaders,'tiebreak_trace':trace,'playin_games':matches,'final_playoff_seeds':final,'nonplayoff_lottery_origins':lottery,'first_round_nonlottery_origin_buckets':first,'second_round_origin_buckets':second,'Chicago_2022_rights':rights,'summary':{'regular_games':1230,'conference_seed_rows':30,'division_winners':6,'playin_games':6,'playoff_qualifiers':16,'lottery_origins':14,'Chicago_first_rank_domain':chi_first,'lottery_draw_selected':False,'draft_tie_draw_selected':False},'model_limit':'Fixed productivity without variance produces high/low records. Not observed historical records, calibrated probability, realism forecast, MVP or title selection.','remaining_finite_inputs':['2022 four-lottery-draw and tied-record first-round order selection; second-round tied order is its reverse, never an independent draw; do not apply playoffH2H to draft ties.','Source-supported named existing2022 rights-control obligations beyondChicago; exact composite exercise if needed for named newdraftee, preserve allcounterpart claims.','2022 playoffs and two laterseason consumers; no unrelated private whole-ledger or absentreceipt gate.'],'certification':{'selected_legal_fictional_playin_family':True,'independent_review_completed':False,'actual_private_medical_receipts_or_contracts_certified':False,'full2022origin60_control60_executed':False,'new_draftee_Tender_UPC_or_author_lock':False,'whole_macro3_or_manuscript':False},'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}
def validate(v,root=ROOT):return []if v==build(root)else ['Saved seed/rights output differs from sources']
def markdown(v):
    a=['# 2021–22 순위·플레이인·2022 권리 조건 소비','',v['status'],'','[공식 동률규칙 PDF](https://ak-static-int.nba.com/wp-content/uploads/sites/2/2017/06/NBA_Tiebreaker_Procedures.pdf)의 첫4조건·부분해소 재시작만으로 현재시드동률을 닫았다. PDF발행2017과2021–22 검색원문 관측을 구분하고, 필요한원문·직접HTTP403미채택·web body관측을 `primary_provenance`에 보존했다. 원NBA 실제동률결과/시드복사0.','', 'Pacific LAC/LAL/PHX64승: 셋H2H4/8→division LAC11/16·나머지10/16으로divisionwinnerLAC; conference3way에서LAC부분분리→남은2way처음재시작→H2H2/4·division10/16동률→PHXconference42/52 vsLAL41/52. 원점수차없어도현재종료.','','| East | West |','|---|---|']
    a += [f"| {e['seed']} {e['team']} {e['wins']}–{e['losses']} | {w['seed']} {w['team']} {w['wins']}–{w['losses']} |"for e,w in zip(v['conference_seeds']['EAST'],v['conference_seeds']['WEST'])]
    a += ['','[2021–22 승인 PR](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/)과 [공식 날짜](https://www.nba.com/news/2022-nba-play-in-tournament-schedule)에서 4/12·13·15를 소비한다. 가상팀/승자만 새모델이다. retained계약/원Γ를같은salaryyear4/15까지명시연장하는가족·no-newmove·STANDARDactive만선택. CHI4/10COBY_OUT을5일연속하는새위임가용선택이며원82canon의새날짜인증은아니다.','','| 날짜 | 경기 | 선택승자 |','|---|---|---|']
    a += [f"| {r['date']} | {r['home']}–{r['away']} | {r['winner']} |"for r in v['playin_games']]
    a += ['','16qualified/14lottery를분리했다. [2022 공식 Draft 발표](https://www.nba.com/news/nba-draft-2022-ties-broken-official-release)의5/17·6/23과별도draftdraw를소비한다. 원역사추첨/순번은이월하지않는다. 기존 NBA규약 §7.02(c) 원PDF85–87에 따라 2R 동률순서는1R 동률선택의 역순이며 독립2R draw가 아니다. CHI1R17이면2R48, 1R18이면2R47; 64승4팀2R54–57도같은원순서의역순이다. Chicago자체1R은17/18, 복합2R은CHI47/48·DET32·LAL54–57 입력함수. 실제draw/optionexercise/finalholder는null이며세원청구를보존한다. Chicago에추가PORfirst/원DeRozan송출을만들지않는다.','',v['model_limit'],'','[현행로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 상태 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 | joint1230/순위/playin 작업선택;2022draw·권리·플레이오프/후속시즌 미완료 |','| 4 장기커리어 | 진행 |','| 5 전체구조 | 기능43/미완료 |','| 6 규격·ContextPack | source53/Pack0 |','| 7 통합·작가승인 | 미완료 |','','미완료 큰묶음5/6번까지4. v0.30 PARTIAL·CLOSED·원고0. 실제접수·원의료·사적계약 인증0, 전체60control·신인지명·UPC0.','']
    return '\n'.join(a)
def self_test():
    original=playin_game
    def bad(*a,**kw):
        v=original(*a,**kw);v['winner'],v['loser']=v['loser'],v['winner'];return v
    with patch(__name__+'.playin_game',side_effect=bad):
        try:build()
        except AssertionError:pass
        else:raise AssertionError('Returned play-in winner false-pass')
    return 1
def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
    if a.check:need(direct(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved seed/rights consumer stale')
    print(json.dumps({'current':True,'summary':v['summary'],'writer_controls':self_test()if a.self_test else None}))
if __name__=='__main__':main()
