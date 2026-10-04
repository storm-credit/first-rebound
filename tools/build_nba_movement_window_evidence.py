"""Reconcile one frozen NBA public movement snapshot; never certify legal execution."""
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA = '3d9d7a6dd7ccd39ddfdd1799a26ef9901b44682d85a26f05239b468a8ae92e3a'
OUTPUT = ROOT / 'research/NBA_MOVEMENT_WINDOW_EVIDENCE_2026_10_04.json'
CHI, ORL = 1610612741, 1610612753
PLAYER_IDS = {'Robert Franks':1629606, 'Donta Hall':1629743, 'Devin Cannady':1629962,
              'Karim Mane':1630211, 'Moritz Wagner':1629021, 'Ignas Brazdeikis':1629649,
              'Sindarius Thornwell':1628414}

def digest(value):
    return hashlib.sha256(value).hexdigest()

def date(row):
    return row['TRANSACTION_DATE'][:10]

def window(rows, start, end):
    return [x for x in rows if start <= date(x) <= end]

def related_groups(rows, team):
    groups = {x['GroupSort'] for x in rows if x['TEAM_ID']==team or x['Additional_Sort']==team}
    return [x for x in rows if x['GroupSort'] in groups]

def outbound_player_rows(rows, team):
    # A broad candidate screen, not a legal Standard-contract/TPE classification.
    return [x for x in rows if x['Transaction_Type']=='Trade'
            and x['Additional_Sort']==team and x['PLAYER_ID']>0]

