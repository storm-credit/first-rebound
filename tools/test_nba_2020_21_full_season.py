"""F acceptance tests: scope, constrained roles, full joint paths and honest holds."""
import copy
import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path
import build_nba_2020_21_full_season as f


class FullSeasonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.minutes=json.loads(f.MINUTES.read_text());cls.out=json.loads(f.OUT.read_text())
        cls.previous=json.loads(f.e.OUT.read_text());cls.raw=f.groups()
        cls.inputs=f.paired_inputs(cls.minutes)
        cls.env=f.bi.cc.envelopes(f.rating_maps())

    def test_source_scope_closes859_without_overlap(self):
        meta=json.loads(f.META.read_text());rows=f.bi.cc.read(f.OBS)
        ids={r['event_id'] for r in rows}
        self.assertEqual(len(ids),859);self.assertEqual(len(rows),22873)
        self.assertEqual(len(self.raw),1718)
        self.assertEqual(f.bi.cc.sha(f.OBS),meta['snapshot_sha256'])
        allgames={g['id'] for g in f.bi.lb.normalized_games()}
        old={g['id'] for g in f.bi.lb.normalized_games() if 'CHI' in (g['home'],g['away'])}
        for p in (f.bi.OUT,f.e.d.OUT,f.e.OUT):
            stage={r['event_id'] for r in json.loads(p.read_text())['game_summary']}
            self.assertFalse(stage&old);old|=stage
        self.assertFalse(ids&old);self.assertEqual(ids|old,allgames)
        self.assertEqual(self.out['uncomputed_game_count'],0)

    def test_all_minute_constraints_and_corrupt_witness(self):
        f.verify_minutes(self.minutes)
        corrupted=copy.deepcopy(self.minutes)
        b=next(b for b in corrupted['branches'] if b['changed'])
        b['lineup_witness'][0]['seconds']+=1
        with self.assertRaises(AssertionError):f.verify_minutes(corrupted)
        for b in self.minutes['branches']:
            bad={r['player'] for r in self.raw[b['event_id'],b['team']]
                 if int(r['seconds'])==0 and r['comment']!="DNP - Coach's Decision"}-set(b['newcomers'])
            self.assertFalse(bad&set(b['alternate_seconds']))
            if (b['event_id'],b['team']) in f.THREE_SECOND_RESIDUES:
                self.assertEqual(b['clock_correction']['seconds'],-3)

    def test_role_fallback_is_explicit_and_score_blind(self):
        rows=self.raw['2021-02-04_PHI_POR','POR']
        before=f.allocate(rows,'LOW_MINUTES',None)
        self.assertEqual(before['status'],'CAPACITY_HOLD')
        after=f.allocate(rows,'LOW_MINUTES',None,True)
        self.assertEqual(after['status'],'CONDITIONAL_CAPACITY_PASS')
        self.assertEqual(after['minute_bounds_seconds'],before['minute_bounds_seconds'])
        perturbed=copy.deepcopy(rows)
        for r in perturbed:r['pts']='999';r['plus_minus']='-999'
        self.assertEqual(after,f.allocate(perturbed,'LOW_MINUTES',None,True))
        emergency=[b for b in self.minutes['branches'] if b['role_tier']!='BASE']
        self.assertEqual(len({b['event_id'] for b in emergency}),7)
        self.assertTrue(all(b['base_policy_failure']['status']=='CAPACITY_HOLD' for b in emergency))

    def test_paired_inputs_keep_missing_ratings_symbolic(self):
        self.assertEqual(len(self.inputs),11748)
        missing={p for r in self.inputs for p in r['unknown_coefficients']}
        self.assertEqual(missing,{'Fictional Rival','Grant Riller','Donta Hall'})
        for r in self.inputs:
            self.assertEqual(r['home_margin_constant'],-r['away_margin_constant'])
            self.assertEqual(r['home_margin_band'],f.bi.cc.band(r['home_margin_constant'],r['unknown_coefficients'],self.env[r['method']]))
            self.assertFalse(r['selected'])

    def test_joint_intervals_tile_all564_upstream_conditions(self):
        grouped=defaultdict(list)
        for r in self.out['season_bridge']:grouped[r['source_bridge_index']].append(r)
        self.assertEqual(set(grouped),set(range(len(self.previous['season_bridge']))))
        for i,rows in grouped.items():
            source=self.previous['season_bridge'][i];rows.sort(key=lambda r:r['shared_rival_rating_open_interval'])
            self.assertEqual(rows[0]['shared_rival_rating_open_interval'][0],source['shared_rival_rating_open_interval'][0])
            self.assertEqual(rows[-1]['shared_rival_rating_open_interval'][1],source['shared_rival_rating_open_interval'][1])
            for a,b in zip(rows,rows[1:]):self.assertAlmostEqual(a['shared_rival_rating_open_interval'][1],b['shared_rival_rating_open_interval'][0])
            for r in rows:
                self.assertEqual(r['source_condition'],source['source_condition'])
                self.assertTrue(r['zero_boundaries_unresolved'])
                self.assertFalse(r['unresolved_games'])

    def test_all1080_winners_use_one_rival_rating(self):
        actual=f.bi.lb.normalized_games();lookup=defaultdict(list)
        for r in self.inputs:lookup[r['profile'],r['method'],r['fatigue']].append(r)
        for row in self.out['season_bridge']:
            source=self.previous['season_bridge'][row['source_bridge_index']]
            c=row['source_condition'];profile,rival,_=c['path_id'].split('/');rival=int(rival.split('_')[1])
            inputs={r['event_id']:r for r in lookup[profile,c['method'],c['fatigue']] if r['rival_minutes'] in (None,rival)}
            self.assertEqual(len(inputs),859)
            lo,hi=row['shared_rival_rating_open_interval'];rating=(lo+hi)/2
            old=set(source['changed_game_ids']);changed=set(row['changed_game_ids']);wins=Counter()
            for g in actual:
                winner=f.bi.lb.changed_game(g)['winner'] if g['id'] in old else g['winner']
                if g['id'] in inputs:
                    band=f.conditional_band(inputs[g['id']],rating,self.env[c['method']])
                    self.assertTrue(band[0]>0 or band[1]<0)
                    winner=g['home'] if band[0]>0 else g['away']
                self.assertEqual(winner!=g['winner'],g['id'] in changed)
                wins[winner]+=1
            self.assertEqual(dict(wins),row['team_wins']);self.assertEqual(sum(wins.values()),1080)
            self.assertEqual(wins['CHI'],source['team_wins']['CHI'])

    def test_league_identity_and_postseason_are_not_probabilities(self):
        seen=set();covered=[]
        for c in self.out['league_cases']:
            identity=tuple(c['changed_game_ids']);self.assertNotIn(identity,seen);seen.add(identity)
            covered+=c['bridge_indices']
            self.assertEqual(c['joint_playin_outcome_count'],64)
            self.assertEqual(c['possible_distinct_lottery_fields'],25)
            self.assertFalse(c['selected']);self.assertIsNone(c['later_tie_hold'])
            for i in c['bridge_indices']:self.assertEqual(self.out['season_bridge'][i]['changed_game_ids'],c['changed_game_ids'])
        self.assertEqual(sorted(covered),list(range(len(self.out['season_bridge']))))
        self.assertEqual(sum(g['both_observed_held'] for g in self.out['game_summary']),422)
        self.assertFalse(self.out['manuscript_allowed'])

    def test_role_stress_and_selection_board_preserve_open_choices(self):
        stress=self.out['emergency_role_stress']
        self.assertFalse(stress['coefficient_selected'])
        self.assertTrue(any(r['differs_from_zero_role_cost'] for r in stress['rows'] if r['role_penalty_per48_minutes']==6))
        self.assertFalse(any(r['differs_from_zero_role_cost'] for r in stress['rows'] if r['role_penalty_per48_minutes']<=3))
        board=f.selection_board(self.out);covered=[]
        for family in board['policy_families']:
            covered+=family['bridge_indices'];self.assertFalse(family['selected'])
        self.assertEqual(sorted(covered),list(range(len(self.out['season_bridge']))))
        self.assertEqual([x['id'] for x in board['execution_conditions']],[f'EX{i:02d}' for i in range(1,9)])
        for r in self.out['season_bridge']:
            if r['team_wins']['CHI']==33:self.assertEqual(r['source_condition']['fatigue'],0)

    def test_provenance_tracks_current_artifacts(self):
        self.assertEqual(self.minutes['observation_sha256'],f.bi.cc.sha(f.OBS))
        self.assertEqual(self.minutes['script_sha256'],f.bi.cc.sha(Path(f.__file__)))
        for name,h in self.out['source_sha256'].items():
            p=Path(f.__file__) if name==Path(f.__file__).name else f.S/name
            self.assertEqual(f.bi.cc.sha(p),h)


if __name__=='__main__':unittest.main()
