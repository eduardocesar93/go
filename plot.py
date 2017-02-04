import numpy as np
import matplotlib.pyplot as plt
import pylab
import csv
import math
from scipy import stats


def line_plot(label, data, directory, output_name, x_label, y_label, width=11.7, height=8.27, linear_regression=True,
              log=False):
    fig, ax = plt.subplots()
    fig.set_size_inches(width, height)
    if log:
        output_name += ' [Log]'
        y_label += ' [Log]'
        x_label += ' [Log]'
        label += ' [Log]'
        data[0] = [math.log10(data[0][i]) for i in range(len(data[0]))]
        data[1] = [math.log10(data[1][i]) for i in range(len(data[1]))]
    ax.set(xlabel=x_label, ylabel=y_label, title=output_name)
    plt.plot(data[0], data[1], color='b', label=label)
    plt.grid(True)
    if linear_regression:
        slope, intercept, r_value, p_value, std_err = stats.linregress(data[0], data[1])
        data_linear_regression = [slope * data[0][i] + intercept for i in range(data[0])]
        plt.plot(data[0], data_linear_regression, color='r', label='Linear Regression')
        plt.text(0.8, 0.8, 'Linear Regression: {0:.2f}x + {0:.2f}'.format(round(slope, 4)) + '\n'
                 + 'r-value: {0}'.format(round(r_value, 4)) + '\n'
                 + 'p-value: {0}'.format(round(p_value, 4)), ha='center', va='center',
                 transform=ax.transAxes)
    pylab.savefig('{0}/{1}.png'.format(directory, output_name))
    pylab.clf()
    plt.close(fig)


def colormap(data, directory, output_name, x_label, y_label, width=11.7, height=8.27, percentile=False):
    fig, ax = plt.subplots()
    fig.set_size_inches(width, height)
    max_value = 0
    plot_data = data.values
    if percentile:
        max_value = np.percentile(plot_data, percentile)
    ax.set(xlabel=x_label, ylabel=y_label, title=output_name)
    masked_array = np.ma.array(plot_data)
    mesh = ax.pcolormesh(masked_array, cmap='rainbow', vmin=0, vmax=max_value)
    plt.colorbar(mesh, ax=ax)
    pylab.savefig("{0}/{1}.png".format(directory, output_name), bbox_inches='tight')
    pylab.clf()
    plt.close(fig)


def save_scatter_csv(data, directory, output_name, labels=False):
    with open('{0}/{1}.csv'.format(directory, output_name), 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        if labels:
            writer.writerow(labels)
        for i in range(len(data[0])):
            writer.writerow([data[0][i], data[1][1]])


def save_matrix_csv(data, directory, output_name, labels=False):
    with open('{0}/{1}.csv'.format(directory, output_name), 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        if labels:
            writer.writerow(labels)
        for i in range(len(data)):
            for j in range(len(data[i])):
                writer.writerow([data[i][j], data[i][j]])
