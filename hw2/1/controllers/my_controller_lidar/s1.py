import numpy as np
import matplotlib.pyplot as plot
import math
import random


def data_builder(data, degree):
    x_array = []
    y_array = []
    for i in range(0, degree):
        x_array.append((data[i] * math.cos(i * math.pi / 180)))
        y_array.append((data[i] * math.sin(i * math.pi / 180)))
    return x_array, y_array


def scatter_plot(x_array, y_array):
    plot.scatter(x_array, y_array)
    plot.show()


def read_from_file():
    data = []
    with open('a.txt', 'r') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            data.append(round(float(currentPlace), 5))
    return data


def shebhe_inverse(x, y):
    x_np = np.array(x)
    y_np = np.array(y)
    data_np_array = np.vstack((x_np, y_np)).T
    data_transpose = data_np_array.transpose()
    matrix = np.dot(data_transpose, data_np_array)
    mat_inv = np.linalg.inv(matrix)
    mult = np.dot(mat_inv, data_transpose)
    const = np.ones(shape=(data_np_array.shape[0], 1))
    a, b = np.dot(mult, const)[:, 0]
    m = -a / b
    c = 1 / b
    ytemp = m * x_np + c
    plot.scatter(x_np, y_np)
    plot.plot(x_np, ytemp, 'r')
    plot.grid()
    plot.show()


def ransac(x, y):
    best_count = float(-(math.inf))
    best_m = 0
    best_c = 0
    max_dis = 0.15
    check = 120
    x_np = np.array(x)
    y_np = np.array(y)
    data = np.vstack((x_np, y_np)).T
    for i in range(check):
        inlier_count = 0
        temp1 = random.randint(0, len(data) - 1)
        temp2 = random.randint(0, len(data) - 1)
        while temp1 == temp2: temp2 = random.randint(0, len(data) - 1)
        m = (data[temp1][1] - data[temp2][1]) / (data[temp1][0] - data[temp2][0])
        c = (-1 * m) * (data[temp1][0] + data[temp1][1])
        for i in range(0, len(data)):
            if i == temp1 or i == temp2: continue
            distance = abs((-1 * m) * data[i][0] + data[i][1] - c) / math.sqrt(m * m + 1)
            if distance < max_dis:
                inlier_count += 1
        if inlier_count > best_count:
            best_count = inlier_count
            best_m = m
            best_c = c
    ytemp = best_m * x_np + best_c
    plot.scatter(x_np, y_np)
    plot.plot(x_np, ytemp, 'r')
    plot.grid()
    plot.show()


def get_most_distanse(data):
    dmax = 0
    index = -1
    temp1 = 0
    temp2 = len(data) - 1
    for i in range(temp1 + 1, temp2):
        m = (data[temp1][1] - data[temp2][1]) / (data[temp1][0] - data[temp2][0])
        c = (-1 * m) * (data[temp1][0] + data[temp1][1])
        distance = abs((-1 * m) * data[i][0] + data[i][1] - c) / math.sqrt(m * m + 1)
        if (distance > dmax):
            index = i
            dmax = distance
    return dmax, index


def split_and_merge(data, threshold):
    if len(data) < 5:
        return [data]
    d, ind = get_most_distanse(data)
    if d > threshold:
        d1, ind1 = get_most_distanse(data[:ind + 1, :])
        d2, ind2 = get_most_distanse(data[ind:, :])
        p1 = split_and_merge(data[:ind + 1], threshold)  # split and merge left array
        p2 = split_and_merge(data[ind:], threshold)  # split and merge right array
        points = p1 + p2
    else:
        points = [data]
    return points


def main1():
    data = read_from_file()
    degree = 90
    x, y = data_builder(data, degree)
    dtype = [("x", float), ("y", float)]
    # scatter_plot(x, y)
    # shebhe_inverse(x,y)
    # ransac(x,y)
    x_np = np.array(x)
    y_np = np.array(y)
    data = np.vstack((x_np, y_np)).T

    # data = np.sort(data, order=0)

    columnIndex = 0
    # Sort 2D numpy array by 2nd Column
    data = data[data[:, columnIndex].argsort()]
    a = split_and_merge(data, 0.3)
    plot.scatter(x_np, y_np)

    for i in range(len(a)):
        x1 = a[i][0][0]
        y1 = a[i][0][1]
        x2 = a[i][-1][0]
        y2 = a[i][-1][1]
        plot.plot([x1, x2], [y1, y2], linestyle='-')

    # len(a)

    plot.show()


main1()
