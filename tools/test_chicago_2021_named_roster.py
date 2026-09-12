import unittest
import build_chicago_2021_named_roster as m


class NamedRosterTests(unittest.TestCase):
    def test_taken_prospect_never_reassigned(self):
        self.assertEqual(m.choose_remaining(['Moody','Duarte'],['Moody']),'Duarte')
        self.assertIsNone(m.choose_remaining(['Moody','Duarte'],['Moody','Duarte']))

    def test_replacement_removes_reserve_and_rejects_duplicate(self):
        self.assertEqual(m.replace_slots({'reserve':2000000,'core':10},{'reserve':'center'},{'center':1789256}),{'core':10,'center':1789256})
        with self.assertRaises(ValueError):
            m.replace_slots({'r1':1,'r2':1},{'r1':'same','r2':'same'},{'same':1})

    def test_space_does_not_create_exception(self):
        x=m.build();e=x['exception_counterexample']
        self.assertGreater(x['centers']['Gorgui Dieng']['min_conditional_apron_gap'],0)
        self.assertFalse(e['remaining_NTMLE_sufficient'])
        self.assertFalse(e['BAE_sufficient'])
        self.assertFalse(e['exceptions_may_be_added_together'])

    def test_named_budget_preserves_provisional_and_slot_boundaries(self):
        x=m.build()
        self.assertEqual(x['named_standard_slots'],15)
        self.assertEqual(sum(sum(v.values()) for v in x['primary_healthy_position_budget'].values()),240)
        for a in x['availability'].values():
            self.assertIsNone(a['selected_player'])
        self.assertFalse(x['actual_contracts_agreed'])
        self.assertFalse(x['draft_players_selected'])
        self.assertFalse(x['author_locked'])
        self.assertEqual(x['centers']['Tony Bradley']['max_budget'],x['parent_G1A_max_budget']+x['gross_budget_delta_from_G1A'])

    def test_hold_sequence_and_draft_rookie_class_are_explicit(self):
        x=m.build()
        self.assertTrue(all(c['additional_real_amount_still_required']==0 for c in x['valentine_hold_sequence']))
        self.assertTrue(all(not c['exact_sequence_executed'] for c in x['valentine_hold_sequence']))
        r=x['rookie39_classification']
        self.assertFalse(r['is_rookie_free_agent'])
        self.assertEqual(r['FA_counterexample_extra'],743920)
        self.assertFalse(r['counterexample_selected'])


if __name__=='__main__':unittest.main()
