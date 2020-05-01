import streamlit as st
import SessionState
import random
import os

from db import get_presets_conditions, write_task_to_db, show_db
from algorithms import ExpertsTask


def presentation_page():
    st.markdown(markdown2string('data/markdown/presentation_page.md'))


def file_selector(folder_path='./data/input_files'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


def show_answer(condition, write_to_db=True):
    st.balloons()
    st.title('Відповідь')
    task = ExpertsTask(condition)
    task.dynamic_algorithm()
    st.write(task.tf_res)
    st.write(task.experts_res_list)
    if write_to_db:
        write_task_to_db(condition, task.experts_res_list, task.tf_res, method=task.solution_method)


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


def solution_page():
    st.title('Сторінка з рішенням задачі')

    session_state = SessionState.get(choose_button=False, input_type='', random='', file='', db='')
    session_state.input_type = st.selectbox('Оберіть спосіб вхідних даних', ['File', 'Data Base', 'Random'])

    if session_state.input_type == 'Random':
        quantity = st.number_input('Кількість експертів', step=1, value=5, min_value=1, max_value=50)
        min_val = st.number_input('Мінімальне значеня', step=1, value=1, min_value=1, max_value=999)
        max_val = st.number_input('Максимальне значеня', step=1, value=40, min_value=1, max_value=999)
        distribution = st.selectbox('Оберіть розподіл випадкових велечин', ['Рівномірний', 'Нормальний'])

        if st.button('Розв\'язати'):
            condition = generate_random_condition(quantity, min_val, max_val, distribution)
            st.write('Згенерували наступну умову: {}'.format(condition))
            show_answer(condition)
    # кол-во, значения от до, и распределния

    if session_state.input_type == 'Data Base':
        conditions = get_presets_conditions()
        st.table(conditions)
        session_state.condition_id2solve = st.number_input('Введіть ID', step=1, value=1, min_value=1, max_value=len(conditions))

        condition2solve = list(filter(lambda cond: cond.get('task_id') == session_state.condition_id2solve, conditions))[0]
        if st.button('Розв\'язати'):
            show_answer(condition2solve.get('experts', []))

        # метод решения

    if session_state.input_type == 'File':
        filename = file_selector()
        st.write('Ви обрали `%s`' % filename)
        condition = parse_condition_csv(filename)
        st.write(condition)
        if st.button('Розв\'язати'):
            show_answer(condition)


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


def technical_page():
    st.title('Технічна сторінка')
    st.write('Данна сторінка розповість про технічні рішення які були використані в данному проекті')
    st.markdown(markdown2string('data/markdown/technical_page.md'))


def show_db_page():
    st.title('База данних')
    tasks, conditions, solutions = show_db()
    st.write('Задачі:')
    st.table(tasks)
    st.write('Умови:')
    st.table(conditions)
    st.write('Розв\'язки:')
    st.table(solutions)


def main():
    st.sidebar.title("Оберіть сторінку:")
    pages = ['Presentation', 'Solve', 'Show DB', 'Technical details']
    page = st.sidebar.radio("Навігація", options=pages)

    if page == 'Show DB':
        show_db_page()

    if page == 'Presentation':
        presentation_page()
        # описание алгоритмов

    if page == 'Solve':
        solution_page()

    if page == 'Technical details':
        technical_page()


main()
