"""Select existing rookie-option continuity; no new salary or extension terms."""
from pathlib import Path
from copy import deepcopy
import argparse, hashlib, json
import fitz

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_chicago_2022_rookie_option_continuity.py'
OUT='simulation/CHICAGO_2022_ROOKIE_OPTION_CONTINUITY.json'
MD=OUT[:-5]+'.md'
CORE='simulation/CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.json'
REVIEW='reviews/CHI2022_SELECTED_CORE_CONTRACT_G11_INDEPENDENT_REVIEW_2026_10_07.json'
SEQUENCE='simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md'
PINS={'simulation/CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.json': 'cc586a6f801a1e61d60bd9eddbe0e8bfa57415963c2d0d76669683a690551d6c', 'reviews/CHI2022_SELECTED_CORE_CONTRACT_G11_INDEPENDENT_REVIEW_2026_10_07.json': '292f3a0982fe504a5507e38208d2e5295f61055048b207740eb602a1cd60b818', 'simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md': 'd7c270feacbc7030dffa234ac644e7c40e3a5fc25d2a4345cee4ff4be986a4cd'}
CBA=Path('C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf')
CBA_SHA='66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a'

def need(ok,why):
    if not ok: raise ValueError(why)

def text(p): return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p): return hashlib.sha256(text(p).encode()).hexdigest()
def read(root,p): return json.loads(text(root/p)) if p.endswith('.json') else text(root/p)

def notices():
    return [
      {'player':'LaMelo Ball','original_RSC_first_season':'2020-21','original_working_pick':4,'option_number':2,'option_season_number':4,'added_season':'2023-24'},
      {'player':'Chris Duarte','original_RSC_first_season':'2021-22','original_working_pick':10,'option_number':1,'option_season_number':3,'added_season':'2023-24'},
    ]
FIXED_NOTICES=deepcopy(notices())

def build(root=ROOT):
    inputs={}
    for p,h in PINS.items():
        need(sha(root/p)==h,'Accepted continuity source changed: '+p)
        inputs[p]=read(root,p)
        direct=json.loads(text(root/p)) if p.endswith('.json') else text(root/p)
        need(inputs[p]==direct,'Returned continuity source differs from physical bytes: '+p)
    core=inputs[CORE];peer=inputs[REVIEW]
    need(peer['independent_review_completed'] and peer['source_sha256'][CORE]==PINS[CORE],'Core peer changed')
    need(core['certification']['selected_fictional_acceptance_and_existing_forms'],'Existing working contracts not selected')
    rows={x['player']:x for x in core['named_contract_cost_rows']}
    need(rows['LaMelo Ball']['mechanism']=='EXERCISED_ROOKIE_THIRD_YEAR_OPTION_2022_START','Prior third option missing')
    need(rows['Chris Duarte']['mechanism']=='PRESERVED_ROOKIE_SCALE_YEAR2','Duarte original second year missing')
    need('LaMelo2023–24 4년차·Duarte2023–24 3년차 옵션' in inputs[SEQUENCE],'Existing continuity route missing')
    need(hashlib.sha256(CBA.read_bytes()).hexdigest()==CBA_SHA,'Primary CBA raw changed')
    with fitz.open(CBA) as d:
        rule=d[291].get_text().replace('\r\n','\n').replace('\r','\n')
        definition=d[31].get_text().replace('\r\n','\n').replace('\r','\n')
    flat=' '.join(rule.split());defs=' '.join(definition.split())
    need('day following the last day of the first Season' in flat and 'last day of the second Season' in flat and 'October 31' in flat,'Original option windows missing')
    need('signed by the Team' in flat and 'sent by email' in flat,'Signed notification mechanism missing')
    need('ending immediately after the last game of the NBA Finals' in defs,'Season end incorrectly replaced by cap-year end')
    chosen=notices();need(chosen==FIXED_NOTICES,'Named original year/pick/option changed')
    standard=core['selected_registration_July7']['STANDARD']
    need(len(standard)==15 and all(x['player']in standard for x in chosen),'Continuity player absent from existing UPC')
    for x in chosen:
        x.update({'date':'2022-10-01','team':'CHI','action':'EXERCISE_ORIGINAL_TEAM_OPTION_BY_SIGNED_NOTICE',
                  'notice_model':'Valid Chicago-signed notice emailed to the player or representative at the last known address; fictional sending selected, actual receipt not certified.',
                  'window_start':'DAY_AFTER_2021_22_NBA_FINALS_LAST_GAME',
                  'deadline':'2022-10-31','fictional_chronology_constraint':'The modeled 2021-22 NBA Season has ended before October1. Last Finals date/outcome remains joined in the season closeout; Season end is not automatically June30.',
                  'season_end_known_as_actual_alternate_fact':False,
                  'added_year_regular_salary':'ORIGINAL_UPC_OPTION_YEAR_REGULAR_SALARY_FUNCTION',
                  'added_year_likely_unlikely_and_protection':'KEEP_ALL_ORIGINAL_UPC_COMPONENTS_AND_GAMMA',
                  'new_price_or_bonus_selected':False,'third_pick_Charlotte_or_thirteenth_pick_Indiana_salary_copied':False,
                  'new_registration_slot':0,'team_or_player_trade_selected':False,'actual_notice_receipt':None})
    return {'id':'CHICAGO_2022_ROOKIE_OPTION_CONTINUITY','baseline_main':'46ddea1133f44031207baabb4a791bbbe101c9a6',
      'status':'ROUTINE_WORKING_OPTION_NOTICES_SELECTED_CONDITIONAL_DATED_SEASON_JOIN_PENDING',
      'source_sha256':{**PINS,SELF:sha(root/SELF)},
      'primary_rule':{'url':'https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf','raw_cache':str(CBA),'raw_sha256':CBA_SHA,
                      'rule':'VIII1a PDF292/printed270','Season_definition':'I1ooo PDF32/printed10',
                      'page_text_LF_sha256':{'292':hashlib.sha256(rule.encode()).hexdigest(),'32':hashlib.sha256(definition.encode()).hexdigest()}},
      'selected_notices':chosen,
      'authority':'Implementation of existing Chicago core retention and previously documented two option events; no new franchise/title/price selection.',
      'current_roster_preserved':deepcopy(core['selected_registration_July7']),
      'current_2022_23_cost_family_preserved':deepcopy(core['preserved_public_cost_family']),
      'next_2023_eligibility':{'LaMelo':'Operative fourth option preserves 2023-24 original UPC; 2023 rookie-scale extension must use applicable July6 12:01/new-CBA window. Extension/max/honors/first extended cap are not selected here.',
                              'Duarte':'Third option does not exercise the fourth option. His 2024-25 option needs its separate post-second-season/2023October31 window.',
                              'Coby':'No repeated 2022 option event: fourth-year2022-23 option was already selected in2021. 2023 QO/Bird/re-signing remains a separate joined function.',
                              'Wieskamp':'NonRSC2021 contract is not a first-round rookie option; EarlyBird/RFA renewal requires its own analysis.'},
      'boundaries':{'new_upstream_overwrite':False,'actual_end_of_alternate_2021_22_NBA_Season':None,'full_dated_notice_join_closed':False,'new_exact_salary_author_lock':False,
                    'new_2023_extension_or_fifth_rookie_year':False,'whole_FY23_salary_roster_or_macro3':False,'manuscript_allowed':False,'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','new_external_AGY_NLM_Claude_run':'NOT_RUN'}}

