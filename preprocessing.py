import os
import utils
import csv

OUTPUT = 'test'
FILTERS = {'rank': [i + 1 for i in range(50)],
           'result': [0, 1, 2, 3],
           'komi': {'min': 0, 'max': 100},
           'positions': {'min': 0, 'max': 500}
           }
PLOT_STATS = True

total_count = 0
black_win = 0
white_win = 0
valid = 0

csv_file = open('{0}.csv'.format(OUTPUT), 'wb')
writer = csv.writer(csv_file)

for subdir, dirs, files in os.walk("data"):
    if exit_flag:
        break
    for file in files:
        file_path = subdir + os.sep + file
        with open(file_path, 'r') as f:
            game_str = f.read()
            game_instance = utils.convert_game(game_str, FILTERS)
            writer.writerow(game_instance.to_row())
            if game_instance.valid and game_instance:
                valid += 1
            if game_instance.result == 0:
                black_win += 1
            if game_instance.result == 1:
                white_win += 1
            total_count += 1
        if total_count > 1000:
            exit_flag = True
            break

csv_file.close()
print(total_count)
print(black_win)
print(white_win)
print(valid)
