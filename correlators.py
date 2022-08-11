SHIFT = 0.0000001  # переменная сдвига элемента массива констант, для подсчета девиации


def dev(vector):  # считает девиацию i.e. sqrt(sum[x - mean_x]^2)
    mean = sum(vector) / len(vector)
    #mean = 0  # РУБРИКА ЭКСССПЕРИМЕНТЫ ЧАСТЬ 1
    res = 0
    for i in range(len(vector)):
        res += (vector[i] - mean) ** 2
    return res ** 0.5


def cov(vector1, vector2):  # считает ковариацию
    mean1 = sum(vector1) / len(vector1)
    mean2 = sum(vector2) / len(vector2)
    res = 0
    #mean1, mean2 = 0, 0  # РУБРИКА ЭКСССПЕРИМЕНТЫ ЧАСТЬ 2
    for i in range(len(vector2)):
        res += (vector1[i] - mean1) * (vector2[i] - mean2)
    return res


def corr(vector1, vector2):
    res = cov(vector1, vector2)
    dev1, dev2 = dev(vector1), dev(vector2)
    if dev1 == 0:
        vector1[-1] += SHIFT
        dev1 = dev(vector1)
    if dev2 == 0:
        vector2[-1] += SHIFT
        dev2 = dev(vector2)
    return res / (dev1 * dev2)


def corr_of_dataset(filename):  # this function reads file of format 'dx dy' or 'x y newx newy' and returns correlation
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
                return corr(x_arr, y_arr)
        except:
            dataset.close()
            return corr(x_arr, y_arr)


def main():
    fout = open("correlations.txt", 'w')
    print("File consists of data in format: 'filename correlation'", file=fout)

    # TODO - add in list below names of files, where
    files_to_analyse = ['C:\Projects\Astro\data\shift\shift_20x20_' + str(5 * 2 ** i) + 'mks' for i in range(17)]

    for filename in files_to_analyse:
        print(filename, corr_of_dataset(filename), file=fout)
        print("analyzing", filename)

    fout.close()

    return 0


main()
