import unittest
import build_2021_top14_board as m


class Top14Tests(unittest.TestCase):
    def test_earlier_team_can_remove_chicago_preference(self):
        x=m.build();boards={s['id']:s for s in x['scenarios']}
        self.assertEqual(boards['DB1']['board'][8]['proposed_player'],'Moses Moody')
        self.assertEqual(boards['DB1']['CHI10'],'Chris Duarte')
        self.assertEqual(boards['DB2']['CHI10'],'Moses Moody')
        self.assertEqual([r['proposed_player'] for r in boards['DB3']['board'][6:9]],
                         ['Moses Moody','Franz Wagner','Josh Giddey'])

    def test_each_comparison_is_still_available(self):
        for s in m.build()['scenarios']:
            seen=set()
            for r in s['board']:
                self.assertGreaterEqual(len(r['available_comparison']),3)
                self.assertFalse(seen.intersection(r['available_comparison']))
                self.assertNotIn(r['proposed_player'],seen)
                seen.add(r['proposed_player'])

    def test_wrong_priority_and_roster_duplicates_fail(self):
        rows=[dict(pick=1,control_team_if_no_new_trade='A',priority=['x','x','y'])]
        with self.assertRaises(ValueError):m.resolve(rows)
        rows[0]['priority']=['x','y']
        with self.assertRaises(ValueError):m.resolve(rows)
        with self.assertRaises(ValueError):m.overlay_roster({'named_roster_without_protagonist':{'Moses Moody':1,'Chris Duarte':2}},'Chris Duarte')

    def test_roster_cost_and_center_exception_are_separate(self):
        x=m.build()
        for s in x['scenarios']:
            self.assertEqual(len(s['named_roster_example_without_protagonist'])+1,15)
            self.assertEqual(s['CHI_rookie_first_salary_budget'],4373040)
            self.assertEqual(s['budget_delta_from_G3'],0)
        self.assertTrue(x['scenarios'][3]['rotation_rebuild_required'])

    def test_first14_is_not_full_draft_or_new_lottery(self):
        x=m.build()
        self.assertEqual(len(x['remaining_origin_order_first_round'])+len(x['second_round_origin_order']),46)
        self.assertFalse(x['CHI39_availability_verified'])
        self.assertIsNone(x['CHI39_proposed_player'])
        self.assertFalse(x['original_lottery_rerun'])
        self.assertFalse(x['author_locked'])
        self.assertIsNone(x['selected_scenario'])


if __name__=='__main__':unittest.main()
