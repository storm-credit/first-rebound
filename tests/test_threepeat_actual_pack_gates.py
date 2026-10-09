"""Boundary attacks in TemporaryDirectory only; fixtures create no story authority."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'tools/build_threepeat_actual_context_packs.py'
spec = importlib.util.spec_from_file_location('threepeat_compiler', MODULE)
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


class CurrentPackGates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='threepeat-pack-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.common = {'scope_id': 'TEST_ONLY_NOT_STORY_AUTHORITY', 'producer_id': 'producer',
                       'manuscript_allowed': False, 'design_gate': 'CLOSED', 'freeze': 'v0.30 PARTIAL'}
        self.make_fixture(20)

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(compiler.serialized(data))

    def ref(self, path, pointer=''):
        return {'path': path, 'source_sha256': compiler.digest(self.root / path), 'json_pointer': pointer}

    def make_fixture(self, n):
        self.policy = {'minimum_percent': 75, 'maximum_percent': 85, 'denominator': 'ALL_FINAL_EPISODES',
                       'counted_categories': ['NBA'], 'category_definitions': {
                           'NBA': 'Test NBA calendar', 'NBA_DRAFT': 'Test draft selection',
                           'PRE_NBA': 'Test prior school calendar', 'POST_NBA': 'Test post-service calendar'}}
        self.selection_doc = {'status': 'DELEGATED_SELECTED_DESIGN_TARGET_REVISED_EXECUTION_PENDING',
                              'selected_design_targets': {'Chicago_title_years': [2023, 2024, 2025],
                                                         'main_story_climax_and_end_year': 2025,
                                                         'retirement_epilogue_year': 2035},
                              'records': {}}
        for cid, kind in {**compiler.CRITICAL_CHOICES, 'CATEGORY': 'EPISODE_CATEGORY_POLICY'}.items():
            self.selection_doc['records'][cid] = {'choice_id': cid, 'kind': kind,
                'selected': True, 'status': 'SELECTED_FICTIONAL_USED_RESOLUTION',
                'authority_class': 'DELEGATED_SELECTED', 'resolution': 'TEST_ONLY chosen input',
                'unresolved_used_dependencies': []}
        self.selection_doc['records']['CATEGORY']['policy'] = copy.deepcopy(self.policy)
        self.selection_doc['records']['C01_CALENDAR'].update(
            used_calendar_status='SELECTED_RESOLVED', covered_exit_port_ids=['PORT_M08'])
        self.scope = {**self.common, 'status': 'LOCKED_CURRENT_PACK_SCOPE',
                      'active_unit_ids': compiler.UNITS, 'required_exit_port_ids': ['PORT_' + u for u in compiler.UNITS],
                      'category_policy': self.policy,
                      'consequential_choice_requirements': [
                          {'choice_id': c, 'kind': k, 'use_mode': 'USED'} for c, k in compiler.CRITICAL_CHOICES.items()]}
        self.history = {**self.common, 'status': 'LOCKED_CURRENT_SELECTED_HISTORY',
                        'current_used_scope_complete': True, 'finite_used_exit_ports': [],
                        'unit_exits': [], 'consequential_choices': []}
        for index, unit in enumerate(compiler.UNITS):
            choices = ['C01_CALENDAR'] if unit == 'M08' else (['EARLY_REWARD_IMPLEMENTATION'] if unit == 'M04' else [])
            self.history['finite_used_exit_ports'].append({'port_id': 'PORT_' + unit, 'unit_id': unit,
                'status': 'SELECTED_RESOLVED', 'entry_state': 'ENTRY_' + unit, 'changed_action': 'Test independent choice',
                'durable_cost': 'Test carried cost', 'exit_state': 'EXIT_' + unit, 'consequential_choice_ids': choices})
            self.history['unit_exits'].append({'unit_id': unit, 'entry_state': 'ENTRY_' + unit,
                'exit_state': 'EXIT_' + unit, 'port_ids': ['PORT_' + unit],
                'next_unit_id': compiler.UNITS[index + 1] if index < 9 else None,
                'next_entry_state': 'ENTRY_' + compiler.UNITS[index + 1] if index < 9 else None})
        for cid, unit in [('C01_CALENDAR', 'M08'), ('EARLY_REWARD_IMPLEMENTATION', 'M04')]:
            self.history['consequential_choices'].append({'choice_id': cid, 'status': 'RESOLVED_SELECTED',
                'resolution': 'TEST_ONLY chosen input', 'used_port_ids': ['PORT_' + unit]})
        # Four non-NBA units; the count is test data, never a production N recommendation.
        units = ['M01', 'M02', 'M03'] + ['M04'] * (n - 10) + compiler.UNITS[3:]
        self.episodes = []
        self.blueprints = []
        for number, unit in enumerate(units, 1):
            episode = {'episode': number, 'unit_id': unit,
                'category': 'PRE_NBA' if unit in {'M01', 'M02', 'M03'} else ('POST_NBA' if unit == 'EPI' else 'NBA'),
                'episode_function': f'TEST_ONLY access boundary {number}', 'action_choice': 'Test chosen action',
                'durable_cost': 'Test durable cost', 'state_change': 'Test changed state',
                'entry_state': 'ENTRY_' + unit, 'exit_state_required': 'EXIT_' + unit,
                'consumed_exit_port_ids': ['PORT_' + unit],
                'consequential_choice_ids': ['C01_CALENDAR'] if unit == 'M08' else
                    (['EARLY_REWARD_IMPLEMENTATION'] if unit == 'M04' else [])}
            self.episodes.append(episode)
            self.blueprints.append({**self.common, **copy.deepcopy(episode), 'status': 'ACTUAL_VERIFIED',
                'timeline_window': 'TEST_ONLY', 'unit_question': 'Test unit question', 'primary_devices': ['CHOICE'],
                'setup_to_plant': 'Test setup', 'payoff_to_consume': 'Test payoff', 'reader_question': 'Test hook',
                'relationship_state': 'Test observed relationship', 'physical_state': 'Test selected physical state',
                'basketball_goal': 'Test tactical objective', 'forbidden_changes': 'No test authority in repository',
                'unresolved_used_dependencies': [], 'claims': [{'text': 'Test selected event',
                    'status': 'AUTHOR_MODELED_DESIGN', 'temporal_kind': 'OBSERVED_EVENT'}],
                'information_boundary': {'status': 'LOCKED_SELECTED_SCENE_ACCESS', 'pov_character': 'Test actor',
                    'clock_basis': 'TEST_ONLY ordered event origin', 'clock_order_verified': True,
                    'scene_segments': [{'segment_id': 'SCENE', 'scene_order': 2, 'pov_character': 'Test actor',
                                        'known_claim_indexes': [0]}],
                    'access_witnesses': [{'segment_id': 'SCENE', 'owner': 'Test actor', 'scene_order': 2,
                        'acquired_order': 1, 'event_order': 1, 'access_method': 'Test direct observation',
                        'knowledge_kind': 'OBSERVED_EVENT', 'claim_indexes': [0]}]}})
        self.allocation = {**self.common, 'status': 'LOCKED_CURRENT_FINAL_EPISODE_FUNCTION_TABLE',
                           'final_episode_count': n, 'episodes': self.episodes}
        self.refresh()

    def refresh(self):
        self.write('canon/test_selections.json', self.selection_doc)
        self.scope['selected_scope_ref'] = self.ref('canon/test_selections.json', '/selected_design_targets')
        self.scope['category_policy']['selection_source_ref'] = self.ref('canon/test_selections.json', '/records/CATEGORY')
        for choice in self.history['consequential_choices']:
            if choice['status'] != 'NOT_USED':
                choice['selection_source_ref'] = self.ref('canon/test_selections.json', '/records/' + choice['choice_id'])
        for port in self.history['finite_used_exit_ports']:
            port['source_refs'] = [self.ref('canon/test_selections.json', '/selected_design_targets')]
        for bp in self.blueprints:
            for claim in bp['claims']:
                if not claim.get('test_preserve_native_text_refs'):
                    claim['source_refs'] = [self.ref('canon/test_selections.json', '/selected_design_targets')]
        self.write(compiler.SCOPE, self.scope)
        self.write(compiler.HISTORY, self.history)
        self.write(compiler.ALLOCATION, self.allocation)
        self.write('design/test_blueprints.json', {'status': 'ACTUAL_VERIFIED_CURRENT_BLUEPRINT_BUNDLE',
                                                 'producer_id': 'blueprint_producer', 'blueprints': self.blueprints})
        rows = [{'episode': i, 'qualified_status': 'ACTUAL_VERIFIED',
                 'blueprint': self.ref('design/test_blueprints.json', f'/blueprints/{i-1}')}
                for i in range(1, len(self.episodes) + 1)]
        self.authority = {**self.common, 'status': 'ACTUAL_CURRENT_BLUEPRINT_AUTHORITY', 'episode_authorities': rows}
        paths = [compiler.SCOPE, compiler.HISTORY, compiler.ALLOCATION, 'design/test_blueprints.json', 'canon/test_selections.json']
        paths.extend(getattr(self, 'additional_reviewed_paths', []))
        self.review = {'status': 'ACCEPTED_CURRENT_THREEPEAT_PACK_INPUTS', 'independent_review_completed': True,
                       'reviewer_id': 'other_reviewer', 'reviewed_artifacts_sha256': {p: compiler.digest(self.root / p) for p in paths},
                       'reviewed_authority_payload_sha256': compiler.authority_payload_digest(self.authority)}
        self.write('reviews/test_review.json', self.review)
        self.authority['independent_review'] = self.ref('reviews/test_review.json')
        self.write(compiler.BLUEPRINT, self.authority)

    def reject(self, regex):
        with self.assertRaisesRegex(ValueError, regex):
            compiler.compile_inputs(self.root)

    def test_variable_final_n_current_units_and_closed_outputs(self):
        for n in (20, 24):
            with self.subTest(n=n):
                self.make_fixture(n)
                result = compiler.compile_inputs(self.root)
                self.assertEqual((result['final_episode_count'], len(result['packs'])), (n, n))
                self.assertTrue(all(p['manuscript_allowed'] is False for p in result['packs']))
                self.assertNotIn('whole_original_scope_complete', self.history)

    def test_missing_current_authority_never_uses_candidate_or_legacy(self):
        (self.root / compiler.ALLOCATION).unlink()
        self.reject('not issued')
        self.assertFalse((self.root / compiler.OUT).exists())

    def test_c01_source_unselected_cannot_be_laundered_by_locked_history_and_new_review(self):
        self.selection_doc['records']['C01_CALENDAR'].update(selected=False, status='UNSELECTED')
        self.refresh()
        self.reject('not selected in its source')

    def test_resolved_flag_cannot_hide_calendar_or_early_reward_hold(self):
        for cid in compiler.CRITICAL_CHOICES:
            with self.subTest(choice=cid):
                original = copy.deepcopy(self.selection_doc['records'][cid])
                self.selection_doc['records'][cid]['unresolved_used_dependencies'] = ['Unresolved actual used date']
                self.refresh()
                self.reject('dependencies on HOLD')
                self.selection_doc['records'][cid] = original
        self.selection_doc['records']['C01_CALENDAR']['covered_exit_port_ids'] = ['PORT_M07']
        self.refresh()
        self.reject('calendar port coverage')

    def test_critical_choice_cannot_be_declared_not_used(self):
        self.scope['consequential_choice_requirements'][0]['use_mode'] = 'NOT_USED'
        self.history['consequential_choices'][0].update(status='NOT_USED', used_port_ids=[])
        self.refresh()
        self.reject('critical selection missing')

    def test_unused_personal_award_is_allowed_but_cannot_supply_highermax(self):
        self.scope['consequential_choice_requirements'].append({'choice_id': 'MVP', 'kind': 'PERSONAL_AWARD', 'use_mode': 'NOT_USED'})
        self.history['consequential_choices'].append({'choice_id': 'MVP', 'status': 'NOT_USED', 'used_port_ids': [], 'resolution': None})
        self.refresh()
        compiler.compile_inputs(self.root)
        self.blueprints[0]['claims'][0]['effect_kind'] = 'PERSONAL_AWARD_MAX_SALARY'
        self.refresh()
        self.reject('HigherMax')

    def test_finite_history_and_final_episode_exit_coverage_are_required(self):
        self.history['current_used_scope_complete'] = False
        self.refresh()
        self.reject('used history is incomplete')
        self.history['current_used_scope_complete'] = True
        self.episodes[-1]['consumed_exit_port_ids'] = []
        self.blueprints[-1]['consumed_exit_port_ids'] = []
        self.refresh()
        self.reject('every finite used exit')

    def test_final_n_and_policy_cannot_be_inferred_or_redefined(self):
        self.allocation['final_episode_count'] = None
        self.refresh()
        self.reject('explicitly locked')
        self.allocation['final_episode_count'] = len(self.episodes)
        self.scope['category_policy']['minimum_percent'] = 70
        self.refresh()
        self.reject('75–85 policy')

    def test_draft_inclusion_requires_an_explicit_selected_policy(self):
        self.episodes[2]['category'] = self.blueprints[2]['category'] = 'NBA_DRAFT'
        self.scope['category_policy']['counted_categories'] = ['NBA', 'NBA_DRAFT']
        self.refresh()
        self.reject('differs from selected policy')
        self.selection_doc['records']['CATEGORY']['policy']['counted_categories'] = ['NBA', 'NBA_DRAFT']
        self.refresh()
        result = compiler.compile_inputs(self.root)
        self.assertEqual((result['nba_percent'], result['strict_draft_excluded_percent']), (85, 80))

    def test_stale_review_and_detached_authority_payload_are_rejected(self):
        self.allocation['episodes'][0]['episode_function'] = 'Changed after review'
        self.write(compiler.ALLOCATION, self.allocation)
        self.reject('not independently reviewed')
        self.refresh()
        self.authority['episode_authorities'][0]['qualified_status'] = 'CANDIDATE'
        self.write(compiler.BLUEPRINT, self.authority)
        self.reject('payload changed')

    def test_producer_is_not_an_independent_reviewer(self):
        self.review['reviewer_id'] = 'producer'
        self.write('reviews/test_review.json', self.review)
        self.authority['independent_review'] = self.ref('reviews/test_review.json')
        self.write(compiler.BLUEPRINT, self.authority)
        self.reject('cannot be independent reviewer')

    def test_authority_episode_boolean_and_float_ids_cannot_alias_one(self):
        for value in (True, 1.0):
            with self.subTest(value=value):
                self.refresh()
                self.authority['episode_authorities'][0]['episode'] = value
                self.review['reviewed_authority_payload_sha256'] = compiler.authority_payload_digest(self.authority)
                self.write('reviews/test_review.json', self.review)
                self.authority['independent_review'] = self.ref('reviews/test_review.json')
                self.write(compiler.BLUEPRINT, self.authority)
                self.reject('not Boolean or float')

    def test_candidate_open_gate_and_device_budget_fail_even_with_new_review(self):
        bp = self.blueprints[0]
        original = copy.deepcopy(bp)
        for key, value, regex in [('status', 'CANDIDATE', 'not actual verified'),
                                  ('design_gate', 'OPEN', 'remain CLOSED'),
                                  ('primary_devices', ['A', 'B', 'C'], 'device budget')]:
            with self.subTest(key=key):
                bp.clear()
                bp.update(copy.deepcopy(original))
                bp[key] = value
                self.refresh()
                self.reject(regex)

    def test_boolean_nonfinite_and_future_clock_attacks(self):
        witness = self.blueprints[0]['information_boundary']['access_witnesses'][0]
        for value, regex in [(True, 'finite clock'), (float('nan'), 'finite clock'), (float('inf'), 'finite clock'), (3, 'after scene')]:
            with self.subTest(value=value):
                if isinstance(value, float):
                    with self.assertRaisesRegex(ValueError, regex):
                        compiler.clock(value, 'hostile runtime clock')
                    continue
                witness['acquired_order'] = value
                self.refresh()
                self.reject(regex)

    def test_ghost_witness_and_unknown_claim_access_are_rejected(self):
        boundary = self.blueprints[0]['information_boundary']
        boundary['access_witnesses'][0]['segment_id'] = 'GHOST'
        self.refresh()
        self.reject('Ghost witness')
        boundary['access_witnesses'][0]['segment_id'] = 'SCENE'
        boundary['access_witnesses'][0]['owner'] = 'Other actor'
        self.refresh()
        self.reject('owner is not')
        boundary['access_witnesses'][0]['owner'] = 'Test actor'
        boundary['scene_segments'][0]['known_claim_indexes'] = [True]
        self.refresh()
        self.reject('index out of range')

    def test_rfc6901_empty_key_root_and_array_integer_syntax(self):
        data = {'': {'a/b~c': [12]}, '0': 'numeric dict key'}
        self.assertIs(compiler.resolve_pointer(data, ''), data)
        self.assertEqual(compiler.resolve_pointer(data, '//a~1b~0c/0'), 12)
        self.assertEqual(compiler.resolve_pointer(data, '/'), data[''])
        self.assertEqual(compiler.resolve_pointer(data, '/0'), 'numeric dict key')
        for pointer in ('//a~1b~0c/-1', '//a~1b~0c/00', '//a~1b~0c/-', '/bad~2escape'):
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                compiler.resolve_pointer(data, pointer)

    def test_duplicate_json_keys_and_exponent_overflow_fail(self):
        for body in ('{"x":1,"x":2}', '{"x":1e999}', '{"x":NaN}'):
            with self.subTest(body=body):
                target = self.root / 'hostile.json'
                target.write_text(body, encoding='utf-8')
                with self.assertRaises(ValueError):
                    compiler.load(self.root, 'hostile.json')

    def test_source_escape_and_stale_blueprint_fail(self):
        for relative in ('../outside.json', str(self.root / 'absolute.json')):
            with self.subTest(path=relative), self.assertRaises(ValueError):
                compiler.safe_path(self.root, relative)
        self.refresh()
        self.blueprints[0]['reader_question'] = 'Edited after accepted exact pin'
        self.write('design/test_blueprints.json', {'status': 'ACTUAL_VERIFIED_CURRENT_BLUEPRINT_BUNDLE',
            'producer_id': 'blueprint_producer', 'blueprints': self.blueprints})
        self.reject('Stale source')

    def test_markdown_and_csv_native_text_sources_need_no_json_wrapper(self):
        for path, body in [('canon/test_timeline.md', '# TEST ONLY\nSelected test date\n'),
                           ('simulation/test_minutes.csv', 'actor,seconds\nTest,15\n')]:
            (self.root / path).parent.mkdir(parents=True, exist_ok=True)
            (self.root / path).write_text(body, encoding='utf-8')
        self.additional_reviewed_paths = ['canon/test_timeline.md', 'simulation/test_minutes.csv']
        refs = []
        for path in self.additional_reviewed_paths:
            refs.append({**self.ref(path), 'format': 'UTF8_TEXT',
                         'text_locator': {'kind': 'LINE_RANGE', 'start_line': 2, 'end_line': 2}})
        claim = self.blueprints[0]['claims'][0]
        claim.update(test_preserve_native_text_refs=True, source_refs=refs)
        self.refresh()
        compiler.compile_inputs(self.root)
        refs[0]['text_locator']['start_line'] = 0
        self.refresh()
        self.reject('Text locator line range')

    def test_text_source_cannot_launder_selection_or_json_pointer(self):
        path = 'canon/test_plain_selection.md'
        (self.root / path).write_text('selected: true', encoding='utf-8')
        source = compiler.Sources(self.root, {path: compiler.digest(self.root / path)})
        ref = {**self.ref(path), 'format': 'UTF8_TEXT', 'text_locator': {'kind': 'WHOLE_TEXT'}}
        with self.assertRaisesRegex(ValueError, 'must resolve to an object'):
            compiler.selected_record(source.read(ref), 'CALENDAR_AVAILABILITY')
        ref['json_pointer'] = '/selected'
        with self.assertRaisesRegex(ValueError, 'cannot use a JSON pointer'):
            source.read(ref)

    def test_output_preflight_never_partially_writes_before_later_collision(self):
        result = compiler.compile_inputs(self.root)
        output = self.root / compiler.OUT
        output.mkdir(parents=True)
        collision = output / 'EP0020.json'
        collision.write_text('old fixture', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Refusing stale'):
            compiler.write_outputs(self.root, result)
        self.assertEqual([p.name for p in output.iterdir()], ['EP0020.json'])

    def test_temp_only_complete_output_write_and_idempotent_check(self):
        result = compiler.compile_inputs(self.root)
        compiler.write_outputs(self.root, result)
        compiler.write_outputs(self.root, result, check=True)
        compiler.write_outputs(self.root, result)
        self.assertEqual(len(list((self.root / compiler.OUT).glob('*.json'))), 21)
        extra = self.root / compiler.OUT / 'stale.json'
        extra.write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unexpected stale'):
            compiler.write_outputs(self.root, result, check=True)

    def test_partial_io_exception_removes_the_just_created_file(self):
        result = compiler.compile_inputs(self.root)
        original_open = Path.open

        class PartialFailure:
            def __init__(self, handle):
                self.handle = handle

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.handle.close()

            def write(self, content):
                self.handle.write(content[:9])
                raise OSError('Injected partial write')

        def opening(path, mode='r', *args, **kwargs):
            handle = original_open(path, mode, *args, **kwargs)
            if mode == 'xb' and path.name == 'EP0001.json':
                return PartialFailure(handle)
            return handle

        with patch.object(Path, 'open', opening):
            with self.assertRaisesRegex(OSError, 'Injected partial write'):
                compiler.write_outputs(self.root, result)
        self.assertEqual(list((self.root / compiler.OUT).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
