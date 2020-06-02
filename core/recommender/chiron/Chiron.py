import random


def roulette(ls):
    i = 1
    l = len(ls)

    while i < l:
        ls[i] = ls[i] + ls[i - 1]
        i = i + 1

    r = random.randint(0, ls[l - 1] - 1)

    # print ls

    i = 0
    while i < l:
        if r < ls[i]:
            return i

        i = i + 1
