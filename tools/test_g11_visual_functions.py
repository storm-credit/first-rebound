import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import check_g11_visual_functions as v
import build_g11_component_progress as p

class VisualEvidenceTests(unittest.TestCase):
    def setUp(self):self.d=json.loads((v.ROOT/v.SOURCE).read_text(encoding='utf-8'))
    def bad(self,edit):
        edit(self.d);self.assertTrue(v.validate(self.d))
    def test_baseline(self):self.assertEqual(v.validate(self.d),[])
    def test_missing_end_page(self):self.bad(lambda d:d['chapters'][4].update(observed_spreads=[[1,2],[3,4],[5,6]]))
    def test_author_note_region(self):self.bad(lambda d:d['chapters'][4]['function_regions'][-1].update(viewer_pages=[7,9]))
    def test_fake_body_hash(self):self.bad(lambda d:d['chapters'][0].update(body_sha256='a'*64))
    def test_fake_numeric_metric(self):self.bad(lambda d:d['chapters'][0]['quantitative_metrics'].update(sentence_count=12))
    def test_component_promotion(self):self.bad(lambda d:d['observed_components'].append('opening'))
    def test_duplicate_chapter(self):self.bad(lambda d:d['chapters'][-1].update(chapter=4))
    def test_reading_double_count(self):self.bad(lambda d:d.update(new_unique_readings=5))
    def test_full_p3_promotion(self):self.bad(lambda d:d.update(whole_P3_completed_chapters=5))
    def test_gate_promotion(self):self.bad(lambda d:d.update(manuscript_allowed=True))
    def test_duplicate_region(self):self.bad(lambda d:d['chapters'][1]['function_regions'][0].update(id='F1-1'))
    def test_unsupported_component_not_counted(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'source.json').write_text(json.dumps(self.d,ensure_ascii=False),encoding='utf-8')
            with patch.object(p,'SOURCES',{'필드의 고인물':{'opening':['source.json']}}):report=p.build(root)
        self.assertEqual(report['status'],'FAIL');self.assertEqual(report['components']['opening']['observed'],0)
    def test_invalid_visual_evidence_not_counted(self):
        self.d['chapters'][0]['body_sha256']='fake'
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'source.json').write_text(json.dumps(self.d,ensure_ascii=False),encoding='utf-8')
            with patch.object(p,'SOURCES',{'필드의 고인물':{'function':['source.json']}}):report=p.build(root)
        self.assertEqual(report['status'],'FAIL');self.assertEqual(report['components']['function']['observed'],0)
    def test_component_counts_separate(self):
        report=p.build();self.assertEqual(report['status'],'PASS')
        self.assertEqual(report['components']['function']['observed'],20)
        self.assertEqual(report['components']['opening']['observed'],15)
        self.assertEqual(report['unique_component_chapters'],20)
        self.assertEqual(report['components']['function']['by_evidence_mode'],{'RETAINED_DOM_COMPONENT_RECORDS':15,'VISUAL_SELECTED_FUNCTIONS':5})
        self.assertEqual(report['components']['function']['cross_modality_semantic_calibration'],'NOT_RUN')

if __name__=='__main__':unittest.main()
