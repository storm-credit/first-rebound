"""Read-only closure checks for selected current design and every generated Pack."""
import hashlib,json
from pathlib import Path
from build_threepeat_actual_context_packs import ROOT,compile_inputs,write_outputs,digest

def main():
 result=compile_inputs(ROOT);write_outputs(ROOT,result,check=True)
 assert result['final_episode_count']==61 and result['nba_count']==46
 packs=result['packs'];assert len(packs)==61
 bps=[p['blueprint'] for p in packs]
 assert [b['episode'] for b in bps]==list(range(1,62))
 assert all(p['manuscript_allowed'] is False for p in packs)
 selected=json.loads((ROOT/'design/THREEPEAT_CURRENT_SCENE_ACCESS_SELECTION_2026_10_12.json').read_text(encoding='utf-8-sig'))
 claims=segments=witnesses=0
 for b,access in zip(bps,selected['rows']):
  boundary=b['information_boundary'];ss=boundary['scene_segments'];cs=b['claims']
  assert cs[ss[0]['known_claim_indexes'][0]]['text']==access['entry_observation_text']
  assert b['action_choice_scope'].startswith('NONDIEGETIC')
  assert b['entry_state_scope'].startswith('NONDIEGETIC')
  ids=[x['segment_id'] for x in ss]
  if b['episode'] in [6,16,25,28,31]:
   assert ids.index('FOLLOW_ON_TRIGGER_OBSERVATION')<ids.index('FOLLOW_ON_1')<ids.index('END_OBSERVATION')
  if b['episode']==61:assert not any(s.startswith('FOLLOW_ON') for s in ids)
  claims+=len(cs);segments+=len(ss);witnesses+=len(boundary['access_witnesses'])
 last=bps[59];cs=last['claims'];ss=last['information_boundary']['scene_segments']
 a=next(s for s in ss if s['literal_when']=='2025Jun22remaining16.1')
 c=next(s for s in ss if s['literal_when']=='2025Jun22remaining15.6')
 assert '릴리스' in cs[a['known_claim_indexes'][0]]['text'] and '받은' in cs[c['known_claim_indexes'][0]]['text']
 assert a['scene_order']<c['scene_order']
 assert all('0.2' not in x['text'] for x in cs)
 return {'status':'CURRENT_MACRO1_6_MECHANICAL_CLOSEOUT_PASS','episode_packs':61,'claims':claims,
  'scene_segments':segments,'access_witnesses':witnesses,'NBA46of61_draft_excluded_percent':100*46/61,
  'source_count':len(result['used_sources_sha256']),'manifest_LF_sha256':digest(ROOT/'context-packs/threepeat-actual/manifest.json'),
  'scope':'Current selected design and pre-manuscript Pack integrity only; independent receipts remain separately bound; no prose/government/private-ledger certification.',
  'manuscript_allowed':False,'design_gate':'CLOSED','freeze':'v0.30 PARTIAL'}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False))
