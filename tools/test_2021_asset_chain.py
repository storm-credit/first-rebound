import json
import unittest
import build_2021_asset_chain as b


class AssetChainTests(unittest.TestCase):
    def setUp(self):
        self.s = json.loads(b.SOURCE.read_text())
        self.p = json.loads(b.PRIOR.read_text())

    def test_second_round_later_pick_both_directions(self):
        for bos, mem, origin in [(60, 31, 'BOS'), (31, 60, 'MEM')]:
            d = b.split_boston_memphis(bos, mem)
            self.assertEqual(d['ORL_if_terms_adopted'], {'origin': origin, 'pick': 60})
            self.assertEqual(d['BOS_retained_before_other_obligations']['pick'], 31)
        self.assertIsNone(b.split_boston_memphis(45, None))
        for bos, mem in [(30, 60), (31, 61), (40, 40)]:
            with self.assertRaises(ValueError):
                b.split_boston_memphis(bos, mem)

    def test_denver_protection_boundary(self):
        t = self.s['denver_preceding_pick']
        self.assertEqual(b.preceding_denver({2023: 15}, t)['year'], 2023)
        self.assertEqual(b.preceding_denver({2023: 14}, t)['status'], 'WAIT_FOR_OUTCOME')
        self.assertEqual(b.preceding_denver({2023: 14, 2024: 15}, t)['year'], 2024)

    def test_denver_terminal_does_not_create_gordon_asset(self):
        t = self.s['denver_preceding_pick']
        d = b.preceding_denver({2023: 14, 2024: 14, 2025: 14}, t)
        self.assertEqual([(x['year'], x['round']) for x in d['asset']], [(2025, 2), (2026, 2)])
        result = b.build(self.s, self.p)
        self.assertIsNone(result['Denver']['gordon_after_preceding_conversion'])
        self.assertIsNone(result['Denver']['gordon_terminal_conversion'])

    def test_tpe_snapshot_is_consistency_not_trade_date_proof(self):
        d = b.build(self.s, self.p)['Boston']
        self.assertEqual([x['balance_if_no_prior_use_usd'] for x in d['tpe_comparisons']], [11500000, 11350000, 11050000])
        self.assertEqual(d['inferred_consumption_if_same_exception_and_no_other_uses_usd'], 17450000)
        self.assertFalse(d['exact_trade_date_charge_verified'])
        self.assertIsNone(d['exact_alternate_tpe_balance_usd'])

    def test_other_tpe_use_cannot_be_hidden(self):
        self.assertEqual(b.tpe_remaining(28500000, 17450000, 1000000), 10050000)
        self.assertLess(b.tpe_remaining(28500000, 17450000, 12000000), 0)
        self.assertIsNone(b.tpe_remaining(28500000, 17450000, None))

    def test_no_author_or_future_result_promotion(self):
        d = b.build(self.s, self.p)
        self.assertIsNone(d['Boston']['selected_2025_split'])
        self.assertEqual(d['Denver']['selected_preceding_result']['status'], 'WAIT_FOR_OUTCOME')
        self.assertFalse(d['exact_execution_cleared'])
        self.s['season_selected'] = True
        with self.assertRaises(AssertionError):
            b.build(self.s, self.p)


if __name__ == '__main__':
    unittest.main()
