import copy
import tempfile
import unittest
from pathlib import Path
import build_cp2_design_packets as m


class DesignBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.a, self.c, self.p = [m.load(p) for p in [m.STRUCTURE, m.CAREER, m.PROMISES]]

    def errors(self):
        return m.validate_design(self.a, self.c, self.p)

    def test_cross_document_packet(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(m.validate_samples(m.load(m.PACKS)), [])

    def test_allocation_and_parent_corruption(self):
        self.a['acts'][6]['NBA_content_allocation']['regular'] += 1
        self.a['subacts'][8]['parent_act'] = 'NO_ACT'
        errors = self.errors()
        self.assertTrue(any('allocation mismatch' in e for e in errors))
        self.assertTrue(any('unknown parent' in e for e in errors))

    def test_proposals_cannot_become_approved_results(self):
        self.c['seasons'][9]['awards'] = ['MVP']
        self.c['author_locked'] = True
        self.c['rival_lifetime_one_club_author_locked'] = True
        errors = self.errors()
        self.assertTrue(any('promoted into results' in e for e in errors))
        self.assertTrue(any('promotion forbidden' in e for e in errors))
        self.assertTrue(any('lifetime team' in e for e in errors))

    def test_receiving_teammate_must_have_prior_acts(self):
        rel = next(x for x in self.p['promises'] if x['id'] == 'P3')
        rel['variations'] = ['A06-S2', 'A06-S3']
        self.assertIn('final receiver: fewer than three prior Acts', self.errors())
        rel['payoff'] = 'A99-S1'
        self.assertTrue(any('dangling' in e for e in self.errors()))

    def test_stale_source_is_not_silently_refreshed(self):
        samples = copy.deepcopy(m.load(m.PACKS))
        p = samples['samples'][0]
        p['source_content_sha256']['canon/CAREER_TIMELINE.md'] = '0' * 64
        errors = m.validate_samples(samples)
        self.assertTrue(any('STALE canon/CAREER_TIMELINE.md' in e for e in errors))

    def test_sample_body_and_author_lock_cannot_be_changed_under_valid_source_hashes(self):
        samples = m.make_samples()
        samples['samples'][0]['allowed_facts'] = ['unverified championship']
        samples['samples'][0]['author_locked'] = True
        samples['author_locked'] = True
        errors = m.validate_samples(samples)
        self.assertTrue(any('content differs' in e for e in errors))
        self.assertTrue(any('purpose or author lock' in e for e in errors))
        self.assertTrue(any('sample promoted' in e for e in errors))

    def test_duplicate_source_link_is_not_hidden_by_set_comparison(self):
        samples = m.make_samples()
        samples['samples'][0]['source_links'].append(samples['samples'][0]['source_links'][0])
        self.assertTrue(any('duplicate source link' in e for e in m.validate_samples(samples)))

    def test_claim_without_pinned_source_is_rejected(self):
        samples = m.make_samples()
        samples['samples'][0]['fact_evidence'][0]['source_paths'] = ['missing/source.json']
        self.assertTrue(any('claim source not hash-pinned' in e for e in m.validate_samples(samples)))

    def test_conditional_claim_cannot_be_promoted_to_fact(self):
        samples = m.make_samples()
        samples['samples'][0]['fact_evidence'][2]['status'] = 'FACT'
        self.assertTrue(any('invalid or promoted claim status' in e for e in m.validate_samples(samples)))

    def test_source_hash_ignores_only_checkout_line_endings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'sample.md'
            path.write_bytes(b'alpha\nsecond\n')
            expected = m.sha('sample.md', root)
            path.write_bytes(b'alpha\r\nsecond\r\n')
            self.assertEqual(m.sha('sample.md', root), expected)
            path.write_bytes(b'alpha\r\nchanged\r\n')
            self.assertNotEqual(m.sha('sample.md', root), expected)

    def test_no_skipped_year_or_pretended_episode_completion(self):
        self.c['seasons'].pop(6)
        self.a['planned_episode_outlines_completed'] = 780
        errors = self.errors()
        self.assertIn('career season continuity', errors)
        self.assertIn('slots cannot become finished episode outlines', errors)

    def test_planned_slots_cannot_replace_verified_final_functions(self):
        self.a['final_episode_functions_completed'] = self.a['total_planned_units']
        self.assertIn('final function count differs from verified assignments', self.errors())

    def test_duplicate_final_function_cannot_consume_two_slots(self):
        self.a['final_episode_function_paths'] *= 2
        self.a['final_episode_functions_completed'] = 2
        errors = self.errors()
        self.assertIn('duplicate final function path', errors)
        self.assertIn('final function allocation/order collision', errors)

    def test_review_loaded_claims_cannot_become_character_knowledge(self):
        sample = m.make_samples()['samples'][0]
        sample['information_boundary']['story_known_claim_indexes'] = [0]
        self.assertTrue(any('in-world input' in e for e in m.validate_information_boundary(sample)))

    def test_unapproved_pov_or_exact_date_is_rejected(self):
        sample = m.make_samples()['samples'][1]
        sample['information_boundary']['pov_author_locked'] = True
        sample['information_boundary']['exact_scene_date'] = '2028-06-01'
        self.assertTrue(m.validate_information_boundary(sample))

    def test_past_observation_clock_blocks_future_knowledge(self):
        witness = dict(claim_kind='PAST_OBSERVED_EVENT', event_on='1900-01-02',
                       acquired_on='1900-01-03', segment_on='1900-01-04',
                       access_route='PUBLIC_RECORD', holder_id='TEST_ONLY',
                       source_path='TEST_ONLY', source_verified=True)
        self.assertEqual(m.assess_observed_access(witness),
                         'SUPPLIED_CLOCK_REPRODUCTION_PASS_NOT_NARRATIVE_CLEARANCE')
        witness['segment_on'] = '1900-01-01'
        self.assertEqual(m.assess_observed_access(witness), 'FAIL')
        witness['segment_on'] = '1900-01-04'
        witness['event_on'] = '1900-01-05'
        self.assertEqual(m.assess_observed_access(witness), 'FAIL')

    def test_unknown_date_or_unverified_route_is_not_clock_pass(self):
        witness = dict(claim_kind='PAST_OBSERVED_EVENT', event_on=None,
                       acquired_on='1900-01-03', segment_on='1900-01-04')
        self.assertEqual(m.assess_observed_access(witness), 'HOLD')
        witness['event_on'] = 'invalid'
        self.assertEqual(m.assess_observed_access(witness), 'HOLD')
        witness.update(event_on='1900-01-02', access_route='PUBLIC_RECORD',
                       holder_id='TEST_ONLY', source_path='TEST_ONLY', source_verified=False)
        self.assertEqual(m.assess_observed_access(witness), 'HOLD')
        witness.update(source_verified=True, claim_kind='FUTURE_PLAN')
        self.assertEqual(m.assess_observed_access(witness), 'HOLD')


if __name__ == '__main__':
    unittest.main()
