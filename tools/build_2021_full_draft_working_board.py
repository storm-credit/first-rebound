"""Join the existing DB1/C39A board to frozen control60 and unselected T1.

This candidate executes a complete ordering, not actual or author-locked draft
choices, private eligibility papers, contracts, or the T2/T3 alternate boards.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from unittest.mock import patch
import build_2021_full_draft_comparison as g7

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_2021_full_draft_working_board.py'
OUT='research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json'
MD=OUT[:-5]+'.md'
G7='simulation/NBA_2021_FULL_DRAFT_COMPARISON.json'
BRIDGE='simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json'
AP1='research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json'
SQ1='simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json'
SOURCES=[G7,'simulation/NBA_2021_FULL_DRAFT_COMPARISON_INPUTS.json',
 'tools/build_2021_full_draft_comparison.py',
 'simulation/NBA_2021_FIRST_ROUND_CONTINUATION.json',
 'simulation/NBA_2021_DRAFT_ASSETS.json',
 'simulation/CHICAGO_2021_NAMED_ROSTER_OPTIONS.json',BRIDGE,AP1,SQ1,
 'research/NBA_2021_PICK16_COST_CLOSURE_BRIDGE_2026_10_07.json',
 'design/NBA_2021_PICK16_AP1_SG16_DIRECTION_DECISION_PACKET_2026_10_07.md',
 'research/NBA_2021_FULL_DRAFT_COMPARISON_SOURCES.json',
 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json',
 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json','AGENTS.md']
PINS={'simulation/NBA_2021_FULL_DRAFT_COMPARISON.json': '31e524c981a07240c835150e7db1d753191c92e205a03bc5207208aca07dbb8f', 'simulation/NBA_2021_FULL_DRAFT_COMPARISON_INPUTS.json': 'ab916ca4b1805be8b780532a744c975dd0c63d56f9c9411310d3848f27508b8f', 'tools/build_2021_full_draft_comparison.py': '86066ec12904a34abfceea2c449707ecb2b0ee8b0dc02d89b6a47527641d54e3', 'simulation/NBA_2021_FIRST_ROUND_CONTINUATION.json': 'ce468e2803c4e0aa7715a43fadf032cdd7964424549d051bb041725f01c091db', 'simulation/NBA_2021_DRAFT_ASSETS.json': 'eb1f204a56ffea45a3153b1067954e96331f35cba5910651b1e18d724a8dcaeb', 'simulation/CHICAGO_2021_NAMED_ROSTER_OPTIONS.json': 'd4bdf4d2bbd8e8ca33f9894b7d84241bc23bfd30e102eedfa63f8726087d1502', 'simulation/NBA_2020_21_RESULT_AND_PICK_EXECUTION_BRIDGE.json': '3e35fd2abfeb32e2bc5b66b7796f843ca117359be1a419d037844d29177a26d8', 'research/NBA_2021_PICK16_BOS_OKC_HOU_WORKING_EXECUTION_2026_10_07.json': '86b9989daa20eced72106c25b14fb8d8b3b32d201132a0b87ba466b0ce51fba0', 'simulation/CHICAGO_2021_APPROVED_A_DRAFT_SIGNING_EXECUTION.json': '11140e49baa665f18e267fa6419efa238302250b724fa51cfd3262b010b4a312', 'research/NBA_2021_PICK16_COST_CLOSURE_BRIDGE_2026_10_07.json': 'e1a9809fabcf4a63b703479df8eeb0fc9db615670e23a24f5f61f707003c37b1', 'design/NBA_2021_PICK16_AP1_SG16_DIRECTION_DECISION_PACKET_2026_10_07.md': '4c39cb640c607accda1fd0063c5f28c93e6ed654e21ff52c92734429fff4a839', 'research/NBA_2021_FULL_DRAFT_COMPARISON_SOURCES.json': 'baf2b83b4b58071fdff5e076fea8118b8204608c9e172b43c4681438694c91eb', 'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json': '253e4a4aa803cc493b0cb59715dd4eb74d4545abfe19a7161766fd7446cf9088', 'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json': '9e6a4510d5f3bc2a04e667d65ac88e476583ae9de98be213f3be98165548d0ce', 'AGENTS.md': '67f21ebf14a0ec428196fe20077ad8eb1a4b3920b7983e900f8eae00577a53f2'}
CACHE=Path.home()/'AppData/Local/Temp/first-rebound-draft60-20261007'
WEB_FILES={'web_source_snapshot.json':'56391d0d8da43b1b18fa9579d71e279cae13aa892eb9f7e4ae028131ba57fd58',
 'web_prospect_rest.json':'0e7aade1a7a1e91a4a979e4d915a9821441adbaaed792b0470b2be032a552c22'}
FIXED_NAMES=('Cade Cunningham', 'Jalen Green', 'Evan Mobley', 'Scottie Barnes', 'Jalen Suggs', 'Jonathan Kuminga', 'Franz Wagner', 'Josh Giddey', 'Moses Moody', 'Chris Duarte', 'Davion Mitchell', 'Corey Kispert', 'Joshua Primo', 'James Bouknight', 'Trey Murphy', 'Alperen Sengun', 'Ziaire Williams', 'Tre Mann', 'Jalen Johnson', 'Quentin Grimes', 'Usman Garuba', 'Jared Butler', 'Ayo Dosunmu', 'Josh Christopher', 'Keon Johnson', 'Nahshon Hyland', 'Cameron Thomas', 'Jaden Springer', 'Isaiah Jackson', 'JT Thor', 'Kai Jones', 'Rokas Jokubaitis', 'Herbert Jones', 'Kessler Edwards', 'Jeremiah Robinson-Earl', 'Dayron Sharpe', 'Santi Aldama', 'Isaiah Livers', 'Joe Wieskamp', 'Miles McBride', 'Neemias Queta', 'Greg Brown', 'Isaiah Todd', 'BJ Boston', 'Juhann Begarin', 'Dalano Banton', 'Sharife Cooper', 'Sam Hauser', 'Filip Petrusev', 'Charles Bassey', 'Marcus Zegarowski', 'Jericho Sims', 'Luka Garza', 'Aaron Wiggins', 'Jason Preston', 'Scottie Lewis', 'Balsa Koprivica', 'Jay Huff', 'RaiQuan Gray', 'Sandro Mamukelashvili')
ALIASES={'Nahshon Hyland':"Nah'Shon Hyland",'Dayron Sharpe':"Day'Ron Sharpe"}


def text(p):return (ROOT/p).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def load(p):return json.loads(text(p))


def policy():
    return {'source_board':'DB1','CHI39':'C39A','conditional_asset_scenario':'T1_AP1_AND_SG16',
      'AP1_direction_author_selected':False,'SG16_direction_author_selected':False,
      'other_58_draftees_author_locked':False,'new_other_draft_night_trades':0,
      'candidate_participation':'Every named public2021 prospect participates legally in the modeled2021 draft, including any applicable timely early-entry/non-withdrawal conditions. This is an explicit candidate admissibility condition, not proof of counterfactual private papers.',
      'actual_participant_set_or_private_medical_certified':False,
      'new_NBA_UPC_or_RequiredTender_executed_by_this_board':False}


def checked_policy():
    p=policy()
    assert p=={
      'source_board':'DB1','CHI39':'C39A','conditional_asset_scenario':'T1_AP1_AND_SG16',
      'AP1_direction_author_selected':False,'SG16_direction_author_selected':False,
      'other_58_draftees_author_locked':False,'new_other_draft_night_trades':0,
      'candidate_participation':'Every named public2021 prospect participates legally in the modeled2021 draft, including any applicable timely early-entry/non-withdrawal conditions. This is an explicit candidate admissibility condition, not proof of counterfactual private papers.',
      'actual_participant_set_or_private_medical_certified':False,
      'new_NBA_UPC_or_RequiredTender_executed_by_this_board':False},'Policy/authority/participation meaning changed'
    return p


def inputs():
    assert set(PINS)==set(SOURCES)
    for p,s in PINS.items():assert sha(p)==s,'Source changed '+p
    model=load(G7);assert model==g7.build(),'G7 source producer differs'
    assert model['recommended_comparison']=='DB1' and model['recommended_CHI39_option']=='C39A'
    assert not model['full_draft_finally_selected']
    b=next(x for x in model['scenarios'] if x['id']=='DB1')['board']
    bridge=load(BRIDGE);ap=load(AP1);sq=load(SQ1)
    assert bridge['pick_control_snapshot']['scope']=='AS_OF_FROZEN_APPROVED_SEASON_ASSETS_BEFORE_OPTIONAL_OFFSEASON_MOVES'
    assert ap['independent_review_completed'] and not ap['authority']['long_term_trade_direction_selected']
    closure=load('research/NBA_2021_PICK16_COST_CLOSURE_BRIDGE_2026_10_07.json')
    assert closure['public_family_AP1_remaining_OKC_budget_gap_closed'] and not closure['author_selected']
    assert sq['independent_review_completed']
    return copy.deepcopy(b),bridge['pick_control_snapshot']['rows'],ap,sq


def prospect_sources():
    records=[];sections=[]
    for name,pin in WEB_FILES.items():
        p=CACHE/name;raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        s=json.loads(raw.decode('utf8'));assert isinstance(s,str)
        # The first response combines three official pages; only its first
        # section is the prospects table. Cached web-tool text is not HTML.
        section=s.split('--------------------------------------------------------------------------------')[0]
        sections.append(section)
        records.append({'id':name,'url':'https://www.nba.com/draft/2021/prospects',
            'cache_path':str(p),'serialized_web_response_sha256':pin,'bytes':len(raw),
            'classification':'OFFICIAL_NBA_PAGE_OBSERVED_WEB_TOOL_TEXT_NOT_ORIGINAL_HTML',
            'collection_date':'2026-10-07','raw_HTML_recovered':False})
    observed={}
    for section in sections:
        for ln,n,fields in re.findall(r'L(\d+): .*?†([^†]+?) \| ([^\n]+)',section):
            if not 162<=int(ln)<=250:continue
            cells=[x.strip() for x in fields.split('|')];assert len(cells)==7
            observed[n]={'observed_prospect_name':n,'locator':'2021prospects NAME table webline'+ln,
              'source':'https://www.nba.com/draft/2021/prospects',
              'observed_age_explicitly_excluded_from_2021_inputs':True,
              'school_status_measurements_not_used_as_counterfactual_biography':True}
    assert len(observed)==89
    failures=[]
    for filename in ['sources.json','apihub_sources.json']:
        for r in json.loads((CACHE/filename).read_text(encoding='utf8')):
            raw=Path(r['cache_path']).read_bytes()
            assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['raw_sha256']
            assert r['http_status']==403
            failures.append({**r,'used_as_original_body':False})
    return observed,records,failures


def join(board,frozen,ap,sq,observed):
    assert len(board)==len(frozen)==len(ap['draft_control_candidate_rows'])==60
    assert tuple(x['proposed_player'] for x in board)==FIXED_NAMES,'Existing DB1 names/order changed'
    assert [r['pick'] for r in board]==list(range(1,61))
    assert len({r['proposed_player'] for r in board})==60
    assert [r['pick'] for r in frozen]==list(range(1,61))
    assert frozen[15]['origin']==frozen[15]['control_holder']=='BOS'
    assert board[9]['team']=='CHI' and board[9]['proposed_player']=='Chris Duarte'
    assert board[38]['team']=='CHI' and board[38]['proposed_player']=='Joe Wieskamp'
    assert not any(r['proposed_player']=='Alperen Sengun' for r in board[:15]),'Sengun consumed before SG16'
    assert board[15]['proposed_player']=='Alperen Sengun'
    taken=set();rows=[];unchanged=0
    for r,f,a in zip(board,frozen,ap['draft_control_candidate_rows']):
        k=r['pick'];n=r['proposed_player'];pub=ALIASES.get(n,n)
        assert pub in observed,'No original2021 prospect identity '+n
        assert a['pick']==k and a['origin']==f['origin']
        assert a['frozen_macro2_holder']==f['control_holder']
        assert a['conditional_after_SG16_holder']==r['team']
        if k!=16:
            assert f['control_holder']==a['conditional_after_AP1_holder']==r['team']
            unchanged+=1
        else:
            assert a['conditional_after_AP1_holder']=='OKC' and r['team']=='HOU'
        assert n not in taken and n in r['available_comparison']
        assert all(x not in taken for x in r['available_comparison']),str(k)+' prior taken candidate still available'
        row={'pick':k,'round':f['round'],'origin':f['origin'],
          'frozen_before_optional_offseason_holder':f['control_holder'],
          'conditional_holder_at_selection':a['conditional_after_AP1_holder'],
          'selecting_team':a['conditional_after_AP1_holder'],
          'conditional_final_draft_rights_holder':r['team'],'player':n,
          'prior_selected_player_count':len(taken),'available_when_selected_in_this_board':True,
          'remaining_comparison_candidates':copy.deepcopy(r['available_comparison']),
          'public_identity_evidence':copy.deepcopy(observed[pub]),
          'name_alias_used':None if pub==n else {'repository':n,'official_page':pub},
          'candidate_legal_participation_condition':True,
          'actual_counterfactual_eligibility_or_medical_certified':False,
          'original_G7_reasoning_source':'simulation/NBA_2021_FULL_DRAFT_COMPARISON.md',
          'new_author_lock':False,'new_NBA_contract_or_tender':False,
          'execution_class':'PRESERVED_CHICAGO_LOCAL_WORKING_DIRECTION' if k in [10,39] else 'UNSELECTED_OTHER_DRAFTEE_CANDIDATE',
          'conditional_asset_event':'AP1_JULY28_THEN_SG16_POST_SELECTION_JULY29' if k==16 else None}
        rows.append(row);taken.add(n)
    assert unchanged==59
    assert [r['pick'] for r in rows if r['execution_class']=='PRESERVED_CHICAGO_LOCAL_WORKING_DIRECTION']==[10,39]
    return rows


def build():
    p=checked_policy();board,frozen,ap,sq=inputs();obs,raw,fail=prospect_sources()
    rows=join(board,frozen,ap,sq,obs)
    return {'id':'NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07',
      'schema':'DB1_C39A_T1_CONDITIONAL_WORKING_BOARD_V1','status':'INDEPENDENTLY_REVIEWED_COMPLETE_60_ROW_CONDITIONAL_WORKING_CANDIDATE',
      'baseline_main':'5fa8b1ec50fbbeccd8dd8308cfd7c81518c03ffc',
      'source_sha256':{**PINS,SELF:sha(SELF)},'hash_convention':'UTF8BOMstrip;CRLF/CRtoLF',
      'raw_source_observations':raw,'failed_direct_HTML_retrievals':fail,
      'policy':p,'draft_date':'2021-07-29','rows':rows,
      'asset_event_order':[{'date':'2021-07-28','event':'AP1','scope':'UNSELECTED_T1_CANDIDATE',
                           'effect':'BOS16 toOKC before draft; preserve other named claims/contracts from independently reviewed packet.'},
                          {'date':'2021-07-29','event':'SELECT16','scope':'UNSELECTED_T1_CANDIDATE','team':'OKC','player':'Alperen Sengun'},
                          {'date':'2021-07-29','event':'SG16','scope':'UNSELECTED_T1_CANDIDATE',
                           'effect':'OKC assigns unsignedSengun rights toHOU afterselection and beforefirstRequiredTender; receives preservedDET/WASclaims.'}],
      'participation_boundary':{
        'public_2021_prospect_identity_supported':60,'candidate_participation_family_explicit':True,
        'all_counterfactual_participants_historically_certified':False,
        'private_workout_or_all_unpublished_ledger_new_gate':False,
        'changed_college_causal_scope':['Filip Petrusev: keep public2021 identity and explicitly candidate professional/eligible participation; do not copy rival-alteredGonzaga scoring/awards/transition as canon.',
                                      'Joel Ayayi remains tracked but unselected; no new college/entry result is selected by this board.'],
        'later_NBA_success_or_current_dynamic_age_used_in2021_choice':False},
      'other_directions':{'T2':'NOT_BUILT_NOT_SELECTED: retainOKC16, re-evaluate namedteam demand and downstream rights before any execution.',
                          'T3':'NOT_BUILT_NOT_SELECTED: retainBOS16/Walker andOKCHorford/Brown; noHOU16 rights assignment.',
                          'T2_T3_completion_count':0},
      'authority':{'M1_A_reapproval_required':False,'AP1_SG16_author_selected':False,
        'all60_author_selected':False,'other58_author_selected':False,
        'actual_draft_or_League_approval_certified':False,'all_team_registration_completed':False,
        'whole_macro3_complete':False,'new_REGISTER_promotion':False,'independent_review_completed':True},
      'summary':{'rows':60,'unique_players':60,'first_round':30,'second_round':30,
        'preserved_local_CHI_working_rows':2,'other_unselected_candidate_rows':58,
        'holders_unchanged_from_S2':59,'conditional_asset_holder_changes':1,
        'Sengun_pre16_consumption':0,'unmatched_public_prospect_identities':0,
        'T1_direction_selected':False,'other_directions_completed':0,'new_NBA_UPCs_or_Tenders':0},
      'remaining_named_execution':['AP1/SG16 consequentialdirection remainsunselected; this completeT1 candidate doesnotselectit.',
         'Other58 draftedplayers remainworkingcandidates; chosenboard/worldpath mustbe explicitly adoptedbeforecanonpromotion.',
         'Afterrightsselection, constructnamedUPC/Tender/overseas/TW/standardregistration-and-cost execution separately; no60newstandardcontracts.',
         '2021–22 and2022–23 contracts/minutes/health/results anddownstreamNBA assets remainmacro3 work.'],
      'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False}


def validate(o):
    try:return [] if o==build() else ['Saved board/source/order/holder/authority differs from full reconstruction']
    except (AssertionError,KeyError,ValueError,TypeError,OSError) as e:return [str(e)]


def markdown(o):
    table='\n'.join(f"|{r['pick']}|{r['origin']}|{r['frozen_before_optional_offseason_holder']}|{r['selecting_team']}|{r['conditional_final_draft_rights_holder']}|{r['player']}|" for r in o['rows'])
    return f'''# 2021 전체 드래프트 작업 보드 — DB1/C39A·조건부 T1

{o['status']}. 기존 G7 한 보드를 실행 순서로 연결한 **60행 후보**다. Chicago10 Duarte/39 Wieskamp의 국소 작업 방향은 보존한다. 다른58 지명·T1 AP1/SG16 중요 방향·전체3번·실제NBA접수·등록·새작가잠금은 미완료/false다.

## 소유·선택·양도 순서

S2 완료의 origin/control60은 optionaloffseason 전 스냅샷이다. 조건부 T1 July28 AP1로 BOS16→OKC, July29 OKC가16에서 Sengun 지명, 그 후 최초RequiredTender 전 SG16로 미서명권리→HOU다. 지명한 구단과 최종권리구단을 분리한다. 나머지59 holder는S2와 같다. SG16 전에 Sengun이 앞순번에 선택되면 거부한다. 다른 draftnight 거래는 추가하지 않는다.

|순번|원소유|S2 holder|조건부 지명팀|조건부 최종권리팀|기존 DB1 후보|
|---:|---|---|---|---|---|
{table}

## 실제 원문 회수와 가용성의 범위

[NBA2021 prospects](https://www.nba.com/draft/2021/prospects)의 NAME표 webline162–250을 실제 읽고 기존60이름 모두 연결했다. Nahshon/Dayron의 아포스트로피2 alias만 동일 신원으로 정규화한다. 이 원2021 페이지의 현재 나이 필드는 동적2026값이라2021선택에 쓰지 않는다. 현재학교/status/측정도 대체세계 대학전기 인증으로 사용하지 않는다. profile나열은 private medical/조기신청서 전체를 인증하는 명단이 아니다.

직접 www/API-hub HTML6요청은403이라본문0이다. 캐시는 실패바이트SHA와 실제 회수된 **web-tool 텍스트 JSON** SHA를 구분한다. web텍스트를 원HTML이라 부르지 않는다. 같은 관측 묶음의 [NBA 최종 철회 발표](https://www.nba.com/news/nba-announces-51-early-entry-candidates-withdraw-from-2021-draft)는 날짜 구조 참고이고 그 페이지의 단순 부재로60명 개인합법성을 증명하지 않는다. [원역사 결과](https://www.nba.com/news/2021-nba-draft-results-picks-1-60)도 대체보드 선택에 복사하지 않는다.

각 후보의 가용성은 이 한 보드에서 앞서 선택되지 않음/비교목록에 남음으로 전수 검문했다. 합법적2021 참가/필요한 조기신청·미철회는 명시 후보입력 family의 조건이다. actual 대체세계 모든참가·의료·비공개워크아웃 인증은false. Gonzaga가변한 Petrusev의 대학수치·수상·전환을 원역사 그대로 잠그지 않는다. 유한 후보구현을 만들기 위해 모든사적부재/원장을 새 gate로 추가하지 않는다.

## 선택 경계와 다음 실행

[T1/T2/T3 중요 방향 패킷](../design/NBA_2021_PICK16_AP1_SG16_DIRECTION_DECISION_PACKET_2026_10_07.md)은 미선택이다. T2/T3 보드는 이 파일에서 만들거나 완료계수하지 않았다. T1이 선택되지 않아도 승인Chicago 코어의 독립 계약/옵션 준비는 계속한다. 이 보드의 지명권60개는 일반계약60자리·양수NBA분60개를 뜻하지 않는다. 선택 뒤 선수별UPC/Tender/해외/TW/표준등록·비용을 연결하고2021–23시즌으로 이어간다.

## 전체7행

|번호|작업|상태|
|---|---|---|
|1|2020드래프트연쇄|완료|
|2|Chicago2020–21|S2완료|
|3|2021–23거래·계약|T1조건부60행후보 준비; 중요방향/후속계약·시즌 미완료|
|4|장기커리어|후속 연결 미완료|
|5|결말·전체구조|누적22국소기능; 전체 미완료|
|6|집필규격·ContextPack|문체완료·실제Pack0|
|7|통합·독립·작가승인|전체G15/G16/G17미완료|

미완료 큰 묶음5. v0.30 PARTIAL·설계/원고CLOSED·원고0. 새중앙/REGISTER/Git변경0.
'''


def self_test(o):
    result=[]
    for label,change in [
      ('wrong_holder16',lambda x:x['rows'][15].update(selecting_team='HOU')),
      ('duplicate_player',lambda x:x['rows'][20].update(player='Alperen Sengun')),
      ('whole_draft_author_lock',lambda x:x['authority'].update(all60_author_selected=True)),
      ('T2_completed',lambda x:x['other_directions'].update(T2_T3_completion_count=1)),
      ('old_dynamic_age_is2021',lambda x:x['rows'][0]['public_identity_evidence'].update(observed_age_explicitly_excluded_from_2021_inputs=False)),
      ('NBA_UPC',lambda x:x['rows'][0].update(new_NBA_contract_or_tender=True))]:
        bad=copy.deepcopy(o);change(bad);assert validate(bad),label;result.append(label)
    for label,change in [
      ('constructor_T1_selected',lambda x:x.update(AP1_direction_author_selected=True)),
      ('constructor_extra_trade',lambda x:x.update(new_other_draft_night_trades=1))]:
        p=policy();change(p)
        with patch(__name__+'.policy',return_value=p):
            try:build()
            except AssertionError:result.append(label)
            else:raise AssertionError(label)
    board,frozen,ap,sq=inputs();obs,_,_=prospect_sources()
    b=copy.deepcopy(board);b[5]['proposed_player'],b[15]['proposed_player']=b[15]['proposed_player'],b[5]['proposed_player']
    try:join(b,frozen,ap,sq,obs)
    except AssertionError:result.append('upstream_Sengun_taken6_even_unique60')
    else:raise AssertionError('Sengun early falsepass')
    f=copy.deepcopy(frozen);f[15]['control_holder']='HOU'
    try:join(board,f,ap,sq,obs)
    except AssertionError:result.append('upstream_S2_16_wrongholder')
    else:raise AssertionError('S2holder falsepass')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args();o=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(ROOT/MD).write_text(markdown(o),encoding='utf8')
    if a.check:assert not validate(load(OUT));assert text(MD)==markdown(o)
    tests=self_test(o) if a.self_test else []
    print(json.dumps({'current':True,**o['summary'],'negative_controls':tests}))
