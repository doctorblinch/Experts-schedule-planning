import random

import streamlit as st
import SessionState
import os

from db import get_presets_conditions, write_task_to_db, show_db
from bokeh.plotting import figure
from bokeh.models import HoverTool
from algorithms import ExpertsTask
from functions import create_file_with_condition, markdown2string, parse_condition_csv, generate_random_condition, configure_height4graph_from_condition


def presentation_page():
    st.markdown(markdown2string('data/markdown/presentation_page.md'))
    st.markdown('''## 3. Складність алгоритмів
        
На графіках далі ми будемо бачити залежність часу 
виконання алгоритму від кількості експертів.
        
### 3.1 Жадібний алгоритм
        
Як бачимо на малюнку жадібний алгоритм емперично має складність 
$O(N) = N * log(N)$ 
        
Для 2000 експертів:''')
    st.image('data/pictures/greedy2000.png')
    st.write('Для 5000 експетів:')
    st.image('data/pictures/greedy5000.png')

    st.markdown('''
### 3.2 Жадібний алгоритм + рекурсивний оптимізатор

Як бачимо на малюнку жадібний алгоритм разом з рекурсивним оптимізатором емперично має складність 
$O(N) = N * log(N)$ 

Для 2000 експертів''')
    st.image('data/pictures/recursive2000.png')
    st.write('Для 5000 експертів')
    st.image('data/pictures/recursive5000.png')

    st.markdown('''
### 3.3 Динамічний алгоритм

Як бачимо на малюнку динамічний алгоритм емперично має складність 
$O(N) = N * log(N)$

Для 2000 експертів 
    ''')
    st.image('data/pictures/dynamic2000.png')
    st.write('Для 5000 експертів')
    st.image('data/pictures/dynamic5000.png')

    st.markdown('''
    
Для наглядності зобразимо роботу усіх трьох алгоритмів на одному графіку

Для 2000 експертів 
        ''')
    st.image('data/pictures/comparison2000.png')
    st.write('Для 5000 експертів')
    st.image('data/pictures/comparison5000.png')

    st.markdown('''
### 3.5 Порівняння точності алгоритмів

Для подальшого аналізу візьмемо розв’язок динамічного алгоритму як оптимальний для
даної задачі та порівняємо з ним розв’язки інших алгоритмів. На графіках зображено
залежність відхилення значення цільової функції від оптимального значення по кількості
експертів для жадібного алгоритму та алгоритму з рекурсивним покращувачем.

Для 2000 експертів 
        ''')
    st.image('data/pictures/deviation2000.png')
    st.write('Для 5000 експертів')
    st.image('data/pictures/deviation5000.png')

    st.markdown('''
    Залежність часу роботи алгоритмів від вхідних границь часу для генераії експертів,
    причому максимальний час роботи одного експерта обмежений ≤200:
            ''')
    st.image('data/pictures/rightlimit1.png')
    st.markdown('''
        Залежність часу роботи алгоритмів від вхідних границь часу для генераії експертів,
        причому максимальний час роботи одного експерта також збільшується в залежності від
        кількості простору для генерації експертів:
                ''')
    st.image('data/pictures/rightlimit2.png')


