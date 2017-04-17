import sys
import preprocessing
import csv
import random
import game
import utils
from progressbar import print_progress_bar
from numpy.random import choice

count_matrix = 0
count_not_matrix = 0


def main():
    filters = preprocessing.FILTERS
    aleatory = int(sys.argv[1])
    input_name = sys.argv[2]
    if aleatory == 1:
        number_games = int(sys.argv[3])
    else:
        number_games = int(sys.argv[4])
        output_name = sys.argv[3]
    matrix = []
    if aleatory == 1:
        with open('aggregated-data/{0}.csv'.format(input_name), 'w') as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            index = 0
            print_progress_bar(index, number_games, prefix='Progress:', suffix='Complete', length=40)
            for i in range(number_games):
                new_game = create_new_game_matrix(matrix)
                utils.is_valid(new_game, filters)
                writer.writerow(new_game.to_row())
                index += 1
                print_progress_bar(index, number_games, prefix='Progress:', suffix='Complete', length=40)
    else:
        with open('results/{0}/ Transition Matrix.csv'.format(input_name), 'r') as csv_file:
            reader = csv.reader(csv_file, lineterminator='\n')
            for i, line in enumerate(reader):
                new_line = []
                for num in line:
                    new_line.append(int(num))
                matrix.append(new_line)
        with open('aggregated-data/{0}.csv'.format(output_name), 'w') as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            index = 0
            print_progress_bar(index, number_games, prefix='Progress:', suffix='Complete', length=40)
            for i in range(number_games):
                new_game = create_new_game_matrix(matrix)
                utils.is_valid(new_game, filters)
                writer.writerow(new_game.to_row())
                index += 1
                print_progress_bar(index, number_games, prefix='Progress:', suffix='Complete', length=40)


def create_new_game():
    new_game = game.Game()
    new_game.black_ranking = 1
    new_game.white_ranking = 1
    new_game.handicap = 0
    new_game.result = 0
    new_game.size = 19
    new_game.komi = 0
    new_game.positions = list()
    color_position = 0
    while True:
        possible_positions = list()
        for i in range(19):
            for j in range(19):
                if new_game.states[-1][i][j] == 0:
                    possible_positions.append([i, j])
        random.shuffle(possible_positions)
        color_char = 'b'
        if color_position == 1:
            color_char = 'w'
        index = 0
        possible = False
        while index < len(possible_positions):
            visited = list()
            for i in range(19):
                visited.append(19 * [False])
            surrounded = list()
            for i in range(19):
                surrounded.append(19 * [False])
            new_game.states[-1][possible_positions[index][0]][possible_positions[index][1]] = color_position + 1
            game.visit(new_game.states[-1], surrounded, (color_position + 1) % 2 + 1, visited,
                       possible_positions[index][0], possible_positions[index][1])
            if not game.is_surrounded(surrounded, visited):
                possible = True
                new_position = [color_char, possible_positions[index][0], possible_positions[index][1]]
                new_game.positions.append(new_position)
                new_game.get_next_position(new_position)
                break
            else:
                new_game.states[-1][possible_positions[index][0]][possible_positions[index][1]] = 0
                index += 1
        color_position = (color_position + 1) % 2
        if not possible:
            break
    return new_game


def create_new_game_matrix(matrix):
    new_game = game.Game()
    new_game.black_ranking = 1
    new_game.white_ranking = 1
    new_game.handicap = 0
    new_game.result = 0
    new_game.size = 19
    new_game.komi = 0
    new_game.positions = list()
    color_position = 0
    last_position = -1
    global count_matrix
    global count_not_matrix
    while True:
        possible_positions = list()
        for i in range(19):
            for j in range(19):
                if new_game.states[-1][i][j] == 0:
                    value_position = -1
                    if i not in [0, 18] and j not in [0, 18]:
                        matrix_position = [
                            [new_game.states[-1][i-1][j-1], new_game.states[-1][i-1][j], new_game.states[-1][i-1][j+1]],
                            [new_game.states[-1][i][j-1], new_game.states[-1][i][j], new_game.states[-1][i][j+1]],
                            [new_game.states[-1][i+1][j-1], new_game.states[-1][i+1][j], new_game.states[-1][i+1][j+1]]
                        ]
                        value_position = utils.process_value(matrix_position)
                    possible_positions.append([i, j, value_position])
        color_char = 'b'
        if color_position == 1:
            color_char = 'w'
        possible = False
        positions_sampled = []
        if last_position != -1 and last_position < len(matrix):
            possibles_states = matrix[last_position]
            possible_matrix_positions = [position[2] if position[2] < 1000 else 0 for position in possible_positions]
            sum_values = sum([possibles_states[i] for i in possible_matrix_positions])
            if sum_values != 0:
                for index in range(10):
                    weights = [possibles_states[i] * 1.0 / sum_values for i in possible_matrix_positions]
                    chosen_position_index = choice([i for i in range(len(possible_positions))], 1, p=weights)
                    chosen_position = possible_positions[chosen_position_index]
                    positions_sampled.append(chosen_position)
        index = 0
        random.shuffle(possible_positions)
        while index < len(possible_positions):
            if index == 0 and len(positions_sampled) != 0:
                sample_index = 0
                while sample_index < len(positions_sampled):
                    visited = list()
                    for i in range(19):
                        visited.append(19 * [False])
                    surrounded = list()
                    for i in range(19):
                        surrounded.append(19 * [False])
                    new_game.states[-1][positions_sampled[sample_index][0]][positions_sampled[sample_index][1]]\
                        = color_position + 1
                    game.visit(new_game.states[-1], surrounded, (color_position + 1) % 2 + 1, visited,
                               positions_sampled[sample_index][0], positions_sampled[sample_index][1])
                    if not game.is_surrounded(surrounded, visited):
                        possible = True
                        new_position = [color_char, positions_sampled[sample_index][0],
                                        positions_sampled[sample_index][1]]
                        new_game.positions.append(new_position)
                        new_game.get_next_position(new_position)
                        last_position = positions_sampled[sample_index][2]
                        break
                    else:
                        new_game.states[-1][positions_sampled[sample_index][0]][positions_sampled[sample_index][1]] = 0
                        sample_index += 1
            if possible:
                count_matrix += 1
                break
            count_not_matrix += 1
            visited = list()
            for i in range(19):
                visited.append(19 * [False])
            surrounded = list()
            for i in range(19):
                surrounded.append(19 * [False])
            new_game.states[-1][possible_positions[index][0]][possible_positions[index][1]] = color_position + 1
            game.visit(new_game.states[-1], surrounded, (color_position + 1) % 2 + 1, visited,
                       possible_positions[index][0], possible_positions[index][1])
            if not game.is_surrounded(surrounded, visited):
                possible = True
                new_position = [color_char, possible_positions[index][0], possible_positions[index][1]]
                new_game.positions.append(new_position)
                new_game.get_next_position(new_position)
                last_position = possible_positions[index][2]
                break
            else:
                new_game.states[-1][possible_positions[index][0]][possible_positions[index][1]] = 0
                index += 1
        color_position = (color_position + 1) % 2
        if not possible:
            break
    return new_game

if __name__ == '__main__':
    main()
    print(count_matrix)
    print(count_not_matrix)
