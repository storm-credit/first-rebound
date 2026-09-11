import copy
import json
import unittest
from collections import Counter

import build_chicago_2020_21_availability_policy as j


class PolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.minutes=json.loads(j.MINUTES.read_text())
        cls.data=json.loads(j.OUT.read_text())

    def test_terry_all_dates_and_source_controls(self):
        _,_,branches,_,_=j.load()
        rr=[r for r in self.minutes['records'] if r['policy']=='J1_TERRY_LEAVE']
        self.assertEqual(len(rr),54)
        self.assertEqual(len({r['variant']['event_id'] for r in rr}),27)
        self.assertEqual(Counter(r['source']['stage'] for r in rr),{'F':46,'B':4,'CHI_POST':4})
        for r in self.minutes['records']:
            b=r['variant'];old=r['control']
            self.assertEqual(old,branches[b['event_id'],b['team'],b['profile']])
            if r['policy']=='J1_TERRY_LEAVE':self.assertEqual(old['alternate_seconds']['Tyrell Terry'],360)

    def test_witnesses_and_tamper_rejected(self):
        j.verify_minutes(self.minutes)
        data=copy.deepcopy(self.minutes)
        b=next(r['variant'] for r in data['records'] if r['variant']['status']!='CAPACITY_HOLD')
        b['lineup_witness'][0]['seconds']+=1
        with self.assertRaises(AssertionError):j.verify_minutes(data)

    def test_no_removed_player_or_new_target_boost(self):
        for r in self.minutes['records']:
            b=r['variant'];old=r['control']['alternate_seconds']
            if b['status']=='CAPACITY_HOLD':continue
            self.assertFalse(set(b['absent_players'])&set(b['alternate_seconds']))
            for p in b['newcomers']:self.assertAlmostEqual(b['alternate_seconds'].get(p,0),old.get(p,0))
            gained=sum(max(0,n-old.get(p,0)) for p,n in b['alternate_seconds'].items())
            self.assertAlmostEqual(gained,sum(old.get(p,0) for p in b['absent_players']),places=5)

    def test_capacity_certificates_and_no_full_result_fill(self):
        failed=[r['variant'] for r in self.minutes['records'] if r['variant']['status']=='CAPACITY_HOLD']
        self.assertEqual(len(failed),11)
        self.assertEqual(len({b['event_id'] for b in failed}),6)
        for b in failed:
            c=b['capacity_certificate']
            self.assertTrue(c['role_shortfalls_seconds'] or c['total_shortfall_seconds']>0)
        for r in self.data['season_diagnostics']:
            if r['policy']=='J2_LEAVE_NO_FOLLOWUPS':
                self.assertIsNone(r['team_wins']);self.assertIsNone(r['seeds']);self.assertTrue(r['unresolved_game_ids'])

    def test_two_team_changes_use_one_control(self):
        rr=[r for r in self.data['impacts'] if len(r['team_effects'])==2]
        self.assertEqual(len({r['event_id'] for r in rr}),3)
        for r in rr:
            self.assertEqual(len({x['team'] for x in r['team_effects']}),2)
            if r['status']=='CAPACITY_HOLD':continue
            c0=r['team_effects'][0]['control_home_margin_constant']
            expected=c0+sum(x['home_margin_constant']-x['control_home_margin_constant'] for x in r['team_effects'])
            self.assertAlmostEqual(r['home_margin_constant'],expected)

    def test_complete_seasons_and_scope(self):
        self.assertFalse(self.data['season_selected']);self.assertFalse(self.data['manuscript_allowed'])
        complete=[r for r in self.data['season_diagnostics'] if r['status']=='FULL_CONDITIONAL_SCHEDULE']
        self.assertEqual(len(complete),16)
        actual=j.bi.lb.normalized_games()
        for r in complete:
            self.assertEqual(sum(r['team_wins'].values()),1080)
            self.assertEqual(r['team_win_delta'],{});self.assertEqual(r['flips'],[])
            changed=set(r['changed_game_ids'])
            games=[{**g,'winner':(g['away'] if g['winner']==g['home'] else g['home']) if g['id'] in changed else g['winner']} for g in actual]
            self.assertEqual(j.bi.lb.record_wins(games),r['team_wins'])
            self.assertEqual(j.f.e.d.ps.order(games),r['seeds'])

    def test_chicago_winter_not_double_counted_or_approved(self):
        rows=self.data['chicago_winter_existing_zero_minutes']
        self.assertEqual(Counter(r['episode'] for r in rows),{'CARTER_WINTER':11,'PORTER_BACK':15})
        self.assertTrue(all(r['actual_seconds']==r['alternate_seconds']==0 for r in rows))
        self.assertFalse(self.data['recommendation_is_author_approval'])
        self.assertFalse(self.data['new_contract_or_medical_facts'])

    def test_impact_rebuild_and_upstream_hashes(self):
        self.assertEqual(j.impact_records(self.minutes),self.data['impacts'])
        for name,digest in self.data['source_sha256'].items():
            candidates=[j.S/name,j.S.parent/'research'/name,j.S.parent/'canon'/name,j.S.parent/'tools'/name]
            p=next(p for p in candidates if p.exists())
            self.assertEqual(j.cc.sha(p),digest)


if __name__=='__main__':unittest.main()
