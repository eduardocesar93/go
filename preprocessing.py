import os
import utils
import csv

OUTPUT = 'test'

total_count = 0
black_win = 0
white_win = 0
valid = 0

exit_flag = False
csv_file = open('{0}.csv'.format(OUTPUT), 'wb')
writer = csv.writer(csv_file)

for subdir, dirs, files in os.walk("data"):
    if exit_flag:
        break
    for file in files:
        file_path = subdir + os.sep + file
        with open(file_path,'r') as f:
            game_str = f.read()
            game_instance = utils.convert_game(game_str)
            writer.writerow(game_instance.to_row())
            if game_instance.valid:
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
