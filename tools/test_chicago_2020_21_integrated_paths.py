"""Shared uncertainty and missing-impact regression checks for season integration."""
import copy
import json
import unittest
import build_chicago_2020_21_integrated_paths as ip

class IntegratedPathsRegression(unittest.TestCase):
 def test_shared_rating_does_not_allow_impossible_two_wins(self):
  games=[{'date':'first','constant':-1.,'coefficient':1.}, {'date':'second','constant':-1.,'coefficient':-1.}]
  # Independent game extrema permit two wins; one shared rating cannot.
  result=ip.interval_summary(games,-2,2)
  self.assertEqual(result['positive_margin_count_range'],[0,1])
  self.assertEqual([r['positive_margin_games'] for r in result['rating_intervals']],[1,0,1])

 def test_opponent_win_transfer_has_opposite_sign(self):
  games=[{'date':'one','opponent':'A','actual_margin':-2,'constant':2.,'coefficient':0.}, {'date':'two','opponent':'B','actual_margin':3,'constant':1.,'coefficient':0.}]
  row=ip.interval_summary(games,-1,1)['rating_intervals'][0]
  self.assertEqual(row['chicago_win_delta_vs_actual'],1)
  self.assertEqual(row['opponent_win_deltas_from_chicago_games'],{'A':-1})

 def test_exact_zero_is_an_unresolved_boundary(self):
  result=ip.interval_summary([{'date':'only','constant':0.,'coefficient':1.}],-1,1)
  self.assertEqual(result['zero_margin_boundaries'],[{'rating':0.0,'unresolved_dates':['only']}])

 def test_unknown_player_crossing_zero_cannot_be_counted_as_fixed_sign(self):
  data=json.loads(ip.OUT.read_text());cross=copy.deepcopy(json.loads(ip.cc.OUT.read_text()));close=json.loads(ip.close.OUT.read_text())
  candidates=[r for r in cross['post_inputs'] if r['opponent']=='ORL' and r['method']=='BPM_MAR25_EB' and r['prior']=='BASE']
  self.assertTrue(candidates)
  for row in candidates:row['margin_constant']=0
  with self.assertRaises(AssertionError):
   ip.season_games(data['remaining_pre_paired_inputs'],cross,close,'LOW_MINUTES','RIVAL_28','FOURNIER_PATH_RETAINED','PORTER_ZERO','BPM_MAR25_EB','BASE',0)

if __name__=='__main__':unittest.main()
