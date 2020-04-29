import streamlit as st
import os


def presentation_page():
    st.markdown(markdown2string('data/markdown/presentation_page.md'))


def file_selector(folder_path='./data/input_files'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


def solution_page():
    st.title('Сторінка з рішенням задачі')
    input_type = st.selectbox('Оберіть спосіб вхідних даних', ['File', 'Data Base', 'Random'])
    if st.button('Обрати'):
        if input_type == 'Random':
            st.button('Solve')

        if input_type == 'Data Base':
            st.dataframe([1,23,4])
            st.number_input('Input ID')
            st.button('Solve')

        if input_type == 'File':
            filename = file_selector()
            st.write('Ви обрали `%s`' % filename)
            st.button('Solve')


def markdown2string(file_path):
    with open(file_path, 'r') as f:
        string = f.read()

    return string


def technical_page():
    st.title('Технічна сторінка')
    st.write('Данна сторінка розповість про технічні рішення які були використані в данному проекті')
    st.markdown(markdown2string('data/markdown/technical_page.md'))


if __name__ == '__main__':
    st.sidebar.title("Оберіть сторінку:")
    pages = ['Presentation', 'Solve', 'Technical details']
    page = st.sidebar.radio("Навігація", options=pages)

    if page == 'Presentation':
        presentation_page()

    if page == 'Solve':
        solution_page()

    if page == 'Technical details':
        technical_page()