def build(snapshot, client_proof):
    raw=snapshot.read_bytes()
    if digest(raw)!=EXPECTED_SHA:
        raise ValueError('Frozen source changed; re-read and review before accepting another snapshot')
    source=json.loads(raw)['NBA_Player_Movement']; rows=source['rows']
    if len(rows)!=9927 or not all(isinstance(x,dict) and all(k in x for k in
            ['TEAM_ID','PLAYER_ID','Additional_Sort','GroupSort','TRANSACTION_DATE','Transaction_Type']) for x in rows):
        raise ValueError('Source shape/count mismatch')
    chi_window=window(rows,'2019-07-06','2019-07-07')
    trades=[x for x in chi_window if x['Transaction_Type']=='Trade']
    chi=related_groups(chi_window,CHI)
    orl=related_groups(window(rows,'2021-03-25','2021-05-16'),ORL)
    own=[x for x in orl if x['TEAM_ID']==ORL and date(x)>='2021-04-12']
    guide_path=ROOT/'research/D1_ORLANDO_CALENDAR_SOURCES_2026_10_02.json'
    guide=json.loads(guide_path.read_text(encoding='utf-8'))
    comparison=[]; used=set()
    for g in guide['events']:
        pid=PLAYER_IDS[g['player']]
        action='Waive' if g['action'].startswith(('RELEASE','WAIVE')) else 'Signing'
        match=[x for x in own if date(x)==g['date'] and x['PLAYER_ID']==pid and x['Transaction_Type']==action]
        if len(match)>1: raise ValueError('Ambiguous date/player/action match')
        item=dict(guide_event=g, player_id=pid, feed_groups=[x['GroupSort'] for x in match])
        if not match:
            item['status']='GUIDE_ONLY_EVENT_NOT_DELETED'
        else:
            x=match[0]; used.add(x['GroupSort']);desc=x['TRANSACTION_DESCRIPTION']
            target=None if action=='Waive' else 'Two-Way Contract' if 'TWO_WAY' in g['action'] else 'Rest-of-Season Contract' if 'REST_OF_SEASON' in g['action'] else '10-Day Contract' if 'TEN_DAY' in g['action'] else None
            item['status']='CONTRACT_CLASS_CONFLICT' if target and target not in desc else 'DATE_PLAYER_ACTION_MATCH'
            item['contract_class_match']=None if target is None else target in desc
            item['feed_description']=desc
            item['nth_contract_scope']='Ordinal, if present, is sourced to guide only'
        comparison.append(item)
    statuses={k:sum(x['status']==k for x in comparison) for k in ['DATE_PLAYER_ACTION_MATCH','CONTRACT_CLASS_CONFLICT','GUIDE_ONLY_EVENT_NOT_DELETED']}
    extended=related_groups(window(rows,'2019-07-01','2020-11-18'),CHI)
    return {
      'schema':'NBA_PUBLIC_MOVEMENT_WINDOW_EVIDENCE_V1', 'baseline_main':'0a6bfca8209c4655d59c892cd9bc27ee9bf0b8ea',
      'status':'PRIMARY_PUBLIC_INVENTORY_RECONCILIATION_NOT_LEGAL_CERTIFICATE',
      'source':{'url':'https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json','nba_consumer_page':'https://www.nba.com/players/transactions','observed_local_date':'2026-10-04','snapshot_sha256':EXPECTED_SHA,'bytes':len(raw),'row_count':len(rows),'date_range':[min(date(x) for x in rows),max(date(x) for x in rows)],'client_proof':json.loads(client_proof.read_text(encoding='utf-8')),'ui_row_limit':500,'snapshot_input_is_full_feed':True},
      'chicago':{'date_window':['2019-07-06','2019-07-07'],'league_trade_row_count':len(trades),'league_trade_group_count':len({x['GroupSort'] for x in trades}),'related_rows':chi,'outbound_player_linked_trade_candidates':outbound_player_rows(trades,CHI),'positive_player_id_is_not_contract_type_proof':True,'legal_TPE_origin_count':None,'extended_public_window':['2019-07-01','2020-11-18'],'extended_related_trade_rows':[x for x in extended if x['Transaction_Type']=='Trade'],'extended_outbound_player_candidates':outbound_player_rows(extended,CHI),'negative_claim_scope':'Only this published snapshot and dates; not hidden events, intraday order, alternative-world changes or legal balances'},
      'chicago_global_trade_window_rows':trades,
      'orlando':{'date_window':['2021-03-25','2021-05-16'],'related_group_count':len({x['GroupSort'] for x in orl}),'related_rows':orl,'guide_comparison_window':['2021-04-12','2021-05-16'],'guide_event_count':len(comparison),'own_feed_event_count':len(own),'comparison_counts':statuses,'comparison':comparison,'feed_only_groups':[x['GroupSort'] for x in own if x['GroupSort'] not in used],'guide_path':str(guide_path.relative_to(ROOT)).replace('\\','/'),'guide_sha256':digest(guide_path.read_bytes()),'hall_may9_selected_world':'OMITTED_BY_EXISTING_AUTHOR_APPROVAL_NOT_RESTORED','historical_trade_groups_are_not_alternative_world_roster_inputs':True},
      'boundaries':{'midnight_is_actual_receipt_time':False,'waive_means_zero_salary':False,'Signing_Contract_excludes_Summer':False,'draft_consideration_identifies_pick_terms':False,'feed_absence_proves_event_absence':False,'source_verified_legal_proofs_added':0,'complete_domain_legal_proofs_added':0,'manuscript_allowed':False,'new_author_locks':0}
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--snapshot',required=True,type=Path);ap.add_argument('--client-proof',required=True,type=Path);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    result=build(args.snapshot,args.client_proof)
    if args.check:
        if json.loads(OUTPUT.read_text(encoding='utf-8'))!=result: raise ValueError('Evidence changed; review before rewriting')
    else:
        OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'snapshot_rows':result['source']['row_count'],'CHI_window_trade_rows':result['chicago']['league_trade_row_count'],'CHI_outbound_candidates':len(result['chicago']['outbound_player_linked_trade_candidates']),'ORL_comparison':result['orlando']['comparison_counts'],'legal_proofs_added':0}))
if __name__=='__main__': main()
