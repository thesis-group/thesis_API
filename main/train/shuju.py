# coding=utf-8
import random
import numpy as np

la = 0.3
exp = 10
var = 3

exp2 = 0.8
var2 = 0.2


def write_data(file, N):
    xs = [random.expovariate(la) for i in range(N)]
    ps = np.cumsum(xs)

    for i in range(0, N):
        cd = random.normalvariate(exp, var)
        if cd < 0:
            cd = 0.5
        rd = random.normalvariate(exp2, var2) * cd
        ls = cd * 2.5
        file.write(str(ps[i]))
        file.write(',')
        file.write(str(cd))
        file.write(',')
        file.write(str(rd))
        file.write(',')
        file.write(str(ls))
        file.write('\n')


if __name__ == '__main__':
    with open('train_data.txt', mode='a+') as f:
        write_data(f, 80 * 1000)  # 80组，每组1000个
    with open('data.txt', mode='a+')as f:
        write_data(f, 20 * 1000)
