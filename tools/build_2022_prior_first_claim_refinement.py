"""Four current first-round allocations from preserved public prior claim families.

No lottery result, later original trade, future rank or private receipt is selected.
The original 2020 Utah exchange is an admitted preserved public atomic template.
"""
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
import argparse,csv,hashlib,io,json,re
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2022_prior_first_claim_refinement.py'
OUT='research/NBA_2022_PRIOR_FIRST_CLAIM_REFINEMENT_2026_10_08.json'
MD=OUT[:-5]+'.md'
MAP='simulation/NBA_2022_NAMED_ASSET_CONTROL_MAP.json'
T1='simulation/NBA_2021_T1_SELECTED_DRAFT_EXECUTION.json'
RJ='simulation/2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.csv'
ZEKE='simulation/2020_DRAFT_ZEKE_NNAJI_RELANDING_BOARD.csv'
PINS={MAP:'ca1be50a889fa8aa1ad47cc696d64c7bfc00cc7ebd77b2bdf9ede815ca88d4f2',T1:'f8c78e99cce1b02a051c94339b550fdb52205d3988db8bbe69b780559c3bc306',RJ:'31ee11da45a3f3833da7f589adb3f31b54092ffb6fcce3b3dfb5d99dbf528891',ZEKE:'149c7d324c97cec64870159c9cc5cc470ebb285aa25f822293ac299d7a1c3766'}
CACHE=Path('C:/Users/Storm Credit/AppData/Local/Temp/fr-control2022-20261007')
RAW={'phoenix_shams_oembed.raw':'9613295bf3b008bd72c6c9583a58ca34155b5970ef1037d140c3521b8d121bd7','uta_cobb_oembed.raw':'cec1dc92a9e3f48253a0aee6399dc9defed10a9a767b9f67f8b4be9d81056138','hawks_2020_fact_sheet.pdf':'ef82b33affc3c0243129d40f10c06a95cadd4ae2d6e254094aeb0de82f4e59cf'}
PUBLIC={
 'PHX':{'protection_by_year':{'2022':12,'2023':10,'2024':8,'2025':0},'claim_holder':'OKC'},
 'UTA':{'2020_2021_convey_interval':[8,14],'2022_protection':6,'claim_holder':'MEM'},
 'OKC':{'2022_protection':14,'claim_holder':'ATL','nonconvey_fallback':[{'origin':'OKC','year':2024,'round':2},{'origin':'OKC','year':2025,'round':2}]},
 'LAL':{'2021_reported_convey_threshold_variants':[7,8],'2022_after_nonconvey':'UNPROTECTED','claim_holder':'NOP'}
}
FIXED_PUBLIC=deepcopy(PUBLIC)
WEB=[
 {'id':'PHX_SHAMS_ORIGINAL','url':'https://twitter.com/ShamsCharania/status/1328401869618765829','delivery_url':'https://publish.twitter.com/oembed?url=https://twitter.com/ShamsCharania/status/1328401869618765829','date':'2020-11-16','classification':'ORIGINAL_JOURNALIST_DISCLOSURE_OFFICIAL_X_DELIVERY_NOT_TEAM_CONTRACT_CERT','raw':'phoenix_shams_oembed.raw','parsed_scope':'2022/23/24/25 protection thresholds only; no later realized ranks.'},
 {'id':'UTA_COBB_ORIGINAL','url':'https://twitter.com/DavidWCobb/status/1141390973869678592','delivery_url':'https://publish.twitter.com/oembed?url=https://twitter.com/DavidWCobb/status/1141390973869678592','date':'2019-06-19','classification':'ORIGINAL_JOURNALIST_DISCLOSURE_OFFICIAL_X_DELIVERY_NOT_TEAM_CONTRACT_CERT','raw':'uta_cobb_oembed.raw','parsed_scope':'2020/21 convey only8–14,2022 top6. His prediction of actual convey year is not adopted.'},
 {'id':'ATL_TEAM_FACT_SHEET','url':'https://atlantahawkspr.wordpress.com/wp-content/uploads/2020/08/atlanta-hawks-2020-nba-draft-lottery-fact-sheet.pdf','date':'2020-08-20','classification':'TEAM_PR_OFFICIAL_PDF','raw':'hawks_2020_fact_sheet.pdf','pdf_page':2,'parsed_scope':'OKC2022 top14, conditional2024/25 second fallback. Also ATLown2022second top55; not consumed here.'},
 {'id':'UTA2020_ORIGINAL_ATOM','url':'https://www.nba.com/jazz/news/utah-jazz-acquire-27th-and-38th-picks-draft-day-swap-new-york','date':'2020-11-18','classification':'INDEXED_TEAM_BODY_READ_NORMAL_OPEN_IFRAME','web_ref':'turn2299search0','raw_body_adopted':False,'parsed_scope':'UTA23 and AnteTomic rights toNYK; NYK27+38 toUTA. No player-only fake edge.'},
 {'id':'LAL_AD_BONTEMPS_REPORT','url':'https://www.espn.com/nba/story/_/id/26981805/sources-lakers-reach-deal-pelicans-davis','classification':'ORIGINAL_ESPN_REPORT_INDEXED_BODY_READ','web_ref':'turn2301search0','raw_body_adopted':False,'parsed_scope':'2021 top8 conveyed toNOP, otherwise2022 unprotected. Publication metadata presentlyNov13,2019; not silently re-dated to original June report.'},
 {'id':'LAL_AD_REPORT_VARIANT','url':'https://www.salaryswish.com/draft/2019','classification':'SECONDARY_NUMERIC_TEMPLATE_INDEXED_NOT_PRIMARY_CERT','web_ref':'turn2301search10','raw_body_adopted':False,'parsed_scope':'2021 protected8–30 implies convey1–7. The7/8 boundary is unresolved and not selected; rank22 is outside both.'},
 {'id':'LAL_NBA_AMBIGUOUS_SHORTHAND','url':'https://www.nba.com/news/report-anthony-davis-lakers','classification':'NBA_REPORT_INDEXED_SHORTHAND_CONFLICT_NOT_NUMERIC_AUTHORITY','web_ref':'turn2301search5','raw_body_adopted':False,'parsed_scope':'Top-eight protected wording conflicts with original reporter direction. No inverted2021 allocation consumed.'}
]
FIXED_WEB=deepcopy(WEB)

