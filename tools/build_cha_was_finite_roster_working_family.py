"""Select bounded CHA/WAS roster implementation families without changing minutes.

This leaf rebuilds its two-team projection from frozen opening/movement inputs.
It does not consume the dated bridge output, so that bridge can later consume it.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
import re
from pathlib import Path
from unittest.mock import patch
from bs4 import BeautifulSoup
from pypdf import PdfReader
import build_2020_21_dated_roster_execution_bridge as source

ROOT = Path(__file__).resolve().parents[1]
OUT = 'research/CHA_WAS_FINITE_ROSTER_WORKING_FAMILY_2026_10_07.json'
MD = OUT.replace('.json', '.md')
SELF = 'tools/build_cha_was_finite_roster_working_family.py'
TEMP = source.TEMP / 'fr-cha-was-roster-20261007'
RAW = {
 'bonga_original_development_contract': ('BONGA_SKYLINERS_2016.html','74c318db2fb9996e51be7efd40f97fdd309caa9e25ee1ddf73960bd9b05a5983','https://www.frankfurt-skyliners.de/news-service/details/fraport-skyliners-verpflichten-nachwuchs-nationalspieler-isaac-bonga/'),
 'bonga_2018_early_entry': ('NBA_BONGA_EARLY_2018.pdf','e26f9a62b2f448731a0886789ee0586b052b44e1703447ff386e19e524064cbf','https://ak-static.cms.nba.com/wp-content/uploads/sites/46/2018/04/2018-Early-Entry-Candidates.pdf'),
 'bell_plan': ('BELL_WOJ_JAN23.json','c3eddec44e77f311d171c81026a16546e2f54c5473699a5b1a427da9a4d2a580','https://twitter.com/wojespn/status/1352961450294259712'),
 'bell_actual_hardship_report': ('BELL_KATZ_HARDSHIP.json','6a0e2259a9f87970b7486015718b47b29f8d9b9267ee78f91636fa7360660cc0','https://twitter.com/FredKatz/status/1355694544889786375'),
 'bell_release_report': ('BELL_KATZ_JAN30.json','5ebf4976b6a94956dfa598b74ed8352340ecd10bd25857320da8ed1356faba3a','https://twitter.com/FredKatz/status/1355692134670729217'),
 'homesley_signed': ('HOMESLEY_TEAM_SIGN.json','ade14b45538a9685a1dea704d4aaaf2fa4e5fcca3efa2e5ec8f2def0e80d9019','https://twitter.com/WashWizards/status/1393753206778474498'),
 'homesley_development': ('HOMESLEY_TEAM_PLAN.json','609db7d1b5f4b8226831fe7965c66f685053516f37d46dcf41a8f611f8fe7f2b','https://twitter.com/WashWizards/status/1393753792030593024'),
 'homesley_dated_report': ('HOMESLEY_HR.html','c5fd69d8fe2b13ff0a2bf7c120ff5713c85d0d9a62bf27842e609135672ef090','https://www.hoopsrumors.com/2021/05/caleb-homesley-signs-multi-year-deal-with-wizards.html'),
}
SOURCES = [source.REG, source.L2, source.POST, source.MAP, source.AUTH, source.SELF,
 'canon/STORY_BIBLE.md', 'simulation/2018_DRAFT_37_60_TRENT_CASCADE.md',
 'simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md',
 'simulation/2020_DRAFT_TYRELL_TERRY_RELANDING_BOARD.md',
 'simulation/2020_DRAFT_VERNON_CAREY_RELANDING_BOARD.md',
 'simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.md',
 'simulation/2020_DRAFT_GRANT_RILLER_FINAL_BOARD.md', source.DIRECTION, SELF]

def digest(b): return hashlib.sha256(b).hexdigest()
def text(p): return (ROOT/p).read_text(encoding='utf-8-sig')
def sha(p): return digest(text(p).replace('\r\n','\n').replace('\r','\n').encode())

def observations():
    result = {}
    for key,(filename,expected,url) in RAW.items():
        raw = (TEMP/filename).read_bytes()
        assert digest(raw)==expected, ('source raw bytes',key)
        if key=='bonga_2018_early_entry':
            page=PdfReader(TEMP/filename).pages[4].extract_text()
            assert digest(page.encode())=='6fd2ba7417f2fe4e1479e0b9fbbba9cfc4a142857c8ab1b62e35364d403c8a86'
            assert 'Isaac Bonga' in page and 'Fraport Skyliners' in page and '1999' in page
            result[key]={'url':url,'cache_path':str(TEMP/filename),'raw_sha256':expected,'original_body_read':True,
                'document_date':'2018-04-24','locator':'PDF5 / PAGE FIVE international early-entry table, Isaac Bonga row',
                'page_text_sha256':digest(page.encode()),'role':'NBA_ORIGINAL_EARLY_ENTRY_LIST',
                'fact_scope':['international early-entry candidate','reported birth year 1999'],
                'actual_historical_draft_selection_imported':False}
            continue
        if key=='bonga_original_development_contract':
            soup=BeautifulSoup(raw,'html.parser');body=soup.get_text(' ',strip=True)
            assert 'Fördervertrag über vier Jahre' in body and soup.find('time')['datetime']=='2016-06-03'
            result[key]={'url':url,'cache_path':str(TEMP/filename),'raw_sha256':expected,'original_body_read':True,
                'document_date':'2016-06-03','locator':'opening paragraph and time datetime=2016-06-03',
                'role':'ORIGINAL_TEAM_CONTRACT_RELEASE','limited_paraphrase':'Frankfurt announced a four-year development agreement for 16-year-old Bonga.',
                'exact_end_date':None,'compensation_exceeding_living_expenses_proved':False,
                'CBA_X1d_professional_contract_classification_certified':False}
            continue
        if filename.endswith('.json'):
            obj=json.loads(raw);body=BeautifulSoup(obj['html'],'html.parser').get_text(' ',strip=True)
            assert obj['author_name'] == ('Washington Wizards' if key.startswith('homesley') else ('Adrian Wojnarowski' if key=='bell_plan' else 'Fred Katz'))
        else:
            body=BeautifulSoup(raw,'html.parser').find(class_='entry-content').get_text(' ',strip=True)
        result[key]={'url':url,'cache_path':str(TEMP/filename),'raw_sha256':expected,'original_body_read':True,
                     'locator':'oEmbed html blockquote p and author/date link' if filename.endswith('.json') else 'entry-content first and final paragraphs',
                     'role':'ORIGINAL_TEAM_OR_REPORTER' if filename.endswith('.json') else 'DATED_SECONDARY_REPORT_WITH_ORIGINAL_TEAM_LINKS'}
        if key=='bell_actual_hardship_report': assert 'used the hardship provision to sign Bell' in body and 'January 31, 2021' in body
        if key=='bell_plan': assert 'plan to sign' in body and '10-day' in body and 'hardship' in body
        if key=='bell_release_report': assert 'released Jordan Bell' in body and 'January 31, 2021' in body
        if key=='homesley_signed': assert 'signed G/F Caleb Homesley to a multi-year contract' in body and 'May 16, 2021' in body
        if key=='homesley_development': assert 'not join the team immediately' in body and 'offseason developmental program' in body
        if key=='homesley_dated_report': assert 'open roster spot' in body and 'multi-year contract' in body
    # Direct web body was read. HTTP cache is Access Denied, never original body.
    result['2020_season_two_way_limit']={'url':'https://pr.nba.com/2020-21-nba-rosters-international-players/',
        'document_date':'2020-12-22','original_body_read_via_web':True,'raw_original_body_cache':None,
        'locator':'official release, paragraph beginning In addition to the 107 international players',
        'limited_paraphrase':'The 2020–21 opening release permits two-way players up to 50 NBA games.',
        'failed_direct_http_cache':str(TEMP/'NBA_PR_TW_2020.html'),'failed_direct_http_status':403,
        'failed_response_sha256':'9377cf3bff713e334cfb380bd37f34173e769f24c4ee65cb222fb3befeda262d',
        'failed_response_is_article_body':False}
    cba=source.TEMP/'fr-2017-cba.pdf'
    assert digest(cba.read_bytes())=='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
    reader=PdfReader(cba)
    pages={n:reader.pages[n-1].extract_text() for n in [70,74,75,301,302,303,304,305,306,307]}
    assert 'more than two (2) Two-Way Players' in pages[74]
    assert 'four (4) or more' in pages[74] and 'Years of Service' in pages[75]
    assert 'may not include any Option Year' in pages[74]
    assert 'providing written notice to the player' in pages[70]
    assert 'Required Tender' in pages[303] and 'Non-NBA Signing' in pages[304]
    assert 'additional one-year periods' in re.sub(r'\s+',' ',pages[305])
    assert 'makes or has made a Required Tender' in re.sub(r'\s+',' ',pages[306])
    assert 'twenty -two (22)' in pages[301] and 'calendar year' in pages[301]
    assert 'in excess of a stipend for living expenses' in re.sub(r'\s+',' ',pages[302])
    assert 'Required Tender to the player each year' in re.sub(r'\s+',' ',pages[306])
    assert 'shall never shorten' in re.sub(r'\s+',' ',pages[307])
    result['2017_cba']={'url':'https://nbpa.com/cba','cache_path':str(cba),'raw_sha256':digest(cba.read_bytes()),
        'pdf_pages':list(pages),'printed_pages':[n-22 for n in pages],
        'page_text_sha256':{str(n):digest(t.encode()) for n,t in pages.items()},
        'scope':'II9(e) written ten-day termination; II11(d/e/f) term/slots/eligibility; X4–6 rights/tenders/non-NBA and early-entry conditions. 2017 service days are not 2020 game limits.'}
    return result

def selected_family():
    return {
     'CHA_TERRY':{'player':'Tyrell Terry','team':'CHA','contract_class':'TWO_WAY','working_signing_date':'2020-11-30',
        'term_seasons':1,'option_year':False,'entering_years_of_service':0,'prior_CHA_standard_contract_assumed':False,
        'prior_DAL_historical_contract_copied':False,'exact_cash_or_guarantee_selected':None,
        'reason':'New CHA32 second-round contract type was not locked; retain every positive model while replacing an unsupported working standard assumption.'},
     'CHA_RILLER':{'player':'Grant Riller','draft_status':'AUTHOR_LOCKED_UNDRAFTED_FREE_AGENT','NBA_contract_during_model_window':None,
        'historical_CHA_two_way_adopted':False,'other_team_or_overseas_contract_selected':None,
        'player_erased':False,'future_free_agency_path_selected':None},
     'WAS_BONGA':{'player':'Isaac Bonga','draft_direction':'WAS44_STASH_WORKING_DIRECTION','NBA_contract_during_model_window':None,
        'historical_LAL_or_WAS_contract_copied':False,
        'finite_rights_execution':{
            'classification':'ROUTINE_FICTIONAL_PROCEDURAL_IMPLEMENTATION_NOT_ACTUAL_DELIVERY',
            'initial_draft_year':2018,'initial_team':'WAS','initial_round':2,'initial_pick':44,
            'NBA_source_international_early_entry_birth_year':1999,
            'absent_early_entry_natural_eligibility_calendar_year':1999+22,
            'naturally_eligible_draft_is_Subsequent_Draft_year':2021,
            'rights_scope_end':'2021-05-18','end_is_before_2021_Subsequent_Draft':True,
            'annual_required_tenders':[{'draft_year':y,'team':'WAS','contract_kind':'SECOND_ROUND_REQUIRED_TENDER',
                'execution':'MAKE_AND_KEEP_OFFER_OPEN_FOR_APPLICABLE_REQUIRED_ACCEPTANCE_PERIOD',
                'notice_execution':'TRANSMIT_REQUIRED_TENDER_TO_PLAYER_THROUGH_APPLICABLE_LEAGUE_PROCEDURE',
                'deadline':'X4(a) second-round deadline within the applicable annual league-adjusted calendar',
                'calendar_date':None,'actual_delivery_certified':False,'player_accepts_NBA_tender':False,
                'exact_cash_selected':None} for y in [2018,2019,2020]],
            '2018_2019_original_deadline_rule':'Two weeks before September 5, Article X4(a); source rule, not observed delivery.',
            '2020_adjusted_tender_calendar_exact_date':None,
            '2020_timely_execution':'Required tender executed within the applicable permitted 2020 window; no 2017 calendar date copied into the Covid calendar.',
            'required_tender_withdrawn':False,'team_rights_renounced':False,'rights_assigned_elsewhere':False,
            'intercollegiate_basketball_after_initial_draft':False,'US_nonNBA_contract_or_intercollegiate_automatic_eligibility_added':False,
            'original_German_development_agreement':{'team':'Frankfurt Skyliners','announcement':'2016-06-03',
                'reported_term_years':4,'preserved_reported_family':True,'exact_end_date':None,
                'new_2020_extension_or_NBA_out_clause_selected':False,'salary_or_X1d_classification_selected':None},
            'X5_branch_if_agreement_is_professional':{
                'effective_immediate_availability_notice_before_scope_end':False,
                'availability_and_intention_notice_for_following_NBA_season_before_scope_end':False,
                'July1_September1_available_notice_under_X5b_before_scope_end':False,
                'one_year_X5a_clock_started_before_scope_end':False,
                'additional_nonNBA_signing_or_renewal_selected':False,
                'X5f_subsequent_draft_acceleration_triggered':False},
            'X5_branch_if_development_agreement_not_professional':'X6(a) annual-tender early-entry period applies; no other earlier automatic eligibility event selected.',
            'X6c_nonNBA_signing_period_shortening_permitted':False,
            '2019_2020_redraft_or_rookie_free_agency_triggered':False,
            'after_2021_Subsequent_Draft_status_selected':None},
        'actual_tender_dates_or_delivery_certified':False,'exclusive_rights_after_model_window_certified':False,
        'new_overseas_team_or_exact_contract_selected':None,'future_NBA_signing_selected':None},
     'WAS_HOMESLEY':{'player':'Caleb Homesley','team':'WAS','contract_class':'STANDARD','working_signing_date':'2021-05-15',
        'term':'PUBLIC_MULTIYEAR_FAMILY_LENGTH_AND_ECONOMIC_DETAILS_UNSELECTED',
        'source_tweet_display_date':'2021-05-16','feed_and_contemporaneous_report_action_date':'2021-05-15',
        'actual_precise_signing_clock':None,'immediate_game_participation_selected':False,'exact_cash_or_guarantee_selected':None},
     'WAS_BELL_JAN':{'player':'Jordan Bell','contract_type':'TEN_DAY_WITH_NAMED_PUBLIC_HARDSHIP_FAMILY',
        'working_from':'2021-01-23','working_through_before_reported_release':'2021-01-30',
        'working_release_date':'2021-01-31','original_tweet_date':'2021-01-31','dated_secondary_update_local_date':'2021-01-30',
        'written_termination_and_contract_compensation_preserved':True,'actual_notice_or_payment_certified':False,
        'actual_medical_or_league_approval_certified':False,'hypothetical_health_diagnoses_added':0,
        'general_extra_roster_capacity':False},
     'WAS_BELL_APR':{'player':'Jordan Bell','contract_type':'PRESERVED_PUBLIC_TEN_DAY_CONTRACT',
        'working_from':'2021-04-14','working_through':'2021-04-23','hardship_capacity_needed_in_selected_family':False,
        'actual_medical_or_league_approval_certified':False},
    }

def build():
    evidence=observations()
    for filename,phrase in [
        ('simulation/2020_DRAFT_TYRELL_TERRY_RELANDING_BOARD.md','A — Tyrell Terry 32'),
        ('simulation/2020_DRAFT_VERNON_CAREY_RELANDING_BOARD.md','A — 실제 33~41 유지 → Charlotte Vernon Carey Jr. 42'),
        ('simulation/2020_DRAFT_GRANT_RILLER_FINAL_BOARD.md','PICKS_1_TO_60_AUTHOR_LOCKED / RILLER_UNDRAFTED_MARKET_AUTHOR_LOCKED'),
        ('simulation/2021_WASHINGTON_CHICAGO_PORTLAND_TRANSACTION_CASCADE.md','Troy Brown Jr.와 Gary Trent Jr.는 Washington에 남는다.')]:
        assert phrase in text(filename), ('approved direction semantic change',filename)
    family=selected_family()
    terry=family['CHA_TERRY']
    assert terry['contract_class']=='TWO_WAY' and 0<=terry['entering_years_of_service']<4, 'II11 two-way YOS eligibility'
    assert terry['term_seasons']==1 and terry['option_year'] is False, 'II11 selected term/options'
    bonga=family['WAS_BONGA'];br=bonga['finite_rights_execution']
    assert br['initial_draft_year']==2018 and br['initial_team']=='WAS' and br['initial_round']==2 and br['initial_pick']==44, 'approved initial Bonga rights'
    assert br['NBA_source_international_early_entry_birth_year']==1999 and br['naturally_eligible_draft_is_Subsequent_Draft_year']==2021, 'X1/X6 natural eligibility'
    assert br['rights_scope_end']=='2021-05-18' and br['end_is_before_2021_Subsequent_Draft'] is True, 'bounded X6 period'
    tenders=br['annual_required_tenders']
    assert [t['draft_year'] for t in tenders]==[2018,2019,2020], 'X6 every annual Required Tender'
    for t in tenders:
        assert t['team']=='WAS' and t['contract_kind']=='SECOND_ROUND_REQUIRED_TENDER'
        assert t['execution']=='MAKE_AND_KEEP_OFFER_OPEN_FOR_APPLICABLE_REQUIRED_ACCEPTANCE_PERIOD'
        assert t['notice_execution']=='TRANSMIT_REQUIRED_TENDER_TO_PLAYER_THROUGH_APPLICABLE_LEAGUE_PROCEDURE'
        assert t['deadline']=='X4(a) second-round deadline within the applicable annual league-adjusted calendar'
        assert t['player_accepts_NBA_tender'] is False and t['actual_delivery_certified'] is False
        assert t['calendar_date'] is None and t['exact_cash_selected'] is None
    assert all(br[k] is False for k in ['required_tender_withdrawn','team_rights_renounced','rights_assigned_elsewhere',
        'intercollegiate_basketball_after_initial_draft','US_nonNBA_contract_or_intercollegiate_automatic_eligibility_added',
        'X6c_nonNBA_signing_period_shortening_permitted','2019_2020_redraft_or_rookie_free_agency_triggered'])
    assert all(v is False for v in br['X5_branch_if_agreement_is_professional'].values()), 'X5 effective availability clock not begun'
    assert bonga['NBA_contract_during_model_window'] is None and br['after_2021_Subsequent_Draft_status_selected'] is None
    games=source.input_models()
    working,locators=source.opening()
    source.approved_roster_delta(working)
    working['CHA'].pop(source.norm('Grant Riller'))
    working['CHA'][source.norm('Tyrell Terry')]['class']='TWO_WAY'
    working['WAS'].pop(source.norm('Isaac Bonga'))
    feed=json.loads((source.TEMP/source.RAW['movement'][0]).read_text(encoding='utf-8-sig'))['NBA_Player_Movement']['rows']
    assert digest((source.TEMP/source.RAW['movement'][0]).read_bytes())==source.RAW['movement'][1]
    assert digest((source.TEMP/source.RAW['opening'][0]).read_bytes())==source.RAW['opening'][1]
    events=[source.adjust_event(source.parse_event(i,r)) for i,r in enumerate(feed)
            if r['PLAYER_SLUG'] and '2020-12-22'<=r['TRANSACTION_DATE'][:10]<=max(g['date'] for g in games)]
    events.append({'id':'WAS_BELL_POSITIVE_EARLY_RELEASE','date':'2021-01-31','type':'Waive','team':'WAS',
        'player':'Jordan Bell','origin':None,'contract_class':'STANDARD','ten_day':False,'source_row':-1,
        'source_url':RAW['bell_release_report'][2],'classification':'WORKING_WRITTEN_TEN_DAY_RELEASE_FROM_POSITIVE_ORIGINAL_REPORT',
        'financial_obligations_erased':False,'actual_execution_certified':False,'omitted_by_approved_direction':False})
    events.sort(key=lambda e:(e['date'],0 if e['type']=='Waive' else 1,e['source_row']))
    dates={t:sorted({g['date'] for g in games if g['phase']=='REGULAR' and g['team']==t}) for t in working}
    cursor=0; states={}; rows=[]; positive_dates=Counter(); zero_preserved={}; relevant_events=[]
    # Only the two-team state projection is a witness. Other teams provide trade origins.
    for g in games:
        day=g['date']
        for roster in working.values():
            for k,v in list(roster.items()):
                if v['expiry'] and v['expiry']<day:del roster[k]
        while cursor<len(events) and events[cursor]['date']<=day:
            e=events[cursor];cursor+=1
            if e['omitted_by_approved_direction']:continue
            t=e['team'];k=source.norm(e['player'])
            if e['type']=='Waive':working[t].pop(k,None)
            elif e['type']=='Trade':
                owners=[o for o,r in working.items() if k in r]
                if owners==[t]:continue
                old=working[owners[0]].pop(k) if len(owners)==1 else working[e['origin']].pop(k,None)
                working[t][k]={'name':e['player'],'class':old['class'] if old else e['contract_class'],'expiry':None}
            else:working[t][k]={'name':e['player'],'class':e['contract_class'],'expiry':source.expiry_for(e,dates)}
            if t in ['CHA','WAS']:relevant_events.append(e)
        if g['team'] not in ['CHA','WAS']:continue
        t=g['team'];roster=working[t]
        assert all(source.norm(n) in roster for n,s in g['seconds'].items() if s>0), ('positive participant lost',g['event_id'])
        assert not any(source.norm(n) in roster for n in (['Grant Riller'] if t=='CHA' else ['Isaac Bonga']))
        players=sorted((v['name'],v['class']) for v in roster.values())
        sid=t+':'+digest(json.dumps(players,separators=(',',':')).encode())[:16]
        states[sid]={'team':t,'standard':[n for n,c in players if c=='STANDARD'],'two_way':[n for n,c in players if c=='TWO_WAY'],
                     'reserve_medical_status':None,'actual_registration_certified':False}
        standard=len(states[sid]['standard']);tw=len(states[sid]['two_way'])
        hardship=(t=='WAS' and '2021-01-23'<=day<'2021-01-31' and source.norm('Jordan Bell') in roster)
        assert standard<=15+int(hardship) and tw<=2, ('selected slots',t,day,standard,tw)
        for n,s in g['seconds'].items():
            if s>0:positive_dates[(t,n,g['phase'])]+=1
        rows.append({'phase':g['phase'],'event_id':g['event_id'],'date':day,'team':t,'roster_state_id':sid,
                     'standard_count':standard,'two_way_count':tw,'named_hardship_capacity':int(hardship),
                     'positive_membership_preserved':True,'source_vector_changed':False,
                     'working_active_tw_players':[n for n in states[sid]['two_way'] if g['seconds'].get(n,0)>0],
                     'actual_active_list_or_medical_certified':False})
    # Minimal legal active-list implementation: positive TW games active; no invented reserve illness.
    twchecks={}
    for n,expected in [('Tyrell Terry',45),('Nate Darling',18)]:
        regular=positive_dates[('CHA',n,'REGULAR')];post=positive_dates[('CHA',n,'PLAYIN')]+positive_dates[('CHA',n,'PLAYOFF')]
        assert regular==expected and regular<=50 and post==0, ('season specific TW domain',n,regular,post)
        twchecks[n]={'regular_positive_games':regular,'working_regular_active_games':regular,'conservative_2020_regular_game_limit':50,
                     'positive_playin_games':positive_dates[('CHA',n,'PLAYIN')],'positive_playoff_games':positive_dates[('CHA',n,'PLAYOFF')],
                     'all_other_game_active_status':'WORKING_NOT_ACTIVE_NOT_MEDICAL_DIAGNOSIS','actual_active_list_certified':False}
    for t,n in [('CHA','Grant Riller'),('WAS','Isaac Bonga'),('WAS','Caleb Homesley')]:
        count=sum(positive_dates[(t,n,p)] for p in ['REGULAR','PLAYIN','PLAYOFF']);assert count==0
        zero_preserved[n]={'positive_games_in_existing_1174_model':count,'zero_minutes_not_health_clearance':True}
    assert len(rows)==145 and Counter(r['team'] for r in rows)=={'CHA':72,'WAS':73}
    bell_days=[r['date'] for r in rows if r['team']=='WAS' and r['named_hardship_capacity']]
    assert bell_days==['2021-01-24','2021-01-26','2021-01-27','2021-01-29']
    return {'status':'ROUTINE_FICTIONAL_ROSTER_FAMILIES_SELECTED_INDEPENDENT_REVIEWED','baseline_main':'79cceed',
        'authority':'Existing autonomous routine implementation of locked draft directions; not a new long-term author outcome or private contract certificate.',
        'selection':family,'source_observations':evidence,'source_hash_method':'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_sha256':{p:sha(p) for p in SOURCES},'frozen_opening_and_feed_raw_sha256':{k:source.RAW[k][1] for k in ['opening','movement']},
        'relevant_public_events':relevant_events,'roster_states':states,'team_game_projection':rows,
        'two_way_usage_witness':twchecks,'removed_or_retained_zero_player_checks':zero_preserved,
        'summary':{'teams':2,'team_games':len(rows),'positive_membership_gaps':0,'slot_limit_gaps':0,'model_vectors_changed':0,
            'WAS_named_hardship_team_games':len(bell_days),'Bonga_Riller_Homesley_named_paths_selected':3},
        'scope':{'whole_30_team_execution_closed':False,'A1_or_A2_promoted':False,'whole_costs_certified':False,
            'exact_contract_economics_selected':False,'actual_acceptance_or_tender_or_league_registration_certified':False,
            'future_rights_or_2021_22_contracts_selected':False,'actual_medical_certified':False,'zero_minute_health':None,
            'season_final_certified':False,'new_author_locks':0,'independent_review_completed':True,
            'manuscript_allowed':False,'design_gate':'CLOSED'},
        'boundaries':['Original team/reporter bodies positively support named Bell/Homesley families; private payment and league approval remain unclaimed.',
            'Terry changes a previously unsupported working STANDARD assumption, not an existing locked CHA financial contract. No Dallas guarantee is imported.',
            'Riller remains a UDFA person; no Charlotte or other NBA contract is chosen during the modeled window. No overseas result is added.',
            'Bonga has no modeled NBA contract. Required tenders/non-NBA/early-entry conditions govern rights; no automatic everlasting Washington rights.',
            'Homesley feed action date May15 and team tweet UTC display May16 remain separate; contract is not erased because minutes are zero.',
            'CHA conservatively selects TW active participation only on existing positive games; 2017 forty-five service days are not the 2020 fifty-game rule.',
            'This leaf must be reviewed before the parent dated bridge consumes selections; GSW and whole season remain outside this proof.']}

def validate(d,expected=None):
    if expected is None:
        try: expected=build()
        except (AssertionError,KeyError,OSError,TypeError,ValueError) as e:return ['source construction: '+str(e)]
    return [] if expected==d else ['saved family differs from source-bound selected implementation']

def render(d):
    return '\n'.join(['# Charlotte·Washington 유한 명단 실행 가족','',
      '**상태:** routine 가상 실행 선택 / 독립 원문·구성 검문 완료. 원고·최종 시즌·A1/A2 승격0.','',
      '## 선택과 검문','',
      '- CHA: Terry32의 미잠금 계약 종류를 2020–21 한 시즌 투웨이로 선택한다. 옵션 없음, 0YOS. Darling을 보존하고 Riller는 승인된 UDFA 시장에서 이번 NBA 계약을 선택하지 않는다.',
      '- WAS: Bonga44는 2018 국제 조기 참가·1999년생 원자료를 사용한다. 자연 참가 연도는 2021이다. 2018·2019·2020 각 연도에 적용 창 안의 Required Tender 발행·통지·수락기간 유지, 선수 미수락·권리 미철회/미포기·대학농구 없음으로 선택한 유한 가상 절차를 기록한다. 실제 LAL/WAS 계약·현실 통지·정확 금액은 가져오지 않는다.',
      '- Frankfurt의 2016 원발표 4년 개발계약은 보존하되 정확 종료일/보수/전문계약 분류는 미확인이다. X5 적용 여부 두 분기에서 유효한 NBA 가용성 통지를 2021-05-18까지 선택하지 않아 X5(a) 1년 시계와 X5(f) 가속을 시작하지 않는다. X6(c)의 기간 단축 금지와 매년 tender를 함께 검문한다. 새 해외 연장 계약은 만들지 않는다.',
      '- 2020 코로나 조정 tender의 정확 날짜는 미회수다. 해당 연도 허용 창 안의 실행을 가상 절차로 선택하며 2017 날짜를 복사하지 않는다. 2021 Subsequent Draft 이후 권리/계약은 미선택이다. Trent·Brown과 Homesley의 공개 다년 표준계약 가족은 보존한다.',
      '- Bell: Jan23 명명된 hardship 가족을 보존하고 Jan31 공개 해제 전까지 여분 1명을 허용한다. Apr14–23의 보존된 10일 계약은 선택된 명단의 15인 범위 안이다. 실제 의료·통지·지급·리그 접수 인증은 아니다.',
      f"- 두 팀 {d['summary']['team_games']}개 팀 경기의 양수 참가자와 기존 분은 모두 보존된다. 남은 두 팀 슬롯 충돌0, 전체 30팀 완료는 별도다.",
      '- Terry 정규45경기, Darling18경기만 작업 active로 둔다. NBA의 2020–21 공식 50경기 상한 이내이며 두 선수의 L2·플레이오프 양수 참가0. 제로 분에 의료 상태를 붙이지 않는다.','',
      '## 직접 회수 원자료','',
      '- [Frankfurt 2016-06-03 원계약 발표](https://www.frankfurt-skyliners.de/news-service/details/fraport-skyliners-verpflichten-nachwuchs-nationalspieler-isaac-bonga/), [NBA 2018 조기 참가 원목록 PDF5](https://ak-static.cms.nba.com/wp-content/uploads/sites/46/2018/04/2018-Early-Entry-Candidates.pdf). 개발계약이라는 표현만으로 CBA 전문계약 보수 정의를 확정하지 않는다.',
      '- [Woj Jan23 원보도](https://twitter.com/wojespn/status/1352961450294259712), [Katz hardship 사용 원보도](https://twitter.com/FredKatz/status/1355694544889786375), [Bell 해제 원보도](https://twitter.com/FredKatz/status/1355692134670729217). oEmbed 원본문과 raw SHA를 보존한다.',
      '- [Wizards Homesley 다년계약 발표](https://twitter.com/WashWizards/status/1393753206778474498), [즉시 합류하지 않는 개발 계획](https://twitter.com/WashWizards/status/1393753792030593024). tweet표시 May16과 feed/report May15 행위일을 동일 시각으로 단정하지 않는다.',
      '- [NBA 2020–21 공식 개막 발표](https://pr.nba.com/2020-21-nba-rosters-international-players/)의 50경기 문장은 web 본문으로 읽었다. 별도 HTTP403 응답은 원본문 cache가 아니다.',
      '- 2017 CBA II11 PDF74–75의 기간·슬롯·YOS; X4–6 PDF303–307의 tender/비NBA·early-entry 권리 조건을 직접 읽었다. 2017의 서비스 일수 규칙을 2020 게임 규칙으로 부르지 않는다.','',
      '## 남겨 둔 범위','',
      '- 정확 재정·개인 동의·현실 의료·실제 active/접수·향후 권리 null/false. 전체 비용·GSW·A1/A2·최종 시즌·원고는 이 leaf로 통과하지 않는다.',''])

def self_test(d):
    cases=[('invent standard Terry',lambda x:x['selection']['CHA_TERRY'].update(contract_class='STANDARD')),
      ('third TW',lambda x:x['selection']['CHA_RILLER'].update(historical_CHA_two_way_adopted=True)),
      ('actual cash zero',lambda x:x['selection']['CHA_TERRY'].update(exact_cash_or_guarantee_selected=0)),
      ('everlasting Bonga rights',lambda x:x['selection']['WAS_BONGA'].update(exclusive_rights_after_model_window_certified=True)),
      ('skip2020tender',lambda x:x['selection']['WAS_BONGA']['finite_rights_execution']['annual_required_tenders'].pop()),
      ('startX5clock',lambda x:x['selection']['WAS_BONGA']['finite_rights_execution']['X5_branch_if_agreement_is_professional'].update(effective_immediate_availability_notice_before_scope_end=True)),
      ('wrongnaturalyear',lambda x:x['selection']['WAS_BONGA']['finite_rights_execution'].update(naturally_eligible_draft_is_Subsequent_Draft_year=2020)),
      ('erase Homesley contract',lambda x:x['selection']['WAS_HOMESLEY'].update(contract_class=None)),
      ('generic hardship',lambda x:x['selection']['WAS_BELL_JAN'].update(general_extra_roster_capacity=True)),
      ('real medical',lambda x:x['scope'].update(actual_medical_certified=True)),
      ('whole A2',lambda x:x['scope'].update(A1_or_A2_promoted=True)),
      ('use45day asgamecap',lambda x:x['two_way_usage_witness']['Tyrell Terry'].update(conservative_2020_regular_game_limit=45)),
      ('lose positive player',lambda x:x['roster_states'][next(iter(x['roster_states']))]['standard'].pop())]
    # Compare to one reconstructed expected result, then test actual construction semantics separately.
    for label,mutate in cases:
        changed=deepcopy(d);mutate(changed);assert validate(changed,expected=d),label
    old=source.input_models
    def add_riller():
        games=deepcopy(old());next(g for g in games if g['team']=='CHA')['seconds']['Grant Riller']=1
        return games
    with patch.object(source,'input_models',side_effect=add_riller):
        try:build()
        except AssertionError:pass
        else:raise AssertionError('source positive Riller must block removal')
    for label,mutate in [('constructor4YOS',lambda f:f['CHA_TERRY'].update(entering_years_of_service=4)),
        ('constructorSkip2019Tender',lambda f:f['WAS_BONGA']['finite_rights_execution']['annual_required_tenders'].pop(1))]:
        wrong=deepcopy(selected_family());mutate(wrong)
        with patch(__name__+'.selected_family',return_value=wrong):
            try:build()
            except AssertionError:pass
            else:raise AssertionError('constructor false PASS: '+label)
    return len(cases)+3

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    d=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(render(d),encoding='utf-8')
    errors=[]
    if a.check:
        if json.loads(text(OUT))!=d:errors.append('JSON stale')
        if text(MD)!=render(d):errors.append('MD stale')
    negatives=self_test(d) if a.self_test else 0
    print(json.dumps({'current':not errors,'errors':errors,'summary':d['summary'],'negative_controls':negatives},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
