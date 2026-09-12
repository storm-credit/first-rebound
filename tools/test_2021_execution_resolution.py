import json
import unittest
from build_2021_execution_resolution import SOURCE, build, funding, gordon_after_first_delivery, mcgee_second


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.s = json.loads(SOURCE.read_text())

    def test_gordon_protection_and_terminal(self):
        t = self.s['gordon']
        self.assertEqual(gordon_after_first_delivery(2023,{2025:6},t)['asset']['year'],2025)
        self.assertEqual(gordon_after_first_delivery(2023,{2025:5,2026:5,2027:5},t)['status'],'CONDITIONAL_REPORTED_EXTINCTION')
        self.assertEqual(gordon_after_first_delivery(2025,{2027:6},t)['asset']['year'],2027)

    def test_dependency_cannot_use_future_or_conversion_as_delivery(self):
        t=self.s['gordon']
        self.assertEqual(gordon_after_first_delivery(2024,{2025:30},t)['status'],'WAIT_FOR_OUTCOME')
        self.assertEqual(gordon_after_first_delivery(None,{2027:30},t)['status'],'PREDECESSOR_LINK_UNRESOLVED')
        with self.assertRaises(ValueError): gordon_after_first_delivery(2026,{},t)

    def test_second_round_boundary_does_not_invent_rollover(self):
        t=self.s['mcgee']
        self.assertEqual(mcgee_second(2023,46,t)['status'],'PROTECTED_TERMINAL_UNRESOLVED')
        self.assertEqual(mcgee_second(2023,47,t)['asset']['pick'],47)
        self.assertEqual(mcgee_second(2027,31,t)['asset']['pick'],31)
        self.assertEqual(mcgee_second(2027,None,t)['status'],'WAIT_FOR_OUTCOME')
        with self.assertRaises(ValueError): mcgee_second(2027,30,t)

    def test_funding_needs_separate_exception_and_exact_balance(self):
        t=self.s['mcgee']
        f=funding(t)
        self.assertEqual(f['simple_175_allowance_usd'],2935987)
        self.assertEqual(f['shortfall_usd'],1264013)
        self.assertFalse(f['simple_matching_pass'])
        self.assertIsNone(f['exact_tpe_full_charge_coverage'])
        self.assertTrue(funding(dict(t,exact_available_grant_tpe_usd=4200000))['exact_tpe_full_charge_coverage'])
        self.assertFalse(funding(dict(t,exact_available_grant_tpe_usd=4199999))['exact_tpe_full_charge_coverage'])

    def test_unknowns_and_recommendations_never_become_execution_clearance(self):
        r=build()
        self.assertIsNone(r['chicago_actual_residual_usd'])
        self.assertTrue(all(x['actual_waiver_charge_usd'] is None for x in r['chicago_camp']))
        self.assertIsNone(r['selected_gordon_asset'])
        self.assertIsNone(r['selected_mcgee_assets'])
        self.assertEqual(r['requirements_closed'],0)
        self.assertFalse(any(r[k] for k in ('author_locked','season_selected','exact_execution_cleared','manuscript_allowed')))


if __name__ == '__main__': unittest.main()
