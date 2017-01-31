import unittest
import utils

games = ['(;GM[1]FF[4]SZ[19]PW[supertjc]WR[6d]PB[YoungPro]BR[6d]DT[2016-07-01]PC[The KGS Go Server at \
http://www.gokgs.com/]KM[6.50]RE[W+Time]RU[Japanese]CA[UTF-8]ST[2]AP[CGoban:3]TM[73]OT[1/6 Canadian]AB\
[aa][ab]AW[af][ag];B[pd];W[qp];B[op];W[lp];B[pm];W[oo];B[no];W[on];B[qq];W[rq];B[pp];W[qo];B[po];W[pn]\
;B[qn];W[nn];B[rr];W[rn];B[qm];W[rm];B[rl];W[ql];B[qk];W[pl];B[om];W[ol];B[nm];W[mn];B[nl];W[pq];B[qr]\
;W[rp];B[nq];W[rk];B[ok];W[sl];B[pk];W[rl];B[nk];W[mq];B[mr];W[lr];B[nr];W[pr];B[ps];W[os];B[or];W[qs]\
;B[sr];W[ms];B[ns];W[rs];B[ps];W[qd];B[qe];W[os];B[ls];W[sq])']


class TestUtilFunctions(unittest.TestCase):
    def test_rank(self):
        self.assertEqual(utils.rank('30k'), 1)
        self.assertEqual(utils.rank('1k'), 30)
        self.assertEqual(utils.rank('1d'), 31)
        self.assertEqual(utils.rank('7d'), 37)
        self.assertEqual(utils.rank('1p'), 41)
        self.assertEqual(utils.rank('10p'), 50)

    def test_convert_game(self):
        result_game = utils.convert_game(games[0])
        self.assertEqual(result_game.positions[5], ['w', 16, 15])
        self.assertEqual(result_game.positions[-2], ['b', 11, 18])
        self.assertEqual(result_game.positions[-1], ['w', 18, 16])
        self.assertEqual(result_game.komi, 6.5)
        self.assertEqual(result_game.result, 1)
        self.assertEqual(result_game.black_ranking, utils.rank('6d'))
        self.assertEqual(result_game.white_ranking, utils.rank('6d'))
        self.assertTrue(result_game.valid)


class TestGameMethods(unittest.TestCase):
    def test_to_row(self):
        game = utils.convert_game(games[0])
        row = game.to_row()
        self.assertTrue(len(row) > 0)
        self.assertEqual(len(row), 7)
        self.assertEqual(row[0], utils.rank('6d'))
        self.assertEqual(row[1], utils.rank('6d'))
        self.assertEqual(row[2], 1)
        self.assertTrue(row[3])
        self.assertEqual(row[4], 6.5)
        self.assertEqual(row[5], 19)
        self.assertTrue(len(row[6]) > 0)

if __name__ == '__main__':
    unittest.main()