def file_selector(folder_path='./data/input_files'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


def show_answer(condition, method='Метод динамічного програмування', write_to_db=False):
    st.balloons()
    st.title('Відповідь')
    task = ExpertsTask(condition)
    if method == 'Метод динамічного програмування':
        task.dynamic_algorithm()
    elif method == 'Жадібний алгоритм + рекурсивний покращувач':
        task.greedy_algorithm()
        task.recursive_optimization()

    st.write('Метод розв\'язання - "{}"'.format(task.solution_method))
    st.write('Значення цільової функції = {}.'.format(task.tf_res))
    st.write('Вектор взятих експертів X={}.'.format(task.experts_res_list))
    if write_to_db:
        write_task_to_db(condition, task.experts_res_list, task.tf_res, method=task.solution_method)

    pss = configure_height4graph_from_condition(task.experts)
    # st.write(pss)
    _tools_to_show = 'box_zoom,pan,save,hover,reset,tap,wheel_zoom'
    p = figure(height=200, tools=_tools_to_show)
    for i in range(len(pss)):
        p.line([pss[i][0], pss[i][1]], [pss[i][2], pss[i][2]],
               color='red' if task.experts_res_list[i] == 1 else 'blue',
               line_width=4, line_dash="solid")
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Start", "@x"), ]
    hover.mode = 'mouse'

    st.bokeh_chart(p)
    st.write('На графіку червоні проміжкі відповідають обраним експертам, сині - не обраним.')


def solution_page():
    st.title('Сторінка з розв\'язанням задачі')

    session_state = SessionState.get(choose_button=False, input_type='', random='', file='', db='')
    session_state.input_type = st.selectbox('Оберіть спосіб вхідних даних', ['File', 'Data Base', 'Random'])

    if session_state.input_type == 'Random':
        quantity = st.number_input('Кількість експертів', step=1, value=50, min_value=1, max_value=500)
        min_val = st.number_input('Мінімальне значеня', step=1, value=1, min_value=1, max_value=99999)
        max_val = st.number_input('Максимальне значеня', step=1, value=1000, min_value=1, max_value=99999)
        max_len = st.number_input('Максимальна тривалість роботи експерта',
                                  step=1, value=200, min_value=1, max_value=99999)
        distribution = st.selectbox('Оберіть розподіл випадкових велечин',
                                    ['Рівномірний', 'Усічений нормальний',
                                     'Рівномірний для відрізків обмеженної довжини'])

        method = st.selectbox('Оберіть метод вирішення задачі',
                              ['Метод динамічного програмування',
                               'Жадібний алгоритм + рекурсивний покращувач',
                               'Обидва метода']
                              )

        if st.button('Розв\'язати'):
            condition = generate_random_condition(quantity, min_val, max_val, distribution, max_len)
            st.write('Згенерували наступну умову: {}'.format(condition))
            st.bokeh_chart(draw_graphic_of_condition(condition))

            if method == 'Обидва метода':
                show_answer(condition, 'Метод динамічного програмування')
                show_answer(condition, 'Жадібний алгоритм + рекурсивний покращувач')
            else:
                show_answer(condition, method)

    if session_state.input_type == 'Data Base':
        conditions = get_presets_conditions()
        st.table(conditions)
        session_state.condition_id2solve = st.number_input('Введіть ID', step=1, value=1, min_value=1,
                                                           max_value=len(conditions))

        condition2solve = list(filter(
            lambda cond: cond.get('task_id') == session_state.condition_id2solve, conditions)
        )[0]
        method = st.selectbox('Оберіть метод вирішення задачі',
                              ['Метод динамічного програмування',
                               'Жадібний алгоритм + рекурсивний покращувач',
                               'Обидва метода']
                              )

        if st.button('Розв\'язати'):
            show_answer(condition2solve.get('experts', []), method)

    if session_state.input_type == 'File':
        filename = file_selector()
        st.write('Ви обрали `%s`' % filename)
        condition = parse_condition_csv(filename)
        st.bokeh_chart(draw_graphic_of_condition(condition))
        # st.write(condition)
        method = st.selectbox('Оберіть метод вирішення задачі',
                              ['Метод динамічного програмування',
                               'Жадібний алгоритм + рекурсивний покращувач',
                               'Обидва метода']
                              )
        if st.button('Розв\'язати'):
            show_answer(condition, method)


@st.cache(allow_output_mutation=True)
def get_condition_state():
    return []


def create_condition_page():
    st.title('Сторінка для створення власної умови задачі')
    annotation = get_condition_state()
    if st.button('Додати експерта'):
        annotation.append(tuple())

    if st.button('Видалити останнього експерта'):
        annotation.pop(len(annotation)-1)

    for i in range(len(annotation)):
        st.subheader('Експерт №{}'.format(i + 1))
        a = st.number_input('Початок роботи {}-го експерта'.format(i + 1), step=1, value=5, min_value=1, max_value=100)
        b = st.number_input('Кінець роботи {}-го експерта'.format(i + 1), step=1, value=20, min_value=1, max_value=100)
        annotation[i] = (a, b)

    if st.button('Візуалізувати'):
        st.bokeh_chart(draw_graphic_of_condition(annotation))
    if st.button('Створити'):
        create_file_with_condition(annotation)


def draw_graphic_of_condition(cond):
    colors = ['firebrick', 'navy', 'green', 'yellow', 'red', 'blue', 'pink', 'orange',
              '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#d62728']
    pss = configure_height4graph_from_condition(cond)
    # st.write(pss)
    _tools_to_show = 'box_zoom,pan,save,hover,reset,tap,wheel_zoom'
    p = figure(height=200, tools=_tools_to_show)
    for i in range(len(pss)):
        p.line([pss[i][0], pss[i][1]], [pss[i][2], pss[i][2]], color=random.choice(colors), line_width=4,
               line_dash="solid")
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Time", "@x"), ]
    hover.mode = 'mouse'
    return p


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
    pages = ['Presentation', 'Solve', 'Show DB', 'Create condition', 'Technical details']
    page = st.sidebar.radio("Навігація", options=pages)

    if page == 'Show DB':
        show_db_page()

    if page == 'Presentation':
        presentation_page()

    if page == 'Solve':
        solution_page()

    if page == 'Technical details':
        technical_page()

    if page == 'Create condition':
        create_condition_page()


if __name__ == __main__:
    main()
