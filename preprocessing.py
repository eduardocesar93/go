import os
import utils
import csv

OUTPUT = 'test'

total_count = 0
black_win = 0
white_win = 0
valid = 0

exit = False
csv_file = open('{0}.csv'.format(OUTPUT), 'wb')
writer = csv.writer(csv_file)

for subdir, dirs, files in os.walk("data"):
    if exit:
        break
    for file in files:
        filepath = subdir + os.sep + file
        with open(filepath,'r') as f:
            game_str = f.read()
            game = utils.convert_game(game_str)
            writer.writerow(game.to_row())
            if game.valid:
                valid += 1
            if game.result == 0:
                black_win += 1
            if game.result == 1:
                white_win += 1
            total_count += 1
        if total_count > 1000:
            exit = True
            break

csv_file.close()
print(total_count)
print(black_win)
print(white_win)
print(valid)
