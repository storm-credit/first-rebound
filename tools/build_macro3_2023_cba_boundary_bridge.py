"""Bind dated macro3 consumers to operative CBA boundaries, not contract choices."""
from __future__ import annotations
import argparse, hashlib, json
from copy import deepcopy
from datetime import datetime, timedelta
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
from pypdf import PdfReader
import build_chicago_long_core_cba as prior

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tools/build_macro3_2023_cba_boundary_bridge.py'
SOURCE = 'research/MACRO3_2023_CBA_BOUNDARY_PRIMARY_SOURCES_2026_10_07.json'
CORE = 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json'
RIGHTS = 'research/SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY_2026_10_07.json'
OUT = 'research/MACRO3_2023_CBA_BOUNDARY_BRIDGE_2026_10_07.json'
MD = OUT.replace('.json', '.md')
PINS = {'research/MACRO3_2023_CBA_BOUNDARY_PRIMARY_SOURCES_2026_10_07.json': '59b03c494187eb29177640806ae97427a837abff38bf4516f588758fc87a0112', 'simulation/CHICAGO_2022_CORE_RETENTION_SELECTED_FAMILY.json': 'e7d0f4b15bc06c7cd16a38d158b38a78871fb7372d412639e33bb20c31d225a7', 'research/SIMONOVIC_2022_23_SELECTED_RIGHTS_FAMILY_2026_10_07.json': 'c404fc401f6c30809ed5098663dd2b277b1c4cb7844d15c697991460f1290ac4', 'tools/build_chicago_long_core_cba.py': '415d5bc239e590a30e46f8cfd5dca2149c2b7f1df25d6bb25aef8f681c4fc693', 'simulation/CHICAGO_LONG_CORE_CBA_INPUTS.json': '7985e65cb5e184356aead888d4f016aca187dd2dd3185ea6de76527a6937fe0c'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()

def read(root, path):
    return json.loads((root/path).read_text(encoding='utf-8-sig'))

def physical_sources(root=ROOT):
    for p, expected in PINS.items():
        require(sha(root/p)==expected, 'Reviewed repository source changed: '+p)
    s=read(root,SOURCE)
    require(s==json.loads((root/SOURCE).read_text(encoding='utf-8-sig')), 'Returned source manifest differs from physical source')
    pdf=s['cba_pdf']; raw=Path(pdf['path']).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==pdf['raw_sha256'], 'CBA PDF bytes changed')
    r=PdfReader(Path(pdf['path']))
    for p in pdf['pages']:
        actual=r.pages[p['pdf_page_one_based']-1].extract_text()
        require(hashlib.sha256(actual.encode()).hexdigest()==p['text_sha256'], 'CBA primary page changed')
    n=s['nbpa'];body=Path(n['path']).read_bytes()
    require(hashlib.sha256(body).hexdigest()==n['raw_sha256'], 'NBPA body changed')
    require(b'took effect on July 1, 2023' in body and b'Effective through 6/30/2023' in body, 'NBPA operative boundary not in body')
    require(n['facts']=={'2017_effective_through':'2023-06-30','2023_effective_from':'2023-07-01'}, 'Effective dates falsely changed')
    return s

def contract_cba(date_ET):
    date=datetime.fromisoformat(date_ET).date().isoformat()
    return '2017_OPERATIVE' if date<='2023-06-30' else '2023_OPERATIVE'

def extension_window(first_regular_date, second_option_exercised, qualifying_veteran):
    require(type(second_option_exercised) is bool and type(qualifying_veteran) is bool, 'Eligibility must be explicit')
    end=(datetime.fromisoformat(first_regular_date)-timedelta(days=1)).strftime('%Y-%m-%dT18:00:00')
    return {'opens_ET':'2023-07-06T12:01:00','closes_ET':end,'eligible':second_option_exercised and qualifying_veteran,'physical_first_regular_date_supplied':False,'date_is_caller_parameter_not_selected_schedule':True}

def extension_allowed(at_ET, first_regular_date, second_option_exercised=True, qualifying_veteran=True):
    w=extension_window(first_regular_date,second_option_exercised,qualifying_veteran)
    return w['eligible'] and w['opens_ET']<=at_ET<=w['closes_ET']

