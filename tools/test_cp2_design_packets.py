import copy
import unittest
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

    def test_no_skipped_year_or_pretended_episode_completion(self):
        self.c['seasons'].pop(6)
        self.a['planned_episode_outlines_completed'] = 780
        errors = self.errors()
        self.assertIn('career season continuity', errors)
        self.assertIn('slots cannot become finished episode outlines', errors)


if __name__ == '__main__':
    unittest.main()
