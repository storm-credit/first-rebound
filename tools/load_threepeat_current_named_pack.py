"""Read current Pack with selected display identity; never rewrite story/knowledge."""
import argparse
import json
from build_threepeat_actual_context_packs import ROOT, load, safe_path, digest, require

BINDING='context-packs/THREEPEAT_CURRENT_PROTAGONIST_IDENTITY_BINDING_2026_10_12.json'

def checked_rows():
    binding=load(ROOT,BINDING)
    source=binding['identity_source']
    require(digest(safe_path(ROOT,source['path']))==source['LF_sha256'],'Stale identity source')
    identity=load(ROOT,source['path'])
    require(identity['selected'] is True and identity['actor_id']=='PROTAGONIST','Unselected identity')
    require(identity['authority_class']=='AUTHOR_DELEGATED_SELECTION','Missing naming delegation')
    manifest=binding['base_manifest']
    require(digest(safe_path(ROOT,manifest['path']))==manifest['LF_sha256'],'Stale Pack manifest')
    require(binding['episode_count']==61 and len(binding['episodes'])==61,'Incomplete naming coverage')
    require([r['episode'] for r in binding['episodes']]==list(range(1,62)),'Episode sequence mismatch')
    require(identity['name_ko']=='권태오' and identity['name_en']=='Taeo Kwon' and identity['signature_nickname']=='TKO','Wrong selected identity')
    for value in (binding,identity):
        require(value['design_gate']=='CLOSED' and value['manuscript_allowed'] is False and value['freeze']=='v0.30 PARTIAL','Gate changed')
    for row in binding['episodes']:
        ep=row['episode']
        require(row['pack_path']==f'context-packs/threepeat-actual/EP{ep:04}.json','Wrong episode Pack')
        require(digest(safe_path(ROOT,row['pack_path']))==row['pack_LF_sha256'],'Changed original Pack')
        require(row['name_ko']==identity['name_ko'] and row['name_en']==identity['name_en'] and row['actor_id']==identity['actor_id'],'Actor mapping mismatch')
        expected=identity['usage_rules']['ep1_3' if ep<=3 else 'ep4_27' if ep<=27 else 'ep28_61']
        require(row['allowed_display_aliases']==expected,'Alias phase mismatch')
        require(row['TKO_editorially_eligible'] is (ep>=28),'Nickname introduced too early')
        require(row['nickname_known_to_every_actor'] is False,'Identity label incorrectly supplies actor knowledge')
    return binding,identity

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--episode',type=int,choices=range(1,62))
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    binding,identity=checked_rows()
    if args.check:
        result={'status':'PASS_61_SELECTED_IDENTITY_BINDINGS','name_ko':identity['name_ko'],'nickname':identity['signature_nickname'],'original_Packs_unchanged':61,'manuscript_allowed':False}
    else:
        if args.episode is None:parser.error('Use --episode 1..61 or --check')
        row=binding['episodes'][args.episode-1]
        result={'original_pack':load(ROOT,row['pack_path']),'current_identity_binding':row,'identity_source':binding['identity_source'],'identity_knowledge_boundary':'Names do not grant nickname knowledge or alter source facts'}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
