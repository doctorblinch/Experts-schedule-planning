from algorithms import ExpertsTask
import random
import timeit
import time
import math
import matplotlib.pyplot as plt
from functions import generate_random_condition

N = 1000


def generate_experts(n):
    exps = []

    for _ in range(n):
        b = random.randint(1, 200)
        e = random.randint(b + 1, int(50 + b))
        exps.append((b, e))

    return exps


def execution_time_greedy(exps_task):
    start = timeit.default_timer()
    exps_task.greedy_algorithm()
    end = timeit.default_timer()
    return (end - start) * 1000


def execution_time_recursive(exps_task):
    start = timeit.default_timer()
    exps_task.recursive_optimization()
    end = timeit.default_timer()
    return (end - start) * 1000


def execution_time_dynamic(exps_task):
    start = timeit.default_timer()
    exps_task.dynamic_algorithm()
    end = timeit.default_timer()
    return (end - start) * 1000


def complexity_plots():
    amounts = range(1, N + 1)

    times_greedy = []
    times_recursive = []
    times_dynamic = []

    tf_greedy = []
    tf_recursive = []
    tf_dynamic = []

    for i in range(1, N + 1):
        # b = random.randint(1, 200)
        # e = random.randint(b, int(40 + b * 0.8))
        # exps_list.append((b, e))
        exps_list = generate_random_condition(i, 1, 1000, 'Рівномірний для відрізків обмеженної довжини', 200)
        exps_task = ExpertsTask(exps_list)

        times_greedy.append(execution_time_greedy(exps_task))
        tf_greedy.append(exps_task.tf_res)

        times_recursive.append(execution_time_recursive(exps_task))
        tf_recursive.append(exps_task.tf_res)

        times_dynamic.append(execution_time_dynamic(exps_task))
        tf_dynamic.append(exps_task.tf_res)

    comp_log = [n * math.log(n, 2) / 5000 for n in amounts]
    comp_sq = [n * n / 400000 for n in amounts]
    plt.plot(amounts, times_greedy, amounts, comp_log, comp_sq, 'red')
    plt.legend(['f(N)', 'N*log(N)', 'N^2'])
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Amount of experts')
    plt.show()

    comp_log = [n * math.log(n, 2) / 500 for n in amounts]
    comp_sq = [n * n / 30000 for n in amounts]
    plt.plot(amounts, times_recursive, amounts, comp_log, comp_sq, 'red')
    plt.legend(['f(N)', 'N*log(N)', 'N^2'])
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Amount of experts')
    plt.show()

    comp_log = [n * math.log(n, 2) / 7000 for n in amounts]
    comp_sq = [n * n / 500000 for n in amounts]
    plt.plot(amounts, times_dynamic, amounts, comp_log, comp_sq, 'red')
    plt.legend(['f(N)', 'N*log(N)', 'N^2'])
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Amount of experts')
    plt.show()

    plt.plot(amounts, times_recursive, 'mediumpurple', amounts, times_greedy, amounts, times_dynamic, 'limegreen')
    plt.legend(['Recursive optimization', 'Greedy algorithm', 'dynamic algorithm'])
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Amount of experts')
    plt.show()

    eval_greedy = [abs(((j - i) / j) * 100) for i, j in zip(tf_greedy, tf_dynamic)]
    eval_recursive = [abs(((j - i) / j) * 100) for i, j in zip(tf_recursive, tf_dynamic)]

    plt.plot(amounts, eval_greedy, amounts, eval_recursive, 'limegreen')
    plt.legend(['Greedy algorithm', 'Recursive optimization'])
    plt.ylabel('Deviation from the optimal value (in %)')
    plt.xlabel('Amount of experts')
    plt.show()


def limits_plots():
    right_limits = [i * 1000 for i in range(1, 101, 10)]
    max_len = [i * 100 for i in range(1, 101, 10)]

    times_greedy = []
    times_recursive = []
    times_dynamic = []

    tf_greedy = []
    tf_recursive = []
    tf_dynamic = []

    for i, j in zip(right_limits, max_len):
        exps_list = generate_random_condition(N, 1, i, 'Рівномірний для відрізків обмеженної довжини', j)
        exps_task = ExpertsTask(exps_list)

        times_greedy.append(execution_time_greedy(exps_task))
        tf_greedy.append(exps_task.tf_res)

        times_recursive.append(execution_time_recursive(exps_task))
        tf_recursive.append(exps_task.tf_res)

        times_dynamic.append(execution_time_dynamic(exps_task))
        tf_dynamic.append(exps_task.tf_res)

    plt.plot(right_limits, times_recursive, 'mediumpurple', right_limits, times_greedy, right_limits, times_dynamic, 'limegreen')
    plt.legend(['Recursive optimization', 'Greedy algorithm', 'dynamic algorithm'])
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Right limit of the end point')
    plt.show()

if __name__ == '__main__':
    limits_plots()