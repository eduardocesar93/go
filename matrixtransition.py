import csv
from game import nesting

files = [
    "data-test",
    "data",
    "matrix-simulated",
    "random-simulated"
]

directory = "results"
lim = 1000
nesting_list = []

for file in files:
    matrix = []
    with open('{0}/{1}/Transition Matrix.csv'.format(directory, file), 'r') \
            as csv_file:
        reader = csv.reader(csv_file, lineterminator='\n')
        for i, line in enumerate(reader):
            new_line = []
            for num in line:
                new_line.append(int(num))
            matrix.append(new_line)
    nesting_list.append(nesting(matrix, lim))

with open('{0}/{1}.csv'.format(directory, 'nesting.csv'), 'w') as csv_file:
    writer = csv.writer(csv_file, lineterminator='\n')
    for i in range(len(files)):
        writer.writerow([files[i], nesting_list[i]])
