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

        return None

    def __restore_init_lists(self):
        zipped_pairs = zip(self.experts, self.indices)
        zipped_pairs = sorted(zipped_pairs, key=lambda pair: pair[1])
        self.experts = [i for i, j in zipped_pairs]
        self.indices = [j for i, j in zipped_pairs]

        return None

    def __target_function(self, res_list=None):
        result = 0
        outside_res_list = False
        if res_list is None:
            outside_res_list = True
            res_list = self.experts_res_list

        for expert, i in zip(self.experts, res_list):
            result += (expert[1] - expert[0]) * i

        if outside_res_list:
            self.tf_res = result

        return result

    def __compute_previous_intervals(self):
        start = [i[0] for i in self.experts]
        finish = [i[1] for i in self.experts]

        prev = []
        for j in range(len(self.experts)):
            i = bisect.bisect_right(finish, start[j]) - 1
            prev.append(i)

        return prev

    def __compute_solution(self, j, p, opt):
        if j >= 0:
            if self.experts[j][1] - self.experts[j][0] + opt[p[j]] > opt[j - 1]:
                self.experts_res_list[self.indices[j]] = 1
                self.__compute_solution(p[j], p, opt)
            else:
                self.__compute_solution(j - 1, p, opt)

        return None

    def greedy_algorithm(self, pos=None):
        outside_pos = False
        if pos is None:
            outside_pos = True
            pos = [1 for _ in self.experts]

        result_list = [0 for _ in self.experts]

        while 1 in pos:
            max_len = -1
            max_index = -1
            for i in range(len(self.experts)):
                if pos[i] == 1 and self.experts[i][1] - self.experts[i][0] > max_len:
                    max_len = self.experts[i][1] - self.experts[i][0]
                    max_index = i

            result_list[max_index] = 1
            pos[max_index] = 0

            for i in range(len(self.experts)):
                if self.experts[max_index][0] < self.experts[i][1] and self.experts[max_index][1] > self.experts[i][0]:
                    pos[i] = 0

        if outside_pos:
            self.experts_res_list = result_list
            self.__target_function()
            self.solution_method = 'Greedy algorithm'

        return result_list

    def recursive_optimization(self, first_loop=True):
        if first_loop:
            self.greedy_algorithm()

        length = len(self.experts)
        spaces_values = [0 for _ in range(length + 1)]
        spaces_indices = [-1 for _ in range(length + 1)]

        end_prev = min(self.experts, key=lambda expert: expert[0])[0]
        end_max = max(self.experts, key=lambda expert: expert[1])[1]
        index_prev = -1

        for i in range(length):
            if self.experts_res_list[i] == 1:
                spaces_values[i] = self.experts[i][0] - end_prev
                spaces_indices[i] = index_prev
                end_prev = self.experts[i][1]
                index_prev = i

        spaces_values[length] = end_max - end_prev
        spaces_indices[length] = index_prev

        while sum(spaces_values) != 0:
            max_index = spaces_values.index(max(spaces_values))

            pos = [1 for _ in self.experts]

            if max_index != length:
                pos[max_index] = 0

            if spaces_indices[max_index] != -1:
                pos[spaces_indices[max_index]] = 0
            new_res_list = self.greedy_algorithm(pos)
            new_tf_res = self.__target_function(new_res_list)

            if new_tf_res > self.tf_res:
                spaces_values = [0 for _ in range(length + 1)]
                self.experts_res_list = new_res_list
                self.tf_res = new_tf_res
                self.recursive_optimization(first_loop=False)
            else:
                spaces_values[max_index] = 0

        self.solution_method = 'Greedy algorithm + recursive optimization'
        return None

    def dynamic_algorithm(self):
        self.experts_res_list = [0 for _ in self.experts]
        self.__sort_init_lists()

        prev = self.__compute_previous_intervals()

        opt = collections.defaultdict(int)
        opt[-1] = 0
        opt[0] = 0
        for j in range(1, len(self.experts)):
            opt[j] = max(self.experts[j][1] - self.experts[j][0] + opt[prev[j]], opt[j - 1])

        self.__compute_solution(len(self.experts) - 1, prev, opt)

        self.__restore_init_lists()
        self.__target_function()
        self.solution_method = 'Dynamic programming algorithm'

        return None


if __name__ == '__main__':
    example = ExpertsTask(EXPERTS)
    print('Experts =', example.experts)
    print('X =', example.experts_res_list)
    print('Z =', example.tf_res)
    print(example.solution_method)
    print('--------------------------------')
    example.greedy_algorithm()
    print('Experts =', example.experts)
    print('X =', example.experts_res_list)
    print('Z =', example.tf_res)
    print(example.solution_method)
    print('--------------------------------')
    example.recursive_optimization()
    print('Experts =', example.experts)
    print('X =', example.experts_res_list)
    print('Z =', example.tf_res)
    print(example.solution_method)
    print('--------------------------------')
    example.dynamic_algorithm()
    print('Experts =', example.experts)
    print('X =', example.experts_res_list)
    print('Z =', example.tf_res)
    print(example.solution_method)