def lm1_reference(cap_first_extended_year, higher_max, signed_new_bonuses=0):
    """Existing 25->30% proposal only; higher-max qualification remains input."""
    require(type(higher_max) is bool and cap_first_extended_year>0 and signed_new_bonuses==0, 'Unadmitted LM1 salary input')
    percent=30 if higher_max else 25
    first=Fraction(cap_first_extended_year*percent,100)
    salary=[first+first*Fraction(8*i,100) for i in range(5)]
    require(all(n.denominator==1 for n in salary), 'Reference cents require explicit rounding')
    return {'Higher_Max_parameter':higher_max,'percent':percent,'reference_salary_by_year':[int(n) for n in salary],'sum':int(sum(salary)),'cap_year_used':'2024-25_FIRST_EXTENDED_YEAR','actual_qualification_or_mutual_consent_certified':False,'contract_selected':False}

def table_scope(at_ET, row, after_that_salary_year_regular=False, prior_TMLE=False):
    if contract_cba(at_ET)=='2017_OPERATIVE':
        return {'status':'2017_CONSUMER_REQUIRED_NOT_2023_TABLE','current':None,'next_year':None}
    year=int(at_ET[:4]) if at_ET[5:7]>='07' else int(at_ET[:4])-1
    return prior.transaction_apron_limits(row,year,after_that_salary_year_regular,prior_TMLE)

def second_round_exception(at_ET, draft_rights_owned, draft_rookie_status, existing_NBA_UPC):
    # II15(b)(iii) starts12:01 ET on first moratorium day, even though the
    # new CBA itself is already operative earlier that day.
    return at_ET>='2023-07-01T12:01:00' and contract_cba(at_ET)=='2023_OPERATIVE' and draft_rights_owned and draft_rookie_status and not existing_NBA_UPC

