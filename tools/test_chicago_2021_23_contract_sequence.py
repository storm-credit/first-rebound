import json
import unittest
from build_chicago_2021_23_contract_sequence import ROOT,INPUT,build,run_route,normal_cap,future_budget,single_season_starter_sufficient


class ContractSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=json.loads(INPUT.read_text());cls.x=build()
        cls.g1=json.loads((ROOT/cls.p['parent_budget']).read_text())
        g7=json.loads((ROOT/cls.p['parent_roster']).read_text())
        top=max(cls.g1['rookie_fourth_cases'],key=lambda c:c['salary'])
        cls.final=dict(g7['scenarios'][0]['named_roster_without_protagonist'],Protagonist=top['salary'])

    def test_room_boundary_and_order_are_material(self):
        p=self.p;route=p['routes'][2]
        good=run_route(p,self.final,route,1000000)
        limit=good['normal_extra_upper_at_Caruso']
        self.assertTrue(run_route(p,self.final,route,1000000,normal_extra=limit)['conditional_numeric_pass'])
        self.assertFalse(run_route(p,self.final,route,1000000,normal_extra=limit+1)['conditional_numeric_pass'])
        early=run_route(p,self.final,route,1000000,late_first=True)
        self.assertLess(early['normal_extra_upper_at_Caruso'],limit)
        self.assertEqual(early['normal_extra_upper_at_Caruso'],5551917)
        # Minimum/Bird additions may finish above cap even though Caruso fit.
        at_limit=run_route(p,self.final,route,1000000,normal_extra=limit)
        self.assertLess(at_limit['rows'][-1]['cap_room'],0)

    def test_ntmle_trigger_persists_after_unused_exception_disappears(self):
        route=self.p['routes'][0];v=run_route(self.p,self.final,route,1000000)
        self.assertEqual(v['rows'][-1]['unused_NTMLE_in_this_restricted_model'],0)
        self.assertTrue(v['rows'][-1]['hard_cap_from_this_route'])
        self.assertFalse(v['room_MLE_eligible_under_assumed_prior_uses'])
        bound=v['apron_extra_upper_after_trigger']
        self.assertTrue(run_route(self.p,self.final,route,1000000,apron_extra=bound)['conditional_numeric_pass'])
        self.assertFalse(run_route(self.p,self.final,route,1000000,apron_extra=bound+1)['conditional_numeric_pass'])

    def test_fa_holds_count_for_empty_places_not_standard_contracts(self):
        contracts={str(i):1000000 for i in range(9)}
        self.assertEqual(normal_cap(contracts,{'M':20000000,'T':9000000,'V':8000000},925258)['incomplete_count'],0)
        self.assertEqual(normal_cap(contracts,{},925258)['incomplete_count'],3)
        with self.assertRaises(ValueError):normal_cap(contracts,{'0':1},925258)
        for r in self.x['routes']:
            self.assertEqual(r['maximum_salary_example']['final_slots'],15)
            self.assertEqual(len(r['cases']),60)
            self.assertTrue(all(c['numeric_pass_at_zero_extra'] for c in r['cases']))

    def test_unknown_prior_starter_criterion_is_not_failure(self):
        self.assertTrue(single_season_starter_sufficient(41,None))
        self.assertTrue(single_season_starter_sufficient(None,2000))
        self.assertIsNone(single_season_starter_sufficient(40,1999))
        self.assertIsNone(single_season_starter_sufficient(None,None))
        for row in self.x['protagonist_QO_cases']:
            self.assertIsNone(row['selected_QO']);self.assertIsNone(row['actual_starter_criteria_met'])
            self.assertEqual(row['starter_QO_reference'],7921300)
            self.assertLess(row['nonstarter_QO_budget_upper'],row['starter_QO_reference'])

    def test_carter_decreasing_salaries_and_rfa_are_not_same_contract(self):
        options=self.x['Carter_options'];self.assertEqual([o['total'] for o in options],[50000000,40000000,60000000,None])
        for o in options[:3]:
            a=o['salary_2022_to_2026']
            self.assertTrue(all(abs(y-z)*100<=a[0]*8 for y,z in zip(a,a[1:])))
        self.assertIsNone(options[3]['salary_2022_to_2026'])
        self.assertTrue(all(not o['contract_agreed'] for o in options))

    def test_waiving_valentine_does_not_erase_dead_money(self):
        policy=self.p['followup_2022_policies'][2]
        unknown=future_budget(self.g1,self.p,policy)[0]
        known=future_budget(self.g1,self.p,policy,dead_salary=1000000)[0]
        self.assertIsNone(unknown['total_with_confirmed_dead_salary'])
        self.assertEqual(known['total_with_confirmed_dead_salary'],unknown['known_budget_excluding_dead_salary']+1000000)
        self.assertTrue(unknown['Valentine_waiver_charge_requires_resolution'])
        self.assertEqual(self.x['budget2022_case_count'],192)
        rt1=next(r for r in self.x['budget2022_cases'] if r['policy']=='RT1')
        self.assertEqual(rt1['delta_from_G1'],-206244)

    def test_numeric_routes_do_not_clear_contracts_or_world(self):
        x=self.x
        self.assertTrue(x['NTMLE_entry_lower_plus_exception_exceeds_cap'])
        for k in ['contracts_agreed','author_locked','season_selected','exact_execution_cleared','manuscript_allowed']:self.assertFalse(x[k])
        self.assertIsNone(x['selected_route']);self.assertIsNone(x['selected_Carter_contract'])
        for r in x['routes']:
            self.assertIsNone(r['actual_normal_extra']);self.assertIsNone(r['actual_apron_extra'])


if __name__=='__main__':unittest.main()
