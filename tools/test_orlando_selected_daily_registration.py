import copy,json,unittest
import build_orlando_selected_daily_registration as m

class DailyRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.r,self.d,self.s=[json.loads((m.ROOT/p).read_text(encoding='utf-8')) for p in [m.INPUT,m.DECISION,m.SOURCE]]
    def build(self):return m.build(self.r,self.d,self.s)
    def test_off_days_and_endpoints(self):
        d=self.build();self.assertEqual((d['calendar_days'],d['game_days'],d['off_days']),(35,19,16))
        self.assertEqual((d['rows'][0]['date'],d['rows'][-1]['date']),('2021-04-12','2021-05-16'))
        self.assertTrue(all(r['standard_count']==15 and r['two_way_count']<=2 for r in d['rows']))
    def test_author_omission_preserves_april_contract(self):
        d=self.build();by={r['date']:r for r in d['rows']}
        self.assertIn('Donta Hall',by['2021-05-01']['standard'])
        for day in ['2021-05-02','2021-05-08','2021-05-09','2021-05-10','2021-05-16']:
            self.assertNotIn('Donta Hall',by[day]['standard'])
        self.assertEqual(d['selected_omitted_actions'],1)
    def test_brazdeikis_continuation_not_duplicate(self):
        d=self.build();by={r['date']:r for r in d['rows']}
        self.assertEqual(by['2021-05-11']['standard'],by['2021-05-12']['standard'])
        self.r['contracts']=[c for c in self.r['contracts'] if c['source']!='LR_BRAZ_ROS']
        with self.assertRaises(AssertionError):self.build()
    def test_wrong_release_date_rejected(self):
        next(e for e in self.s['events'] if e['player']=='Donta Hall' and e['action']=='RELEASE_TEN_DAY')['date']='2021-05-03'
        with self.assertRaises(AssertionError):self.build()
    def test_wrong_contract_class_rejected(self):
        next(e for e in self.s['events'] if e['player']=='Devin Cannady' and e['action']=='WAIVE_TWO_WAY')['action']='RELEASE_TEN_DAY'
        with self.assertRaises(AssertionError):self.build()
    def test_duplicated_player_rejected(self):
        self.r['contracts'].append(copy.deepcopy(self.r['contracts'][0]))
        with self.assertRaises(AssertionError):self.build()
    def test_inactive_player_preserved(self):
        d=self.build();self.assertTrue(all({'Al-Farouq Aminu','Jonathan Isaac','Markelle Fultz'}<=set(r['standard']) for r in d['rows']))
    def test_new_fact_or_gate_promotion_rejected(self):
        self.s['original_contracts_or_league_registration_certified']=True
        with self.assertRaises(AssertionError):self.build()
        self.s['original_contracts_or_league_registration_certified']=False;self.r['season_selected']=True
        with self.assertRaises(AssertionError):self.build()
    def test_output_cannot_claim_whole_S2_domain(self):
        d=self.build()
        for k in ['complete_counterfactual_domain','source_verified_for_full_S2_legal_proof','legal_registration_cleared','exact_salary_cleared','health_cleared','F4_complete','season_selected','manuscript_allowed','author_locked']:
            self.assertIs(d[k],False)
    def test_unknown_contract_class_rejected(self):
        next(c for c in self.r['contracts'] if c['player']=='Chasson Randle')['type']='OTHER'
        with self.assertRaises(AssertionError):self.build()
    def test_all_thirteen_baseline_players_preserved(self):
        next(c for c in self.r['contracts'] if c['player']=='Zeke Nnaji')['player']='Unknown replacement'
        with self.assertRaises(AssertionError):self.build()
    def test_duplicate_game_row_rejected_before_date_mapping(self):
        self.r['orl_game_checks'].append(copy.deepcopy(self.r['orl_game_checks'][0]))
        with self.assertRaises(AssertionError):self.build()
    def test_summary_counts_derived_from_rows(self):
        d=self.build()
        self.assertEqual(d['two_way_count_max'],max(r['two_way_count'] for r in d['rows']))
        self.assertEqual(d['standard_count_max'],max(r['standard_count'] for r in d['rows']))

if __name__=='__main__':unittest.main()