def build(root=ROOT):
    s=physical_sources(root)
    core=read(root,CORE);rights=read(root,RIGHTS)
    require(core==json.loads((root/CORE).read_text(encoding='utf-8-sig')) and rights==json.loads((root/RIGHTS).read_text(encoding='utf-8-sig')), 'Returned retained inputs changed')
    require(core['summary']['standard']==15 and core['summary']['two_way']==2 and core['summary']['apron_public_family_upper']==172483541, 'Prior FY22 cost or slots changed')
    announcement=s['nba_cap_announcement']
    require(announcement['moratorium_end_ET']=='2023-07-06T12:00:00' and announcement['free_agency_negotiation_start_ET']=='2023-06-30T18:00:00', 'Attributed public moratorium input changed')
    # The exact next regular-season date is a test parameter, not an adopted calendar.
    test_first='2023-10-24'
    clocks=[(t,extension_allowed(t,test_first)) for t in ('2023-07-06T12:00:00','2023-07-06T12:01:00','2023-10-23T18:00:00','2023-10-23T18:00:01')]
    require([allowed for _,allowed in clocks]==[False,True,True,False], 'Rookie extension boundary lost')
    tables=[{'at_ET':d,'row':row,'after_salary_year_regular':after,'rules':table_scope(d,row,after)} for d,row,after in [('2023-06-30T18:00:00','H',True),('2023-07-06T12:01:00','H',False),('2024-06-23T12:00:00','H',True),('2024-07-06T12:01:00','H',False),('2024-07-06T12:01:00','G',False)]]
    # Independent caller expectations: do not obtain expected values by calling
    # the returned constructor again. PDF212/214/215 define these distinct phases.
    expected_tables=[
      {'status':'2017_CONSUMER_REQUIRED_NOT_2023_TABLE','current':None,'next_year':None},
      {'status':'APRON_TABLE_SCOPE_ONLY','current':None,'next_year':None},
      {'status':'APRON_TABLE_SCOPE_ONLY','current':None,'next_year':'second'},
      {'status':'APRON_TABLE_SCOPE_ONLY','current':'second','next_year':None},
      {'status':'TRANSITION_TPE_ENDED_REQUIRES_OTHER_ROUTE','current':None,'next_year':None}]
    require([t['rules'] for t in tables]==expected_tables,'Returned table loses dated current/next-year CBA restriction')
    lm=[lm1_reference(140588000,h) for h in (False,True)]
    for returned,percent,higher in zip(lm,(25,30),(False,True)):
        first=Fraction(140588000*percent,100)
        expected=[int(first*(1+Fraction(8*i,100))) for i in range(5)]
        require(returned['reference_salary_by_year']==expected and returned['sum']==sum(expected),'Returned LM1 salary schedule loses first-year-based annual raises')
        require(returned['percent']==percent and returned['Higher_Max_parameter']==higher and not returned['contract_selected'] and not returned['actual_qualification_or_mutual_consent_certified'],'Returned LM1 eligibility or scope falsely promoted')
    return {'id':'MACRO3_2023_CBA_BOUNDARY_BRIDGE','baseline_main':'15e0e1f2edcc9862b096cc190b752aecbe3aca31','classification':'PRIMARY_SOURCE_DATED_LEGAL_APPLICABILITY_AND_CONDITIONAL_CONSUMER_FUNCTIONS','source_sha256':{**PINS,SELF:sha(root/SELF)},
     'facts':{'2017_through':'2023-06-30','2023_from':'2023-07-01','NBA_announcement':deepcopy(announcement),'rookie_extension_opens_ET':'2023-07-06T12:01:00','rookie_extension_deadline':'18:00 ET on day before first regular day of second option year; caller must bind actual chosen season calendar','source_pdf_pages':[p['pdf_page_one_based'] for p in s['cba_pdf']['pages']]},
     'contract_boundary_tests':[{'at_ET':d,'operative':contract_cba(d)} for d in ('2023-06-29T12:00:00','2023-06-30T23:59:59','2023-07-01T00:00:00')],
     'extension_boundary_tests':[{'at_ET':t,'allowed':a,'first_regular_day_test_parameter':test_first} for t,a in clocks], 'apron_table_dated_tests':tables,
     'LaMelo_LM1_conditional_reference':lm,'LaMelo_higher_max_requirement':'II7(a),(c),(d): All-NBA or DPOY immediately prior or 2 of prior3; MVP1 of prior3. Contract mechanism depends on already-qualified status vs fourth-RSC-year conditional clause. All-Star alone is insufficient; no award, cap or contract chosen.',
     'Coby_handoff':{'QO_issue_by_2023_June29_under_2017_XI4':'UNEXECUTED: exact rookie-scale/YOS/starter tests and valid tender must be consumed from dated selected season','negotiation_before_moratorium_is_not_signed_UPC':True,'July6_after_moratorium_retention_offer':'UNEXECUTED: lawful current signing mechanism/consent/current six-costs and membership still needed','QO_automatically_recomputed_by_2023_rules':False},
     'second_round_exception_tests':[{'case':n,'allowed':second_round_exception(d,owned,rookie,upc)} for n,d,owned,rookie,upc in [('2022_NEW_RIGHT','2022-08-25T12:00:00',True,True,False),('2023_JULY1_NOON_BEFORE_WINDOW','2023-07-01T12:00:00',True,True,False),('2023_DRAFT_ROOKIE_WITH_RIGHT','2023-07-01T12:01:00',True,True,False),('WIESKAMP_ALREADY_NBA_CONTRACTED','2023-07-06T12:01:00',False,False,True)]],
     'awards_tests':[{'season_start_year':y,'rules':prior.award_requirement('MVP',y,[32]*64)} for y in (2022,2023)],
     'frozen_pick_tests':[{'salary_year_start':y,'rules':prior.frozen_pick(y,True,{})} for y in (2023,2024)],
     'preserved_FY22':{'standard':15,'two_way':2,'apron_public_family_upper':172483541,'new_2023_rules_retroactively_applied':False,'Simonovic_selected_overlay_retained':True,'old_private_receipts_certified':False},
     'remaining_finite_inputs':['2021-22/2022-23 actual selected result model and consumed rosters/availability.','Coby QO exact admitted-scale/starter tests; signing family and FY23 named six-costs.','LaMelo fourth-option eligibility and exact chosen2023 extension; first-extended-year cap and qualifying honors not auto-historical.','2022/2023 selected draft and later assets; relevant operation-specific 2023/2024 apron tests.'],
     'new_contract_or_author_season_selections':0,'whole_macro3_complete':False,'whole_G16_complete':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}

def validate(x,root=ROOT):
    try:
        require(x==build(root),'Saved bridge differs from source-bound legal consumers');return []
    except (ValueError,AssertionError) as e:return [str(e)]

