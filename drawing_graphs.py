from math import log10
import matplotlib.pyplot as plt
# this file was made to draw graph (size of area -- correlation of fluctuations in this area)
# so it contains some very specific functions - use and modify with care


def get_parameters_from_filename(filename):  # data are stored in format 'filename correlation'
    parameters = filename.split("shift")[-1].split("_")[1:]
    lattice_size = list(map(int, parameters[0].split("x")))  # количество точек в формате NxМ
    step = int(parameters[-1][:-3])
    return step, lattice_size[0], lattice_size[1], step * lattice_size[0]


def import_data(filename):
    x_arr, y_arr = [], []
    f = open(filename, 'r')
    temp = f.readline()  # нужно, так как первая строка содержит описание формата файла
    while True:
        try:
            temp = f.readline().split()
            if len(temp) == 2:
                x_arr.append(get_parameters_from_filename(temp[0])[3])
                y_arr.append(abs(float(temp[1])))
            else:
                return x_arr, y_arr
        except:
            print("Something went wrong at extracting from file")


def import_data_log(filename):
    x_arr, y_arr = [], []
    f = open(filename, 'r')
    temp = f.readline()  # нужно, так как первая строка содержит описание формата файла
    while True:
        try:
            temp = f.readline().split()
            if len(temp) == 2:
                x_arr.append(log10(get_parameters_from_filename(temp[0])[3]))
                y_arr.append(log10(abs(float(temp[1]))))
            else:
                return x_arr, y_arr
        except:
            print("Something went wrong at extracting from file")


def import_shifts(filename):
    x_arr, y_arr = [], []
    f = open(filename, 'r')
    while True:
        try:
            temp = list(map(float, f.readline().split()))
            if len(temp) == 2:
                x_arr.append(temp[0])
                y_arr.append(temp[1])
            else:
                return x_arr, y_arr
        except:
            print("Something went wrong at extracting from file")


def draw_corr_graph(filename, name="График скоррелированности смещений в зависимости от размера области"):
    x, y = import_data(filename)
    plt.scatter(x, y, marker='x', s=16, color='black')
    plt.xlabel('Size of area, mks')
    plt.ylabel('Correlation')
    plt.title(name)
    plt.show()


def draw_corr_graph_log(filename, name="График скоррелированности смещений в зависимости от размера области"):
    x, y = import_data_log(filename)
    plt.scatter(x, y, marker='x', s=16, color='black')
    plt.xlabel('Size of area, mks')
    plt.ylabel('Correlation')
    plt.title(name + ".\n Логарифмический масштаб")
    plt.show()


def draw_shift(filename):
    x, y = import_shifts(filename)
    print(x)
    print(y)

    plt.scatter(x, y)
    plt.xlabel('dx')
    plt.ylabel('dy')
    #plt.scatter(x[20:40], y[20:40], color='b')
    plt.show()


def draw_shifted_lattice(filename):
    dx, dy = import_shifts(filename)
    lattice_size_x = get_parameters_from_filename(filename)[1]
    lattice_size_y = get_parameters_from_filename(filename)[2]
    lattice_step = 20
    x = [lattice_step * (i % lattice_size_x) + dx[i] for i in range(len(dx))]
    y = [lattice_step * (i // lattice_size_y) + dy[i] for i in range(len(dy))]
    plt.scatter(x, y, s=4)
    plt.xlabel("x' for " + str(get_parameters_from_filename(filename)[0]) + "mks grid")
    plt.ylabel("y'")
    plt.show()


draw_corr_graph_log("correlations_with_E_from_largest_scale.txt", "Матожидание - взято с наибольшей решетки")
draw_corr_graph_log("correlations_with_E_0.txt", "Матожидание = 0")
#draw_shift("C:\\Projects\\Astro\\data\\shift\\shift_20x20_1008895mks")
#draw_shifted_lattice("C:\\Projects\\Astro\\data\\shift\\shift_20x20_1513342mks")
