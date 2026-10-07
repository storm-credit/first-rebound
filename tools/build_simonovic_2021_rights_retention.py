"""Finite Simonovic rights family through SQ1 Aug12; not perpetual rights.

An institutional operative tender calendar is an external rule parameter, not
an invented2020 deadline or actual delivery receipt. NBA activation is absent.
"""
import argparse
import copy
import hashlib
import json
import re
from datetime import date,timedelta
from pathlib import Path
from unittest.mock import patch
import fitz
from bs4 import BeautifulSoup
import build_2021_approved_a_draft_signing_execution as sq

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_simonovic_2021_rights_retention.py'
OUT='research/SIMONOVIC_2021_RIGHTS_RETENTION_2026_10_07.json'
MD=OUT[:-5]+'.md'
SQ=sq.OUT
CLOCK='research/O15G15BC_SIMONOVIC_DRAFT_RIGHTS_CLOCK.md'
EARLY='research/O15G15BD_SIMONOVIC_EARLY_ENTRY_2021_DRAFT_CLOCK.md'
LOAN='research/O15G15BE_SIMONOVIC_OLIMPIJA_MEGA_LOAN_CHAIN.md'
PINS={'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json': '11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312', 'tools/build_2021_approved_a_draft_signing_execution.py': '2e5c63ae32cc3897e1117c895687c047ed4fb1256e4addf888330697dc70c304', 'research/O15G15BC_SIMONOVIC_DRAFT_RIGHTS_CLOCK.md': '27c44d66451c909f4e36de21ffcc7b26ff48ceac01678e3387914a0ed0cb523a', 'research/O15G15BD_SIMONOVIC_EARLY_ENTRY_2021_DRAFT_CLOCK.md': 'aa92337c1a39144fd2a3a7423c39f24a144a2916700c1a34dae84191bbeae011', 'research/O15G15BE_SIMONOVIC_OLIMPIJA_MEGA_LOAN_CHAIN.md': 'c7cdcc51e813cc9187af26b752f2f175205bdfb4b3d1db305e0abc7aa6cb5d6b', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
BASELINE='db1a59ec55fcacf7bbbb042bb1b460ca5600fbad'
DRAFT=date(2020,11,18)
END=date(2021,8,12)
NATURAL=date(2021,7,29)
RAW_DIR=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-simonovic-20261007')
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'
RAW=[
 ('NBA_DRAFT2020','https://www.nba.com/news/2020-nba-draft-results-picks-1-60','2689c6aa77ae0dc0da32fdb85381b5bcbdfdc301738316b14c54269c1d6a8fcc'),
 ('NBA_EARLY2020','https://pr.nba.com/twenty-three-early-entry-candidates-withdraw-from-nba-draft-2020-presented-by-state-farm/','e88f043cb1c448122361df6ba76495f66f5bad80874833f4a9a90a0721ae36bc'),
 ('BULLS_SIGN2021','https://www.nba.com/bulls/news/bulls-sign-rookies-dosunmu-and-simonovic','f9194554db5d943ded3e7a41b3eff7f0f1aabafbcce635d5075f03818c849fc6'),
 ('NBA_CBA2020','https://pr.nba.com/nba-nbpa-2020-21-season/','1c52c58a661108b42f00374e51971d2c244e89a29a143fbb8a6151d1a2329e94'),
 ('ABA_DRAFT_LOAN','https://www.aba-liga.com/news/44140','4a9d8044ce5fdaeeb93e5d350e3e505045c277927ca4976c03319c01fc2eaca8'),
 ('ABA_2018_CONTRACT','https://www.aba-liga.com/news/40325','6cec9763e746987c0bc64d62e21503dbb123074f1210ce511a4b0365c2d763b3'),
]

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def normalized(t):return t.replace('\r\n','\n').replace('\r','\n')

def raw_sources():
    obs=[];bodies={}
    for ident,url,pin in RAW:
        p=RAW_DIR/(ident+'.html');raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin,ident
        soup=BeautifulSoup(raw,'html.parser')
        if ident=='BULLS_SIGN2021':
            node=soup.find('script',id='__NEXT_DATA__');assert node
            def find(o):
                if isinstance(o,dict):
                    if 'contentStructured' in o:return o['contentStructured']
                    for v in o.values():
                        f=find(v)
                        if f is not None:return f
                if isinstance(o,list):
                    for v in o:
                        f=find(v)
                        if f is not None:return f
                return None
            parts=find(json.loads(node.string));assert parts
            body=' '.join(x.get('text',BeautifulSoup(x.get('html',''),'html.parser').get_text(' ',strip=True)) for x in parts)
            extraction='HTML __NEXT_DATA__ contentStructured text fields; not iframe shell'
        else:body=soup.get_text(' ',strip=True);extraction='BeautifulSoup HTML text'
        body=normalized(body);bodies[ident]=body
        obs.append({'id':ident,'url':url,'cache_path':str(p),'raw_sha256':pin,'bytes':len(raw),
          'classification':'PRIMARY_CLUB_LEAGUE_OR_NBA_PUBLIC_BODY','extraction':extraction,
          'normalized_extracted_text_sha256':hashlib.sha256(body.encode()).hexdigest()})
    checks={'NBA_DRAFT2020':['44.','Bulls draft','Marko Simonovic'],
      'NBA_EARLY2020':['Marko Simonovic','Mega Bemax','1999','November 18'],
      'BULLS_SIGN2021':['44th-overall pick in 2020','terms of the contracts were not released',
                        'continued his career overseas during the 2020-21 season','KK Mega Basket','June 11'],
      'NBA_CBA2020':['adjustments','December 22','November 22'],
      'ABA_DRAFT_LOAN':['on a loan at Mega Soccerbet','44th'],
      'ABA_2018_CONTRACT':['multi-annual deal','Marko Simonović','Petrol Olimpija']}
    for ident,tokens in checks.items():
        for token in tokens:assert token in bodies[ident],ident+':'+token
    assert re.search(r'Marko Simonovic.{0,180}Mega Bemax.{0,180}1999 DOB',bodies['NBA_EARLY2020'])
    raw=CBA.read_bytes();assert hashlib.sha256(raw).hexdigest()==CBA_SHA
    doc=fitz.open(stream=raw,filetype='pdf');pages={}
    for n in [30,31,32,252,301,302,303,304,305,306,307,308]:
        t=normalized(doc[n-1].get_text());pages[str(n)]=hashlib.sha256(t.encode()).hexdigest()
    for n,tokens in {30:['one (1) Season','October 15','signed by the Team'],
      304:['Section 5.','previously','covers all or any part'],305:['one-year','September 10','bona fide'],
      306:['next NBA Draft','personal delivery'],307:['shall never','same, but no greater'],252:['thirty (30) days']}.items():
        compact=' '.join(doc[n-1].get_text().split())
        for token in tokens:assert token in compact,f'CBA{n}:{token}'
    obs.append({'id':'CBA2017','url':'https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf',
       'cache_path':str(CBA),'raw_sha256':CBA_SHA,'bytes':len(raw),
       'classification':'PRIMARY_OFFICIAL_CBA','extraction':'PyMuPDF page.get_text();LF normalized',
       'pdf_page_one_based_normalized_text_sha256':pages})
    return obs

def sources(reader=load,hasher=sha):
    assert set(PINS)=={SQ,sq.SELF,CLOCK,EARLY,LOAN,'AGENTS.md'}
    for p,pin in PINS.items():assert hasher(p)==pin,'Unreviewed source change '+p
    prior=reader(SQ);assert not sq.validate(prior),'SQ1 current producer validation'
    assert len(prior['standard_roster_working'])==15 and len(prior['two_way_working'])==2
    assert prior['Simonovic']['standard_contract_added'] is False
    assert max(e['date'] for e in prior['working_events'])=='2021-08-12'
    assert not any('simonovi' in str(x).lower() for x in prior['standard_roster_working'])
    return prior

def operating_policy():
    return {
      'initial_draft':'2020-11-18','initial_round':2,'initial_pick':44,'rights_holder':'CHI','birth_year':1999,
      'international_early_entry':True,'natural_eligibility_draft_year':2021,
      'existing_NonNBA_contract_covers_part_of_2020_21_NBA_Season':True,
      'professional_compensation_above_living_stipend_in_admitted_contract_family':True,
      'actual_original_foreign_compensation_or_exact_end_date':None,
      'Petrol_Cedevita_legal_entity_identity_automatically_equated':False,
      'new_NonNBA_signings_from_initial_draft_through_scope_end':0,
      'new_foreign_extension_or_loan_reexecution_selected':False,
      'intercollegiate_basketball_after_initial_draft':False,
      'initial_Required_Tender':{
        'fictional_procedural_implementation':'Offer compliant team-signed one-Season Standard UPC at statutory minimum under ArticleI1(ddd), delivered personally to player/representative in the operative2020 tender window; player does not accept.',
        'operative_delivery_window_parameter':'W20 from applicable NBA/NBPA adjusted calendar; a nonempty legal tender window, exact endpoints not recovered',
        'submission_selection_function':'choose first admissible delivery date d in W20; no historical d asserted',
        'operative_acceptance_deadline_parameter':'A20 from applicable adjusted RequiredTender rules',
        'offer_acceptance_time':'At least A20; no shortened player acceptance window',
        'team_signed':True,'personally_delivered_to_player_or_representative_in_window':True,
        'offer_term_seasons':1,'minimum_salary':'then applicable statutory MinimumAnnualSalary for0NBA YOS',
        'extra_bonus_or_option_added':False,'player_accepted':False,'tender_withdrawn':False,
        'NBA_exclusive_rights_expressly_renounced':False,
        'actual_window_endpoints_or_delivery_date':None,'actual_league_receipt_certified':False},
      'NBA_UPC_executed_through_scope_end':False,'new_NBA_trade_or_draft_rights_assignment_selected':False,
      'no_new_rights_renunciation_or_agreed_tender_withdrawal_in_working_path':True,
      '2021_annual_tender_if_due_by_scope_end':'Supply same valid one-Season minimum offer within applicable annual operative window; unaccepted. No guessed modified deadline.',
      'future_2021_Sept_notice_or_tender_automatically_completed':False,
      'family_scope_end':'2021-08-12','forever_rights_certified':False,
      'post_Aug12_overseas_contract_or_NBA_registration_selected':False,
    }

FIXED_POLICY=operating_policy()
def checked_policy():
    p=operating_policy();assert p==FIXED_POLICY,'Working rights/tender/foreign-clock policy changed'
    t=p['initial_Required_Tender']
    assert p['rights_holder']=='CHI' and p['initial_pick']==44 and p['birth_year']==1999
    assert p['existing_NonNBA_contract_covers_part_of_2020_21_NBA_Season']
    assert p['new_NonNBA_signings_from_initial_draft_through_scope_end']==0
    assert not p['NBA_UPC_executed_through_scope_end']
    assert t['team_signed'] and t['offer_term_seasons']==1 and not t['player_accepted'] and not t['tender_withdrawn']
    assert not t['NBA_exclusive_rights_expressly_renounced'] and t['actual_window_endpoints_or_delivery_date'] is None
    return p

def tender_date_selector(window_first,window_last,acceptance_deadline):
    """Existential construction for each supplied operative institutional window.

    This isn't a guess at calendar endpoints. Test examples are declared model
    samples, not recovered NBA calendar dates. Reject impossible/retroactive input.
    """
    assert DRAFT<=window_first<=window_last,'Nonempty postdraft legal window required'
    assert acceptance_deadline>=window_first,'Acceptance deadline precedes delivery'
    return window_first

def availability_clock():
    days=[];d=DRAFT
    while d<=END:
        expires=d.replace(year=d.year+1)
        assert expires>END
        days.append({'hypothetical_effective_immediate_notice_date':d.isoformat(),
          'X5a_one_year_expiry':expires.isoformat(),'rights_period_has_not_ended_at_scope_end':True})
        d+=timedelta(days=1)
    drafts=[]
    for draft in [DRAFT,NATURAL]:
        expires=draft.replace(year=draft.year+1)
        assert expires>END
        drafts.append({'hypothetical_X5a2_applicable_draft_date':draft.isoformat(),
          'X5a_one_year_expiry':expires.isoformat(),'rights_period_has_not_ended_at_scope_end':True})
    assert min(x['X5a_one_year_expiry'] for x in days+drafts)=='2021-11-18'
    return days,drafts

def build(reader=load,hasher=sha):
    prior=sources(reader,hasher);obs=raw_sources();p=checked_policy();days,drafts=availability_clock()
    return {'id':'SIMONOVIC_2021_RIGHTS_RETENTION_2026_10_07','schema':'FINITE_SECOND_ROUND_NONNBA_RIGHTS_FAMILY_V1',
      'status':'SOURCE_SUPPORTED_WORKING_RETENTION_FAMILY_INDEPENDENTLY_REVIEWED',
      'baseline_main':BASELINE,'source_sha256':dict(PINS,**{SELF:sha(SELF)}),
      'source_hash_method':'UTF8BOMstripped;CRLF/CRtoLF','raw_sources':obs,
      'source_facts':{
        '2020_initial_round_pick_holder':[2,44,'CHI'],'2020_international_early_entry_birth_year':1999,
        '2018_source':'ABA original multi-annual Petrol Olimpija contract report; exact years/entity succession not recovered',
        '2020_source':'ABA draft-date Mega loan report',
        '2021_Bulls_source':'Original NBA signing announcement also confirms continued2020–21 Mega career, including June11 event. It does not release contract terms.',
        'actual2021NBAactivation_not_copied':True,'actual_foreign_contract_end_or_notice_or_tender':None,
        '2020_public_calendar_adjustments_do_not_publish_tender_deadline':True},
      'working_policy':p,
      'quantifier':{'preserved_external_inputs':'All admitted original NonNBA contract durations/availability dates and institutional operative tender windows consistent with the positive sources and rules.',
        'constructed_implementation':'For each admissible window choose compliant team tender delivery; retain unaccepted/no withdrawal/no renunciation/no newNonNBA signing throughAug12.',
        'required_window_is_a_rule_input_not_a_private_receipt':'Exact adjusted2020 calendar not recovered; the family constructs a compliant offer under the applicable operative rule, not a historical submission claim.',
        'lawful_tender_family_existence_is_not_actual_submission':True},
      'rights_clock':{'initial_draft':DRAFT.isoformat(),'scope_end':END.isoformat(),
        'natural_international_22_year_draft':NATURAL.isoformat(),
        'X5_nonNBA_season_condition_supported_in_preserved_public_family':True,
        'immediate_notice_cells':days,'next_season_notice_draft_cells':drafts,
        'no_effective_notice_branch':'One-year availability clock has not begun; only the bounded Aug12 outcome is certified in this working family.',
        'earliest_possible_X5a_expiry':'2021-11-18','scope_end_precedes_earliest_expiry_by_days':(date(2021,11,18)-END).days,
        'X6_natural2021_does_not_delete_active_X5_period':'X6(a) subject to5; X6(c) NonNBA signing never shortens early-entry exclusive period. Natural2021 is retained as the ordinary fallback, not misreported as automatic FA.',
        'X5e_early_FA_guard':'No new NonNBA signing after initial draft throughAug12 in this working path, so the conjunctive newSigning+bonaFideEffort+tenderFailure trigger is absent. No inference about actual private signing history.',
        'X4f_g_early_FA_guards':'No agreed tender withdrawal and no express rights renunciation are selected; they would reopen immediately.',
        'X5b_c_July_notice':'Any qualifyingJuly1 availability notice with actualSeptember1 freedom requires tender bySept10 to extend; both September checkpoints are outside this Aug12 certificate.',
        'fallback_ordinary_X4_X6_without_qualified_NonNBA':{'July29_2021_subsequent_draft_or_FA_may_apply':True,'covered_by_this_family':False},
        'whole2021_22_rights_window_certified':False,'indefinite_exclusivity_certified':False},
      'roster_and_cost':{'through':'2021-08-12','source_working_standard_players':copy.deepcopy(prior['standard_roster_working']),
        'source_working_two_way_players':copy.deepcopy(prior['two_way_working']),
        'standard_contract_count_preserved':15,'two_way_count_preserved':2,
        'new_Simonovic_NBA_UPC':False,'new_NBA_salary_charge_usd':0,
        'why_zero':'Only unsigned second-round negotiating rights and unaccepted tender; no player-executed NBA UPC. Does not imply foreign compensation0.',
        'foreign_pay_or_buyout_amount_certified':False,'NBA_buyout_or_foreign_compensation_payment_selected':False,
        'actual_registered_roster_or_medical_certified':False},
      'assignment_and_acceptance_boundary':{'rights_transfer_selected':False,
        'X7_same_but_no_greater_rights_if_later_assigned':True,'unsigned_rights_assignment_has_no_30day_rookie_contract_wait':True,
        'if_NBA_UPC_accepted':'Reopen SQ1 slot/budget; 16th standard contract is not automatically accepted into the selected regular-season15. VII8(d)(i)30day trade wait then applies to signed Draft Rookie, not to this unsigned claim.',
        'actual2021signing_fact_does_not_certify_prior_exclusive_clock':True},
      'post_scope_reopen':[
        'Aug13 or any change to noNBA UPC/noNonNBA signing/withdrawal/renunciation working path.',
        'QualifiedSeptember1 availability with timelySeptember10 tender; validate actual applicable annual calendar before modelling continuation.',
        'EarliestNov18 one-year endpoint: newNonNBA contract/bona-fide negotiation/tender under5(d)-(f), subsequent draft orFA outcome separately.',
        'Foreign contract end does not alone erase NBA exclusive rights; effective written availability notice and5(g)delivery controls the clock.',
        'No automatic future extension/overseas team/term/2022NBAactivation chosen.'
      ],
      'summary':{'rights_holder':'CHI','origin_year':2020,'origin_pick':44,'scope_start':'2020-11-18','scope_end':'2021-08-12',
        'immediate_notice_dates_checked':len(days),'next_season_draft_clock_examples':len(drafts),
        'standard_count_before_after':[15,15],'two_way_count_before_after':[2,2],
        'constructed_finite_retention_family_supported':True,'actual_Tender_or_rights_certificate':False,
        'new_NBA_contracts':0,'new_foreign_contracts':0,'whole_future_rights_PASS':False},
      'authority':{'routine_candidate_within_SQ1_noNBAactivation':True,'new_long_term_choice_selected':False,
        'new_author_lock':False,'actual_foreign_or_NBA_consents_certified':False,'macro3_complete':False,
        'new_REGISTER_or_central_promotion':False},
      'independent_review_completed':True,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','actual_context_packs':0,'manuscript_count':0,'manuscript_allowed':False}

def validate(value):
    try:return [] if value==build() else ['Rights family not exact source reconstruction']
    except (AssertionError,KeyError,ValueError,TypeError,OSError) as e:return [str(e)]

def markdown(d):
    return f'''# Simonović 2020 #44 — SQ1 2021-08-12까지의 미서명 권리 가족

**{d['status']}**. 무기한 독점이나2021–22 전체 창 종료가 아닌, 기존 SQ1 마지막8/12의 권리/명단 연결 후보입니다. 원역사8/18 NBA입단은 사실이며 이 경로에서 NBAUPC는0입니다.

## 사실·규칙·후보

[NBA 초기 지명](https://www.nba.com/news/2020-nba-draft-results-picks-1-60)은 CHI2020#44입니다. [Early Entry](https://pr.nba.com/twenty-three-early-entry-candidates-withdraw-from-nba-draft-2020-presented-by-state-farm/)는1999년생 국제 참가자를 명시합니다. [Bulls 원입단](https://www.nba.com/bulls/news/bulls-sign-rookies-dosunmu-and-simonovic)은2020–21 Mega 경력과2021원입단을 확인하며 계약조건은 공개하지 않습니다. [ABA2018 계약](https://www.aba-liga.com/news/40325), [2020 임대](https://www.aba-liga.com/news/44140)는 계약/임대 관측을 연결합니다. Petrol과 Cedevita 법인·정확 만료일·보수·NBA해지조항을 자동 확정하지 않습니다.

X5 진입은 초기지명 당시 존재한 비NBA 프로 계약이 직후 NBA시즌 일부를 덮는 가족입니다. Bulls의 실제2020–21 해외 경력과 계약/임대 발표를 긍정 근거로 그 공개 보존 가족을 구성합니다. X1(d)의 생활비 수당보다 큰 프로 보수 조건은 가족 입력으로 보존하며 실제 보수액을 인증하지 않습니다. 단순 임대 보도만으로 모든 private 계약/승계 조건을 확정하지 않습니다.

새 작가잠금0. 루틴 후보는 **초기 유효RequiredTender·미수락·미철회·미renounce·초기지명 이후8/12까지 새NonNBA서명0·NBAUPC0**입니다. 기존 해외계약이 끝나도 자동 연장하거나 새 계약을 채우지 않습니다. 8/12 해외팀에 실제 등록되어 있었다는 인증도 없습니다.

## 유한 종료 증인

X5(a)의 두 유효 가용통지 시계는 초기지명2020-11-18보다 앞설 수 없습니다. 즉시 가용통지의 모든 가상 날짜{d['summary']['immediate_notice_dates_checked']}개와 applicable2020/2021 draft 기준 두 날짜를 검문했습니다. 가장 이른1년말단 **2021-11-18**, SQ1 **2021-08-12**보다{d['rights_clock']['scope_end_precedes_earliest_expiry_by_days']}일 늦습니다. 유효 통지 없음이면 시계가 미개시이며 이 문서는8/12까지만 다룹니다. 실제 통지일을 선택하지 않습니다.

1999년생 국제 선수의 natural22세 draft2021-07-29는 X6 기본 경계입니다. 그러나 X6(a)는X5에 종속되고 X6(c)는 비NBA서명이 기존 기간을 단축하지 않으므로, 현재 활동 중인 X5의1년을7/29에 자동 삭제하지 않습니다. 새NonNBA서명0 조건은 X5(e)의 기간말단 전 즉시FA(새서명+bona-fide협상+tender실패) 반례를 차단하는 **후보 행동**입니다. 이를 원역사 실제 부재 사실로 읽지 않습니다.

## Tender 절차와 미조회 날짜

I1(ddd)의 RequiredTender는 구단이 서명한 **1시즌 표준UPC·법정 최소연봉 이상** 제안을 개인/대리인에게 적법하게 전달하고 요구 수락 시간을 보장하는 절차입니다. 선수 미수락이면 이 모델에서 실행된 NBAUPC가 없습니다. X4(f)의 선수 서면동의 철회나(g)의 NBA expressrenounce를 선택하면 권리가 즉시 재개방됩니다.

[NBA/NBPA2020 조정 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)는 수정된 달력의 존재를 지지하지만 정확Tender기한을 공개하지 않습니다. **W20=적용되는 유효 제출창**, **A20=적용되는 수락 마감**을 제도적 외부입력으로 남깁니다. 비어 있지 않은 W20마다 첫 허용일d를 선택하고 최소 A20까지 제안을 여는 후보를 구성합니다. 2020의7/15·9/5·10/15를 실제개정일로 넣지 않았으며 실제 제출·접수는false/null입니다. 이 법적 구현 가능 가족과 원역사 실제 제출은 구분합니다. 2021 annual창이8/12 이전에 적용된다면 동일 절차를 그창에서 공급하며, 이후창은 다음 검문 대상입니다.

2021July1 예고+실제September1 장애 없음일 때X5(b)/(c)의September10Tender는 이8/12범위 이후입니다. 전체2021–22 권리 존속, 추가해외계약, bona-fide협상 및X5(d)–(f) 후속draft/FA는 재개방 대상입니다. 이를 완료로 숨기지 않습니다.

## 명단·비용·양도

CHI 표준15/TW2를 그대로 보존합니다. 미계약2R 권리·미수락제안은 Simonović의16번째 표준계약을 추가하지 않습니다. 신규NBA급여0은 해외급여0이나원계약보장0을 뜻하지 않습니다. 새NBA계약·해외이적료 지급을 선택하지 않습니다.

X7의 권리 양도는 같은 권리만 이전하며 시계를 새로 만들지 않습니다. 이번 경로는 양도0입니다. **30일**은 VII8(d)(i)의 서명한 DraftRookie 표준계약 거래 대기로, 미서명 권리 유지/양도에 자동 이식하지 않습니다. Tender수락/NBA입단은 별도 비용·명단·예외 경로를 재검문해야 하며 원8/18 입단을 복사하지 않습니다.

새raw6와재사용CBA12쪽 지문·초기기관창 및 notice변조 검문은 JSON/생성기에 있습니다. 별도 담당자의 원문·시계·constructor반례 검문을 수용했습니다. 전체2021–22 권리·wholemacro3/원장/중앙 승격0입니다.

## 진행표

[현행 전체 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)

|번호|단계|상태|
|---|---|---|
|1|2020 draft연쇄|완료|
|2|Chicago2020–21|완료|
|3|2021–23 거래·계약|전체 비용·#16·현재 권리 창 후보 검문|
|4|장기 커리어|후속 설계 남음|
|5|결말·전체 구조|전체 기능표 남음|
|6|집필 규격·Context Pack|현재누적21 국소기능·Pack0|
|7|통합·독립·작가 승인|최종 미완료|

미완료큰묶음5, freezev0.30PARTIAL, 설계/원고CLOSED, 원고0.
'''

def self_test():
    value=build();controls=[]
    for label,change in [
      ('wrong_origin',lambda x:x['source_facts'].update({'2020_initial_round_pick_holder':[2,44,'ORL']})),
      ('NBA_activation_copy',lambda x:x['roster_and_cost'].update(new_Simonovic_NBA_UPC=True)),
      ('forever_rights',lambda x:x['rights_clock'].update(indefinite_exclusivity_certified=True)),
      ('deadline_invented',lambda x:x['working_policy']['initial_Required_Tender'].update(actual_window_endpoints_or_delivery_date='2020-09-05')),
      ('natural_draft_erases_clock',lambda x:x['rights_clock'].update(earliest_possible_X5a_expiry='2021-07-29')),
      ('new_foreign_signing_without5e',lambda x:x['working_policy'].update(new_NonNBA_signings_from_initial_draft_through_scope_end=1)),
      ('wholemacro3',lambda x:x['authority'].update(macro3_complete=True))]:
        bad=copy.deepcopy(value);change(bad);assert validate(bad),label;controls.append(label)
    for label,change in [
      ('constructor_newforeign',lambda p:p.update(new_NonNBA_signings_from_initial_draft_through_scope_end=1)),
      ('constructor_withdrawal',lambda p:p['initial_Required_Tender'].update(tender_withdrawn=True)),
      ('constructor_playeraccepts',lambda p:p['initial_Required_Tender'].update(player_accepted=True)),
      ('constructor_wrong_term',lambda p:p['initial_Required_Tender'].update(offer_term_seasons=2))]:
        bad=operating_policy();change(bad)
        with patch(__name__+'.operating_policy',return_value=bad):
            try:build()
            except AssertionError:controls.append(label)
            else:raise AssertionError(label)
    # Synthetic operative-window examples are tests only, not asserted NBA dates.
    d=tender_date_selector(date(2020,11,19),date(2020,11,25),date(2020,12,10));assert d==date(2020,11,19)
    try:tender_date_selector(date(2020,9,1),date(2020,9,5),date(2020,10,15))
    except AssertionError:controls.append('retroactive2020calendar_rejected')
    else:raise AssertionError('Past calendar accepted')
    return controls

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');args=ap.parse_args();d=build()
    if args.write:
        (ROOT/OUT).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(d),encoding='utf-8')
    if args.check:assert not validate(load(OUT));assert text(MD)==markdown(d)
    controls=self_test() if args.self_test else []
    print(json.dumps({'current':True,'summary':d['summary'],'negative_controls':controls},ensure_ascii=False))
