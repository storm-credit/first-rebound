"""Regression: observed baseline must ignore replacement menus and retain family/fatigue."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build_chicago_2020_21_season_connection as sc

class SeasonConnectionRegression(unittest.TestCase):
 def test_baseline_is_independent_of_unselected_replacements(self):
  expected=sc.build()['season_baseline_diagnostics']
  with patch.object(sc,'REPL',{key:'Unknown Replacement' for key in sc.REPL}):
   alternate=sc.build()
  self.assertEqual(expected,alternate['season_baseline_diagnostics'])
  self.assertTrue(any(r['unknown_opponent_coefficients'] for r in alternate['pre_inputs']))

 def test_family_prior_and_fatigue_match_audited_pre_inputs(self):
  data=sc.build();cross=json.loads(sc.POST.read_text())
  for row in data['season_baseline_diagnostics']:
   i=sc.FAT.index(row['fatigue']);pre=[r for r in cross['pre_opponent_held_inputs'] if (r['method'],r['prior'])==(row['method'],row['prior'])]
   post={}
   for r in cross['post_inputs']:
    if (r['method'],r['prior'],r['availability'])==(row['method'],row['prior'],row['availability']):
     post[r['date']]=r['actual_margin']+r['chi_impact']+r['fatigue_deltas'][i]
   self.assertEqual(row['numeric_margin_wins'],sum(r['opponent_held_margin'][i]>0 for r in pre)+sum(v>0 for v in post.values()))
  target=[r for r in data['season_baseline_diagnostics'] if (r['method'],r['prior'],r['availability'])==('RAPTOR_RS_EB','BASE','PORTER_ZERO')]
  self.assertGreater(target[0]['numeric_margin_wins'],target[-1]['numeric_margin_wins'])

 def test_disagreeing_post_branch_baselines_are_rejected(self):
  cross=copy.deepcopy(json.loads(sc.POST.read_text()))
  # Only one of several same-date branches is corrupted; cannot pick first silently.
  rows=[r for r in cross['post_inputs'] if r['opponent']=='MIN' and (r['method'],r['prior'],r['availability'])==('RAPTOR_RS_EB','BASE','PORTER_ZERO')]
  self.assertGreater(len(rows),1);rows[-1]['chi_impact']+=1
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'cross.json';p.write_text(json.dumps(cross))
   with patch.object(sc,'POST',p),self.assertRaises(AssertionError):sc.build()

if __name__=='__main__':unittest.main()
