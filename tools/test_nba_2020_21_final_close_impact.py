"""Contract tests for E's new source scope and joint, not independent, rival paths."""
import copy
import json
import unittest
from collections import Counter, defaultdict
import build_nba_2020_21_final_close_impact as e


class FinalCloseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j=json.loads(e.OUT.read_text())
        cls.previous=json.loads(e.d.OUT.read_text())

    def test_scope_source_hashes_and_policy_join(self):
        q=e.bi.cc.read(e.queue.QUEUE);teams=e.bi.cc.read(e.queue.TEAM_QUEUE)
        obs=e.bi.cc.read(e.OBS);meta=json.loads(e.queue.META.read_text())
        ids={r['event_id'] for r in q};done={r['event_id'] for r in self.j['game_summary']}
        self.assertEqual(len(ids),939);self.assertEqual(len(teams),1878)
        self.assertEqual(Counter(r['event_id'] for r in teams),Counter({gid:2 for gid in ids}))
        self.assertEqual(sum(int(r['observation_rows']) for r in teams),25042)
        self.assertEqual(e.bi.cc.sha(e.OBS),meta['snapshot_sha256'])
        self.assertEqual(e.bi.cc.sha(e.queue.TEAM_QUEUE),meta['team_queue_sha256'])
        self.assertEqual(done,{r['event_id'] for r in q if int(r['actual_margin'])<=3})
        self.assertEqual(len(done),80);self.assertEqual(len(obs),2169)
        self.assertFalse(done & {r['event_id'] for r in self.previous['game_summary']})
        self.assertFalse(done & {r['event_id'] for r in json.loads(e.bi.OUT.read_text())['game_summary']})
        pending=e.pending(self.j)
        self.assertEqual(len(pending),859);self.assertEqual(done|{r['event_id'] for r in pending},ids)
        for r in teams:
            p=e.queue.policy(r['team'],r['date'])
            self.assertEqual(r['policy_id'],p['policy_id'])
            self.assertEqual(r['execution_conditions'],p['execution_conditions'])

    def test_rescreen_witnesses_are_hypothetical_and_reproducible(self):
        screen=json.loads(e.queue.OUT.read_text());actual=e.bi.lb.normalized_games()
        self.assertEqual(screen['single_flip_trials'],6573)
        cases={r['id']:r for r in self.previous['league_cases']}
        for s in screen['cases']:
            prior=cases[s['id']];changed=set(prior['changed_game_ids'])
            for label,w in s['witnesses'].items():
                if label=='later_tie':continue
                games=[e.bi.lb.changed_game(g) if g['id'] in changed or g['id']==w['event_id'] else dict(g) for g in actual]
                self.assertEqual(e.d.ps.order(games),w['seeds'])
                self.assertFalse(w['selected'])
        self.assertFalse(screen['manuscript_allowed'])

    def test_lineups_clocks_health_and_corrupt_witness(self):
        j=self.j;e.verify_minutes(j['branches'],j['lineup_witnesses'])
        altered=copy.deepcopy(j['lineup_witnesses']);idx=next(i for i,w in enumerate(altered) if w)
        altered[idx][0]['seconds']+=1
        with self.assertRaises(AssertionError):e.verify_minutes(j['branches'],altered)
        clock=next(b for b in j['branches'] if (b['event_id'],b['team'])==('2021-02-10_PHX_MIL','MIL'))
        self.assertEqual(clock['clock_correction']['raw_total_seconds'],14403)
        self.assertEqual(clock['clock_correction']['seconds'],-3)
        for b in j['branches']:
            if b['team']=='MIN':
                # Regression: a narrow role map formerly added15-20 center minutes.
                self.assertLessEqual(max((n for p,n in b['delta_seconds'].items()
                    if p in j['roles']['MIN']['center']),default=0),180)
            if b['team']=='ORL' and b['date']=='2021-05-01':
                self.assertNotIn('Chuma Okeke',b['alternate_seconds'])
                self.assertNotIn('Terrence Ross',b['alternate_seconds'])
                self.assertNotIn('James Ennis III',b['alternate_seconds'])
            if b['team']=='DET' and b['date']=='2021-03-26':
                self.assertIn('Kira Lewis Jr.',b['starters'])
                self.assertNotIn('Rodney McGruder',b['starters'])

    def test_joint_rating_partitions_cover_each_upstream_interval(self):
        grouped=defaultdict(list)
        for row in self.j['season_bridge']:grouped[row['source_bridge_index']].append(row)
        self.assertEqual(set(grouped),set(range(72)))
        for ix,rows in grouped.items():
            source=self.previous['season_bridge'][ix];rows.sort(key=lambda r:r['shared_rival_rating_open_interval'])
            self.assertEqual(rows[0]['shared_rival_rating_open_interval'][0],source['shared_rival_rating_open_interval'][0])
            self.assertEqual(rows[-1]['shared_rival_rating_open_interval'][1],source['shared_rival_rating_open_interval'][1])
            for left,right in zip(rows,rows[1:]):
                self.assertAlmostEqual(left['shared_rival_rating_open_interval'][1],right['shared_rival_rating_open_interval'][0])
            for row in rows:
                self.assertEqual(row['source_condition'],source['source_condition'])
                self.assertEqual(row['team_wins']['CHI'],source['team_wins']['CHI'])
                self.assertEqual(sum(row['team_wins'].values()),1080)
                self.assertEqual(sum(row['win_deltas_vs_D'].values()),0)
                self.assertEqual(row['other_games_held'],859)
                self.assertFalse(row['selected'])

    def test_interval_results_use_one_rating_across_all_new_games(self):
        actual={g['id']:g for g in e.bi.lb.normalized_games()}
        self.assertEqual(len(self.j['paired_inputs']),1176)
        for row in self.j['season_bridge']:
            c=row['source_condition'];profile,rival,_=c['path_id'].split('/');rival=int(rival.split('_')[1])
            lo,hi=row['shared_rival_rating_open_interval'];rating=(lo+hi)/2
            chosen=[x for x in self.j['paired_inputs'] if (x['profile'],x['method'],x['fatigue'])==(profile,c['method'],c['fatigue']) and x['rival_minutes'] in (None,rival)]
            self.assertEqual(len(chosen),80)
            changed=set(row['changed_game_ids'])
            for x in chosen:
                self.assertTrue(set(x['unknown_coefficients'])<={e.RIVAL})
                value=x['home_margin_constant']+x['unknown_coefficients'].get(e.RIVAL,0)*rating
                g=actual[x['event_id']];winner=g['home'] if value>0 else g['away']
                self.assertEqual(winner!=g['winner'],x['event_id'] in changed)
                self.assertAlmostEqual(x['home_margin_constant'],-x['away_margin_constant'])

    def test_league_cases_do_not_turn_combinations_into_probabilities(self):
        self.assertFalse(self.j['selected']);self.assertFalse(self.j['manuscript_allowed'])
        seen=set()
        for case in self.j['league_cases']:
            self.assertFalse(case['selected'])
            key=tuple(case['changed_game_ids']);self.assertNotIn(key,seen);seen.add(key)
            self.assertEqual(case['possible_distinct_lottery_fields'],25)
            self.assertEqual(case['joint_playin_outcome_count'],64)
            for i in case['bridge_indices']:
                self.assertEqual(self.j['season_bridge'][i]['changed_game_ids'],case['changed_game_ids'])
        # Retained directions include49 observed-held games; distinguish them.
        retained=[g for g in self.j['game_summary'] if g['status']=='ALL_TESTED_RETAIN']
        self.assertEqual(sum(g['both_observed_held'] for g in retained),49)


if __name__=='__main__':unittest.main()
