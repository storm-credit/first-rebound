"""Public named DET prior-cost envelope; new B operating path remains unselected."""
import argparse,copy,hashlib,json,re
from pathlib import Path
from fractions import Fraction
from unittest.mock import patch
from bs4 import BeautifulSoup
import fitz
import build_detroit_2021_opening_named_operating_family as operating
ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_detroit_2021_initial_residual_cost_family.py'
OUT='research/DETROIT_2021_INITIAL_RESIDUAL_COST_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
CACHE=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-det-cost-20261007')

def text(path):return (ROOT/path).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(path):return hashlib.sha256(text(path).encode()).hexdigest()
def load(path):return json.loads(text(path))
def integer(x):return int(re.sub('[^0-9]','',x)) if re.search('[0-9]',x)else None
def tables(raw):
    soup=BeautifulSoup(raw,'html.parser')
    return [[[td.get_text(' ',strip=True)for td in tr.find_all(['th','td'])]for tr in table.select('tr')]for table in soup.select('table')]
def widget_decode(raw):
    s=raw.decode('utf8');a=s.index("document.write('")+len("document.write('");b=s.rindex("');")
    return s[a:b].replace('\\n','\n').replace('\\"','"').replace("\\'","'").replace('\\t','\t').replace('\\/','/')

def source_view():
    observed=[]
    for r in RAW:
        if 'cache_path' in r:
            raw=Path(r['cache_path']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==r['raw_sha256'],'Raw source changed: '+r['id']
        observed.append({**r,'adopted_body':r.get('status')==200 and r['id']not in ['BI_cdx','josh-smith']})
    w=next(r for r in RAW if r['id']=='BI_widget_20210605225504')
    decoded=widget_decode(Path(w['cache_path']).read_bytes())
    wr=tables(decoded)[0]
    future={row[0]:row[2]for row in wr[1:]if len(row)==6 and not row[0].endswith('Total:')}
    ss={}
    for r in RAW:
        if r['id'] in ['jerami-grant','josh-jackson','jahlil-okafor','mason-plumlee','blake-griffin','dewayne-dedmon','zhaire-smith','cory-joseph','deividas-sirvydis','rodney-mcgruder','tyler-cook','dzanan-musa','anthony-lamb','liangelo-ball','louis-king','reggie-jackson']:
            ss[r['id']]=tables(Path(r['cache_path']).read_bytes())
    body=BeautifulSoup((CACHE/'BI_20210728232429.html').read_bytes(),'html.parser').get_text(' ',strip=True)
    assert '(Updated on 7/22/21)'in body and 'Dennis Smith Jr ($17,060,031)'in body
    assert 'Cory Joseph $12,600,000 ($2.4 million guaranteed)'in body
    assert 'Mason Plumlee — 10 percent'in body
    return {'future':future,'vendor_tables':ss,'BI_body':body,'observations':observed,'decoded_raw_sha256':hashlib.sha256(decoded.encode()).hexdigest()}

def find_row(v,name,season,cap):
    rows=[r for t in v['vendor_tables'][name]for r in t if r and r[0].split(' ')[0]==season and any(x=='$'+format(cap,',')for x in r[1:6])]
    assert rows,'Missing named row '+name+'/'+season+'/'+str(cap)
    return rows[0]

def routine_policy():
    return {'selected':False,'B_Lyles_no_agreement_preserved':True,
     'effective_waiver_before_old_guarantee_trigger':['Cory Joseph','Rodney McGruder','Tyler Cook'],
     'original_already_owed_protected_salaries_not_waived_to_zero':True,
     'Joseph_old_2400000_remains':True,'Cook_full_old_1701593_reserved_even_if_unprotected':True,
     'legal_renunciation_after_July1_and_before_Olynyk':['Dennis Smith Jr.','Wayne Ellington','Brandon Knight','John Henson','Jordan McRae','Louis King','Anthony Lamb','LiAngelo Ball','Dzanan Musa','Tyler Cook','Rodney McGruder','Cory Joseph'],
     'no_outstanding_QO_for_renounced_names_at_renunciation':True,
     'preserved_RFA_QO_names':['Saben Lee','Frank Jackson','Hamidou Diallo'],
     'other_unsigned_first_round_rights_in_public_template':[],
     'no_other_offer_sheet_or_First_Refusal_Notice_selected':True,
     'all_renounceable_unused_exceptions_renounced_before_room_use':True,
     'minimum_and_later_room_MLE_statutory_paths_preserved':True,
     'no_new_unreported_settlement_resolution_or_salary_agreement_selected':True,
     'unknown_private_costs_certified_zero':False,'actual_notices_or_receipts_certified':False}

FIXED_POLICY=copy.deepcopy(routine_policy())

def construct_costs(v):
    f=v['future']
    expected={'Blake Griffin (W)':'$29,764,126','Dewayne Dedmon (W)':'$2,866,667','Zhaire Smith (W)':'$1,068,200','Dzanan Musa (W)':'','Jerami Grant':'$20,002,500','Mason Plumlee':'$8,137,500','Josh Jackson':'$5,005,350','Jahlil Okafor':'$2,130,023','Cory Joseph':'$12,600,000','Rodney McGruder':'$5,000,000','Deividas Sirvydis':'$1,517,981','Tyler Cook':'$1,701,593','Tyler Cook -- E':'','Tyler Cook - E':'','Saben Lee':'','Frank Jackson':'$1,789,256','Dennis Smith Jr':'$7,705,447','Wayne Ellington':''}
    assert all(f.get(n)==a for n,a in expected.items()),'Published future template semantics changed'
    assert len(f)==23,'Future public actor set changed'
    live={n:find_row(v,n,'2021-22',a)for n,a in [('jerami-grant',20002500),('josh-jackson',5005350),('jahlil-okafor',2130023),('mason-plumlee',9248333)]}
    assert all(r[-2:]==['$0','$0']for r in live.values()),'Published retained performance template changed'
    assert '$8,137,500 (+2%)'in live['mason-plumlee'],'Plumlee original base changed'
    for n,a in [('blake-griffin',29764126),('dewayne-dedmon',2748674),('zhaire-smith',1068200),('cory-joseph',2400000),('deividas-sirvydis',1517981)]:find_row(v,n,'2021-22',a)
    mc=find_row(v,'rodney-mcgruder','2021-22',5000000)
    assert mc[-3:]==['$0','$0','$0'],'McGruder zero-protection template changed'
    cook=find_row(v,'tyler-cook','2021-22',1701593)
    assert cook[-3:]==['$0','$0','$0'],'Cook protection template changed'
    musa=find_row(v,'dzanan-musa','2021-22',3615054)
    assert 'No (Dec 20, 2020)'in musa and musa[-3:]==['$0','$0','$0'],'Musa option nonexercise source changed'
    reggie=find_row(v,'reggie-jackson','2019-20',18086956)
    assert reggie[-2:]==['$0','$0']
    camp=[]
    for n,a in [('anthony-lamb',898310),('liangelo-ball',898310),('louis-king',449115)]:
        row=find_row(v,n,'2020-21',a);assert row[-2:]==['$0','$0']
        camp.append({'name':n,'old_contract_year':'2020-21','full_old_base_cash_reservation':a,'observed_row':row,'not_future_NBA_salary_fact':True})
    return {'retained_rows':live,'public_future_template':f,'camp':camp,
     'X_rows':[{'name':'Mason Plumlee historical post-assignment cap minus retained base upper','usd':9248333-8137500,'classification':'CONSERVATIVE_EXTRA_RESERVATION_NOT_ACTUAL_DET_TRADE_KICKER_TRIGGER'},
      {'name':'Dewayne Dedmon observed stretch source discrepancy','usd':2866667-2748674,'classification':'MAX_TWO_POSITIVE_REPORTS_MINUS_INCLUDED_BASE'},
      {'name':'Deividas Sirvydis source discrepancy reservation','usd':1603559-1517981,'classification':'EXISTING_AJ_DISCLOSED_DIFFERENCE_NOT_NEW_SOURCE_ENDPOINT'},
      {'name':'Tyler Cook old full annual amount','usd':1701593,'classification':'PROTECTED_RESIDUE_OUTER_RESERVATION_NOT_ZERO_GUARANTEE_CERT'},
      {'name':'2020 Lamb/Ball/King entire old cash','usd':sum(x['full_old_base_cash_reservation']for x in camp),'classification':'ENTIRE_PAST_CASH_EXTRA_RESERVATION_NOT_PAYMENT_ZERO_OR_FUTURE_ALLOCATED_SALARY_FACT'},
      {'name':'Lamb/Ball possible Exhibit10 cash','usd':100000,'classification':'TWO_50000_EXTRA_RESERVATIONS_NOT_ASSERTED_2021_CAP_CHARGE'}]}

def build():
    assert all(sha(p)==h for p,h in PINS.items()),'Reviewed source snapshot changed'
    op=load(operating.OUT)
    assert op==operating.build(),'Operating source meaning differs'
    pol=routine_policy();assert pol==FIXED_POLICY,'Legal operating conditions changed'
    v=source_view();c=construct_costs(v)
    ledger=load('research/O15G15AJ_DETROIT_AUG6_NAMED_SALARY_LEDGER.json')
    core=dict(ledger['original_core']);core.pop('Killian Hayes');core.pop('Saddiq Bey')
    core.update({'Patrick Williams':5572680,'Kira Lewis Jr.':3277080,'Mason Plumlee':8137500})
    dead=ledger['candidate_dead_money'];holds={'Jalen Suggs unsigned120pct hold':6592920,'Saben Lee FA':925258,'Frank Jackson QO':1939350,'Hamidou Diallo QO':2079826}
    base=sum(core.values())+sum(dead.values())+sum(holds.values());assert base==100052228
    x=sum(r['usd']for r in c['X_rows']);assert x==5361732
    ceiling=112414000-base-3000000;assert ceiling==9361772
    q=min(12195122,112414000-base-x);assert q==7000040 and q>=3000000
    initial_states=operating.trace(x,q,load(operating.AL),load(operating.AQ),load(operating.AR),op['policy'])
    # A widened legal outer estimate is retained separately; it is not an actual extra debt.
    broad_extra=16371000-(2748674+1068200)
    broad_x=x-(2866667-2748674)+broad_extra
    assert broad_x>ceiling
    with fitz.open(operating.CBA)as d:
        pages=[42,43,54,55,206,207,208,209,211,212,213,239,240,241,249,250,303,304]
        page_sha={str(n):hashlib.sha256(d[n-1].get_text().replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()for n in pages}
        assert 'fifteen percent (15%)'in d[249].get_text()
        assert '$5,000 and $50,000' in d[41].get_text()
        assert 'Two-Way Qualifying Offer'in d[206].get_text()
        assert 'only players who shall be counted'in d[211].get_text()
    return {'id':'DETROIT_2021_INITIAL_RESIDUAL_COST_FAMILY_2026_10_07','status':'INDEPENDENTLY_REVIEWED_PUBLIC_NAMED_SIX_CATEGORY_INITIAL_COST_ENVELOPE',
     'baseline_main':'e8070d14e7cfa43eab17c7e1cf62c5cbc71bba85','source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'Repository UTF8 BOMstrip CRLF/CR toLF; external raw bytes separate',
     'raw_observations':v['observations'],'BI_widget_decoding':{'source_raw':str(CACHE/'BI_widget_20210605225504.raw'),'method':'Extract literal document.write payload; replace escaped newline/tab/quote/slash; BeautifulSoup table cells','decoded_utf8_sha256':v['decoded_raw_sha256'],'capture':'2021-06-05T22:55:04','original_body_updated':'2021-07-22 separate capture2021-07-28','June_snapshot_is_not_July_table_timestamp':True},
     'CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(operating.CBA),'raw_sha256':operating.CBA_SHA,'PDF_1based_text_LF_sha256':page_sha},
     'scope':'Source-supported published named economic template plus explicit lawful fictional clearance/renunciation and conservative fullcash reservations. Not a certificate of all private original agreements or unreported future resolution events.',
     'policy':pol,'base_ledger':{'current_8':core,'already_included_prior_5':dead,'preserved_rookie_and_RFA_4':holds,'sum':base,'cap_counted_players_before_Olynyk':12,'incomplete_roster_charge':0},
     'source_contract_templates':c,'six_category_map':[
      {'id':'LIVE_AND_NOTIFIED_AGREEMENTS','bound':'Retained public rows plus canonical2020rookie aggregate80–120% upper and unsignedSuggs hold. Vendor zero incentive fields define published template, not private Γ absence; Plumlee extra1,110,833 reserved. Proposed other forms apply only after Olynyk; Lyles agreement0 is explicit B candidate, not copied history.'},
      {'id':'PRIOR_WAIVED_CAMP_AND_STRETCH','bound':'Five named old liabilities remain in base; Dedmon/Sirvydis maxsource extra203,571. Cook full1,701,593, oldcampfull2,245,735+possible100k reserved in addition. Musa valid4thoption nonexercise yields no newprotected2021salary; Reggie ordinaryended2019–20. Originalfuturepublished23actor template covers known retained economic rows; no private-debt absence or every former player certified.'},
      {'id':'FA_QO_OFFER_AND_FRN','bound':'Preserve Lee/Frank/Diallo charge until replacement. Smith/Ellington and other unused namedrights legally renounce; no outstandingQO is required at that action. No other offerSheet/FRN is selected; any newly selected notice reopens X, not presumed actual0.'},
      {'id':'DRAFT_AND_REQUIRED_TENDER','bound':'Suggs6592920 unsigned1R alreadybase; Aldama later minimumTender3m reservation in trace before acceptance, not initial8/9UPC. Otherpublicold2RrightsHands/Radicevic/JanisTimma/rights-only have no executedUPC or new2021outstandingTender selected. Any requirednewTender before8/9 reopens named charge.'},
      {'id':'ROSTER_AND_INCOMPLETE','bound':'8live +Suggs firsthold +3FA/QO =12 legal count, regardless waived former5/camp. Later trace count cannot lose 2021positive10; candidateactive12/15STD2TW remains separate. Offseasonmax20 includesTW; actualactive/medical0.'},
      {'id':'ANNUAL_EXCEPTIONS','bound':'Renounce unusedNTMLE/BAE/TPE before room calculation underVII6m2. Statutorymin/rookie and later eligibleRoomMLE preserved; roomMLE/NTMLE/BAE combination forbidden. Money sent/received in trades not playercapcost but separate annualcash rule. No exception receipt actualcert.'}],
     'initial_X':{'public_named_family_upper':x,'actual_X':None,'all_possible_private_original_costs_covered':False,'nonempty_q_threshold':ceiling,'spare_to_threshold':ceiling-x,'legal_q_family':[3000000,q],'exact_q_selected':None,'same_original_reported_Olynyk_amount_carried':False,'changed_longterm_contract_offer_is_unselected_consequential_comparison':True,'function':'For every admitted X in [0,5361732], q in [3000000,min(12195122,12361772-X)] exists.'},
     'candidate_trace_at_envelope_endpoint':initial_states,'later_apron_boundary':{'trace_final_normal_salary_upper':initial_states[-1]['team_salary_upper'],'full_adjusted_apron_cost_not_certified':True,'no_new_roomMLE_hardcap':True,'BKN_current_budget_asset_and_matching_not_closed':True},
     'broad_stretch_outer_screen':{'last_prior_cap_outer':109140000,'fifteen_percent':16371000,'replace_known_two_stretch_with_full_statutory_outer':broad_extra,'resulting_X_outer':broad_x,'passes_nonempty_q_screen':False,'actual_extra_debt_found':False,'actual_illegality_found':False,'explanation':'Law-only15pct over-envelope need not be saturated by the public named family. It is a failed sufficient bound, not a fabricated debt or private-absence gate.'},
     'Nets_conditional_manifest_only':{'date':'2021-09-04','out_DET':['Sekou Doumbouya','Jahlil Okafor'],'in_DET':['DeAndre Jordan full current9881598','BKN2022 second','WAS2024 conditional second','GSW2025 conditional second','BKN2027 second','cash amount unknown'],'source': 'research/O15G15AE_DETROIT_AUGUST15_AND_SEPTEMBER_ASSET_BRIDGE.md','actual_complete_original_release_body_new_download':False,'new_download403_not_evidence':True,'exact_changed_world_holder_protection_priority_cash_balance':None,'cost_family_closes_asset_ownership':False},
     'remaining_named_scope':['Review this public initialX template and clearance/renunciation family before adoption.','A/B direction, Olynyk reducedoffer and changedmincontracts remain unselected; preserve downstreamLyles/Bagley comparison.','DET/BKN jointfutureseconds/cash/bonus/matching and entirelaterapron need separate finite witness.','Identify any preserved extra namedliability or newly selected notice/settlement and re-open its owncharge, without requiring everyprivate receipt.'],
     'certification':{'independent_review_completed':True,'conditional_initial_X_family_supported':True,'whole_DET_cost_legal_or_roster_execution_PASS':False,'actual_contract_salary_or_cents':False,'actual_acceptance_or_notices':None,'author_selected_A_or_B':False,'whole_macro3_complete':False,'central_or_REGISTER_changed':False,'manuscript_count':0},'progress':op['progress']}

def validate(o):
    try:assert o==build(),'Saved envelope differs from current source reconstruction';return []
    except(AssertionError,KeyError,OSError,ValueError)as e:return[str(e)]

def markdown(o):
    x=o['initial_X'];b=o['broad_stretch_outer_screen']
    lines=['# Detroit 초기 X: 공개 실명 비용 가족','',o['status'],'','원 AL/AQ/AR와 검문된 B 운영안을 보존하고 초기 추가비용을 여섯 범주로 연결했다. 실제 사적 장부를 인증하지 않으며 새 계약·A/B 방향을 선택하지 않는다.','',f"기존 포함액 **100,052,228**, 초기 X 공개 가족 상단 **{x['public_named_family_upper']:,}**, 비공허 문턱 **9,361,772**. 여유 **{x['spare_to_threshold']:,}**. 따라서 그 가족의 X마다 Olynyk 새 제안 q가 **3,000,000–{x['legal_q_family'][1]:,}**에서 존재한다. 원12,195,122급여를 그대로 승인했다는 뜻이 아니다.",'','|추가 예약|달러|범위|','|---|---:|---|']
    for r in o['source_contract_templates']['X_rows']:lines.append(f"|{r['name']}|{r['usd']:,}|{r['classification']}|")
    lines+=['','캠프의 옛 전액과 Cook의 전액을 더해도 기존 보호급여를 지우지 않았다. 과거 현금 예약을 미래 급여 사실로 부르지 않는다. Plumlee의 후행 이적 cap차액은 retained계약의 실제 새 kicker로 복사하지 않고 추가상단만 사용했다.','', '## 실제 새 원자료','', '17 SalarySwish raw를 회수했다. 16개에서 계약행을 읽었고 Josh Smith 페이지는 과거 계약행이 없어 개별 말단 근거로 세지 않았다. 표는 league계약서가 아닌 vendor 경제템플릿이다. Pincus의 [2021년7월22일 본문](https://web.archive.org/web/20210728232429id_/https://www.basketballinsiders.com/detroit-pistons-team-salary/)과 [6월5일 future widget](https://web.archive.org/web/20210605225504id_/http://hw-files.com/tools/salaries/salaries_widget_new.php?team_id=13)은 별도 캡처다. 한 날짜로 합치지 않았다. 원JS와 decodeSHA를 분리했다. NBA3 URL의 HTTP403·현재BI리다이렉트는 본문 근거로 세지 않았다. Keith Smith의9월9일 oEmbed는 원기자 게시물의 합계 앵커일 뿐 Reddit표를 원문으로 인증하지 않았다.','', '## 여섯 범주와 합법 후보 조건','']
    for r in o['six_category_map']:lines.append(f"- **{r['id']}**: {r['bound']}")
    lines+=['',f"법규15%만으로 모르는 이전stretch전부를 **16,371,000**에 예약하면 X **{b['resulting_X_outer']:,}**가 문턱을 넘는다. 이것은 더 넓은 상단검사 실패이고 실제부채·불법반례가 아니다. 여기의 더 좁은 가족은 당시 공개 future23행과 원계약 positive행에 의해 명명되며, 모든 비공개 조항의 부재를 인증하지 않는다. 식별되는 새 보존의무·새 settlement가 있으면 해당 이름을 재개방한다.",'','Nets후속은 두선수/Jordan전액/네조건부2R/현금 전체가 필요하다. 목록은 연결했지만 변경세계의 실제소유·보호·priority·cash잔액·Brooklyn전체비용은 아직 미검문이다. 초기 room함수가 닫힌다고 이 거래나 전체apron이 닫히지 않는다.','', '[2017 CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) II6, VII4/6m/7d6, X4 원쪽을 직접 대조했다. effectiveclearance·unusedrights/exceptionrenunciation·validQO 보존은 실제서류 발견이 아니라 가상 합법 실행 조건이다. 법정 minimum 수치의3m 기존 상단조건도 유지한다.','', '[원 DET 운영안](DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.md) · [로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','', '|번호|묶음|상태|','|---|---|---|','|1|2020드래프트 연쇄|완료|','|2|Chicago2020–21|S2완료|','|3|2021–23 거래·계약|DET 초기 공개X상단 후보 산출; 방향·공동거래·whole비용 남음|','|4|장기 커리어|후속시즌 대기|','|5|결말·전체구조|전체 기능표 남음|','|6|집필규격·ContextPack|현행 누적등록기 참조·Pack0|','|7|통합·독립·작가승인|최종CLOSED|','','미완료 큰 묶음5 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.','']
    return '\n'.join(lines)

def self_test():
    out=build();tests=[]
    bad=copy.deepcopy(out);bad['base_ledger']['already_included_prior_5']['Cory Joseph old-contract guarantee']=0;assert validate(bad);tests.append('lost_old_guarantee')
    old=source_view;v=old();v['future']['Dewayne Dedmon (W)']='$0'
    with patch(__name__+'.source_view',return_value=v):
        try:build()
        except AssertionError:tests.append('source_stretch_removed')
        else:raise AssertionError('Source empty debt false PASS')
    p=routine_policy();p['no_outstanding_QO_for_renounced_names_at_renunciation']=False
    with patch(__name__+'.routine_policy',return_value=p):
        try:build()
        except AssertionError:tests.append('renounce_live_QO')
        else:raise AssertionError('Invalid QO renunciation accepted')
    p=routine_policy();p['unknown_private_costs_certified_zero']=True
    with patch(__name__+'.routine_policy',return_value=p):
        try:build()
        except AssertionError:tests.append('private_absence_invented')
        else:raise AssertionError('Private falsecertificate accepted')
    return tests

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
    print(json.dumps({'current':True,'X_upper':o['initial_X']['public_named_family_upper'],'q_upper':o['initial_X']['legal_q_family'][1],'whole_cost':False,'negative_controls':self_test()if a.self_test else[]},ensure_ascii=False))
PINS={'research/DETROIT_2021_OPENING_NAMED_OPERATING_FAMILY_2026_10_07.json': '7490b1a46a744088980c115680140383615a2e6ec92901e1fdd901c326861be0', 'tools/build_detroit_2021_opening_named_operating_family.py': 'ff635732271be6c65959a4d60e5f8f72deb79eba01fe1fb1c69532d000375fe9', 'research/O15G15AJ_DETROIT_AUG6_NAMED_SALARY_LEDGER.json': '60d2affe397313d19b8f3f5450db9308dc6bab98864ca725e1f73c30cc5f71bb', 'research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.json': 'cd0d31fced740134f94f34d1a6ce7b24c1205ce9360be3ae61e2d4abf43253b2', 'research/O15G15AQ_DETROIT_LEE_CAP_ROOM_AND_NONBIRD_ROUTE.json': '6b4806825d623e445f17a093239800a8f49f7841266244129818275681a622fa', 'research/O15G15AR_DETROIT_NAMED_EXIT_AND_ROSTER_CHARGE.json': '9f75d9af0af324303dc670249b023f69005dd3fb2624edf7322c4e2791469ac5', 'research/O15G15AN_DETROIT_WAIVER_AND_EXCEPTION_BRANCHES.json': '5647681551ab54121bde49fc657b0ab7e18807cbf6029ecafede627cd320e266', 'research/O15G15AK_DETROIT_AUG6_RIGHTS_AND_WAIVER_TIMING.md': '9c306fe85a0e85181cc6330dc06de36ea90db1a349caeca9ca72b04a7a8cb6ce', 'research/O15G15AE_DETROIT_AUGUST15_AND_SEPTEMBER_ASSET_BRIDGE.md': 'b4304e955abf2b8acad7d7a5d1b32182b3a9445902a372929383faae4c899d5e', 'research/O15G15AU_DETROIT_AUG6_CONSIDERATION_LEDGER.md': 'cf96e40e2683d0375d11f9eeea016238c65e4a4072ac5e0ecf3b64276351390a'}
RAW=[{'id': 'jerami-grant', 'url': 'https://www.salaryswish.com/players/jerami-grant', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\jerami-grant.html', 'raw_sha256': 'b0d9badcd599cbb53c633b8d218ffcdf2c45638586c9119bdce64733fdee4981', 'bytes': 111787}, {'id': 'josh-jackson', 'url': 'https://www.salaryswish.com/players/josh-jackson', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\josh-jackson.html', 'raw_sha256': '0b740f103517d48b74cbabd8b3efbfa899b7b93e0d00fd71ef339ea447ba5bc8', 'bytes': 104737}, {'id': 'jahlil-okafor', 'url': 'https://www.salaryswish.com/players/jahlil-okafor', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\jahlil-okafor.html', 'raw_sha256': '9f0cfadb71f647163036628823193a207e8c98a9bfd3b975adc6adce9af102d5', 'bytes': 123402}, {'id': 'mason-plumlee', 'url': 'https://www.salaryswish.com/players/mason-plumlee', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\mason-plumlee.html', 'raw_sha256': 'a27473776a5ed78d7abb6c49ae958e72cc3bbb28bd3b00c32ec41fcea4d86c22', 'bytes': 134659}, {'id': 'blake-griffin', 'url': 'https://www.salaryswish.com/players/blake-griffin', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\blake-griffin.html', 'raw_sha256': '38102508aeffa8834030feb0b1f9ffaeca3b7fca6dd9608aae9791ef0062e78b', 'bytes': 125605}, {'id': 'dewayne-dedmon', 'url': 'https://www.salaryswish.com/players/dewayne-dedmon', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\dewayne-dedmon.html', 'raw_sha256': '8afc0380b9638ce8294ccb2ed9eaf7aa910129e1c461f1b5a267fd49193b09d8', 'bytes': 170409}, {'id': 'zhaire-smith', 'url': 'https://www.salaryswish.com/players/zhaire-smith', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\zhaire-smith.html', 'raw_sha256': '2de262df849ef31fd51f4791f1b60ebca2a5f6458078d7405ea8f0c8c1d0caaa', 'bytes': 132425}, {'id': 'cory-joseph', 'url': 'https://www.salaryswish.com/players/cory-joseph', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\cory-joseph.html', 'raw_sha256': 'ee58f96b935696c7cb0166f6d1ec8bc4ee2faf6be2eff82475043264c5b952b0', 'bytes': 125819}, {'id': 'deividas-sirvydis', 'url': 'https://www.salaryswish.com/players/deividas-sirvydis', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\deividas-sirvydis.html', 'raw_sha256': '71351cc6ddca184d3ac517c31a0e176fb4a8314af4e6a40ffba5f5be8df588c6', 'bytes': 111683}, {'id': 'rodney-mcgruder', 'url': 'https://www.salaryswish.com/players/rodney-mcgruder', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\rodney-mcgruder.html', 'raw_sha256': '89edb8120cd7d2c06fa0f2ac470a52313805daa06d2f9f4f2d7c2e09e1df9cc7', 'bytes': 130047}, {'id': 'tyler-cook', 'url': 'https://www.salaryswish.com/players/tyler-cook', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\tyler-cook.html', 'raw_sha256': 'a562899f6111d8593be3f715feb9754b1c0cff31f0aa430dec6fb4f2e73fe2af', 'bytes': 159828}, {'id': 'dzanan-musa', 'url': 'https://www.salaryswish.com/players/dzanan-musa', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\dzanan-musa.html', 'raw_sha256': '7ca936d4133b9107bf59069e19510f1d1a7e0c3d74488cff272b25e8aee432a9', 'bytes': 94643}, {'id': 'anthony-lamb', 'url': 'https://www.salaryswish.com/players/anthony-lamb', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\anthony-lamb.html', 'raw_sha256': '5a5e160632714eb6cd6e72fe6c7c610087267699bc0e6ec0bc347d6fdf2ec985', 'bytes': 132809}, {'id': 'liangelo-ball', 'url': 'https://www.salaryswish.com/players/liangelo-ball', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\liangelo-ball.html', 'raw_sha256': '6c3c983aa4c83b8b7f406c9862d29438efa870ce676072bafbfb828c35537462', 'bytes': 104072}, {'id': 'louis-king', 'url': 'https://www.salaryswish.com/players/louis-king', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\louis-king.html', 'raw_sha256': 'f8de8e592f84bd04bf2edc968bcc5dfe933c6938793e428522b6c9a767a2cdea', 'bytes': 120225}, {'id': 'josh-smith', 'url': 'https://www.salaryswish.com/players/josh-smith', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\josh-smith.html', 'raw_sha256': 'cfd66808fc12d0a6931f85f4fea53b72beea1f7f06babf56a421e7948d3a9cba', 'bytes': 85140}, {'id': 'reggie-jackson', 'url': 'https://www.salaryswish.com/players/reggie-jackson', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\reggie-jackson.html', 'raw_sha256': '16d0173c498de0879925e6f7ad8acc64946eb23ae8114b76177745f4f6810e4e', 'bytes': 140785}, {'id': 'keith_dead_total', 'url': 'https://publish.twitter.com/oembed?url=https://twitter.com/KeithSmithNBA/status/1435979985911693312', 'final_url': 'https://publish.x.com/oembed?url=https://twitter.com/KeithSmithNBA/status/1435979985911693312', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\keith_dead_total.raw', 'raw_sha256': '877fc033f3ca5c2dce273d9417a2405c8f464ffe899f58ee68a7392db3818b22', 'bytes': 893}, {'id': 'nba_musa', 'url': 'https://www.nba.com/pistons/news/detroit-pistons-waive-dzanan-musa', 'final_url': 'https://www.nba.com/pistons/news/detroit-pistons-waive-dzanan-musa', 'status': 403, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\nba_musa.raw', 'raw_sha256': '979e82efc21bda2395d623fb071b14a76fab479bca635c9fa25745830ea14fee', 'bytes': 435}, {'id': 'nba_camp2020', 'url': 'https://www.nba.com/pistons/news/detroit-pistons-announce-2020-21-training-camp-roster', 'final_url': 'https://www.nba.com/pistons/news/detroit-pistons-announce-2020-21-training-camp-roster', 'status': 403, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\nba_camp2020.raw', 'raw_sha256': '693cfc105058cf009c61b29e633e91d8d803d713500c521f789baba35c566bce', 'bytes': 467}, {'id': 'nba_nets_jordan', 'url': 'https://www.nba.com/nets/news/2021/09/04/brooklyn-nets-complete-trade-detroit-pistons', 'final_url': 'https://www.nba.com/nets/news/2021/09/04/brooklyn-nets-complete-trade-detroit-pistons', 'status': 403, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\nba_nets_jordan.raw', 'raw_sha256': '38f6f26c43ddd73cbd0be4dc386a3871a0fcb54fa481a372c6cef588be25cd4d', 'bytes': 470}, {'id': 'BI_cdx', 'url': 'https://web.archive.org/cdx/search/cdx?url=basketballinsiders.com/detroit-pistons-team-salary/&from=2021&to=2021&output=json&filter=statuscode:200&collapse=timestamp:6', 'final_url': 'https://web.archive.org/cdx/search/cdx?url=basketballinsiders.com/detroit-pistons-team-salary/&from=2021&to=2021&output=json&filter=statuscode:200&collapse=timestamp:6', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\BI_cdx.raw', 'raw_sha256': '937e00f3da6a68336b78d54425bce1aa134952d5c5ac3f10821a994a97706355', 'bytes': 1883}, {'id': 'BI_20210728232429', 'url': 'https://web.archive.org/web/20210728232429id_/https://www.basketballinsiders.com/detroit-pistons-team-salary/', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\BI_20210728232429.html', 'raw_sha256': '3a42043839a33425f32b575a361b35aa20bb13ee0f479f1d9365d3d47a756a3f', 'bytes': 114273}, {'id': 'BI_20210605222356', 'url': 'https://web.archive.org/web/20210605222356id_/http://www.basketballinsiders.com/detroit-pistons-team-salary/', 'status': 200, 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\BI_20210605222356.html', 'raw_sha256': 'f5b78216d9b46623457c1df58b4ce7fcfdd7076e320ae7d68d95e90c77812126', 'bytes': 132101}, {'id': 'BI_widget_20210605225504', 'url': 'https://web.archive.org/web/20210605225504id_/http://hw-files.com/tools/salaries/salaries_widget_new.php?team_id=13', 'status': 200, 'raw_sha256': '202e86f644c4884824615c81ac2ffd7b419cbc0568a42a44d4a6025aaab4fe89', 'cache_path': 'C:\\Users\\Storm Credit\\AppData\\Local\\Temp\\first-rebound-det-cost-20261007\\BI_widget_20210605225504.raw', 'bytes': 11924}]

if __name__=='__main__':main()
