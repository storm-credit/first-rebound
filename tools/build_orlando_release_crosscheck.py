"""Crosscheck frozen official team releases; do not certify alternative-world execution."""
from pathlib import Path
import argparse, hashlib, json, re
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'research/ORLANDO_ORIGINAL_RELEASE_CROSSCHECK_2026_10_04.json'
SOURCES=[
 ('hall_apr13',72130,'2021-04-13','https://www.nba.com/magic/orlando-magic-sign-donta-hall-ten-day-contract-20210413','20d8751fa5687cf55cf61d5f9e0d2711d2c2efe1c78b7dd8575d5bbf783d32d2'),
 ('wagner_apr27',72301,'2021-04-27','https://www.nba.com/magic/orlando-magic-sign-moe-wagner-free-agent-center-20210427','37f903e00e9c6a6b239bfa33aafa74d8786c83032aa4b21746e775901a17b6d6'),
 ('brazdeikis_may2',72413,'2021-05-02','https://www.nba.com/magic/orlando-magic-sign-ignas-brazdeikis-10-day-contract-20210502','942192dc0b12878d63e01237fb1f2c04a7633a8e8c3ee2dcd245f0f223b4db8e'),
 ('hall_may9',72507,'2021-05-09','https://www.nba.com/magic/orlando-magic-sign-donta-hall-remainder-season-20210509','6fd8be6e68ba6f937bcd4d56f2a4861764f6aca2a36465f09b6252e9e4b45c5e')]
CLAIMS=[('hall_apr13','Devin Cannady','2021-04-13','release from 10-day contract','guard Devin Cannady has been released from his 10-day contract.'),
 ('wagner_apr27','Robert Franks','2021-04-27','release from 10-day contract','forward Robert Franks has been released from his 10-day contract.'),
 ('brazdeikis_may2','Donta Hall','2021-05-02','release from 10-day contract','forward Donta Hall has been released from his 10-day contract.'),
 ('hall_may9','Donta Hall','2021-05-09','rest of regular season; NBA hardship approval reported','for the remainder of the regular season')]
def sha(b):return hashlib.sha256(b).hexdigest()
def build(cache):
 sources=[]; paragraphs={}
 for key,pid,day,url,expected in SOURCES:
  name='fr-hall-may9-official.html' if key=='hall_may9' else 'fr-'+key+'-official.html'
  raw=(cache/name).read_bytes()
  if sha(raw)!=expected:raise ValueError('Frozen article changed: '+key)
  match=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',raw.decode('utf-8'),re.S)
  if not match:raise ValueError('Missing public article payload: '+key)
  page=json.loads(match.group(1))['props']['pageProps']['pageObject']
  if page['id']!=pid or page['permalink']!=url or page['date'][:10]!=day or page['type']!='article':raise ValueError('Article identity mismatch: '+key)
  body=[x['text'] for x in page['contentStructured'] if x.get('type')=='paragraph' and x.get('text')]
  paragraphs[key]=body
  sources.append(dict(id=key,url=url,article_id=pid,title=page['title'],published_utc=page['date'],modified_utc=page['modified'],http_status_at_collection=200,raw_bytes=len(raw),raw_sha256=expected,body_paragraph_count=len(body),body_text_sha256=sha('\n'.join(body).encode()),access='DIRECT_HTTP_PUBLIC_NEXT_DATA_BODY_READ',publisher='Orlando Magic / NBA.com',receipt_time_not_certified=True))
 feed_path=ROOT/'research/NBA_MOVEMENT_WINDOW_EVIDENCE_2026_10_04.json'
 feed=json.loads(feed_path.read_text(encoding='utf-8'))
 events=[]
 for key,player,day,claim,short_quote in CLAIMS:
  body=paragraphs[key]
  if short_quote not in body[0]:raise ValueError('Expected source statement missing: '+key)
  prior=[x for x in feed['orlando']['comparison'] if x['guide_event']['date']==day and x['guide_event']['player']==player]
  if len(prior)!=1:raise ValueError('Missing/ambiguous guide event')
  expected_status='CONTRACT_CLASS_CONFLICT' if key=='hall_may9' else 'GUIDE_ONLY_EVENT_NOT_DELETED'
  if prior[0]['status']!=expected_status:raise ValueError('Prior discrepancy changed')
  events.append(dict(date=day,player=player,source_id=key,source_paragraph=1,source_paragraph_sha256=sha(body[0].encode()),short_quote=short_quote,historical_claim=claim,prior_feed_status=expected_status,source_fact_verified=True,alternative_world_execution_verified=False))
 if 'The Magic was granted a hardship exception by the NBA in order to add Hall.' not in paragraphs['hall_may9'][0]:raise ValueError('Missing original-world hardship grant')
 return dict(schema='ORLANDO_DATED_RELEASE_CROSSCHECK_V1',baseline_main='20020bd73c3b99c2ff0f66cc28849ebfe880c004',observed_local_date='2026-10-04',sources=sources,events=events,prior_feed_evidence=dict(path=feed_path.relative_to(ROOT).as_posix(),sha256=sha(feed_path.read_bytes()),comparison_counts_preserved=feed['orlando']['comparison_counts']),historical_findings=dict(guide_only_releases_directly_confirmed=3,hall_may9_declared_contract='REMAINDER_OF_REGULAR_SEASON',hall_may9_original_world_hardship_granted=True,preferred_contract_label_basis='Contemporaneous team announcement and team guide; conflicting aggregate feed label retained',documents_recovered=4,publisher_count=1,independent_publisher_increment=0),boundaries=dict(precise_league_receipt_time_verified=False,full_salary_terms_disclosed=False,release_means_zero_residual=False,may9_hardship_transferred_to_selected_world=False,april_hardship_class_inferred=False,selected_may9_contract_omission_preserved=True,selected_april_obligations_preserved=True,full_registration_verified=False,source_verified_legal_proofs_added=0,complete_domain_legal_proofs_added=0,new_author_locks=0,manuscript_allowed=False))
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--cache-dir',type=Path,required=True);ap.add_argument('--check',action='store_true');a=ap.parse_args();out=build(a.cache_dir)
 if a.check:
  if json.loads(OUTPUT.read_text(encoding='utf-8'))!=out:raise ValueError('Stored reconciliation changed')
 else:OUTPUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(documents=4,releases_confirmed=3,hall_may9_label='REST_OF_REGULAR_SEASON',historical_hardship=True,legal_proofs_added=0)))
if __name__=='__main__':main()
