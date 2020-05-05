from algorithms import ExpertsTask
import random
import timeit
import time
import math
import matplotlib.pyplot as plt

N = 5000


def generate_experts(n):
    exps = []

    for _ in range(n):
        b = random.randint(1, 200)
        e = random.randint(b + 1, int(50 + b))
        exps.append((b, e))

    return exps


def execution_time():
    start = timeit.default_timer()
    exps_task.greedy_algorithm()
    end = timeit.default_timer()
    return (end - start) * 1000


if __name__ == '__main__':
    amounts = range(1, N + 1)
    comp_log = [n * math.log(n, 2) / 7000 for n in amounts]
    comp_sq = [n * n / 500000 for n in amounts]

    times = []
    exps_list = []
    for i in range(1, N + 1):
        # b = random.randint(1, 200)
        # e = random.randint(b, int(40 + b * 0.8))
        # exps_list.append((b, e))
        exps_list = generate_experts(i)
        exps_task = ExpertsTask(exps_list)

        times.append(execution_time())

    plt.plot(amounts, times, amounts, comp_log, 'red')
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Amount of experts')
    plt.show()
