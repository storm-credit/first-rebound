"""H acceptance: approval scope, provenance and non-inference from absent rows."""
import json
import unittest
from collections import Counter
import build_chicago_2020_21_availability_reconciliation as h


class ReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out,cls.rows=h.build()

    def test_author_acceptance_does_not_select_health_or_a_metric(self):
        approval=json.loads(h.APPROVAL.read_text())
        self.assertEqual(set(approval['approved']),{'R1','T1','T2','T3','T4'})
        self.assertEqual(approval['approved']['R1']['initial_role_target_minutes'],28)
        self.assertFalse(approval['season_selected'])
        self.assertFalse(approval['manuscript_allowed'])
        self.assertTrue(self.out['candidate_rating_and_method_not_author_locked'])
        self.assertFalse(json.loads(h.g.OUT.read_text())['selected'])

    def test_source_identity_and_saved_calendar_reconstruction(self):
        meta=json.loads(h.META.read_text());source=h.g.f.bi.cc.read(h.OBS)
        self.assertEqual(h.g.f.bi.cc.sha(h.OBS),meta['snapshot_sha256'])
        self.assertEqual(len(source),924)
        self.assertEqual(len({(r['person_id'],r['game_id']) for r in source}),924)
        self.assertEqual(len({r['person_id'] for r in source}),16)
        self.assertEqual(h.g.f.bi.cc.read(h.CAL),[{k:str(v) for k,v in r.items()} for r in self.rows])
        self.assertEqual(self.out['upstream_full_season_sha256'],h.g.f.bi.cc.sha(h.g.f.OUT))

    def test_different_schedule_is_not_an_absence(self):
        edwards=[r for r in self.rows if r['player']=='Anthony Edwards']
        self.assertEqual(len(edwards),72)
        self.assertEqual(Counter(r['historical_evidence'] for r in edwards),
                         {'SAME_DAY_PLAYED':43,'NO_SAME_DAY_ROW':29})
        self.assertTrue(all(r['alternate_availability']=='NOT_SELECTED' for r in edwards))
        self.assertTrue(all(r['priority']=='NO_AUTOMATIC_HEALTH_INFERENCE' for r in edwards))
        self.assertEqual(h.status({'seconds':0,'comment':"DNP - Coach's Decision"}),'SAME_DAY_COACH_DNP')
        self.assertEqual(h.status({'seconds':0,'comment':''}),'SAME_DAY_OTHER_ZERO')
        self.assertEqual(h.status({'seconds':0,'comment':'NWT - Injury/Illness'}),'SAME_DAY_RESTRICTED')

    def test_open_ended_gaps_are_not_silently_dropped(self):
        p=Counter(r['priority'] for r in self.out['priority_queue'])
        self.assertEqual(p,{'LONG_OBSERVATION_GAP_REVIEW':111,
            'OPEN_ENDED_OBSERVATION_GAP_REVIEW':50,'RESTRICTED_SOURCE_REVIEW':9})
        tail=[r for r in self.rows if r['player']=='Tyrell Terry' and r['priority']=='OPEN_ENDED_OBSERVATION_GAP_REVIEW']
        self.assertEqual(len(tail),27)
        self.assertTrue(all(not r['next_source_date'] and not r['source_game_id'] for r in tail))
        self.assertEqual(len(self.out['priority_game_ids']),147)

    def test_watch_rows_and_targets_have_distinct_scope(self):
        self.assertEqual(self.out['scope_counts'],{'CHI_WATCH_ONLY':288,'NEW_TEAM_TARGET':791})
        self.assertEqual(len({(r['scope'],r['event_id'],r['team'],r['player']) for r in self.rows}),1079)
        fictional=[r for r in self.rows if r['historical_evidence']=='FICTIONAL_NO_OBSERVATIONS']
        self.assertEqual(len(fictional),144)
        self.assertTrue(all(not r['source_game_id'] for r in fictional))
        self.assertFalse(self.out['contract_facts']['new_exact_salary_or_pick_terms_recovered'])
        self.assertTrue(all(r['alternate_availability']=='NOT_SELECTED' for r in self.rows))


if __name__=='__main__':
    unittest.main()
