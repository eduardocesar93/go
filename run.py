import sys
import preprocessing
import datetime
import os
import csv
import plot
from game import Game, Stats
from progressbar import print_progress_bar


def main():
    input_dir = sys.argv[1]
    output = sys.argv[2]
    pre_processing = False
    processing = True
    if len(sys.argv) >= 4:
        pre_processing = bool(int(sys.argv[3]))
    if len(sys.argv) >= 5:
        processing = bool(int(sys.argv[4]))
    if pre_processing:
        preprocessing.run(input_dir, output)
    if processing:
        run(input_dir, output)


def run(input_dir, output):
    start_time = datetime.datetime.now()
    index = 0
    stats = Stats()
    results_dir = 'results/{0}'.format(output)
    try:
        os.makedirs('results')
    except FileExistsError:
        pass
    try:
        os.makedirs(results_dir)
    except FileExistsError:
        pass
    with open('aggregated-data/{0}.csv'.format(input_dir), 'r') as csv_file:
        reader = csv.reader(csv_file, lineterminator='\n')
        total_files = sum(1 for row in reader)
        csv_file.seek(0)
        print_progress_bar(index, total_files, prefix='Processing Progress:', suffix='Complete', length=40)
        for row in reader:
            game = Game.row_to_game(row)
            position_index = 0
            if len(game.positions) == 0:
                continue
            while True:
                captures, finish, matrix_value = game.get_next_position(game.positions[position_index])
                stats.update_stats_dynamic(game, captures, matrix_value)
                if finish:
                    stats.last_capture = -1
                    break
                position_index += 1
            stats.update_stats_game(game)
            index += 1
            print_progress_bar(index, total_files, prefix='Processing Progress:', suffix='Complete', length=40)
    final_date = datetime.datetime.now()

    data_lengths = [[i for i in range(len(stats.game_length))], stats.game_length]
    plot.save_scatter_csv(data_lengths, results_dir, 'Game Lengths', labels=['Length', 'Frequency'])
    plot.scatter_plot('Game Lengths', data_lengths, results_dir, 'Game Lengths', 'Length', 'Frequency', 30, 20,
                      linear_regression=False)
    plot.scatter_plot('Game Lengths', data_lengths, results_dir, 'Game Lengths', 'Length', 'Frequency', 30, 20,
                      linear_regression=False, log=True)

    captures = [[i for i in range(len(stats.captures))], stats.captures]
    plot.save_scatter_csv(captures, results_dir, 'Distribuition of Captures', labels=['Time', 'Frequency'])
    plot.scatter_plot('Distribuition of Captures', captures, results_dir, 'Distribuition of Captures', 'Time',
        'Frequency', 30, 20, linear_regression=False)
    plot.scatter_plot('Distribuition of Captures', captures, results_dir, 'Distribuition of Captures', 'Time',
        'Frequency', 30, 20, linear_regression=False, log=True)

    times_capture = [[i for i in range(len(stats.times_capture))], stats.times_capture]
    plot.save_scatter_csv(times_capture, results_dir, 'Capture Intervals', labels=['Time', 'Frequency'])
    plot.scatter_plot('Capture Intervals', times_capture, results_dir, 'Capture Intervals', 'Interval',
        'Frequency', 30, 20, linear_regression=False)
    plot.scatter_plot('Capture Intervals', times_capture, results_dir, 'Capture Intervals', 'Interval',
        'Frequency', 30, 20, linear_regression=False, log=True)

    matrix_values = [[i for i in range(len(stats.matrix_values))], stats.matrix_values]
    plot.save_scatter_csv(matrix_values, results_dir, 'Positions', labels=['Value', 'Frequency'])
    matrix_values.sort()
    plot.scatter_plot('Positions', matrix_values, results_dir, 'Positions', 'Position',
        'Frequency', 30, 20, linear_regression=False)
    plot.scatter_plot('Positions', matrix_values, results_dir, 'Positions', 'Position',
        'Frequency', 30, 20, linear_regression=True, log=True)


    print('\nTotal Time: {0}\n'.format(final_date - start_time) +
          'Errors (game length): {0}\n'.format(stats.errors['game length']) +
          'Errors (win): {0}\n'.format(stats.errors['win']))


if __name__ == '__main__':
    main()
