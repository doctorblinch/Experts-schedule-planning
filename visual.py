import streamlit as st


def presentation_page():
    st.markdown(markdown2string('data/markdown/presentation_page.md'))


def solution_page():
    st.title('Сторінка з рішенням задачі')
    input_type = st.selectbox('Оберіть спосіб вхідних даних', ['File', 'Data Base', 'Random'])
    if st.button('Ok') and input_type == 'Random':
        st.balloons()


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
