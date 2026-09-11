"""I acceptance: reason/causation separation and unchanged-model absence stress."""
import copy
import json
import unittest
from datetime import date
import build_chicago_2020_21_causal_availability as i


class CausalAvailabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.minutes=json.loads(i.MINUTES.read_text())
        cls.out=i.build(cls.minutes)
        cls.sources=json.loads(i.SOURCES.read_text())

    def test_priority_partition_and_reason_scope(self):
        self.assertEqual(len(self.out['episodes']),14)
        self.assertEqual(sum(r['priority_row_count'] for r in self.out['episodes']),170)
        self.assertEqual(self.out['rows_with_episode_reason_anchor'],159)
        self.assertEqual(self.out['rows_without_primary_reason'],11)
        self.assertFalse(any(r['causal_onset_and_transferability_verified'] for r in self.out['episodes']))
        terry={r['id']:r for r in self.out['episodes'] if r['player']=='Tyrell Terry'}
        self.assertEqual(terry['TERRY_ASSIGNMENT']['priority_row_count'],14)
        self.assertEqual(terry['TERRY_PERSONAL']['priority_row_count'],27)

    def test_report_page_and_game_date_match_real_schedule(self):
        sources={s['id']:s for s in self.sources['sources']}
        games=i.f.bi.lb.normalized_games()
        self.assertEqual(len(sources),9);self.assertEqual(len(self.sources['facts']),39)
        for fact in self.sources['facts']:
            source=sources[fact['source_id']]
            self.assertTrue(1<=fact['page']<=source['pages'])
            self.assertTrue(source['report_date']<=fact['game_date'])
            self.assertTrue(any(g['date']==fact['game_date'] and fact['historical_team'] in (g['home'],g['away']) for g in games))

    def test_questionable_is_not_definite_absence(self):
        facts={x['id']:x for x in self.sources['facts']}
        self.assertEqual(facts['IR20']['reported_status'],'QUESTIONABLE')
        observations=i.f.bi.cc.read(i.h.OBS)
        actual=next(r for r in observations if r['player']=='LaMelo Ball' and r['date']=='2021-05-01')
        self.assertGreater(int(actual['seconds']),0)
        for fact,gid,team,p in i.STRESS:
            self.assertEqual(facts[fact]['reported_status'],'OUT')
            self.assertEqual(facts[fact]['player'],p)
            self.assertEqual(facts[fact]['game_date'],gid[:10])

    def test_minutes_and_rejected_corrupt_witness(self):
        i.verify_minutes(self.minutes)
        bad=copy.deepcopy(self.minutes)
        row=next(r for r in bad['variants'] if r['variant']['lineup_witness'])
        row['variant']['lineup_witness'][0]['seconds']+=1
        with self.assertRaises(AssertionError):i.verify_minutes(bad)
        self.assertFalse(self.minutes['selected'])
        self.assertFalse(self.out['season_selected'])

    def test_direct_both_team_margin_matches_increment_result(self):
        f=i.f;raw=f.groups();saved=json.loads(f.MINUTES.read_text());maps=f.rating_maps()
        games=f.bi.lb.normalized_games()
        for row in self.out['bounded_stress']:
            variant=next(v['variant'] for v in self.minutes['variants'] if v['variant']['event_id']==row['event_id'])
            game=next(g for g in games if g['id']==row['event_id'])
            total=sum(int(r['pts']) for r in raw[game['id'],game['home']])-sum(int(r['pts']) for r in raw[game['id'],game['away']])
            for team,sign in [(game['home'],1),(game['away'],-1)]:
                b=variant if team==row['team'] else next(b for b in saved['branches'] if b['event_id']==game['id'] and b['team']==team and b['profile'] in ('LOW_MINUTES','OBSERVED_HELD'))
                effect,unknown=f.bi.cc.form(b['delta_seconds'],maps[row['method']],{})
                self.assertFalse(unknown)
                dates=sorted(g['date'] for g in games if team in (g['home'],g['away']));idx=dates.index(game['date'])
                back=idx>0 and (date.fromisoformat(dates[idx])-date.fromisoformat(dates[idx-1])).days==1
                load=sum(max(0,n) for n in b['delta_seconds'].values())/2880 if back else 0
                total+=sign*(effect-.5*load)
            self.assertAlmostEqual(total,row['stress_home_margin_band'][0],places=6)
        self.assertEqual(len(self.out['bounded_stress']),8)
        self.assertFalse(any(r['direction_changed'] for r in self.out['bounded_stress']))

    def test_short_gap_extras_are_solved_jointly(self):
        self.assertEqual(len(self.out['extra_target_date_out_anchors']),3)
        joint=self.out['joint_restriction_case']
        self.assertEqual(set(joint['players']),{'Gary Trent Jr.','Troy Brown Jr.'})
        self.assertEqual(joint['event_id'],'2021-05-01_DAL_WAS')
        proof=json.loads(i.JOINT.read_text())
        i.f.e.d.verify_minutes(proof['branches'],proof['witnesses'])
        self.assertEqual(i.f.e.d.paired_inputs(proof['branches']),proof['paired_inputs'])
        for b in proof['branches']:
            if b['team']=='WAS':self.assertFalse(set(joint['players'])&set(b['alternate_seconds']))
        changes=[r for r in proof['paired_inputs'] if r['conditional_sign']=='AWAY']
        self.assertEqual(len(changes),3)
        self.assertTrue(all(r['profile']=='HIGH_MINUTES' and r['method']=='RAPTOR_RS_EB' for r in changes))

    def test_joint_season_win_transfer_is_conserved(self):
        rows=self.out['joint_season_diagnostics'];self.assertEqual(len(rows),4)
        changed=[r for r in rows if r['team_win_delta']]
        self.assertEqual(len(changed),1)
        self.assertEqual(changed[0]['team_win_delta'],{'DAL':-1,'WAS':1})
        self.assertTrue(all(sum(r['team_wins'].values())==1080 for r in rows))
        self.assertTrue(all(not r['selected'] for r in rows))


if __name__=='__main__':
    unittest.main()
