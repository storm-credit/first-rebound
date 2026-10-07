"""Ordinary QO functions and bounded cost input, not a new financial selection."""
import argparse
import copy
import hashlib
import json
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import fitz
import build_chicago_2022_23_approved_core_contract_execution as core

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_rookie_rfa_qo_family.py'
OUT='research/CHICAGO_2022_ROOKIE_RFA_QO_FAMILY_2026_10_07.json'
MD=OUT[:-5]+'.md'
BASELINE='16167cf4f6f2da50cbb1c054b948f9efedee3ddc'
BOOK=Path(r'C:/Users/Storm Credit/AppData/Local/Temp/fr-2018-19-cba101-harrison.pdf')
BOOK_SHA='c5ce40b61ae6287afaf173d067b6eb20eee72a58a9dc3d24552c1a424dafb213'
CBA=core.CBA
PINS={'research/CHICAGO_2022_23_APPROVED_CORE_CONTRACT_EXECUTION_2026_10_07.json': '2cc7aeaeaef530f1c3fac5846348792c3d516eb1479af1ce56617deb2e7cb2b5', 'tools/build_chicago_2022_23_approved_core_contract_execution.py': 'edfd73eab1d8617517447edd3093eb2647376e503263b5360890d87cfcc93c05', 'research/CHICAGO_2021_SIGNED_MINIMUM_YEAR2_NUMERIC_REFINEMENT_2026_10_07.json': '47ac976c5d20d6aa95a9d9cfad5e4430785a5975e4213557b57fe8b60d99e24f', 'canon/CAREER_TIMELINE.md': 'c6420cc02031b138103fe83dc02437dd209a3925d005e9a063855a66ee467eca', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json': '4b66d96a274fa4d31e41f6256192449e8b43a6dfc00e8f4e44f4cbd76e83bf78', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
FIXTURE={7:(3701000,4334500,4540700,270,341),9:(3116600,3650100,3823900,274,355),15:(2290900,2682900,2810700,533,398),16:(2176500,2549000,2670500,534,405),17:(2067500,2421500,2536800,536,412),18:(1964300,2300400,2410000,538,419),19:(1875800,2196900,2301600,540,426),20:(1800600,2108900,2209200,542,433),21:(1728600,2024500,2121100,593,441),22:(1659600,1943600,2036200,645,448),23:(1593300,1866000,1954700,697,455),24:(1529600,1791300,1876700,749,462),25:(1468400,1719600,1801600,801,469),26:(1419700,1662600,1741700,803,476),27:(1378700,1614600,1691600,804,483),28:(1370200,1604900,1681100,805,490),29:(1360200,1593000,1669000,805,500),30:(1350400,1581500,1656900,805,500)}
CBAPAGES=[208,209,240,241,294,295,309,310,311,314,315,316,317,318,319,320]

def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))
def ceil(q):return -(-q.numerator//q.denominator)
def rat(q):return {'numerator':q.numerator,'denominator':q.denominator}
def page_hash(t):return hashlib.sha256(t.replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()

def policy():
    return {'scope':'CONDITIONAL_NO2021_EXTENSION_ORDINARY_QO_FUNCTION; NOT_CX4_OR_E4_AUTHOR_SELECTION',
        'Carter_pick':7,'protagonist_team':'Chicago','protagonist_pick_domain':list(range(16,31)),
        'protagonist_exact_pick':None,'original_salary_cap_year':'2018-19',
        'original_third_year_base_floor_fraction':[4,5],'original_third_year_salary_plus_unlikely_ceiling_fraction':[6,5],
        'original_both_options_validly_exercised_and_playing_services_completed':'ADMITTED_CANDIDATE_CONDITION_NOT_ACTUAL_FACT',
        'no2021_extension_branch':True,'ordinary_QO_issue_deadline':'2022-06-29',
        'acceptance_must_remain_open_through':'2022-10-01',
        'Maximum_QO_selected':False,'offer_sheet_or_First_Refusal_exercise_selected':False,
        'starter_outcome_selected':False,'player_acceptance_selected':False,
        'full_future_season_required_to_define_function':False,'actual_QO_delivery_or_contract_cents_certified':False,
        'new_author_lock':False,'whole2022_23_cost_or_roster_closed':False}
FIXED_POLICY=copy.deepcopy(policy())

def checked_policy():
    p=policy();assert p==FIXED_POLICY,'QO branch, dates or authority changed';return p

def read_scale():
    assert hashlib.sha256(BOOK.read_bytes()).hexdigest()==BOOK_SHA,'2018 actual scale raw changed'
    with fitz.open(BOOK) as d:t=d[28].get_text()
    pattern=r'(?m)^\s*(\d+)\s+([\d,]+\.\d)\s+([\d,]+\.\d)\s+([\d,]+\.\d)\s+(\d+\.\d)%\s+(\d+\.\d)%'
    rows={int(k):tuple([int(Decimal(v.replace(',',''))*1000) for v in (a,b,c)]+[int(Decimal(f)*10),int(Decimal(q)*10)]) for k,a,b,c,f,q in re.findall(pattern,t)}
    assert set(rows)==set(range(1,31)),'Actual Exhibit A must contain all30 picks'
    return {k:rows[k] for k in FIXTURE}

def checked_scale():
    s=read_scale();assert s==FIXTURE,'Source scale/anchor changed';return s

def sources():
    assert hashlib.sha256(CBA.read_bytes()).hexdigest()==core.CBA_SHA,'CBA raw changed'
    with fitz.open(CBA) as d:
        pages=[{'PDF_1based':n,'fitz_text_LF_sha256':page_hash(d[n-1].get_text())} for n in CBAPAGES]
        bodies={n:d[n-1].get_text() for n in CBAPAGES}
    for n,words in {295:['first Option Year','Unlikely Bonuses'],310:['fourth Salary Cap','third and fourth Seasons'],311:['ninth player','fifteenth player','one hundred twenty'],315:['June 29','five (5) Seasons'],317:['October 1','July 13'],240:['Qualifying Offer','First Refusal']}.items():
        for w in words:assert w in ' '.join(bodies[n].split()),f'CBA rule anchor {n}/{w}'
    with fitz.open(BOOK) as d:
        bp=[{'PDF_1based':n,'fitz_text_LF_sha256':page_hash(d[n-1].get_text())} for n in (3,29)]
    return {'2017_CBA':{'url':'https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf','cache_path':str(CBA),'raw_sha256':core.CBA_SHA,'pages':pages},
        '2018_actual_Exhibit_A':{'url':'https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf','cache_path':str(BOOK),'raw_sha256':BOOK_SHA,'pages':bp,'table_PDF_1based':29,'table_units':'USD thousands; decimal0.1=USD100','all30_rows_parsed':True,'2017_Exhibit_B3_illustrative_table_used':False,'visual_inspection_cache':'C:/Users/Storm Credit/AppData/Local/Temp/fr-2018-19-cba101-rookie-qo-p29.png'},
        'collection':'REUSED_TWO_OFFICIAL_PDF_CACHES; NEW_DOWNLOADS_ZERO; CBA101_SUMMARY_NOT_COMPLETE_AGREEMENT'}

def starter(gs3,min3,gs4,min4):
    assert all(isinstance(v,int) and v>=0 for v in (gs3,min3,gs4,min4))
    return gs4>=41 or min4>=2000 or gs3+gs4>=82 or min3+min4>=4000

def factors(row):return Fraction(1000+row[3],1000),Fraction(1000+row[4],1000)

def original_vector(row,v):
    v=tuple(Fraction(x) for x in v);s=row[2]
    assert len(v)==3 and v[0]>=Fraction(4*s,5) and min(v[1:])>=0 and sum(v)<=Fraction(6*s,5),'Outside80-120% original three-component family'
    return v

def anchor(row):
    f,q=factors(row);fourth=Fraction(6*row[2],5)*f
    return fourth*q,ceil(Fraction(ceil(fourth))*q)

def own_upper(row):
    f,q=factors(row);fourth=Fraction(6*row[2],5)*f
    # For <=3 monetary components: sumceil(x_i)<=ceil(sumx_i)+2.
    # This conservative screen tolerates upward integer-dollar presentation at
    # BOTH stages. It does not certify an NBA statutory rounding algorithm.
    return ceil(Fraction(ceil(fourth)+2)*q)+2

def result(row,v,is_starter,scale):
    v=original_vector(row,v);f,q=factors(row)
    fourth=tuple(x*f for x in v);own=tuple(x*q for x in fourth)
    if row==scale[7] and not is_starter:
        a,_=anchor(scale[15]);bound=min(sum(own),a)
        return {'rule':'XI1c(ii)(B)_LESSER_OWN_COMPONENT_OFFER_OR_PICK15_BASE_ONLY','own_components':list(map(rat,own)),
            'anchor_base_only':rat(a),'charge_upper_exact_rational':rat(bound),'final_UPC_components_selected':False}
    if row!=scale[7] and is_starter:
        a,_=anchor(scale[9]);return {'rule':'XI1c(ii)(A)_PICK9_BASE_ONLY','components':[rat(a),rat(Fraction(0)),rat(Fraction(0))],'charge_upper_exact_rational':rat(a),'final_UPC_components_selected':False}
    return {'rule':'XI1c(ii)_OWN_FOURTH_YEAR_THREE_COMPONENTS','components':list(map(rat,own)),'charge_upper_exact_rational':rat(sum(own)),'final_UPC_components_selected':False}

def build():
    for p,h in PINS.items():assert sha(p)==h,'Unreviewed source '+p
    saved=load(core.OUT);assert not core.validate(saved),'Upstream core must reconstruct from its sources'
    refinement=load('research/CHICAGO_2021_SIGNED_MINIMUM_YEAR2_NUMERIC_REFINEMENT_2026_10_07.json')
    for p,h in refinement['source_sha256'].items():assert sha(p)==h,'Refinement source stale '+p
    p=checked_policy();s=checked_scale();src=sources();a9,u9=anchor(s[9]);a15,u15=anchor(s[15])
    rows=[];corners=[]
    for k in [7]+list(range(16,31)):
        row=s[k];ss=row[2];f,q=factors(row)
        vectors=[('BASE80',(Fraction(4*ss,5),0,0)),('BASE120',(Fraction(6*ss,5),0,0)),('BASE80_LIKELY40',(Fraction(4*ss,5),Fraction(2*ss,5),0)),('BASE80_UNLIKELY40',(Fraction(4*ss,5),0,Fraction(2*ss,5)))]
        for st in (False,True):
            upper=min(own_upper(row),u15) if k==7 and not st else u9 if k>=16 and st else own_upper(row)
            rows.append({'player':'Carter' if k==7 else 'Protagonist','pick':k,'starter':st,'qo_charge_screen_upper_usd':upper,'rule':result(row,vectors[0][1],st,s)['rule'],
                'third_year_scale_base':ss,'fourth_raise_fraction':rat(f),'QO_raise_fraction':rat(q),'continuous_original_terms_preserved':True})
            for label,v in vectors:corners.append({'pick':k,'starter':st,'simplex_corner':label,'third_year_components':list(map(lambda x:rat(Fraction(x)),v)),'QO_function':result(row,v,st,s)})
    cu=max(r['qo_charge_screen_upper_usd'] for r in rows if r['player']=='Carter')
    pu=max(r['qo_charge_screen_upper_usd'] for r in rows if r['player']=='Protagonist')
    total=cu+pu;assert (cu,pu,total,u15)==(9279761,7921302,17201063,7228449)
    assert len(rows)==32 and len(corners)==128 and all(r['pick'] in [7]+p['protagonist_pick_domain'] for r in rows)
    old=139703142;reserve=61827500;new=old-reserve+total
    return {'id':'CHICAGO_2022_ROOKIE_RFA_QO_FAMILY_2026_10_07','status':'INDEPENDENTLY_REVIEWED_ORDINARY_QO_FUNCTION_AND_CONDITIONAL_COST_INPUT','source_main_snapshot':BASELINE,
        'source_sha256':{**PINS,SELF:sha(SELF)},'source_hash_method':'UTF8 BOM stripped; CRLF/CR to LF','sources':src,'policy':p,
        'rule_map':{'third_to_fourth':'VIII1c(iii): regular, likely and unlikely each increase by pick fourth-year percentage; original conditions unchanged.',
            'own_QO':'XI1c(ii): same three fourth-year components each increase by pick QO percentage.',
            'starter_late_pick':'XI1c(ii)(A): picks10+ meeting Starter Criteria get rank9 at120%, Base only, no bonus.',
            'nonstarter_lottery':'XI1c(ii)(B): picks1-14 failing criteria get lesser own component offer or rank15 at120%, Base only. Carter7 starter stays own, never rank9.',
            'starter_formula':'GS4>=41 OR MIN4>=2000 OR GS3+GS4>=82 OR MIN3+MIN4>=4000; credited Official NBA statistics; future values unselected.',
            'presentation':'Component rational functions are exact input algebra; whole-dollar ceilings are conservative budget screens, not actual negotiated/league-rounded cents.',
            'nonstarter_package_boundary':'Carter lesser-of source alternatives preserved; no ad-hoc elementwise minimum or invented bonus erasure adopted as a final UPC.',
            'valid_offer':'XI1c(i),(v): one-year team-signed UPC, lawful delivery;100% Base skill/injury protection and standard payment, allowable unchanged terms; optional Exhibit6 not modeled as actual medical finding.',
            'eligibility_alternatives':'No timely QO =>UFA July1; unexercised first/second option =>earlier UFA. Both options/completed services are admitted conditions, not historical evidence.',
            'acceptance':'XI4c: offer open throughOct1; withdrawal throughJul13; later withdrawal needs written player agreement and triggers renunciation fromJul14; extension written, not pastMar1.',
            'Maximum_QO':'XI4a(ii), separate5-year maximum/8% offer; not selected. Ordinary QO accepted alternatively, not cumulatively.',
            'FAhold':'VII4d normal cap250/300% previous salary (bounded by max/floor), separate from ordinaryQO; not replaced here.',
            'apron':'VII6m3D excludes ordinaryFA hold but includes greater outstandingQO/FirstRefusal. This leaf supplies two ordinaryQO upper INPUTS only.',
            'First_Refusal':'XI5 offer sheet/right exercise is a separate cost event; not selected, reopens screen. Nonaccepted offer expiry alone does not remove ROFR.'},
        'scale_rows':[{'pick':k,'year1':v[0],'year2':v[1],'year3':v[2],'fourth_raise_permille':v[3],'QO_raise_permille':v[4]} for k,v in sorted(s.items())],
        'anchors':{'rank9':{'base_only_exact':rat(a9),'single_component_screen_upper_usd':u9},'rank15':{'base_only_exact':rat(a15),'single_component_screen_upper_usd':u15}},
        'branch_rows':rows,'simplex_corner_witnesses':corners,'coverage':{'continuous_original_component_simplex':True,'corners':128,'pick_starter_branches':32,'protagonist_exact_pick_selected':False,'actual_official_starter_statistics':None},
        'summary':{'Carter_QO_screen_upper_usd':cu,'protagonist_QO_screen_upper_usd':pu,'combined_QO_screen_upper_usd':total,'old_two_25pct_cap_reserve_usd':reserve,'bounded_input_reduction_usd':reserve-total,
            'old_partial_cost_screen':old,'conditional_replacement_partial_screen':new,'conditional_apron_screen':156982000,'conditional_remaining_X_screen':156982000-new,
            'if_separate_minimum_floorceil_condition_adopted_partial_screen':new-50,'if_same_condition_adopted_remaining_X_screen':156982000-new+50},
        'remaining_named_inputs':['Select consequential Carter extension CX1-3 versus noextension CX4; this conditional function chooses none.','Select protagonist contract/extension and exact2018pick only under existing author authority.','Apply future credited official-stat design to choose Starter branch; no new full-season gate required to define algebra.','Future timely delivery/acceptance/offer sheets/MaximumQO or FirstRefusal events reopen corresponding cost scope.','Other X roster/cost inputs and whole2022-23 family remain unfinished; this is not normal-cap clearance.'],
        'certification':{'independent_review_completed':True,'actual_private_cents_or_receipt':False,'actual_player_acceptance':False,'whole2022_23_cost_or_roster_closed':False,'macro3_closed':False,'new_author_lock':False,'REGISTER_promoted':False,'manuscript_written':0}}

def validate(o):
    try:
        assert o==build(),'Saved artifact differs from source-bound constructor'
        return []
    except (AssertionError,KeyError,ValueError) as e:return [str(e)]

def render(o):
    s=o['summary']
    return '\n'.join(['# Chicago2022 rookie RFA/QO 함수·비용 상한','',f"상태: {o['status']}. 작가 선택·실제 금액·실제 접수·전체 비용 인증은 0.",'',
        '## 새로 완료한 범위','',
        '2017CBA VIII1c / XI1c·4와 NBA2018 실제 ExhibitA(PDF29)를 연결했다. Carter7과 주인공16–30의32개 선발/비선발 가지, 원3년차 기본급·likely·unlikely의 연속80–120% 성분영역을128개 꼭짓점으로 검문한다. 미래 통계나 주인공 정확 순위를 선택하지 않는다.',
        'Carter 선발은 자기 순위의 QO, 비선발은 자기 제안과15번 기본급 제안 중 작은 쪽이다. 주인공 선발은9번120% 기본급·보너스0, 비선발은 자기 원성분의 증가식이다. 원성분 각각의 증가를 보존하며 Carter 비선발의 최종 UPC 성분을 임의로 구성하지 않는다.',
        '정확 유리수 법정 입력식과 보수적 달러 상한을 분리한다. 성분3개에서 각 단계의 ceil 합≤전체 ceil+2를 사용해 원래 계약 성분을 지우지 않는다. 공식 NBA 반올림 알고리즘이나 실제 계약 달러를 인증하지 않는다.',
        '', '| 비용 입력 | USD 상한 |','|---|---:|',f"| Carter | {s['Carter_QO_screen_upper_usd']:,} |",f"| 주인공 | {s['protagonist_QO_screen_upper_usd']:,} |",f"| 합계 | {s['combined_QO_screen_upper_usd']:,} |",f"| 기존2×25%cap 예약 축소 | {s['bounded_input_reduction_usd']:,} |",f"| 기존 부분 비용식에 이 입력만 대입 | {s['conditional_replacement_partial_screen']:,} |",f"| 동일 조건의 미입력X 여유 | {s['conditional_remaining_X_screen']:,} |",'',
        '별도 minimum floor/ceil 조건을 채택한다면 위 부분 비용/여유는 각각50달러 감소/증가한다. 기존 core 파일은 변경하지 않았다. 이 수치는 아직 미입력X가 있는 조건부 apron screen이며 normal salary-cap 또는 전체FY22 PASS가 아니다.',
        '', '## 시간·권리·분류','',
        '양쪽 옵션의 유효 행사와 계약 서비스 완료가 조건이다. 보통 QO는 해당 두번째 옵션 시즌 다음날부터2022-06-29까지 발행하고10-01까지 수락 가능해야 한다. 실제 제시·수락이나 미래 선발 결과는 null/false이다. 미행사 옵션·QO미제시는 별도 UFA 경로이다.',
        'MaximumQO(5년 최대급), FA cap hold(250/300% 등), offer sheet/FirstRefusal 비용은 보통 QO와 별도다. 이 후보는 no2021extension/noMaximumQO/noFirstRefusal 범위에서만 상한 입력을 공급한다. CX4/E4를 작가 확정하지 않는다. 새로운 관련 사건 발생 시 해당 비용을 다시 연다.',
        '', '## 원천·재현','',
        '[NBA2018 actual scale](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) PDF29 실제 표를 읽고 시각 대조했다.2017ExhibitB3의 예시 표는 사용하지 않았다. [2017CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF208–209/240–241/294–295/309–311/314–320을 직접 읽었다. 원cache SHA와 각 추출쪽 SHA는 JSON에 남겼다. 이번 새 다운로드0.',
        '`python -B tools/build_chicago_2022_rookie_rfa_qo_family.py --check --self-test`. 출처LF 지문·upstream 전체재구성·동일ID 표/정책 변조를 거부한다. 작성자 음성검사는 독립 감리로 계수하지 않는다.',
        '', '## 현행7행 진행표','',
        '[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)·[누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md) 기준. 미완료 큰 묶음5, v0.30 PARTIAL / 설계·원고 CLOSED / 실제Pack0 / 원고0.',
        '| 번호 | 상태 |','|---|---|','|1 2020드래프트 연쇄|완료|','|2 Chicago2020–21|완료|','|3 2021–23거래·계약|승인M1/A core 유지; QO 함수 입력 완료, 중요 선택·전체 실행 미완료|','|4 장기 커리어|후속 시즌 입력 대기|','|5 결말·전체 구조|골격 유지, 전체 기능표 미완료|','|6 집필 규격·Context Pack|누적 등록기 참조; 전체G13/실제Pack 미완료|','|7 통합·독립·작가 승인|최종 게이트 미완료|',''])

def self_test():
    o=build();tests=[]
    for name,fn in [('starter_rank9_applied_to_Carter',lambda x:x['branch_rows'][1].update(qo_charge_screen_upper_usd=7921302)),('exact_P_pick_lock',lambda x:x['policy'].update(protagonist_exact_pick=22)),('June30_late_QO',lambda x:x['policy'].update(ordinary_QO_issue_deadline='2022-06-30')),('QO_as_FA_hold',lambda x:x['rule_map'].update(FAhold='QO=FAhold')),('actual_acceptance',lambda x:x['certification'].update(actual_player_acceptance=True)),('whole_cost_PASS',lambda x:x['certification'].update(whole2022_23_cost_or_roster_closed=True))]:
        bad=copy.deepcopy(o);fn(bad);assert validate(bad),name;tests.append(name)
    for name,key,val in [('MaximumQO_constructor','Maximum_QO_selected',True),('extension_constructor','no2021_extension_branch',False),('invented_season_gate','full_future_season_required_to_define_function',True)]:
        bad=policy();bad[key]=val
        with patch(__name__+'.policy',return_value=bad):
            try:build()
            except AssertionError:tests.append(name)
            else:raise AssertionError('Accepted '+name)
    bad=checked_scale();bad[9]=(*bad[9][:4],341)
    with patch(__name__+'.read_scale',return_value=bad):
        try:build()
        except AssertionError:tests.append('sameID_wrong_rank9_source')
        else:raise AssertionError('Accepted wrong source')
    try:original_vector(FIXTURE[7],(Fraction(6*FIXTURE[7][2],5)+1,0,0))
    except AssertionError:tests.append('over120_original_components')
    else:raise AssertionError('Accepted over120')
    assert starter(0,0,41,0) and starter(41,0,41,0) and starter(82,0,0,0) and starter(0,4000,0,0) and not starter(40,1999,40,1999)
    tests.append('starter_exact_boundary_functions')
    return tests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(render(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==render(o),'Markdown stale'
    t=self_test() if a.self_test else []
    print(json.dumps({'current':True,'summary':o['summary'],'negative_controls':t},ensure_ascii=False))
if __name__=='__main__':main()
