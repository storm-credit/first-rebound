import unittest
from hashlib import sha256
from collections import Counter
from build_2021_provisional_draft import HashStream,COMBINATIONS,allocate,draw_four,second_round,core_settlement,pre_order


class DraftTests(unittest.TestCase):
    def test_all_combinations_and_odd_tie_split(self):
        order=[f'T{i:02}' for i in range(14)];wins={t:i for i,t in enumerate(order)}
        wins['T09']=8
        tickets,owners=allocate(order,wins)
        self.assertEqual((tickets['T08'],tickets['T09']),(38,37))
        self.assertEqual(sum(tickets.values()),1000)
        self.assertEqual(len(set(COMBINATIONS)),1001)
        self.assertEqual(COMBINATIONS[-1],(11,12,13,14))
        self.assertIsNone(owners[-1])
        self.assertEqual(Counter(owners)['T08'],38)

    def test_unassigned_and_repeat_are_redrawn(self):
        owners=['A']*140+['B']*140+['C']*140+['D']*580+[None]
        indices=iter([1000,0,1,140,141,280,420])
        winners,log=draw_four(owners,lambda n:next(indices))
        self.assertEqual(winners,['A','B','C','D'])
        self.assertEqual([x['decision'] for x in log],['UNASSIGNED','ACCEPTED','REPEAT_WINNER','ACCEPTED','REPEAT_WINNER','ACCEPTED','ACCEPTED'])

    def test_random_domains_reproduce_without_project_seed(self):
        seed=sha256(b'unit-test-only').digest()
        a,b=HashStream(seed,'test'),HashStream(seed,'test')
        self.assertEqual([a.below(1001) for _ in range(20)],[b.below(1001) for _ in range(20)])
        with self.assertRaises(ValueError):a.below(0)
        order,log=pre_order(['A','B'],dict(A=20,B=20),seed,{'A,B':['B','A']})
        self.assertEqual(order,['B','A']);self.assertEqual(log[0]['method'],'UNCHANGED_HISTORICAL_TIE')

    def test_actual_2021_second_round_origin_fixture(self):
        # NBA Communications June 22 result fixture, not this project's outcome.
        first='DET HOU CLE TOR ORL OKC MIN CHI SAC NOP CHA SAS IND GSW WAS BOS MEM MIA NYK ATL DAL LAL POR MIL LAC DEN BKN PHI PHX UTA'.split()
        wins=dict(zip('HOU DET ORL OKC CLE MIN TOR CHI SAC NOP CHA SAS IND WAS BOS MEM GSW MIA ATL NYK DAL LAL POR MIL LAC DEN BKN PHI PHX UTA'.split(),[17,20,21,22,22,23,27,31,31,31,33,33,34,34,36,38,39,40,41,41,42,42,42,46,47,47,48,49,51,52]))
        expected='HOU DET ORL OKC CLE MIN TOR NOP SAC CHI SAS CHA WAS IND BOS MEM GSW MIA ATL NYK POR LAL DAL MIL DEN LAC BKN PHI PHX UTA'.split()
        self.assertEqual(second_round(first,wins),expected)

    def test_second_round_uses_final_not_pre_lottery_tie(self):
        order=[f'T{i:02}' for i in range(30)]
        wins={t:i for i,t in enumerate(order)};wins['T04']=wins['T05']=4
        before=second_round(order,wins)
        changed=['T05']+[t for t in order if t!='T05']
        after=second_round(changed,wins)
        self.assertLess(before.index('T05'),before.index('T04'))
        self.assertLess(after.index('T04'),after.index('T05'))

    def test_protection_and_swap_without_player_selection(self):
        rest=[f'T{i:02}' for i in range(26)]
        first=['CHI','NOP','MIN','GSW']+rest;second=['CHI','NOP','MIN','GSW']+rest
        r=core_settlement(first,second)
        self.assertEqual(r['MIN_first']['owner'],'MIN')
        self.assertFalse(r['CHI_NOP_second']['swap_exercised_conditionally'])
        first=['CHI','NOP','GSW','MIN']+rest;second=['NOP','CHI','MIN','GSW']+rest
        r=core_settlement(first,second)
        self.assertEqual(r['MIN_first']['owner'],'GSW')
        self.assertTrue(r['CHI_NOP_second']['swap_exercised_conditionally'])
        self.assertEqual(r['CHI_NOP_second']['CHI_receives_pick'],31)


if __name__=='__main__':unittest.main()
