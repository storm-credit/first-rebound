"""Check visual observation declarations, not pixels or original semantics."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE='research/G11_MUNPIA_FIELD_VISUAL_FUNCTIONS_2026_10_01.json'

def validate(data):
    errors=[]
    def require(ok,message):
        if not ok:errors.append(message)
    require(data.get('evidence_mode')=='VISUAL_SELECTED_FUNCTIONS','visual mode missing')
    require(data.get('observed_components')==['function','delivery'],'unsupported component declaration')
    for key in ['G11_final','author_locked','manuscript_allowed','original_text_retained','screenshots_retained','original_text_uploaded']:
        require(data.get(key) is False,'forbidden promotion/retention: '+key)
    for key in ['new_unique_readings','whole_P3_completed_chapters']:
        require(data.get(key)==0,'reused chapter/P3 promotion: '+key)
    require(data.get('selection',{}).get('exhaustive_semantic_partition') is False,'selected coding is not exhaustive')
    require(data.get('edition_identity_authenticated') is False,'edition authentication forbidden')
    require(data.get('selection_timing')=='POST_HOC_HYPOTHESIS_GENERATION','selection bias declaration')
    require(data.get('information_layer')=='DIEGETIC_SELECTED_REGIONS_AND_CASES_NOT_OBSERVER_RELIABILITY','information scope declaration')
    view=data.get('viewport',{})
    require((view.get('width'),view.get('height'),view.get('layout'),view.get('mode'))==(1920,1080,'FULLSCREEN_TWO_PAGE','PAGE'),'page address calibration')
    require(view.get('override_reset') is True and view.get('temporary_tab_closed') is True,'viewer cleanup declaration')
    chapters=data.get('chapters',[])
    require([c.get('chapter') for c in chapters]==[1,2,3,4,5],'five unique ordered chapters required')
    region_ids=[];delivery_ids=[]
    expected_ids=['2374907','2374909','2374911','2378659','2381055']
    for i,c in enumerate(chapters):
        if i>=5:break
        require(c.get('official_url','').split('?')[0]=='https://www.munpia.com/novel/viewer/153525/'+expected_ids[i],'official chapter identity')
        require(c.get('full_display_body_read') is True and c.get('body_end_marker_observed') is True,'start to body end declaration')
        end=c.get('body_end_page',0);total=c.get('viewer_total_pages',0)
        spreads=c.get('observed_spreads',[]);pages={p for pair in spreads for p in pair}
        require(all(len(pair)==2 and pair[1]==pair[0]+1 for pair in spreads),'invalid spread')
        require(end>0 and end<=total and set(range(1,end+1))<=pages,'missing body page/end')
        require(c.get('author_note_excluded') is True,'author note included')
        note=c.get('author_note_start_page')
        require(note is None or end<note<=total,'author note boundary')
        require(c.get('body_sha256') is None and c.get('canonical_sha256') is None,'unmeasured body hash')
        q=c.get('quantitative_metrics',{})
        require(set(q)=={'sentence_count','authored_paragraph_count','first_1000_utf16','voice_counts','inner_thought_ratio','length_distribution'} and all(v is None for v in q.values()),'unmeasured quantities must be null')
        require(bool(c.get('unexecuted_or_unverified')),'unexecuted boundary missing')
        for group in ['function_regions','delivery_cases']:
            require(bool(c.get(group)),'missing '+group)
            for item in c.get(group,[]):
                a,b=item.get('viewer_pages',[0,0])
                require(1<=a<=b<=end and set(range(a,b+1))<=pages,'selected address outside body')
                require(bool(item.get('functional_paraphrase')),'missing functional paraphrase')
                if group=='function_regions':
                    region_ids.append(item.get('id'))
                    require(item.get('semantic_exhaustive') is False,'region exhaustive promotion')
                else:
                    delivery_ids.append(item.get('id'))
                    require(bool(item.get('withheld_promotion')),'missing delivery limitation')
    for ids,key in [(region_ids,'macro_regions'),(delivery_ids,'delivery_cases')]:
        require(len(ids)==len(set(ids)) and len(ids)==data.get('selection',{}).get(key),'selected count/ID mismatch: '+key)
    return errors

if __name__=='__main__':
    d=json.loads((ROOT/SOURCE).read_text(encoding='utf-8'));e=validate(d)
    print(json.dumps(dict(status='FAIL' if e else 'PASS',errors=e,scope='DECLARATIONS_ONLY_NOT_PIXEL_OR_SEMANTIC_AUTHENTICATION'),ensure_ascii=False));raise SystemExit(bool(e))
