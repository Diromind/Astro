SHIFT = 0.0000001  # переменная сдвига элемента массива констант, для подсчета девиации


def get_expectation(filename):
    dataset = open(filename, 'r')

    x_arr = []
    y_arr = []

    while True:
        try:
            temp = list(map(float, dataset.readline().split()))
            if len(temp) == 4:
                x_arr.append(temp[2] - temp[0])
                y_arr.append(temp[3] - temp[1])
            if len(temp) == 2:
                x_arr.append(temp[0])
                y_arr.append(temp[1])
            if len(temp) < 2:
                dataset.close()
                return sum(x_arr) / len(x_arr), sum(y_arr) / len(y_arr)
        except:
            dataset.close()
            return sum(x_arr) / len(x_arr), sum(y_arr) / len(y_arr)


def comparator(x):
    index = int(x.split("_")[-1][:-3])
    return index


def dev(vector, mean=0):  # считает девиацию с матожиданием mean i.e. sqrt(sum[x_i]^2)
    res = 0
    for i in range(len(vector)):
        res += (vector[i] - mean) ** 2
    return res ** 0.5


def cov(vector1, vector2, mean1=0, mean2=0):  # считает ковариацию с заданными средними
    res = 0
    for i in range(len(vector2)):
        res += (vector1[i] - mean1) * (vector2[i] - mean2)
    return res


def corr(vector1, vector2, mean1=0, mean2=0):  # считает корреляцию с заданными матожиданиями
    res = cov(vector1, vector2, mean1, mean2)
    dev1, dev2 = dev(vector1, mean1), dev(vector2, mean2)
    if dev1 == 0:
        vector1[-1] += SHIFT
        dev1 = dev(vector1, mean1)
    if dev2 == 0:
        vector2[-1] += SHIFT
        dev2 = dev(vector2, mean2)
    return res / (dev1 * dev2)


def corr_of_dataset(filename,
                    expectation):  # this function reads file of format 'dx dy' or 'x y newx newy' and returns correlation
    dataset = open(filename, 'r')

    x_arr = []
    y_arr = []

    while True:
        try:
            temp = list(map(float, dataset.readline().split()))
            if len(temp) == 4:
                x_arr.append(temp[2] - temp[0])
                y_arr.append(temp[3] - temp[1])
            if len(temp) == 2:
                x_arr.append(temp[0])
                y_arr.append(temp[1])
            if len(temp) < 2:
                return corr(x_arr, y_arr, expectation[0], expectation[1])
        except:
            dataset.close()
            return corr(x_arr, y_arr, expectation[0], expectation[1])


def main():  # параметр отвечает, какая именно функция будет использована для подсчета корреляции
    #  1 обозначает обычную корреляцию Пирсона, 2 обозначает ее же, но с допущением, что среднее обоих векторов = 0
    fout1 = open("correlations_with_E_from_largest_scale.txt", 'w')
    print("File consists of data in format: 'filename correlation'", file=fout1)
    fout2 = open("correlations_with_E_0.txt", 'w')
    print("File consists of data in format: 'filename correlation'", file=fout2)

    # TODO - add in list below names of files, where
    files_to_analyse = ['C:\Projects\Astro\data\shift\shift_20x20_' + str(5 * 2 ** i) + 'mks' for i in range(17)]
    iterator = 1024
    while iterator < 2000000:
        files_to_analyse.append('C:\Projects\Astro\data\shift\shift_20x20_' + str(iterator) + 'mks')
        iterator = iterator * 3 // 2
    files_to_analyse.sort(key=comparator, reverse=True)

    mean_at_largest_scale = get_expectation(files_to_analyse[0])

    for filename in files_to_analyse:
        print(filename, corr_of_dataset(filename, mean_at_largest_scale), file=fout1)
        print("analyzing", filename)
        print(filename, corr_of_dataset(filename, (0, 0)), file=fout2)
        print("analyzing", filename)

    fout1.close()
    fout2.close()

    return 0


main()
