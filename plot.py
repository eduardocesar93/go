import matplotlib.pyplot as plt
import csv
import math
import numpy as np
from scipy import stats


def scatter_plot(label, data, directory, output_name, x_label, y_label, width=11.7, height=8.27, linear_regression=True,
                 log=False):
    fig, ax = plt.subplots()
    fig.set_size_inches(width, height)
    if log:
        output_name += ' [Log]'
        y_label += ' [Log]'
        x_label += ' [Log]'
        label += ' [Log]'
        x_log = []
        y_log = []
        for i in range(len(data[0])):
            if data[0][i] != 0 and data[1][i] != 0:
                x_log.append(math.log10(data[0][i]))
                y_log.append(math.log10(data[1][i]))
        data[0] = x_log
        data[1] = y_log
    ax.set(xlabel=x_label, ylabel=y_label, title=output_name)
    plt.scatter(data[0], data[1], color='b', label=label)
    min_x = min(data[0])
    max_x = max(data[0])
    plt.xlim(min_x, max_x)
    plt.grid(True)
    if linear_regression:
        slope, intercept, r_value, p_value, std_err = stats.linregress(data[0], data[1])
        data_linear_regression = [slope * data[0][i] + intercept for i in range(len(data[0]))]
        plt.plot(data[0], data_linear_regression, color='r', label='Linear Regression')
        plt.text(0.8, 0.2, 'Linear Regression: {0:.4f}x + {0:.4f}'.format(round(slope, 4), round(intercept, 4)) + '\n'
                 + 'r-value: {0}'.format(round(r_value, 4)) + '\n'
                 + 'p-value: {0}'.format(round(p_value, 4)), ha='center', va='center',
                 transform=ax.transAxes)
    plt.savefig('{0}/{1}.png'.format(directory, output_name))
    plt.clf()
    plt.close(fig)


def colormap(data, directory, output_name, x_label, y_label, width=11.7, height=8.27, percentile=False):
    fig, ax = plt.subplots()
    fig.set_size_inches(width, height)
    percentile_max = 100
    if percentile:
        percentile_max = percentile
    # max_value = np.percentile(data, percentile_max)
    ax.set(xlabel=x_label, ylabel=y_label, title=output_name)
    # mesh = ax.imshow(data, cmap='rainbow', vmin=0, vmax=max_value)
    mesh = ax.imshow(data, cmap='Greys', vmin=0, vmax=1)
    plt.colorbar(mesh, ax=ax)
    plt.show()
    # plt.savefig('{0}/{1}.png'.format(directory, output_name))
    plt.clf()
    plt.close(fig)


def save_scatter_csv(data, directory, output_name, labels=False):
    with open('{0}/{1}.csv'.format(directory, output_name), 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        if labels:
            writer.writerow(labels)
        for i in range(len(data[0])):
            writer.writerow([data[0][i], data[1][i]])


def save_matrix_csv(data, directory, output_name, labels=False):
    with open('{0}/{1}.csv'.format(directory, output_name), 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        if labels:
            writer.writerow(labels)
        for i in range(len(data)):
            row = []
            for j in range(len(data[i])):
                row.append(data[i][j])
            writer.writerow(row)
