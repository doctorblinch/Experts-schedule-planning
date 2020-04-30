import bisect
import collections

EXPERTS = [(1, 14), (2, 7), (7, 16), (14, 22), (18, 28), (25, 30), (28, 35), (30, 34), (34, 40)]

# N = 10
# EXPERTS = [(b:=random.randint(1, 50), random.randint(b, 50)) for i in range(N)]


class ExpertsTask:
    def __init__(self, experts_list):
        self.experts = experts_list
        self.experts_res_list = [0 for _ in experts_list]
        self.tf_res = 0
        self.solution_method = None
        self.indices = list(range(len(experts_list)))

    def __sort_init_lists(self):
        zipped_pairs = zip(self.experts, self.indices)
        zipped_pairs = sorted(zipped_pairs, key=lambda pair: pair[0][1])
        self.experts = [i for i, j in zipped_pairs]
        self.indices = [j for i, j in zipped_pairs]

    def __restore_init_lists(self):
        zipped_pairs = zip(self.experts, self.indices)
        zipped_pairs = sorted(zipped_pairs, key=lambda pair: pair[1])
        self.experts = [i for i, j in zipped_pairs]
        self.indices = [j for i, j in zipped_pairs]

    def __target_function(self):
        z = 0

        for expert, i in zip(self.experts, self.experts_res_list):
            z += (expert[1] - expert[0]) * i
        self.tf_res = z

        return None

    def __compute_previous_intervals(self):
        start = [i[0] for i in self.experts]
        finish = [i[1] for i in self.experts]

        p = []
        for j in range(len(self.experts)):
            i = bisect.bisect_right(finish, start[j]) - 1
            p.append(i)

        return p

    def __compute_solution(self, j, p, opt):
        if j >= 0:
            if self.experts[j][1] - self.experts[j][0] + opt[p[j]] > opt[j - 1]:
                self.experts_res_list[self.indices[j]] = 1
                self.__compute_solution(p[j], p, opt)
            else:
                self.__compute_solution(j - 1, p, opt)

    def greedy_algorithm(self):
        self.experts_res_list = [0 for _ in self.experts]
        pos = [1 for _ in self.experts]

        while 1 in pos:
            max_len = -1
            max_index = -1
            for i in range(len(self.experts)):
                if pos[i] == 1 and self.experts[i][1] - self.experts[i][0] > max_len:
                    max_len = self.experts[i][1] - self.experts[i][0]
                    max_index = i

            self.experts_res_list[max_index] = 1
            pos[max_index] = 0

            for i in range(len(self.experts)):
                if self.experts[max_index][0] <= self.experts[i][1] and self.experts[max_index][1] > self.experts[i][0]:
                    pos[i] = 0

        self.__target_function()
        self.solution_method = 'Greedy algorithm'

        return None

    def recursive_optimization(self):
        pass

    def dynamic_algorithm(self):
        self.experts_res_list = [0 for _ in self.experts]
        self.__sort_init_lists()

        p = self.__compute_previous_intervals()

        opt = collections.defaultdict(int)
        opt[-1] = 0
        opt[0] = 0
        for j in range(1, len(self.experts)):
            opt[j] = max(self.experts[j][1] - self.experts[j][0] + opt[p[j]], opt[j - 1])

        self.__compute_solution(len(self.experts) - 1, p, opt)

        self.__restore_init_lists()
        self.__target_function()
        self.solution_method = 'Dynamic programming algorithm'

        return None


if __name__ == '__main__':
    example = ExpertsTask(EXPERTS)
    print(example.experts)
    print(example.experts_res_list)
    print(example.tf_res)
    print(example.solution_method)
    print('--------------------------------')
    example.greedy_algorithm()
    print(example.experts)
    print(example.experts_res_list)
    print(example.tf_res)
    print(example.solution_method)
    print('--------------------------------')
    example.dynamic_algorithm()
    print(example.experts)
    print(example.experts_res_list)
    print(example.tf_res)
    print(example.solution_method)