def need(x,m):
 if not x:raise AssertionError(m)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def direct(root,p):
 t=text(root/p)
 return list(csv.DictReader(io.StringIO(t)))if p.endswith('.csv')else json.loads(t)
def physical(root,p):return direct(root,p)
def sources(root):
 need(PUBLIC==FIXED_PUBLIC and WEB==FIXED_WEB,'Public policy/source meaning changed')
 src={}
 for p,s in PINS.items():
  need(sha(root/p)==s,'Source stale '+p);v=physical(root,p)
  need(v==direct(root,p),'Returned physical source changed '+p);src[p]=v
 return src

def raw_sources():
 for p,s in RAW.items():need(hashlib.sha256((CACHE/p).read_bytes()).hexdigest()==s,'Raw source changed '+p)
 phx=json.loads((CACHE/'phoenix_shams_oembed.raw').read_bytes());uta=json.loads((CACHE/'uta_cobb_oembed.raw').read_bytes())
 need(phx['author_name']=='Shams Charania'and '1328401869618765829'in phx['html'],'Wrong PHX author/source')
 need(uta['author_name']=='David Cobb'and '1141390973869678592'in uta['html'],'Wrong UTA author/source')
 h=re.sub('<[^>]+>',' ',phx['html']);u=re.sub('<[^>]+>',' ',uta['html'])
 need(all(x in h for x in ('1-12 in 2022','1-10 in 2023','1-8 in 2024','unprotected in 2025')),'PHX numeric disclosure changed')
 need('2020 or 2021'in u and '8-14'in u and 'top-6 protected'in u,'UTA numeric disclosure changed')
 with fitz.open(CACHE/'hawks_2020_fact_sheet.pdf')as d:t=d[1].get_text()
 need('not among #1-14'in t and 'Oklahoma City’s own 2024 and 2025'in t,'ATL current/fallback source changed')
 return {'raw_sha256':deepcopy(RAW),'cache_directory':str(CACHE),'Hawks_PDF_page2_fitz_text_sha256':hashlib.sha256(t.encode()).hexdigest(),'raw_byte_normalization':'NONE','repository_sha_normalization':'BOMstrip CRLF/CR toLF UTF8','network_called_by_builder':False}

def prior_rows(src):
 t=src[T1]['selected_rows'];p={x['origin']:x for x in t if x['round']==1}
 need((p['LAL']['pick'],p['LAL']['conditional_holder_at_selection'])==(22,'LAL'),'LAL prior2021 settlement changed')
 need((p['UTA']['pick'],p['UTA']['conditional_holder_at_selection'])==(30,'UTA'),'UTA prior2021 settlement changed')
 r=[x for x in src[RJ]if x['branch']=='PRIMARY'and x['pick']=='27']
 z=[x for x in src[ZEKE]if x['branch']=='PRIMARY'and x['pick']=='23']
 need(len(r)==len(z)==1 and r[0]['team']=='Utah Jazz'and r[0]['status']=='AUTHOR_LOCKED'and z[0]['team']=='Minnesota Timberwolves'and z[0]['status']=='AUTHOR_LOCKED','Locked2020 landing differs from preserved23→27 atomic template')
 return {'UTA_2020_origin_rank_in_preserved_original_atom':23,'UTA_2020_final_acquired_pick':27,'UTA_2020_original_atom_preserved_as_lawful_working_family':True,'all_2020_origin_ranks_independently_certified':False,'UTA_2021_origin_rank':30,'LAL_2021_origin_rank':22,'original_2021_keeper_settlements_preserved':True}

