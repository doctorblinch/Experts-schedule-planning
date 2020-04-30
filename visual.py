import streamlit as st
import SessionState
import os

from db import get_presets_conditions


def presentation_page():
    st.markdown(markdown2string('data/markdown/presentation_page.md'))


def file_selector(folder_path='./data/input_files'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


def show_answer():
    st.title('answer')
    st.balloons()


def solution_page():
    st.title('Сторінка з рішенням задачі')

    session_state = SessionState.get(choose_button=False, input_type='', random='', file='', db='')
    session_state.input_type = st.selectbox('Оберіть спосіб вхідних даних', ['File', 'Data Base', 'Random'])


#    if session_state.choose_button:
    if session_state.input_type == 'Random':
            quantity = st.number_input('Кількість експертів', step=1, value=5, min_value=1, max_value=50)
            min_val = st.number_input('Мінімальне значеня', step=1, value=1, min_value=1, max_value=999)
            max_val = st.number_input('Максимальне значеня', step=1, value=40, min_value=1, max_value=999)
            distribution = st.selectbox('Оберіть розподіл випадкових велечин', ['Рівномірне', 'Нормальне'])

            if st.button('Solve'):
                show_answer()


        # st.sparkles()
        # st.rainbows()
        # st.giphy("unicorns")
        # кол-во, значения от до, и распределния

    if session_state.input_type == 'Data Base':
        conditions = get_presets_conditions()
        st.dataframe(conditions, width=1000)
        st.number_input('Input ID', step=1, value=1, min_value=1, max_value=len(conditions))
        if st.button('Solve'):
            show_answer()

        # метод решения

    if session_state.input_type == 'File':
        filename = file_selector()
        st.write('Ви обрали `%s`' % filename)
        st.write(parse_condition_csv(filename))
        st.button('Solve')


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


def main():
    st.sidebar.title("Оберіть сторінку:")
    pages = ['Presentation', 'Solve', 'Technical details']
    page = st.sidebar.radio("Навігація", options=pages)

    if page == 'Presentation':
        presentation_page()
        # описание алгоритмов

    if page == 'Solve':
        solution_page()

    if page == 'Technical details':
        technical_page()

main()