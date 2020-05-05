import random
import os


def configure_height4graph_from_condition(condition):
    min_val = min([i[0] for i in condition])
    max_val = max([i[1] for i in condition])

    height_lines = [[0] * (max_val + 1) for i in range(len(condition))]

    new_condition = []
    for section in condition:
        layer = layer_that_can_be_added(height_lines, section)
        new_condition.append((section[0], section[1], layer))

    return new_condition


def layer_that_can_be_added(height_lines, value):
    start, finish = value
    if start != 0:
        start -= 1
    can_be_added = False
    layer = 0
    while not can_be_added:
        for i in height_lines[layer][start:finish + 1]:
            if i == 1:
                layer += 1
                can_be_added = False
                break
            else:
                can_be_added = True

    else:
        for i in range(start, finish + 1):
            height_lines[layer][i] = 1

    return layer


def create_file_with_condition(condition):
    names = {name for root, dirs, files in os.walk('data/input_files') for name in files}
    available_name_found = False
    skeleton = 'condition_{}.csv'
    i = 1
    while not available_name_found:
        if skeleton.format(i) not in names:
            available_name_found = True
            with open('data/input_files/' + skeleton.format(i), 'w') as f:
                for i in condition:
                    f.write('{},{}\n'.format(i[0], i[1]))
        else:
            i += 1


def markdown2string(file_path):
    with open(file_path, 'r') as f:
        string = f.read()

    return string


def parse_condition_csv(path):
    experts = []
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                experts.append(
                    tuple(map(int, line.strip().split(',')))
                )
    except:
        return 'Wrong file format!'

    return experts


def generate_random_condition(quantity, min_val, max_val, distribution):
    condition = []
    if distribution == 'Нормальний':
        for _ in range(quantity):
            a = int(random.normalvariate((max_val + min_val) / 2, (max_val + min_val) / 5))
            b = int(random.normalvariate((max_val + min_val) / 2, (max_val + min_val) / 5))
            a = max_val if a > max_val else a
            a = min_val if a < min_val else a
            b = max_val if b > max_val else b
            b = min_val if b < min_val else b
            condition.append((min(a, b), max(a, b)))
    elif distribution == 'Рівномірний':
        for _ in range(quantity):
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            condition.append((min(a, b), max(a, b)))

    return condition


# EXPERTS = [(1, 14), (2, 7), (7, 16), (14, 22), (18, 28), (25, 30), (28, 35), (30, 34), (34, 40)]
#EXPERTS = [(2, 4), (2, 4), (5, 7), (2, 4)]
#print(configure_height4graph_from_condition(EXPERTS))