def allocation(origin,rank,prior):
 if origin=='PHX':holder='PHX'if rank<=PUBLIC['PHX']['protection_by_year']['2022']else'OKC'
 elif origin=='OKC':holder='OKC'if rank<=PUBLIC['OKC']['2022_protection']else'ATL'
 elif origin=='UTA':
  need(all(not 8<=prior[k]<=14 for k in ('UTA_2020_origin_rank_in_preserved_original_atom','UTA_2021_origin_rank')),'Prior UTA claim already conveyed')
  holder='UTA'if rank<=PUBLIC['UTA']['2022_protection']else'MEM'
 elif origin=='LAL':
  need(all(prior['LAL_2021_origin_rank']>q for q in PUBLIC['LAL']['2021_reported_convey_threshold_variants']),'LAL variant prior branch not invariant')
  holder='NOP'
 else:raise AssertionError('Unexpected origin')
 return {'origin':origin,'year':2022,'round':1,'rank_parameter':rank,'underlying_pick_holder':holder,'current_claim_holder':PUBLIC[origin]['claim_holder'],'new_contract_or_tender':False,'future_actual_delivery_certified':False}

def assert_allocation(row,origin,rank):
 expected={'PHX':'OKC','UTA':'MEM','OKC':'OKC','LAL':'NOP'}[origin]
 need(row=={'origin':origin,'year':2022,'round':1,'rank_parameter':rank,'underlying_pick_holder':expected,'current_claim_holder':{'PHX':'OKC','UTA':'MEM','OKC':'ATL','LAL':'NOP'}[origin],'new_contract_or_tender':False,'future_actual_delivery_certified':False},'Returned allocation differs from public current branch')

def build(root=ROOT):
 src=sources(root);raw=raw_sources();prior=prior_rows(src);rows=[]
 for o in ('PHX','UTA','OKC','LAL'):
  m=next(x for x in src[MAP]['typed_control_rows']if(x['origin'],x['round'])==(o,1));ranks=m['origin_rank_domain']
  need(ranks=={'PHX':[24,25,26,27],'UTA':[29],'OKC':[1,2,3,4,5],'LAL':[24,25,26,27]}[o],'Current source rank domain changed')
  cells=[]
  for r in ranks:
   c=allocation(o,r,prior);assert_allocation(c,o,r);cells.append(c)
  rows.append({'origin':o,'rank_domain':ranks,'public_preserved_prior_claim':deepcopy(PUBLIC[o]),'allocation_cells':cells,'invariant_holder_in_current_rank_domain':cells[0]['underlying_pick_holder'],'exact_rank_selected':None,'source_template_selected_as_lawful_candidate':True,'private_contract_or_actual_delivery_certified':False})
 return {'id':'NBA_2022_PRIOR_FIRST_CLAIM_REFINEMENT','baseline_main':'d74ffd6efcdb18a07285a23ea7a59a014400c32b','status':'FOUR_CURRENT_PRIOR_FIRST_ALLOCATION_FUNCTIONS_SOURCE_SUPPORTED_WORKING_FAMILY_REVIEW_PENDING','source_sha256':{**PINS,SELF:sha(root/SELF)},'primary_and_report_observations':deepcopy(WEB),'raw_provenance':raw,'prior_settlement_family':prior,'refined_first_rows':rows,'summary':{'named_first_functions':4,'current_rank_cells':14,'holder_invariant_origins':4,'exact_rank_or_player_selected':0,'upstream_map_rewritten':False},'scope':{'original_current_protection_family_preserved':True,'2022_draw_not_selected':True,'reported7_8_LAL_boundary_unselected_and_output_invariant':True,'original_Nop_to_Mem_JV_atom_executed':False,'original_UTA_to_OKC_Favors_future_first_atom_executed':False,'private_all_ledger_or_receipt_gate_added':False,'future_2023_2027_realized_ranks_or_fallback_delivery':None,'whole_sixty_control_complete':False,'whole_macro3':False,'independent_review_completed':False},'remaining_inputs':['Remaining named second-round prefixes and three-origin composite exchange counterpart allocation.','Original MIL/MIA sanction causes under selected lawful transaction timing.','Lottery4 and tied first ordering, with second reverse, remain separate working draws.'],'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript':False}

