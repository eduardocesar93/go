import os
import utils
import csv
import datetime
from progressbar import print_progress_bar


FILTERS = {'rank': [i + 1 for i in range(50)],
           'result': [0, 1, 2, 3],
           'komi': {'min': 0, 'max': 100},
           'handicap': {'min': 0, 'max': 2},
           'positions': {'min': 0, 'max': 500}
           }


def run(input_dir, output):
    list_paths = []
    start_time = datetime.datetime.now()
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = subdir + os.sep + file
            list_paths.append(file_path)
    try:
        os.makedirs('aggregated-data')
    except FileExistsError:
        pass
    total_files = len(list_paths)
    total_valid = 0
    index = 0
    print_progress_bar(index, total_files, prefix='Pre-Processing:', suffix='Complete', length=50)
    with open('aggregated-data/{0}.csv'.format(output), 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for file_path in list_paths:
            with open(file_path, 'r') as f:
                game_str = f.read()
                game_instance = utils.convert_game(game_str, FILTERS)
                if game_instance.valid and game_instance:
                    writer.writerow(game_instance.to_row())
                    total_valid += 1
                index += 1
                print_progress_bar(index, total_files, prefix='Pre-Processing:', suffix='Complete', length=50)
    final_date = datetime.datetime.now()
    with open('aggregated-data/{0}-log.txt'.format(output), 'w') as log_file:
        log_file.writelines([
            'Log Data About File "{0}.csv"\n'.format(output),
            'Date - {0}\n'.format(final_date.strftime('%Y-%m-%d %H:%M')),
            'Total Time - {0}\n'.format(final_date - start_time),
            'Total Read Games - {0}\n'.format(total_files),
            'Total Valid Games - {0}\n'.format(total_valid),
            'Filter (rank) - {0}\n'.format(FILTERS['rank']),
            'Filter (result) - {0}\n'.format(FILTERS['result']),
            'Filter (komi) - {0}\n'.format(FILTERS['komi']),
            'Filter (positions) - {0}\n'.format(FILTERS['positions']),
        ])

