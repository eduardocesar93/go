import sys
import preprocessing
import datetime
import os
import csv
from game import Game, Stats
from progressbar import print_progress_bar


def main():
    input_dir = sys.argv[1]
    output = sys.argv[2]
    pre_processing = False
    if len(sys.argv) >= 4:
        pre_processing = bool(int(sys.argv[3]))
    if pre_processing:
        preprocessing.run(input_dir, output)


def run(input_dir, output):
    start_time = datetime.datetime.now()
    index = 0
    stats = Stats()
    with open('aggregated-data/{0}.csv'.format(input_dir), 'r') as csv_file:
        reader = csv.reader(csv_file, lineterminator='\n')
        total_files = sum(1 for row in reader)
        print_progress_bar(index, total_files, prefix='Processing Progress:', suffix='Complete', length=50)
        for row in reader:
            game = Game.row_to_game(row)
            print_progress_bar(index, total_files, prefix='Processing Progress:', suffix='Complete', length=50)
            index += 1
    final_date = datetime.datetime.now()
    print('Completed\n'
          'Total Time: {0}\n'.format(final_date - start_time) +
          'Errors (game length): {0}'.format({stats.errors['']}))

