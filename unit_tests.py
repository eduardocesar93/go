import unittest
import utils
import game

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
        game_instance = utils.convert_game(games[0])
        row = game_instance.to_row()
        self.assertTrue(len(row) > 0)
        self.assertEqual(len(row), 8)
        self.assertEqual(row[0], utils.rank('6d'))
        self.assertEqual(row[1], utils.rank('6d'))
        self.assertEqual(row[2], 1)
        self.assertTrue(row[3])
        self.assertEqual(row[4], 6.5)
        self.assertEqual(row[5], 19)
        self.assertTrue(len(row[7]) > 0)

    def test_row_to_game(self):
        game_instance = utils.convert_game(games[0])
        row = game_instance.to_row()
        converted_game = game.Game.row_to_game(row)
        self.assertEqual(game_instance.positions, converted_game.positions)
        self.assertEqual(game_instance.handicap, converted_game.handicap)
        self.assertEqual(game_instance.black_ranking, converted_game.black_ranking)
        self.assertEqual(game_instance.white_ranking, converted_game.white_ranking)
        self.assertEqual(game_instance.komi, converted_game.komi)
        self.assertEqual(game_instance.valid, converted_game.valid)
        self.assertEqual(game_instance.handicap, converted_game.handicap)

    def test_update_positions(self):
        state = [
            [0, 1, 1 ,1 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
            [0, 1, 2 ,1 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0 ,1 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0 ,0 ,0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0 ,0 ,0, 0, 2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0 ,0 ,0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0],
            [2, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 0, 1, 2, 0, 2, 1, 0, 0, 1, 1],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 2],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 1, 1],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 1, 1, 1],
            [2, 1, 2 ,0 ,0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 1, 2, 1],
            [0, 1, 2 ,0 ,0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 1, 0, 0]]
        deleted_1 = game.update_positions(state, 1, 2, 2)
        deleted_2 = game.update_positions(state, 2, 18, 0)
        deleted_3 = game.update_positions(state, 2, 4, 8)
        deleted_4 = game.update_positions(state, 2, 1, 18)
        deleted_5 = game.update_positions(state, 1, 10, 12)
        deleted_6 = game.update_positions(state, 1, 15, 10)
        deleted_7 = game.update_positions(state, 1, 11, 17)
        self.assertEqual(state[2][2], 1)
        self.assertEqual(state[1][2], 0)
        self.assertEqual(state[1][1], 1)
        self.assertEqual(state[18][0], 2)
        self.assertEqual(state[18][1], 1)
        self.assertEqual(state[10][1], 1)
        self.assertEqual(state[4][8], 2)
        self.assertEqual(state[5][8], 0)
        self.assertEqual(state[5][9], 0)
        self.assertEqual(state[1][18], 2)
        self.assertEqual(state[10][12], 1)
        self.assertEqual(state[10][11], 0)
        self.assertEqual(state[10][13], 0)
        self.assertEqual(state[9][12], 0)
        self.assertEqual(state[11][12], 0)
        self.assertEqual(state[15][10], 1)
        self.assertEqual(state[17][10], 0)
        self.assertEqual(state[18][10], 0)
        self.assertEqual(state[11][17], 1)
        self.assertEqual(state[11][18], 0)
        deleted_8 = game.update_positions(state, 1, 18, 18)
        self.assertEqual(state[18][17], 0)
        self.assertEqual(state[17][17], 2)
        deleted_9 = game.update_positions(state, 1, 18, 17)
        self.assertEqual(state[17][17], 0)
        self.assertEqual(deleted_1, 1)
        self.assertEqual(deleted_2, 0)
        self.assertEqual(deleted_3, 3)
        self.assertEqual(deleted_4, 1)
        self.assertEqual(deleted_5, 7)
        self.assertEqual(deleted_6, 3)
        self.assertEqual(deleted_7, 1)
        self.assertEqual(deleted_8, 0)
        self.assertEqual(deleted_9, 1)

    def test_invertion(self):
        matrix_1 = [[1, 1, 0],
                    [1, 2, 0],
                    [0, 1, 1]]
        matrix_2 = [[2, 1, 0],
                    [0, 1, 1],
                    [0, 2, 2]]
        utils.invertion(matrix_1, horizontal=True)
        utils.invertion(matrix_2, horizontal=True)
        matrix_1_result = [[0, 1, 1],
                           [1, 2, 0],
                           [1, 1, 0]]
        matrix_2_result = [[0, 2, 2],
                           [0, 1, 1],
                           [2, 1, 0]]
        self.assertEqual(matrix_1, matrix_1_result)
        self.assertEqual(matrix_2, matrix_2_result)

    def test_rotate(self):
        matrix_1 = [[1, 1, 0],
                    [1, 2, 0],
                    [0, 1, 1]]
        matrix_2 = [[2, 1, 0],
                    [0, 1, 1],
                    [0, 2, 2]]
        utils.rotate(matrix_1)
        utils.rotate(matrix_2)
        matrix_1_result = [[0, 1, 1],
                           [1, 2, 1],
                           [1, 0, 0]]
        matrix_2_result = [[0, 0, 2],
                           [2, 1, 1],
                           [2, 1, 0]]
        self.assertEqual(matrix_1, matrix_1_result)
        self.assertEqual(matrix_2, matrix_2_result)

    def test_change_color(self):
        matrix_1 = [[1, 1, 0],
                    [1, 2, 0],
                    [0, 1, 1]]
        matrix_2 = [[2, 1, 0],
                    [0, 1, 1],
                    [0, 2, 2]]
        utils.change_colors(matrix_1)
        utils.change_colors(matrix_2)
        matrix_1_result = [[2, 2, 0],
                           [2, 1, 0],
                           [0, 2, 2]]
        matrix_2_result = [[1, 2, 0],
                           [0, 2, 2],
                           [0, 1, 1]]
        self.assertEqual(matrix_1, matrix_1_result)
        self.assertEqual(matrix_2, matrix_2_result)

    def test_process_value(self):
        matrix_1 = [[0, 0, 0],
                    [0, 2, 1],
                    [1, 1, 2]]
        matrix_2 = [[0, 1, 0],
                    [0, 1, 2],
                    [0, 0, 0]]
        self.assertEqual(utils.process_value(matrix_1), 160)
        self.assertEqual(utils.process_value(matrix_2), 114)

if __name__ == '__main__':
    unittest.main()
