"""Select four Toronto working regulation winners from dated lawful role families."""
from __future__ import annotations
import argparse,csv,hashlib,io,json
from collections import Counter
from datetime import date,timedelta
from fractions import Fraction
from pathlib import Path
from statistics import median
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_toronto_2021_22_selected_bpm_results.py'
OUT='simulation/CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS_2026_10_07.json'
MD=OUT[:-5]+'.md'
FILES=['simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json', 'research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv', 'simulation/CHICAGO_2021_22_CALENDAR.csv', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json', 'reviews/DET2_SELECTED_BPM_ROOT_INDEPENDENT_REVIEW_2026_10_07.json', 'reviews/TOR4_OPERATING_ROOT_INDEPENDENT_REVIEW_2026_10_07.json', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json']
PINS={'simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json': '676cb350acdd632dfc0a0b4cc82d8f1d085b243f21fe511caeb11bcc2b993118', 'research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json': '3007e4a2407a02e97998826c3cb8ee352ac2a75353b3c8c5822c16aa55fdbb48', 'simulation/CHICAGO_2021_22_DELEGATED_HEALTH_STATE_SELECTION.json': '274a35e163c7f6fd7f0d3e5494b3c46753aaf9900036676be935f17a9d538c32', 'simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json': '73d51b630e9c9d4ec31b7e3952906165589bd8c49a48bb07c79bdc9ad02e8fca', 'simulation/CHICAGO_2020_21_BPM_MAR25_SNAPSHOT.csv': '1d1455f7f4ddd73ef46e3ce16752b558c392ed2d284434acd295ca6659e937ef', 'simulation/CHICAGO_2021_22_CALENDAR.csv': 'c59ea19a5515d64ed03cae8e0481847b6572d4087bbcefef15896bb7a2489183', 'simulation/NBA_2021_22_REGULAR_BASELINE.csv': '92869bc987896a4172c5e54e3684d2604c5c24d828e9bcf3cc27af30ebc83644', 'simulation/CHICAGO_DETROIT_2021_TWO_DATE_SELECTED_BPM_RESULTS.json': '66c1c862a179648aa72dd81ff13a07345b36889043995ecb583ae57019618c80', 'reviews/DET2_SELECTED_BPM_ROOT_INDEPENDENT_REVIEW_2026_10_07.json': '00daab618ceaaabdab9e62c12150fd20e8c6115dd5fd27063d6b95a797042d17', 'reviews/TOR4_OPERATING_ROOT_INDEPENDENT_REVIEW_2026_10_07.json': 'fa2d027a0a74653848543d11c8ced037d6005245193e01f5537f40d56dc91c90', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json': '4ee9b74e37903a43b0bd50b35c7f24cbabdac13728097a848b553f874bbeef80'}
ALIASES={'LaVine':'Zach LaVine','LaMelo_pick4':'LaMelo Ball','Carter':'Wendell Carter Jr.','Caruso':'Alex Caruso','Markkanen':'Lauri Markkanen','Satoransky':'Tomas Satoransky','Young':'Thaddeus Young','Coby':'Coby White','OG Anunoby':'O.G. Anunoby'}
COMPARATORS=('Devin Vassell','Aaron Nesmith','Josh Green','Saddiq Bey','Desmond Bane')
IDS=('0022100046','0022100472','0022100430','0022101076')
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()
def physical(root,p):
    s=(root/p).read_text(encoding='utf-8-sig')
    return json.loads(s) if p.endswith('.json') else list(csv.DictReader(io.StringIO(s)))
def sources(root):return {p:physical(root,p) for p in FILES}
def observed(row):
    need(row['observed_through']=='2021-03-25','Postopening metric observation used')
    n=int(row['archive_minutes']);need(n>0,'No prior observed minutes')
    return Fraction(row['bpm'])*n/(n+1000)
def ratings(src,names):
    archive={r['nba_player']:r for r in src[FILES[4]]};need(len(archive)==len(src[FILES[4]]),'Duplicate metric name')
    novice=median(observed(archive[n]) for n in COMPARATORS);need(novice==Fraction(-728,1145),'Rookie comparison family changed')
    out={}
    for n in sorted(names):
        if n=='Protagonist':v=Fraction(-1,2);kind='DELEGATED_FICTIONAL_BASE_MINUS1_2_PLUS0_7_AT_FOUR_DATES'
        elif n in ('Chris Duarte','Josh Giddey'):v=novice;kind='DELEGATED_FICTIONAL_ROOKIE_MEDIAN_PROXY_NOT_NCAA_TRANSLATION'
        else:v=observed(archive[ALIASES.get(n,n)]);kind='PREOPENING_HISTORICAL_METRIC_USED_AS_FICTIONAL_PROXY'
        out[n]={'fraction':str(v),'rating':float(v),'classification':kind}
    return out
def selected_chi_clock(row):
    # Source order chosen only for these four dates; cut at quarter ends.
    end=0;out=[]
    for b in row['unordered_regulation_blocks']:
        todo=int(b['minutes']*60)
        while todo:
            n=min(todo,720-end%720);out.append({'start_second':end,'end_second':end+n,'seconds':n,'positions':b['positions']});end+=n;todo-=n
    need(end==2880,'CHI selected sequence not48min');return out
def paired(chi,tor):
    ends=sorted({0,2880}|{x['start_second'] for x in chi+tor}|{x['end_second'] for x in chi+tor})
    out=[];tot={'CHI':Counter(),'TOR':Counter()}
    for a,b in zip(ends,ends[1:]):
        r={'start_second':a,'end_second':b,'seconds':b-a,'quarter':a//720+1}
        need(b<=(a//720+1)*720,'Quarter crossed')
        for team,clock in [('CHI',chi),('TOR',tor)]:
            matches=[x for x in clock if x['start_second']<=a and x['end_second']>=b];need(len(matches)==1,'Clock gap or overlap')
            pos=matches[0]['positions'];need(set(pos)=={'PG','SG','SF','PF','C'} and len(set(pos.values()))==5,'Five-player position collision')
            r[team]=pos
            for p in pos.values():tot[team][p]+=b-a
        out.append(r)
    need(sum(x['seconds'] for x in out)==2880 and all(sum(v.values())==14400 for v in tot.values()),'Paired budget invalid')
    return out,{t:dict(v) for t,v in tot.items()}
def build(root=ROOT):
    for p,h in PINS.items():need(sha(root/p)==h,'Reviewed source changed: '+p)
    src=sources(root)
    need(set(src)==set(FILES),'Source domain changed')
    for p in FILES:need(src[p]==physical(root,p),'Returned source differs from physical source: '+p)
    tor,mia,health,minutes,bpm,cal,league,det,review,torreview,delegation=(src[p] for p in FILES)
    need(mia['selected_route_feasible_under_reported_contract_family'],'Miami selected lawful family not closed')
    need(not mia['actual_NBA_approval_or_contract_receipt_certified'],'Private receipt was fabricated')
    need(delegation['authority_type']=='AUTHOR_DELEGATED_SELECTION','Result delegation missing')
    need(torreview['verdict']=='ACCEPT_CONDITIONAL_NAMED_ROLE_AND_PUBLIC_SCREEN_ONLY' and torreview['input_normalized_sha256'][FILES[0]]==PINS[FILES[0]],'TOR role review missing')
    need(review['input_normalized_sha256'][FILES[7]]==PINS[FILES[7]],'Prior model review missing')
    need(tuple(x['game_id'] for x in tor['Chicago_Toronto_dates'])==IDS,'TOR4 dates changed')
    need(det['selected_policy']['protagonist_selected_effective_rating']==-0.5 and det['selected_policy']['method']=='BPM_MAR25_EB','Working metric policy changed')
    hc={x['game_id']:x for x in health['selected_dates']};calendar={x['game_id']:x for x in cal}
    prepared=[];names=set()
    for d in tor['Chicago_Toronto_dates']:
        gid=d['game_id'];h=hc[gid];c=calendar[gid];row=minutes['rows'][int(d['Chicago_source_pointer']['pointer'].split('/')[-1])]
        need((d['date'],d['home'],d['away'])==(c['date'],c['home'],c['away'])==(h['date'],h['home'],h['away']),'Calendar/health identity mismatch')
        need(row['game_id']==gid and row['state']==h['selected_chicago_state']==d['Chicago_selected_state'],'Wrong selected CHI state')
        need(row['player_minutes']==h['selected_regulation_player_minutes'],'Selected CHI minutes differ')
        cc=selected_chi_clock(row)
        # Independent per-second binding protects the explicitly selected
        # source order even when a returned helper preserves player totals.
        expected_ticks=[tuple(sorted(b['positions'].items())) for b in row['unordered_regulation_blocks'] for _ in range(int(b['minutes']*60))]
        returned_ticks=[tuple(sorted(b['positions'].items())) for b in cc for _ in range(b['end_second']-b['start_second'])]
        need(len(expected_ticks)==2880 and returned_ticks==expected_ticks,'Returned CHI positions/order differs from physical selected block sequence')
        pair,secs=paired(cc,d['Toronto_blocks'])
        need(secs['CHI']=={p:int(v*60) for p,v in h['selected_regulation_player_minutes'].items()} and secs['TOR']==d['Toronto_regulation_player_seconds'],'Paired positive seconds differ')
        need(set(secs['CHI'])<=set(h['working_chicago_operational_availability']['working_active_nominees']),'CHI positive player inactive')
        need(set(secs['TOR'])<=set(tor['selected_role']['active']),'TOR positive player inactive')
        need(not(set(secs['CHI'])&set(row['conditional_unavailable'])),'Unavailable CHI player used')
        names.update(secs['CHI']);names.update(secs['TOR']);prepared.append((d,h,pair,secs))
    rate=ratings(src,names);need(rate==ratings({p:physical(root,p) for p in FILES},names),'Returned rating differs from physical policy')
    games=[]
    for d,h,pair,secs in prepared:
        sums={t:sum(Fraction(rate[p]['fraction'])*n/2880 for p,n in ps.items()) for t,ps in secs.items()}
        yesterday=(date.fromisoformat(d['date'])-timedelta(days=1)).isoformat()
        back={t:any(x['date']==yesterday and t in (x['home'],x['away']) for x in league) for t in secs}
        home=Fraction(2 if d['home']=='CHI' else -2);fatigue=Fraction(1,2)*(int(back['TOR'])-int(back['CHI']));margin=sums['CHI']-sums['TOR']+home+fatigue
        need(margin!=0,'Tie proxy requires explicit overtime result design')
        games.append({'game_id':d['game_id'],'date':d['date'],'home':d['home'],'away':d['away'],'CHI_state':h['selected_chicago_state'],'paired_segments':pair,'player_seconds':secs,'team_weighted_BPM_fraction':{t:str(v) for t,v in sums.items()},'home_effect_fraction':str(home),'back_to_back':back,'fatigue_effect_fraction':str(fatigue),'exact_CHI_minus_TOR_impact':str(margin),'impact_float':float(margin),'selected_regulation_winner':'CHI' if margin>0 else 'TOR','score':None,'overtime_selection':None,'historical_OT_imported':False,'actual_medical_or_private_receipt_certified':False})
    return {'id':'CHICAGO_TORONTO_2021_22_SELECTED_BPM_RESULTS','baseline_main':'560e507db94f2d52c1fb56eeaccc62bb1675e726','source_sha256':{**PINS,SELF:sha(root/SELF)},'status':'FOUR_DELEGATED_FICTIONAL_WORKING_WINNERS_INDEPENDENT_REVIEW_PENDING','authority':'Existing delegated health/season implementation; not new author title/MVP/franchise lock.','policy':{'method':'BPM_MAR25_EB','protagonist_selected_rating_four_dates':-0.5,'fictional_Giddey_Duarte_rookie_proxy':'-728/1145','home':2,'b2b_penalty':0.5,'interaction':0,'CHI_chronology':'Physical block order cut at quarters, explicitly selected working order at four dates only','historical_score_or_OT_used':False,'selected_contract_family':'TOR named lawful minimum/RSC/option/TW and consented foreign-release/assignment routes; MIA selected reported apron family, no private receipt'},'player_ratings':rate,'rows':games,'summary':{'games':4,'CHI_model_wins':sum(g['selected_regulation_winner']=='CHI' for g in games),'TOR_model_wins':sum(g['selected_regulation_winner']=='TOR' for g in games)},'scope':'Absolute additive BPM working model, not calibrated score/probability, measured NCAA translation, clinical status, all82 standings or2022pick. Four dated priors selected; no whole-year growth/MVP/title path inferred.','whole_macro3_or_G16_certified':False,'manuscript_allowed':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED'}
def markdown(x):
    lines=['# Toronto 네 경기의 선택 정규시간 승패','','선택된 Miami 공개 계약 apron 가족과 Toronto T1의 명명된 법적 계약 경로를 소비한다. 네 날짜의 Chicago 건강/출전분과 양팀48/240분을 선택 시계로 연결했다.','','기존 DET 두 경기와 같은 BPM_MAR25_EB·홈2·연전0.5·주인공-0.5를 네 날짜 작업 설계로 선택한다. Giddey/Duarte는 전년도 다섯 신인의 median -728/1145를 쓰는 가상 proxy이며 실제 NCAA→NBA 환산이 아니다.','','| 날짜 | 키 | 작업 승자 | CHI 방향 impact/100 |','|---|---|---|---|']
    lines += [f"| {g['date']} | {g['game_id']} | {g['selected_regulation_winner']} | {g['impact_float']:.6f} |" for g in x['rows']]
    return '\n'.join(lines+['','실제 점수/연장/사적계약/건강/전체시즌·픽은 인증하지 않는다. v0.30 PARTIAL · 설계/원고 CLOSED · 원고0.',''])
def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--check',action='store_true');o=a.parse_args();x=build()
    if o.write:(ROOT/OUT).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(x),encoding='utf-8')
    if o.check:need(physical(ROOT,OUT)==x and (ROOT/MD).read_text(encoding='utf-8')==markdown(x),'Saved TOR4 result stale')
    print(json.dumps(x['summary']))
if __name__=='__main__':main()
