"""Isolated compilation gates; fixtures are not story authority or real Packs."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / 'tools/build_lc1_actual_context_packs.py'
spec = importlib.util.spec_from_file_location('lc1_compiler', MODULE_PATH)
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


class PackBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        common = {'manuscript_allowed': False, 'design_gate': 'CLOSED', 'freeze': 'v0.30 PARTIAL'}
        subacts = [f'A{i:02}-S{j}' for i in range(1, 15) for j in range(1, 4)]
        self.history = {**common, 'status': 'LOCKED_SELECTED_DESIGN_HISTORY', 'whole_original_scope_complete': True,
                        'Act_ids': [f'A{i:02}' for i in range(1, 15)], 'SubAct_ids': subacts}
        self.write(compiler.HISTORY, self.history)
        history_pin = compiler.digest(self.root / compiler.HISTORY)
        self.episodes = []
        self.blueprints = []
        for number, subact in enumerate(subacts, 1):
            episode = {'episode': number, 'act': subact.split('-')[0], 'subact': subact,
                       'category': 'PRE_NBA' if number <= 9 else 'NBA',
                       'episode_function': f'Isolated boundary fixture {number}',
                       'entry_state': 'Supplied entry', 'exit_state_required': 'Supplied exit'}
            blueprint = {**episode, 'timeline_window': 'TEST_ONLY', 'act_question': 'Test question',
                         'subact_question': 'Test question', 'narrative_devices': ['CHOICE'],
                         'active_setup': [], 'payoff_or_defer': [], 'reader_expected_question': 'Test hook',
                         'relationship_state': {}, 'physical_state': {}, 'basketball_constraints': [],
                         'promises_to_pay': [], 'forbidden_moves': [], 'hold_fields': [],
                         'source_content_sha256': {compiler.HISTORY: history_pin},
                         'fact_evidence': [{'claim': 'Test-only selected event', 'status': 'AUTHOR_MODELED_DESIGN',
                                            'source_paths': [compiler.HISTORY]}],
                         'information_boundary': {'status': 'LOCKED_SELECTED_SCENE_ACCESS',
                           'pov_character': 'Test actor', 'clock_order_verified': True,
                           'scene_segments': [{'scene_order': 2, 'pov_character': 'Test actor', 'known_claim_indexes': [0]}],
                           'access_witnesses': [{'owner': 'Test actor', 'method': 'Direct observation',
                              'scene_order': 2, 'kind': 'OBSERVED_EVENT', 'event_order': 1,
                              'acquired_order': 1, 'claim_indexes': [0]}]}}
            self.episodes.append(episode)
            self.blueprints.append(blueprint)
        self.allocation = {**common, 'status': 'LOCKED_FINAL_EPISODE_FUNCTION_TABLE',
                           'final_episode_count': 42, 'episodes': self.episodes}
        self.common = common
        self.refresh_reviewed_inputs()

    def write(self, path, data):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

    def refresh_reviewed_inputs(self):
        self.write(compiler.ALLOCATION, self.allocation)
        self.write('design/test_blueprints.json', self.blueprints)
        reviewed = {p: compiler.digest(self.root / p) for p in
                    (compiler.ALLOCATION, compiler.HISTORY, 'design/test_blueprints.json')}
        review = {'status': 'ACCEPTED_TEST_ONLY', 'independent_review_completed': True,
                  'reviewed_artifacts_sha256': reviewed}
        self.write('reviews/test_review.json', review)
        rows = [{'episode': i, 'qualified_status': 'ACTUAL_VERIFIED', 'independent_review_completed': True,
                 'blueprint': {'path': 'design/test_blueprints.json', 'json_pointer': f'/{i-1}',
                               'source_sha256': reviewed['design/test_blueprints.json']}} for i in range(1, 43)]
        self.write(compiler.BLUEPRINT, {**self.common, 'episode_authorities': rows,
                    'independent_review': {'path': 'reviews/test_review.json',
                                           'source_sha256': compiler.digest(self.root / 'reviews/test_review.json')}})

    def test_full_inputs_compile_while_manuscript_closed(self):
        packs, nba = compiler.compile_inputs(self.root)
        self.assertEqual((len(packs), nba), (42, 33))
        self.assertTrue(all(p['manuscript_allowed'] is False for p in packs))

    def test_partial_history_cannot_compile_even_with_complete_files(self):
        self.history['whole_original_scope_complete'] = False
        self.write(compiler.HISTORY, self.history)
        with self.assertRaisesRegex(ValueError, 'Partial history'):
            compiler.compile_inputs(self.root)

    def test_candidate_is_rejected_even_if_blueprint_is_reviewed(self):
        self.blueprints[0]['fact_evidence'][0]['status'] = 'CANDIDATE'
        self.refresh_reviewed_inputs()
        with self.assertRaisesRegex(ValueError, 'candidate or HOLD'):
            compiler.compile_inputs(self.root)

    def test_future_observation_cannot_be_loaded_as_memory(self):
        self.blueprints[0]['information_boundary']['access_witnesses'][0]['event_order'] = 3
        self.refresh_reviewed_inputs()
        with self.assertRaisesRegex(ValueError, 'Future event'):
            compiler.compile_inputs(self.root)

    def test_changed_blueprint_cannot_bypass_reviewed_digest(self):
        self.blueprints[0]['episode_function'] = 'Unreviewed replacement'
        self.write('design/test_blueprints.json', self.blueprints)
        with self.assertRaisesRegex(ValueError, 'stale Blueprint'):
            compiler.compile_inputs(self.root)

    def test_inference_classification_cannot_leak_into_facts(self):
        claim = self.blueprints[0]['fact_evidence'][0]
        claim['status'] = 'INFERENCE'
        claim['inference_label_visible'] = True
        claim['claim'] = 'Explicitly unconfirmed inference'
        self.blueprints[0]['information_boundary']['access_witnesses'][0]['kind'] = 'EXPLICIT_INFERENCE'
        self.refresh_reviewed_inputs()
        packs, _ = compiler.compile_inputs(self.root)
        self.assertEqual(packs[0]['allowed_facts'], [])
        self.assertEqual(packs[0]['allowed_author_modeled_design'], [])
        self.assertEqual(packs[0]['allowed_knowledge'][0]['status'], 'INFERENCE')
        self.assertEqual(packs[0]['allowed_inferences'][0]['claim'], claim['claim'])


if __name__ == '__main__':
    unittest.main()
