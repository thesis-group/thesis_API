# coding=utf-8
import random
import numpy as np


if __name__ == '__main__':
    la = 0.3
    N = 100000
    xs = [random.expovariate(la) for i in range(N)]
    ps = np.cumsum(xs)

    exp = 10
    var = 3

    exp2 = 0.8
    var2 = 0.2

    txtName = "./data.txt"
    f = open(txtName, "a+")

    for i in range(0, N):
        cd = random.normalvariate(exp, var)
        if cd < 0:
            cd = 0.5
        rd = random.normalvariate(exp2, var2) * cd
        ls = cd * 2.5
        f.write(str(ps[i]))
        f.write(',')
        f.write(str(cd))
        f.write(',')
        f.write(str(rd))
        f.write(',')
        f.write(str(ls))
        f.write('\n')
    f.close()
