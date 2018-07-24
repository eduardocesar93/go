import sys
import datetime
import os
import math
import csv
import matplotlib.pyplot as plt
from game import Game
from utils import matrix_value
from plot import save_scatter_csv
from progressbar import print_progress_bar


DIRECTORY = 'results'
MATRIX = []
LINE_SUM = []
ENTROPY_DIST = []
CROSS_ENTROPY_DIST = []
CROSS_ENTROPY_REL = []
for index in range(250):
    ENTROPY_DIST.append(list())
    CROSS_ENTROPY_DIST.append(list())
    CROSS_ENTROPY_REL.append(list())


def get_matrix_transition(file):
    with open('{0}/{1}/Original Transition Matrix.csv'.
              format(DIRECTORY, file), 'r') as csv_file:
        reader = csv.reader(csv_file, lineterminator='\n')
        for i, line in enumerate(reader):
            new_line = []
            for num in line:
                new_line.append(int(num))
            LINE_SUM.append(sum(new_line))
            MATRIX.append(new_line)


def entropy_sit(game_states, game_positions):
    entropy = 0
    first_position = True
    for position in range(min(len(game_states), len(game_positions))):
        if first_position:
            first_position = False
            continue
        else:
            before_pos = game_positions[position - 1]
            after_pos = game_positions[position]
            before_state = game_states[position - 1]
            after_state = game_states[position]
            before_pos_val = matrix_value(before_state, before_pos)
            after_pos_val = matrix_value(after_state, after_pos)
            if before_pos_val != -1 and after_pos_val != -1:
                all_sum = LINE_SUM[before_pos_val]
                if all_sum != 0:
                    prob = MATRIX[before_pos_val][after_pos_val] /\
                        all_sum
                    if prob != 0:
                        entropy -= prob * math.log(prob)
    if len(game_states) < 250:
        ENTROPY_DIST[len(game_states)].append(entropy)


def cross_entropy(game_states, game_positions):
    entropy = 0
    first_position = True
    for position in range(min(len(game_states), len(game_positions))):
        if first_position:
            first_position = False
            continue
        else:
            before_pos = game_positions[position - 1]
            after_pos = game_positions[position]
            before_state = game_states[position - 1]
            after_state = game_states[position]
            before_pos_val = matrix_value(before_state, before_pos)
            after_pos_val = matrix_value(after_state, after_pos)
            if before_pos_val != -1 and after_pos_val != -1:
                all_sum = LINE_SUM[before_pos_val]
                if all_sum != 0:
                    prob = MATRIX[before_pos_val][after_pos_val] / \
                           all_sum
                    if prob != 0:
                        entropy -= prob * math.log(1 / len(MATRIX[before_pos_val]))
    if len(game_states) < 250:
        CROSS_ENTROPY_DIST[len(game_states)].append(entropy)


def cross_entropy_rel(game_states, game_positions):
    entropy = 0
    first_position = True
    for position in range(min(len(game_states), len(game_positions))):
        if first_position:
            first_position = False
            continue
        else:
            before_pos = game_positions[position - 1]
            after_pos = game_positions[position]
            before_state = game_states[position - 1]
            after_state = game_states[position]
            before_pos_val = matrix_value(before_state, before_pos)
            after_pos_val = matrix_value(after_state, after_pos)
            if before_pos_val != -1 and after_pos_val != -1:
                all_sum = LINE_SUM[before_pos_val]
                if all_sum != 0:
                    prob = MATRIX[before_pos_val][after_pos_val] / \
                           all_sum
                    if prob != 0:
                        entropy += prob * (math.log(prob) - math.log(1 / len(MATRIX[before_pos_val])))
    if len(game_states) < 250:
        CROSS_ENTROPY_REL[len(game_states)].append(entropy)


def main():
    directory = sys.argv[1]
    get_matrix_transition(directory)
    run(directory, entropy_sit)
    run(directory, cross_entropy)
    run(directory, cross_entropy_rel)
    print_scatter_from_dist_list(dist_list=ENTROPY_DIST, dist_name='MEP', directory=directory)
    print_scatter_from_dist_list(dist_list=CROSS_ENTROPY_DIST, dist_name='CROSS', directory=directory)
    print_scatter_from_dist_list(dist_list=CROSS_ENTROPY_REL, dist_name='REL', directory=directory)


def print_scatter_from_dist_list(*, dist_list, dist_name, directory):
    x = [i + 1 for i in range(len(dist_list))]
    y = [sum(row) / len(row) if row else 0 for row in dist_list]
    save_scatter_csv([x, y], f'{DIRECTORY}/{directory}', f'{dist_name}', labels=['time', dist_name])
    plt.xlabel('Time')
    plt.ylabel(f'Entropy {dist_name}')
    plt.title(f'Entropy {dist_name}')
    plt.scatter(x, y)
    plt.savefig(f'{DIRECTORY}/{directory}/{dist_name}.png')
    plt.clf()


def run(directory, entropy_func):
    start_time = datetime.datetime.now()
    index = 0
    results_dir = 'results/{0}'.format(directory)
    try:
        os.makedirs('results')
    except FileExistsError:
        pass
    try:
        os.makedirs(results_dir)
    except FileExistsError:
        pass
    try:
        os.makedirs(results_dir + '/entropy')
    except FileExistsError:
        pass
    with open('aggregated-data/{0}.csv'.format(directory), 'r') as csv_file:
        reader = csv.reader(csv_file, lineterminator='\n')
        total_files = sum(1 for row in reader)
        csv_file.seek(0)
        print_progress_bar(index, total_files, prefix='Processing Progress:',
                           suffix='Complete', length=40)
        for row in reader:
            game = Game.row_to_game(row)
            position_index = 0
            if len(game.positions) == 0:
                continue
            while True:
                captures, finish, _matrix_value =\
                    game.get_next_position(game.positions[position_index])
                entropy_func(game.states, game.positions)
                if finish:
                    break
                position_index += 1
            index += 1
            print_progress_bar(index, total_files,
                               prefix='Processing Progress:',
                               suffix='Complete', length=40)
    final_date = datetime.datetime.now()
    print('\nTotal Time: {0}\n'.format(final_date - start_time))


if __name__ == '__main__':
    main()