def markdown(v):
    return '\n'.join(['# Chicago2022 rookie 옵션 후속 연결','',
      '기존 Chicago 코어 유지의 routine 작업 선택:2022-10-01 LaMelo2023–24 fourth option·Duarte2023–24 third option의 적법한 Chicago signed notice를 선택했다. 실제 통지 영수증이나 새로운 급여/보너스를 인증하지 않는다.','',
      '**CBA Season 종료는 Finals 마지막 경기 직후다. Salary Cap Year의June30과 같다고 추정하지 않는다.** 명시한 fictional chronology 제약(해당 Finals 종료<Oct1)을 최종 시즌 원장과 연결하는 일은 남아 있다.','',
      '|선수|원RSC|추가 옵션 시즌|소비|','|---|---|---|---|',
      '|LaMelo|2020 #4|2023–24 fourth|기존2022–23 third option 이후; 원옵션 급여/보호 유지|',
      '|Duarte|2021 #10|2023–24 third|원2021 RSC second year 이후; fourth option은 별도2023사건|','',
      '실제Charlotte#3/Indiana#13 급여를 복사하지 않고, 새 가격/UPC/자리/선수 거래0이다. 15STD2TW 및 현재 FY22 비용 상단은 기존 소비기와 동일하다. 2023 급여 전체 검문을 이 통지로 완료 처리하지 않는다.','',
      '[선택FY22 계약](CHICAGO_2022_SELECTED_CORE_CONTRACT_CARRIER.md) · [기존계약 순서](CHICAGO_2021_23_CONTRACT_SEQUENCE.md) · [2017 원 CBA](https://nbpa.com/upload/2017-NBA-Collective-Bargaining-Agreement.pdf)','',
      'LaMelo2023 연장/LM1·Coby RFA/QO/Bird·Wieskamp/벤치 FA·두시즌 결산과2023 CBA 비용은 다음 실행이다. 신규 외부CLI NOT_RUN·v0.30 PARTIAL·설계/원고 CLOSED·원고0·미완료5/6번까지4.',''])

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build();out={OUT:json.dumps(v,ensure_ascii=False,indent=2)+'\n',MD:markdown(v)}
    if a.write:
        for f,t in out.items():(ROOT/f).write_text(t,encoding='utf-8')
    if a.check:
        for f,t in out.items():need(text(ROOT/f)==t,'Option artifact stale: '+f)
    print(json.dumps({'working_notices':2,'new_UPC_slots':0,'whole_2023_contracts':False,'Season_end_join':'PENDING_EXPLICIT_FINALS_DATE_CONSTRAINT'}))
if __name__=='__main__':main()