def render(x):
    return '\n'.join(['# 3번 2023 CBA 날짜별 적용 인계','',
      '2017 CBA는 2023June30까지, 새 CBA는 July1부터다. 새 법을 이전 경기/계약 선택으로 소급하거나 실제 cap 공지를 가상 세계의 선택으로 읽지 않는다.',
      '', '## 실제 닫은 적용 경계','',
      '- 공식 NBA June30 18:00 ET 협상 허용과 계약 체결을 분리했다. July6 moratorium 종료는12:00 ET이고 rookie-scale 연장 창은 **12:01 ET**부터다. 하루 전18:00 종료는 실제 다음시즌 달력을 인자로 받아야 한다.',
      '- Coby의 June29 QO는2017 소비기에서 발행/검문한다. 발효일이 왔다고 기존 QO·계약·권리·명단을 무료로 교체하지 않는다.',
      '- VII2(e)의2023–24 F–J 당해 면제와 다음 급여연도 제한,2024–25 새 제한을 분리했다. Second-apron 픽 규칙은2024–25부터이고 정확 시점의Apron Salary가 필요하다.',
      '- LM1의25→30%/5년/첫해8% 산식은 기존 **조건부 제안**이다. 첫 연장연도2024cap을 쓰며 Higher Max/서명수락 미선택을 보존한다. All-Star만으로30%가 되지 않는다.',
      '- 새 second-round 예외는2023 이후 유효권리·draft rookie 계약에만 연결한다. Wieskamp의 이미 체결된2021NBA UPC 갱신이나2022 Tender에 소급0; 예전 지명연도 자체만으로 미서명 draft rookie를 배제하지 않는다.',
      '- 65경기 규칙을2022–23 MVP자격에 소급0. 2023–24의64경기 표본은일반기준 미충족이며 예외/이의·실제수상은 선택0.',
      '', '## 근거·권위','',
      '[NBPA](https://nbpa.com/cba)·[2023 CBA](https://imgix.cosmicjs.com/25da5eb0-15eb-11ee-b5b3-fbd321202bdf-Final-2023-NBA-Collective-Bargaining-Agreement-6-28-23.pdf) 원바이트/15쪽pypdf 지문을 직접대조했다. [NBA2023 공지](https://pr.nba.com/nba-salary-cap-for-2023-24-season-set-at-136-021-million/)는 web귀속본문 관측이며 직접HTTP403/raw본문미인증을 분리한다.',
      'cap/tax/first/second의136.021m/165.294m/172.346m/182.794m는 실제역사 참고값이다. LaMelo 두 참고총액은203,852,600/244,623,120이며 실제 cap·자격·계약체결이 아니다.',
      '', '## 다음 실행','', *['- '+n for n in x['remaining_finite_inputs']], '',
      '[데이터](MACRO3_2023_CBA_BOUNDARY_BRIDGE_2026_10_07.json) · [원문manifest](MACRO3_2023_CBA_BOUNDARY_PRIMARY_SOURCES_2026_10_07.json)',
      '', '새계약선택0·전체3번false·실제Pack0·원고0·미완료5/6번까지4·v0.30 PARTIAL·설계/원고CLOSED.'])+'\n'

def self_test(root=ROOT):
    real=read(root,SOURCE);bad=deepcopy(real);bad['nbpa']['facts']['2023_effective_from']='2023-06-30'
    original=read
    with patch(__name__+'.read',side_effect=lambda r,p:bad if p==SOURCE else original(r,p)):
        try:build(root)
        except ValueError:pass
        else:raise AssertionError('Returned manifest boundary mutation falsely accepted')
    x=build(root);bad=deepcopy(x);bad['extension_boundary_tests'][0]['allowed']=True
    require(bool(validate(bad,root)),'12:00/12:01 saved-result mutation falsely accepted')
    require(not extension_allowed('2023-07-06T12:01:00','2023-10-24',False,True),'Unexercised second option extension falsely accepted')
    require(not second_round_exception('2023-07-06T12:01:00',True,True,True),'Existing UPC falsely uses draft rookie exception')
    require(not second_round_exception('2023-07-01T12:00:00',True,True,False),'Second-round contract before July1 12:01 falsely allowed')
    original_lm=lm1_reference
    def altered_salary(*args,**kwargs):
        r=original_lm(*args,**kwargs);r['reference_salary_by_year'][1]+=100000;r['reference_salary_by_year'][2]-=100000;return r
    with patch(__name__+'.lm1_reference',side_effect=altered_salary):
        try:build(root)
        except ValueError:pass
        else:raise AssertionError('Returned equal-total LM1 salary redistribution falsely accepted')
    original_table=table_scope
    def lost_next_year(d,row,after=False,prior_TMLE=False):
        r=original_table(d,row,after,prior_TMLE)
        if d=='2024-06-23T12:00:00' and row=='H':r['next_year']=None
        return r
    with patch(__name__+'.table_scope',side_effect=lost_next_year):
        try:build(root)
        except ValueError:pass
        else:raise AssertionError('Returned next-year apron limit silently deleted')
    return '7 critical counterexamples rejected, including 2 independently found returned-constructor defects'

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    x=build()
    if a.write:
        (ROOT/OUT).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(render(x),encoding='utf-8')
    if a.check:
        require(not validate(read(ROOT,OUT)), 'Saved bridge failed');require((ROOT/MD).read_text(encoding='utf-8-sig')==render(x), 'Saved MD differs')
    if a.self_test:print(self_test())
    print('2023 CBA dated bridge PASS; contract choices 0, macro3 unclosed')

if __name__=='__main__':main()