def validate(v,root=ROOT):return []if v==build(root)else['First claim refinement differs from source']
def markdown(v):
 lines=['# 2022 prior first: 네 현재 배정 함수','',v['status'],'','[현재 60원점 지도](../simulation/NBA_2022_NAMED_ASSET_CONTROL_MAP.json)의 네 prior first 입력을 새 원 공개 조항과 연결했다. 기존 지도와 선택 순위는 변경하지 않았다. 원 미래 전달·2022 추첨·선수·새 계약 선택은 없다.','','| 원점 | 현재 순번 범위 | 현재 보유자 함수 | 공개 조건 |','|---|---|---|---|','| PHX | 24–27 | OKC | 2022 top12 밖 |','| UTA | 29 | MEM | 원2020/21 비전달 후2022 top6 밖 |','| OKC | 1–5 | OKC | top14 보호 안; ATL 조건부 claim 유지 |','| LAL | 24–27 | NOP | 선택2021 원점22 비전달 후2022 무보호 |','','[Shams 원 공개](https://twitter.com/ShamsCharania/status/1328401869618765829), [Cobb 원 공개](https://twitter.com/DavidWCobb/status/1141390973869678592)는 기자 본인 취재 발표이고 X oEmbed 원 바이트를 확보했다. 구단 원 계약서 인증으로 표시하지 않았다. [Hawks PR 공식 PDF](https://atlantahawkspr.wordpress.com/wp-content/uploads/2020/08/atlanta-hawks-2020-nba-draft-lottery-fact-sheet.pdf) 2쪽은 OKC 보호·미전달 시2024/25 second를 명시한다. 후년 실제 전달을 고르지 않았다.','','Utah2020은 [공식 교환](https://www.nba.com/jazz/news/utah-jazz-acquire-27th-and-38th-picks-draft-day-swap-new-york)의23+Tomic권리→NYK/27+38→UTA 가족을 보존한다. 기존 locked23 Minnesota/27 Utah와 모순이 없으며 이 원 경제 묶음 보존이 후보 조건이다. 모든2020 원점순위의 새 인증은 아니다. 선택2021 UTA30은8–14 밖이므로 추가 비전달, 현재29는top6 밖이다.','','[ESPN 원 취재](https://www.espn.com/nba/story/_/id/26981805/sources-lakers-reach-deal-pelicans-davis)는2021 상위8 전달·비전달 후2022 무보호를 설명한다. 다른 숫자 템플릿의8–30 보호와7/8 경계가 다르고 NBA의 top-eight protected 축약은 방향이 모호하다. 경계를 임의 확정하지 않았다. 선택2021 LAL22는 두 보고 범위에서 모두 비전달이므로 현재 배정은 동일하다. NOP→MEM 원JV 거래는 미선택이므로 그 수령자로 바꾸지 않는다.','','원자료3 raw SHA/원 PDF 추출 SHA와 저장소4핀+SELF를 구분했다. 생성기는 네 함수의14 현재 순번에만 caller 정답 비교를 한다. 원 기자의 미래 전달 예측은 소비하지 않는다. 이전 검문 조상 생성기 재실행0. 전체60 control·징계·복합교환·추첨은 별도 잔여 범위다.','','[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)','','| 묶음 | 현황 |','|---|---|','| 1 드래프트 연쇄 | 완료 |','| 2 Chicago2020–21 | 완료 |','| 3 2021–23 |1230·순위·play-in 완료 /2022 권리 후속 진행 |','| 4 장기 커리어 | 진행 |','| 5 전체 구조 | 진행 |','| 6 집필 규격·Context Pack | 진행·Pack0 |','| 7 통합·작가 승인 | 미완료 |','','미완료 큰 묶음5 /6번까지4. v0.30 PARTIAL·CLOSED·원고0.','']
 return '\n'.join(lines)

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();v=build()
 if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
 if a.check:need(direct(ROOT,OUT)==v and text(ROOT/MD)==markdown(v),'Saved first refinement stale')
 n=0
 if a.self_test:
  orig=allocation
  for key in ('holder','fallback_claim'):
   def bad(o,r,prior):
    c=orig(o,r,prior)
    if o=='OKC':c['underlying_pick_holder'if key=='holder'else'current_claim_holder']='ATL'if key=='holder'else'OKC'
    return c
   with patch(__name__+'.allocation',side_effect=bad):
    try:build()
    except AssertionError:n+=1
    else:raise AssertionError('Returned current branch false PASS')
 print(json.dumps({'current':True,'summary':v['summary'],'writer_controls':n if a.self_test else None}))
if __name__=='__main__':main()
