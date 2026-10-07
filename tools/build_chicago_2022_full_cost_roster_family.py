"""Finite FY22 public contract-category envelope, not a selected draft/roster.

The first-round universe is an economic over-envelope. It is never registered
as thirty Chicago players. Every signed contract consumes a real available
standard or two-way slot. Annual exception renunciation is a candidate action,
not an assertion that an exception was never incorporated.
"""
import argparse,copy,hashlib,itertools,json
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup
import build_chicago_2022_young_satoransky_roster_family as veterans

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_full_cost_roster_family.py'
OUT='research/CHICAGO_2022_FULL_COST_ROSTER_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
YS=veterans.OUT
M=veterans.MATRIX
SQ='simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json'
LEG='research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json'
SIM='research/SIMONOVIC_2021_22_RIGHTS_CONTINUATION_2026_10_07.json'
PINS={'research/CHICAGO_2022_YOUNG_SATORANSKY_ROSTER_FAMILY_2026_10_07.json':'9a1e49c1f0b9d3c95279ff675ac3c42c2a72384c8ed6d11cbeb917e5903ac363','tools/build_chicago_2022_young_satoransky_roster_family.py':'26542d4c198eb008acc5805abba9483e07cd32cd0e9b10e7974c979a84149611','research/CHICAGO_2022_COMBINED_CONTRACT_COST_MATRIX_2026_10_07.json':'1ba9e120872bdfab40f26fe2b56a6cff8c6265d94280ea84b5970ffb0d537d33','tools/build_chicago_2022_combined_contract_cost_matrix.py':'be8787d57ff56b60e93326b073321a32333aa4fef6d5f48a520ceb3957a65259','simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json':'11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312','research/CHICAGO_2021_A_FULL_COST_FAMILY_2026_10_07.json':'7244beff7a120c5ca246a04e72b61586f3cfbe245487d5fc6479f5245fd78d9f','research/SIMONOVIC_2021_22_RIGHTS_CONTINUATION_2026_10_07.json':'605e23f01c818b63a1782246824738c253591fd056bd8b66790c3409036a9937','simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json':'5632957e5e0a02f2d6f241900a3bef2c5790a8993c3494986e383ca3cbff1be3','AGENTS.md':'67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
MEANING={YS:'78ecbab1f5de3600c02f1ac9d25e44d5b1c71d696bbd4f1762d742f4500095c0',M:'01d05685fb87a936879c1bccc18e1b8dc0a1b49476faca884998ab97847dd268',SQ:'be717cd9279bd3709e5e0163aa358b0a118b8a762f816c4423b9aa9846fc47c6',LEG:'80e90c7fa4c21aa1b1f2e3462c58e3bfff6f324af94ca382ff9e76ff5336b0f5',SIM:'b25d2ce8d31e3dcff806182ac1605f13c82a3cf59ac47d2c63f10753cc85328e'}
TEMP=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-chi-fy22-whole-20261007')
CBA=veterans.CBA
CBA_SHA=veterans.CBA_SHA
PAGES=[30,31,54,55,56,57,58,74,75,206,208,209,210,211,212,213,216,217,221,231,232,233,239,240,241,294,295,302,303,304,305,306,307,309,310,311,312,313,317,318,319,412]
FIRST=11060000 # widened published 120%-scale ceiling, not exact agreed salary
MINIMUM=3000000 # fullcash one-year statutory minimum outer screen, not picked wage
TW_HOLD=1017781
APRON_SCREEN=156982000
ACTORS=('Devon Dotson','Tyler Cook')

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def load(p):return json.loads(text(p))
def source_inputs():return {p:load(p)for p in MEANING}

def policy():
    return {'new_important_contract_or_draft_selection':None,'new_assignment_or_sign_and_trade':False,
      'new_performance_signing_promotional_loan_buyout_on_minimum_forms':0,
      'renounce_unused_annual_exceptions_candidate':'2022-07-07 after preceding primary/veteran actions; VII6m2 written renunciation; not retroactive absence',
      'exception_usage_selected':False,'FY21_hardcap_carried':False,
      'generic_exception_premarket_normal_overreserve':20000000,'exception_apron_deemed_component':0,
      'no_new_waiver_settlement_grievance_or_cap_reducing_resolution_event_selected':True,
      'intervening_2021_08_11_to_2022_07_07_new_assignment_or_DPE_grant_selected':False,
      'legacy_reservation_preserved':20743601,
      'Simonovic_RT_fullcash_reservation':3000000,'Simonovic_tender_accepted':False,
      'Simonovic_no_NBA_UPC':True,'Simonovic_new_2022_foreign_agreement_selected':False,
      'TW_new_contract_term_seasons':1,'TW_new_options':False,'TW_no_standard_conversion_selected':True,
      'TW_2022_23_max_active_games':50,'TW_active_games_selected':None,
      'draft_first_rights_count_domain':[0,30],'draft_second_rights_count_domain':[0,30],
      'draft_first_current_Salary_plus_Unlikely_screen':FIRST,'new_statutory_minimum_fullcash_screen':MINIMUM,
      'draft_exact_holder_rank_player_and_terms':None,'new_draft_author_lock':False,
      'new_first_RequiredTender_candidate':'Valid ArticleVIII form, 80–120% applicable scale incl all performance; protection>=80%; team-signed timely July15; acceptance through regular-season opening. Actual delivery/acceptance null.',
      'new_second_RequiredTender_candidate':'One-Season no-bonus statutory minimum; valid X4a lateAugust/September5 window, accepts through at least October15. Offer not automatically signed; actual dates/receipt null.',
      'all_new_live_UPCs_after_moratorium':True,'named_live_identity_replacement_selected':False,
      'new_slots_are_identity_parameters_not_unsigned_players_registered':True}

POLICY=copy.deepcopy(policy())

def checked_policy():
    p=policy();assert p==POLICY,'Candidate mechanism/bonus/calendar/scope changed'
    assert p['draft_first_rights_count_domain']==[0,30] and p['draft_second_rights_count_domain']==[0,30]
    assert p['TW_new_contract_term_seasons']==1 and not p['TW_new_options']
    assert p['legacy_reservation_preserved']==20743601 and not p['FY21_hardcap_carried']
    return p

def observations():
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA
    with fitz.open(CBA)as d:
      ps=[{'PDF_1based':n,'text_sha256':hashlib.sha256(d[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()}for n in PAGES]
      assert 'fifteen (15) or more days'in d[316].get_text()
      assert 'Qualifying Offer is not made'in ' '.join(d[316].get_text().split())
      assert 'two (2), or third of three (3)'in ' '.join(d[311].get_text().split())
      assert 'Two-Way Player Salaries shall be excluded'in d[215].get_text()
      assert 'any time renounce'in d[239].get_text()
      assert 'Required Tender to a First Round'in d[240].get_text()
    pdf=TEMP/'pacers2022.pdf';raw=pdf.read_bytes();assert hashlib.sha256(raw).hexdigest()=='9b33b46bfe88d495a54ad21894fd67eb3b376aff048589a1e609eb82e79b3625'
    with fitz.open(pdf)as d:
      t=d[164].get_text();flat=' '.join(t.split());assert 'more than 50 games during the 2022-23'in flat and '$10.490 million'in flat
      guide={'id':'PACERS_2022_23_OFFICIAL_GUIDE','url':'https://cdn.nba.com/teams/uploads/sites/1610612754/2022/10/2022-23-Pacers-Media-Guide-compressed.pdf','cache_path':str(pdf),'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw),'PDF_1based':165,'printed_page':165,'text_sha256':hashlib.sha256(t.encode()).hexdigest(),'observed_scope':'2022–23 active12–15/regularbench8, TwoWay active50 prorated if late; cap/tax and annual MLE amounts. Old playoff/waiver paragraphs not adopted.'}
    fp=TEMP/'rookie2022HR.html';b=fp.read_bytes();assert hashlib.sha256(b).hexdigest()=='3dc556242780e306f324b9eba04f07f7a03172002415129f9a12f9c799f82bc3'
    soup=BeautifulSoup(b,'html.parser');table=soup.find('table');rows=[]
    for tr in table.find_all('tr')[1:]:
      cells=[c.get_text(' ',strip=True)for c in tr.find_all(['td','th'])]
      if len(cells)==6:rows.append(int(cells[1].replace('$','').replace(',','')))
    assert len(rows)==30 and max(rows)==11055120 and FIRST>=max(rows)
    rookie={'id':'HR_2022_CURRENT_ROOKIE_SCALE_REPORT','url':'https://www.hoopsrumors.com/2022/07/rookie-scale-salaries-for-2022-nba-first-round-picks.html','cache_path':str(fp),'raw_sha256':hashlib.sha256(b).hexdigest(),'raw_bytes':len(b),'classification':'SECONDARY_ORIGINAL_CAP_ANALYSIS_NOT_OFFICIAL_SCALE','locator':'Only table2022/23 column,30 reported120% rows; maximum11,055,120. No realplayer selected in this model.','reported_largest_120pct_firstyear':max(rows),'conditional_widened_screen':FIRST,'exact_statutory_rounding_certified':False}
    return {'CBA':{'url':veterans.RAW[0]['url']if False else 'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':CBA_SHA,'direct_pages':ps},'new_raw_observations':[guide,rookie],'failure_not_adopted':{'url':'https://basketball.realgm.com/nba/info/rookie_scale/2023','http_status':403,'bytes':5533,'body_adopted':False,'repeated':False},'reused_minimum_and_cap_observations':YS}

def tw_component(action,kind):
    # Γ has <4 YOS eligibility for T and15 qualifying days for Q branches.
    # STANDARD_QO includes consecutive-two/three-TW or TW-ineligible cases.
    if action=='NO_QO_KEEP_FA':return {'normal':TW_HOLD,'apron':0,'STD':0,'TW':0,'QO_live':False,'FRN_live':False}
    if action=='NO_QO_RENOUNCE_FA':return {'normal':0,'apron':0,'STD':0,'TW':0,'QO_live':False,'FRN_live':False}
    if action=='NEW_1YEAR_TW':
      if kind=='TW_INELIGIBLE_STANDARD_QO':return None
      return {'normal':0,'apron':0,'STD':0,'TW':1,'QO_live':False,'FRN_live':False}
    standard=kind!='ELIGIBLE_TW_QO'
    if action=='VALID_QO_UNACCEPTED':return {'normal':MINIMUM if standard else TW_HOLD,'apron':MINIMUM if standard else 0,'STD':0,'TW':0,'QO_live':True,'FRN_live':False}
    assert action=='ACCEPT_VALID_QO'
    return {'normal':MINIMUM if standard else 0,'apron':MINIMUM if standard else 0,'STD':int(standard),'TW':int(not standard),'QO_live':False,'FRN_live':False}

def checked_tw(action,kind):
    r=tw_component(action,kind)
    expected={'NO_QO_KEEP_FA':(TW_HOLD,0,0,0,False),'NO_QO_RENOUNCE_FA':(0,0,0,0,False)}
    if action in expected:e=expected[action]
    elif action=='NEW_1YEAR_TW':
      if kind=='TW_INELIGIBLE_STANDARD_QO':assert r is None;return None
      e=(0,0,0,1,False)
    else:
      s=kind!='ELIGIBLE_TW_QO';accepted=action=='ACCEPT_VALID_QO'
      e=((MINIMUM if s else 0)if accepted else (MINIMUM if s else TW_HOLD),MINIMUM if s else 0,int(s and accepted),int(not s and accepted),not accepted)
    assert tuple(r[k]for k in ('normal','apron','STD','TW','QO_live'))==e,'TW/QO form-to-component mismatch'
    assert not r['FRN_live'],'No unselected offer-sheet/FirstRefusalNotice may enter this family'
    return r

def tw_families():
    kinds=('ELIGIBLE_TW_QO','CONSECUTIVE_STANDARD_QO','TW_INELIGIBLE_STANDARD_QO')
    actions=('NO_QO_KEEP_FA','NO_QO_RENOUNCE_FA','NEW_1YEAR_TW','VALID_QO_UNACCEPTED','ACCEPT_VALID_QO')
    families=[]
    for kd,kc,ad,ac in itertools.product(kinds,kinds,actions,actions):
      d=checked_tw(ad,kd);c=checked_tw(ac,kc)
      if d is None or c is None:continue
      families.append({'id':'__'.join([kd,ad,kc,ac]),'Devon_Dotson':{'kind':kd,'action':ad,**d},'Tyler_Cook':{'kind':kc,'action':ac,**c},'normal_added':d['normal']+c['normal'],'apron_added':d['apron']+c['apron'],'STD_added':d['STD']+c['STD'],'TW_added':d['TW']+c['TW']})
    assert len(families)==196
    return families

def assert_tw_families(families):
    kinds=('ELIGIBLE_TW_QO','CONSECUTIVE_STANDARD_QO','TW_INELIGIBLE_STANDARD_QO')
    actions=('NO_QO_KEEP_FA','NO_QO_RENOUNCE_FA','NEW_1YEAR_TW','VALID_QO_UNACCEPTED','ACCEPT_VALID_QO')
    expected_ids=set()
    for kd,kc,ad,ac in itertools.product(kinds,kinds,actions,actions):
      if (kd=='TW_INELIGIBLE_STANDARD_QO' and ad=='NEW_1YEAR_TW')or(kc=='TW_INELIGIBLE_STANDARD_QO' and ac=='NEW_1YEAR_TW'):continue
      expected_ids.add('__'.join([kd,ad,kc,ac]))
    assert len(families)==196 and {f['id']for f in families}==expected_ids,'TW family domain/identity changed'
    for f in families:
      children=[]
      for actor in ('Devon_Dotson','Tyler_Cook'):
        c=f[actor];assert c['kind']in kinds and c['action']in actions
        expected=checked_tw(c['action'],c['kind'])
        assert expected is not None and c=={'kind':c['kind'],'action':c['action'],**expected},'Returned TW child differs from legal form'
        children.append(c)
      assert f['id']=='__'.join([children[0]['kind'],children[0]['action'],children[1]['kind'],children[1]['action']])
      for aggregate,component in [('normal_added','normal'),('apron_added','apron'),('STD_added','STD'),('TW_added','TW')]:
        assert f[aggregate]==sum(c[component]for c in children),'Returned TW aggregate differs from child legal components'

def rookie_component(first_signed,minimum_signed,remaining_STD,first_rights,second_rights,first_RT_live):
    assert type(first_signed)is int and type(minimum_signed)is int and first_signed>=0 and minimum_signed>=0
    assert first_signed+minimum_signed<=remaining_STD,'Unsigned/tender cannot hide a16th standard UPC'
    assert first_signed<=first_rights<=30 and minimum_signed<=2 and 0<=second_rights<=30
    unsigned=first_rights-first_signed
    # Any minimum signing can be an eligible FA or a held2R; no actual name/ownership chosen.
    normal=first_rights*FIRST+minimum_signed*MINIMUM
    apron=(first_signed+unsigned*int(first_RT_live))*FIRST+minimum_signed*MINIMUM
    return {'normal':normal,'apron':apron,'STD_added':first_signed+minimum_signed,'TW_added':0,'first_unsigned':unsigned,'first_tender_live':first_RT_live,'second_unaccepted_tender_cap_overreserve':second_rights*MINIMUM,'second_unaccepted_tender_is_asserted_statutory_charge':False}

def checked_rookie(nf,nm,slots,n1,n2,rt):
    r=rookie_component(nf,nm,slots,n1,n2,rt)
    assert r['normal']==n1*FIRST+nm*MINIMUM and r['apron']==(nf+(n1-nf)*int(rt))*FIRST+nm*MINIMUM,'Draft economic envelope changed'
    assert r['STD_added']==nf+nm and r['STD_added']<=slots
    assert r['first_unsigned']==n1-nf and r['second_unaccepted_tender_cap_overreserve']==n2*MINIMUM
    assert r['second_unaccepted_tender_is_asserted_statutory_charge']is False
    return r

def build():
    for p,h in PINS.items():assert sha(p)==h,'Unreviewed input '+p
    s=source_inputs()
    for p,h in MEANING.items():assert digest(s[p])==h,'Consumed source meaning changed: '+p
    v,m,sq,leg,sim=(s[p]for p in [YS,M,SQ,LEG,SIM])
    assert v['certification']['independent_review_completed'] and len(v['cases'])==12 and len(m['conditional_rows'])==165
    assert {t['player']for t in sq['two_way_working']}==set(ACTORS)
    assert all(t['working_term_seasons']==1 and t['working_signing_date']=='2021-08-13'for t in sq['two_way_working'])
    assert leg['whole_source_supported_cost_family_pass'] and leg['legacy_remaining']['aggregate_upper_usd']==20743601
    assert leg['categories'][5]['after_Aug11']==0 and leg['categories'][5]['status']=='FULL_NOMINAL_NORMAL_EXCEPTION_ENVELOPE_AND_EXPLICIT_RENOUNCE'
    assert 'explicit all-unused renounce August11' in leg['categories'][5]['basis']
    assert leg['categories'][3]['status']=='CLOSED_NAMED_PUBLIC_FAMILY_ALL_TEN_STATES'
    assert sim['summary']['full_target_all_admitted_NBA_clock_Gamma_conditionally_supported']
    p=checked_policy();obs=observations();tw=tw_families();assert_tw_families(tw)
    out=[];checks=0;valid=0;excluded=0
    for cell in v['joined_policy_cost_inputs']:
      end=cell['stages'][-1];base_std=end['signed_STD_range'];assert base_std[0]==base_std[1]
      summaries=[]
      for stage in cell['stages']:
        # Before actions: both completedTW FA amounts; annualexception full possible incorporation reserved.
        pre=stage['leaf_stage']==0
        tw_n=2*TW_HOLD if pre else max(t['normal_added']for t in tw)
        tw_a=0 if pre else max(t['apron_added']for t in tw)
        annual=20000000 if pre else 0
        # Over-envelope of current2022rights; does NOT certify Chicago owns30+30.
        normal=stage['normal_known_upper']+tw_n+30*FIRST+30*MINIMUM+MINIMUM+annual
        apron=stage['apron_known_upper']+tw_a+30*FIRST+30*MINIMUM+MINIMUM
        summaries.append({'date':stage['date'],'source_leaf_stage':stage['leaf_stage'],'source_STD_range':stage['signed_STD_range'],'normal_full_public_category_outer':normal,'apron_full_public_category_outer':apron,'annual_unused_normal_reservation':annual,'Simonovic_fullcash_tender_reservation':MINIMUM,'all_current_draft_universe_reserved_not_registered':True,'signed_roster_selected':False,'negative_screen_is_illegal':False})
      # Exact source165 conditional sums are reused below, not replaced by compact max.
      out.append({'case':cell['case'],'Carter':cell['Carter'],'Protagonist':cell['Protagonist'],'source_branches':end['all_source_branches'],'states':summaries,'signed_veteran_STD':base_std[0],'available_STD_before_TW_QO_or_new_rookies':15-base_std[0]})
    assert len(out)==192
    # Source branch algebra/current15 slots; finite contract action family, not all imaginary future transactions.
    slot_summaries={}
    for vc in v['cases']:
      bs=vc['post_primary_plus_veterans_STD'];key=str(bs)
      if key in slot_summaries:continue
      ss=[]
      for tf in tw:
        current=bs+tf['STD_added'];capacity=15-current
        if capacity<0:excluded+=1;continue
        for nf,nm in itertools.product(range(3),repeat=2):
          if nf+nm>capacity:excluded+=1;continue
          for rt in [False,True]:
            r=checked_rookie(nf,nm,capacity,30,30,rt)
            total=current+r['STD_added'];assert total<=15 and tf['TW_added']<=2 and total+tf['TW_added']<=20
            ss.append({'TW_family':tf['id'],'first_signed':nf,'minimum_signed':nm,'STD':total,'TW':tf['TW_added'],'new_live_cost_upper':nf*FIRST+nm*MINIMUM+tf['normal_added'],'regular14_STD_sufficient_nomination':total>=14,'active12_inactive2_sufficient_only_if14STD_and_available':total>=14})
            valid+=1
      slot_summaries[key]={'valid_signed_slot_forms':len(ss),'forms_sha256':digest(ss),'signed_STD_range':[min(r['STD']for r in ss),max(r['STD']for r in ss)],'TW_range':[min(r['TW']for r in ss),max(r['TW']for r in ss)],'minimum_completion':'If only13STD, add one eligible statutory-minimum FA/2R/acceptedSTD-QO or choose an availablefirstUPC. This requires identity/acceptance choice; unsignedrights are not roster members.','example_legal_form':'no-QO-renouncebothTW; existing13primary + one lawful no-bonus minimumUPC =14STD; nominate12active/2inactive with eligible availability; actual active/medical certificate false.'}
    # Check every165 basebranch ×12 veterans ×3 dates; TW/draft extrema are additive monotone independent of base.
    yf,sf=veterans.forms()
    for b,vc in itertools.product(m['conditional_rows'],v['cases']):
      y=next(f for f in yf if f['id']==vc['Young_form']);t=next(f for f in sf if f['id']==vc['Satoransky_form'])
      for st in range(3):
        old=b['dated_states'][0 if st==0 else 3]
        yc=veterans.component(y,st>=1);sc=veterans.component(t,st>=2)
        n=old['normal_cost_known_upper_including_unrenounced_Young_Satoransky_holds']-47861000+yc['normal_upper']+sc['normal_upper']
        a=old['apron_cost_known_upper_excluding_UFA_holds']+yc['apron_upper']+sc['apron_upper']
        assert n>=0 and a>=0
        full_n=n+(2*TW_HOLD if st==0 else 2*MINIMUM)+30*FIRST+30*MINIMUM+MINIMUM+(20000000 if st==0 else 0)
        full_a=a+(0 if st==0 else 2*MINIMUM)+30*FIRST+30*MINIMUM+MINIMUM
        assert full_n>=n and full_a>=a;checks+=1
    assert checks==5940
    return {'id':'CHICAGO_2022_FULL_COST_ROSTER_FAMILY','status':'INDEPENDENTLY_REVIEWED_FINITE_PUBLIC_CATEGORY_ENVELOPE_AND_SLOT_FILTER_NOT_SELECTED',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8 BOMstrip CRLF/CR toLF; rawbytes separate',
      'sources':obs,'candidate_policy':p,
      'quantifier':'For every admitted existing165 financial branch,12 veteran actions, finite completedTW tenure/QO actions and current2022draft rights subset, these formulas bound all six cost categories. Existential routine exception renunciation/minimum or Bird forms are candidates; exact rights, signatures, consents and results remain unselected.',
      'scope':{'cost_capyear':'2022-23 fullannual cash upper; selected events only July1→July7 proposal window','rights_continuation_certificate_end':'2022-06-30 in priorleaf; July7 is within conservative proved earliestadditional endpoint2022-07-29; no automaticafterJuly29rightslock','whole_FY22_future_transactions_or_roster_selected':False,'named_important_choice_selected':None,'arbitrary_unreported_new_future_settlement_added':False,'source_supported_published_family_only':True},
      'six_category_map':[
        {'id':'LIVE_AND_PROPOSED','closed_template':True,'bound':'Reused165/660 plus12/36/192/5940; allcurrentSalary/performance inreviewedsource. New minimum forms bonus0 by expressproposal, firstrookieallperformancewithin120%; no newassignment andno unpriced internationalfunding.'},
        {'id':'LEGACY_WAIVED_CAMP','closed_template':True,'upper':20743601,'bound':'Originalpublicnamed13 ordinaryterm endpoints plus valid oldstretch16,371,000 andcamp4,372,601 preserved. No newwaiver/resolutionselected; futureactualprivatepayments notcertified.'},
        {'id':'COMPLETED_TW_FA_QO_FRN','closed_template':True,'normal_unrenounced_two_TW_FA':2035562,'maximum_two_standard_QO_cash_reserved':6000000,'bound':'July1 completed2021one-yearTW hold iszeroYOSminimum each, not zeroSalary. NoQO byJune29→UFA; thenvalidrenounce orneweligible1yrTWcandidate. ValidQOconditional15NBAactive/inactivedays→type perXI1cIII. OutstandingSTD-QO apronreserved3m/actor, TW-QOcomponentexcludedunderVII4j. NoFRN/offer-sheet selected; futureFRN reopensnamedoffer notarbitraryzero.'},
        {'id':'DRAFT_REQUIRED_TENDER','closed_template':True,'first_year_reported_scale_max':11055120,'first_salary_plus_unlikely_widened_upper':FIRST,'new_first_count_superset':[0,30],'new_second_count_superset':[0,30],'Simonovic_minimum_offer_fullcash_overreserve':3000000,'bound':'All2022firstrights economic envelope andrequiredtenderreservation, noownershipor30signedplayersclaim. SecondRTunaccepted isnot asserted statutorysalary butfullcash3m/actorreserved. Signedfirst/minimum≤availableSTD. Actual2022board identity/holders/foreignperiodandacceptedTenderremainunselected.'},
        {'id':'ROSTER_INCOMPLETE','closed_template':True,'bound':'Core10+primary3 yields13; veteranandacceptedSTD-QOconsume0..2. LiveUPC additions≤15;TW≤2;offseason≤20. Existingcapcount>=12 meansincomplete0; unsignedrights arenotliveplayers. Aregular14STD sufficient12active/2inactive nomination canbeconstructedbyminimumfiller whenneeded; noactualmedical/seasonplanoridentity selected.'},
        {'id':'ANNUAL_EXCEPTIONS','closed_template':True,'pre_renunciation_normal_outer':20000000,'post_candidate_renunciation_normal_outer':0,'deemed_exception_apron':0,'prior_positive_event_bridge':{'source':LEG,'category_index':5,'event':'Explicit all-unused renounce2021August11','new_assignment_or_DPE_grant_in_intervening_candidate_window':False,'prior_TPE_or_DPE_never_existed_certified':False},'bound':'2022NTMLE10.490m+BAEabout4.105m <20mouter; mutuallyexclusiveTMLE6.479m androom5.401m notstacked. IneligibleBAE canonlyreducebound. ChoosevalidVII6m2renunciationatJuly7, not neverincorporated claim. Prior2021all-unused explicitrenounce removesoldTPE/DPEuse-rights; nointerveningnewassignment/grant isselectedinthisfamily. Itdoesnotcanceloldprotectedcontractpayments. NewNTMLE/BAEorS&TwouldtriggerFY22apron andreopenaffectednamedusage. Bird/minimum/rookies/TW alone donottrigger, noFY21hardcapcarry.'}],
      'TW_families':tw,'TW_rule_domains':{'credited_YOS_for_new1yrTW':'0..3 withno4thYOSduringcontract;notexactfutureplayerYOS','same_team_TW_capyears':'atmost3includingnewyear; prior2permitsonlynew1yr,prior3requiresSTDQOifeligible','ordinaryQO_eligibility':'completedservices+15activeorinactiveNBAregulardays andtimelyJune29offer; physicaldisability validacceptance condition underXI4cIII retained, noactualclinicalcertificate','QO_type':'XI1cIII A second/thirdconsecutive1yr or2yr term→STD;C TW-ineligible→STD;B otherwiseTW','noQO_UFA':'No offer issued byJune29; July1UFA evenif15daycriterionnotknown. No guarantee ofre-signing orfutureFRNabsence.','QO_keep_open_until':'atleast2022-10-01; ordinarywithdrawalbyJuly13; laterwrittenplayerconsent, notautomaticrenouncewhileQOoutstanding','TW2022gamecap':'official2022–23PacersguidePDF16550games; regularNBAactivegamesselectednull/no2017normal45daysmisuse','new_TW_compensation':'applicable2022seasonmodifiedrule input; fullcash<=3mreserveifneeded, TeamSalaryexcludedVII4j; nofutureexactcash0certificate'},
      'draft_domain_not_board':{'first_count_bound_source':'CBA X3 NBA30teams two rounds, anyforfeitureonlyreduces; rankidentityselectednull. Published2022maxscale outercondition protectsnumericrounding uncertainty.','old_unsigned_first_scope':'Onlythepreservedprior2021acceptedpublicportfolio; no arbitraryunreportedoldpick added. CoreDuarte/LaMeloalreadyhaveUPC. Simonovicisnamed2020second not first.','firsthold_normal':'120%applicablescale while unsigned; afterUPCsalary replaceshold, neverdoublecountboth','first_apron':'unsignedordinaryholdexcluded; requiredtenderoutstandingincluded; signedSalary+allperformanceincluded','second_offer':'timelyvalidRT one-yearminimum evenifcouldbeaccepted; cashoverreserveshownbutSTD onlyifaccepted. Do not guess2022selection/renewal/futureidentity.','source2022budget2m_or2.2m_or10.13m_is_contract':False,'future2022rights_execution_remaining':'Applythe eventualdraftcontrol/selection tothisfiniteeconomicfamily, satisfyX4–6 notices/tender atapplicabledates; no rosteradditionwithoutauniqueactualmodeledidentity. Notprivateallledgergate.'},
      'compact_joined_cost_cells':out,'slot_families':slot_summaries,
      'coverage':{'reviewed_base_numeric_branches':165,'reviewed_base_dated_rows':660,'veteran_cases':12,'TW_action_and_type_families':len(tw),'compact_policy_cells':len(out),'exact_base_veteran_dated_recalculations':checks,'slot_filtered_forms_across_STD13_14_15':valid,'incompatible_slot_or_eligibility_forms_rejected':excluded,'all_six_template_categories_accounted':True,'large_draft_envelope_players_registered':0},
      'hardcap_and_feasibility':{'FY21_trigger_does_not_carry':True,'new_FY22_trigger_in_this_Bird_minimum_rookie_TW_family':False,'NTMLE_BAE_ST_received_trigger_if_added':True,'apron_screen':APRON_SCREEN,'apron_statutory_exact_rounding_certified':False,'negative_outer_apron_margin_is_illegal':False,'cap_overage_requires_existing_valid_exception_forms':True,'all_existing_directBird_and_minimum_forms_reused':True,'whole_exact_taxbill_selected':False},
      'certification':{'independent_review_completed':True,'full_public_category_envelope_prepared':True,'whole_FY22_selected_roster_cost_results':False,'actual_private_payments_or_absence_certified':False,'actualconsent_and_league_receipt':None,'actualforeignlaw_or_notice_certified':False,'selectedcontract_or_draft':None,'whole_macro3_complete':False,'central_or_REGISTER_promotion':False,'new_author_lock':False,'manuscript_written':0}}

def validate(o):
    try:assert o==build(),'Saved current source/meaning differs';return[]
    except(AssertionError,KeyError,ValueError,OSError)as e:return[str(e)]

def markdown(o):
    c=o['coverage'];return '\n'.join(['# Chicago FY22: 전체 비용 범주·명단 슬롯의 유한 후보 가족','',o['status'],'',
      '기존165 계약 분기·660 날짜 입력, Young/Satoransky12후보·36상태·192정책셀·5940합산을 보존했다. 기존방향 M1/A를 재승인하지 않고, 계약·신인지명·시즌결과는 선택하지 않는다. 전체 공개 범주 상단을 준비했으며 실제 다음 시즌 전체 완료나 사적 장부 인증으로 승격하지 않는다.','',
      '## 여섯 범주와 명명된 잔여 구현','',
      '1. 현행·새계약: 검문된10이월/핵심3/Y-S 가족의 salary·성과·구간 그대로. 새 최소계약은 법정함수와 명시적 보너스0 제안이며3m는 fullcash 상단이다. 신인 첫계약의 Salary+Unlikely는80–120%scale 제약 안이다.','2. 과거 방출·캠프: 공개 보존부채20,743,601을 유지한다. 원13 ordinary계약의 양수 기간 끝점, oldstretch16,371,000·camp4,372,601이 근거다. 보장0/actual지급0 또는 새 미보고합의를 무한 추가하는 gate가 아니다.','3. Dotson/Cook: SQ1의2021-08-13 1년TW는2022-06-30까지다. July1부터 미renounce FAhold는각 zeroYOSminimum1,017,781. 6월29일까지QO미발행→UFA 이후 hold유지/유효renounce/자격있는새1년TW 제안; QO는15NBAactive/inactive일 조건부로 타입을 분기한다. 두번째/세번째 연속1년TW 또는TW부적격은 **표준QO**이며 단순TW로처리하지 않는다. STD-QO전액3m/인 보수예약, outstandingQO와 FRN 산입을 구별한다. 실제15일/수락/임상과 미래offer-sheet는미선택이다.','4. 신인·Required Tender: 2022 정확board/권리자 미선택을0 비용으로 바꾸지 않았다. CBA 두라운드×30팀 전체superset에 unsignedfirst hold/requiredtender를 넓게 예약한다. [2022 원분석 표](https://www.hoopsrumors.com/2022/07/rookie-scale-salaries-for-2022-nba-first-round-picks.html)의최대120%첫해11,055,120을11.06m 조건부상단으로넓혔다. 이것은공식scale/정확계약이아니다. second unacceptedoffer는실제capcharge라단정하지않고각3m과대예약한다. Simonovic은기존추가기간 최저말단7월29일이July7을덮으므로본순서에서권리를쓸수있는후보; annualRT3m을별도예약하고이후권리/foreign기간은자동확정하지않는다.','5. 명단:13명핵심에서Y/S·acceptedSTDQO·신인UPC만실제슬롯을쓴다. 최대15STD/2TW/오프시즌20; unsigned30+30은등록선수가아니다. 새STD서명수는 각베테랑분기 잔여0/1/2칸과연결했고 과잉서명은거부한다. 13명일때1명의합법최소FA/2R 등으로14STD를채우는candidate를구성할수있으나이름/동의/명단선택은별도다. 실제게임의12active/2inactive·건강·분/결과인증으로확대하지않는다.','6. 연간예외: July1 genericincorporation가능분은20m과대예약, July7유효서면renounce 후보후0으로대체한다. 이전에산입된적없음/사용가능RoomMLE를자동추론하지않는다. 2022NTMLE10.490m/BAE4.105m과상호배타적TMLE/Room경로를구별한다. 해당실사용·S&T수취를추가하면새hardcap과비용을재검문해야한다. Bird·최소·rookie·TW자체는FY22trigger없고FY21hardcap을이월하지않는다.','',
      '## 검문 가능한 계산','',f'완료템플릿 여섯 범주 / {c["TW_action_and_type_families"]} TW타입·행동가족 / {c["compact_policy_cells"]} compact 계약정책셀 / {c["exact_base_veteran_dated_recalculations"]} 원165×12×3 날짜 합산 / {c["slot_filtered_forms_across_STD13_14_15"]} 유효 슬롯형식. 조상165개벡터를다시복제하지않는다.','',
      '전체league초기권리예약은실제Chicago소유를인증하지않고모든가능한현재2022권리부분집합을지배하는경제over-envelope이다. upper가apron을넘는다고Bird계약의위법/실제채무를판정하지않는다. 별도hardcaptrigger 없는가족에서음수 screen은충분조건실패일뿐이다. 의미있는최종비교는후속2022지명권·선수·수락 선택을식에넣는작업이다. 실제Chicago30명서명, unknown0 또는무한private원장요건이아니다.','',
      '[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) I1/II6/11/VII4/6/8/VIII1/X4–6/XI1/4–5/XXIX와 [공식2022–23 Pacers guide](https://cdn.nba.com/teams/uploads/sites/1610612754/2022/10/2022-23-Pacers-Media-Guide-compressed.pdf) PDF165의시즌별50게임/활성명단·예외액을읽었다. 가이드의오래된playoff/waiver문구는채택하지않았다. RealGM직접회수1회403은원문미채택이며반복하지않았다. 최소표·NBAcap은검문된Y/Sleaf raw연결을재사용한다.','',
      '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23거래·계약|FY22공개6범주·슬롯가족준비;방향·신인·시즌미선택|','|4|장기커리어|후속시즌입력대기|','|5|결말·전체구조|전체기능표미완료|','|6|집필규격·ContextPack|현행누적등록기참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','','미완료큰묶음5 / v0.30 PARTIAL / 설계·원고CLOSED / 원고0.',''])

def self_test():
    p=policy();b=copy.deepcopy(p);b['FY21_hardcap_carried']=True
    with patch(__name__+'.policy',return_value=b):
      try:build();raise RuntimeError('FALSE_PASS yearlytrigger')
      except AssertionError:pass
    src=source_inputs();b=copy.deepcopy(src);b[SQ]['two_way_working'][0]['working_term_seasons']=2
    with patch(__name__+'.source_inputs',return_value=b):
      try:build();raise RuntimeError('FALSE_PASS TWexpiry')
      except AssertionError:pass
    original=tw_component
    def wrong(a,k):
      r=original(a,k)
      if r and a=='VALID_QO_UNACCEPTED'and k=='CONSECUTIVE_STANDARD_QO':r['apron']=0
      return r
    with patch(__name__+'.tw_component',side_effect=wrong):
      try:tw_families();raise RuntimeError('FALSE_PASS STDQOapron')
      except AssertionError:pass
    try:checked_rookie(1,0,0,30,30,True);raise RuntimeError('FALSE_PASS16thUPC')
    except AssertionError:pass
    original=rookie_component
    def badrookie(*args):
      r=original(*args);r['apron']-=FIRST;return r
    with patch(__name__+'.rookie_component',side_effect=badrookie):
      try:checked_rookie(0,0,2,30,30,True);raise RuntimeError('FALSE_PASS tendercost')
      except AssertionError:pass
    original=tw_component
    def wrongelig(a,k):
      if a=='NEW_1YEAR_TW'and k=='TW_INELIGIBLE_STANDARD_QO':return {'normal':0,'apron':0,'STD':0,'TW':1,'QO_live':False,'FRN_live':False}
      return original(a,k)
    with patch(__name__+'.tw_component',side_effect=wrongelig):
      try:tw_families();raise RuntimeError('FALSE_PASSineligibleTW')
      except AssertionError:pass
    original_families=tw_families
    def bad_aggregate():
      fs=original_families()
      for f in fs:
        if all(f[a]['kind']=='CONSECUTIVE_STANDARD_QO'and f[a]['action']=='ACCEPT_VALID_QO'for a in ('Devon_Dotson','Tyler_Cook')):f['STD_added']=0
      return fs
    with patch(__name__+'.tw_families',side_effect=bad_aggregate):
      try:build();raise RuntimeError('FALSE_PASS accepted_STDQO_aggregate')
      except AssertionError:pass
    return 7

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(o),encoding='utf-8')
    if a.check:assert validate(load(OUT))==[] and text(MD)==markdown(o)
    print(json.dumps({'current':True,**o['coverage'],'negative_controls':self_test()if a.self_test else None}))
