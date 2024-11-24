import streamlit as st
import pandas as pd
import db
from datetime import datetime
from task_manager import TaskManager

# Создание базы данных
db.create_database()

# Интерфейс Streamlit
st.title('Список дел')

# Форма для добавления задачи
with st.form(key='add_task_form'):
    title: str | None = st.text_input('Название задачи')
    description: str | None = st.text_area('Описание задачи')
    priority = st.selectbox('Приоритет', ['Низкий', 'Средний', 'Высокий'])
    deadline = st.date_input('Дедлайн', datetime.today())
    status = st.selectbox('Статус', ['Новая', 'В процессе', 'Завершена'])

    submit_button: bool = st.form_submit_button(label='Добавить задачу')

    if submit_button:
        TaskManager.add_task(
            title,
            description,
            priority,
            datetime.combine(
                deadline,
                datetime.min.time()),
            status)
        st.success('Задача добавлена!')

# Фильтрация и поиск задач
tasks: list = []
search_query: str | None = st.text_input('Поиск задач')
if search_query:
    tasks: list = TaskManager.search_tasks(search_query)
else:
    selected_options: list = st.multiselect(
        'Сортировать по', ['Название', 'Описание', 'Приоритет',
                           'Дедлайн', 'Статус', 'Создано'])
    column_names: dict = {
        'Название': 'title',
        'Описание': 'description',
        'Приоритет': 'priority',
        'Дедлайн': 'deadline',
        'Статус': 'status',
        'Создано': 'created_at'
    }

    for i in range(len(selected_options)):
        selected_options[i] = column_names[selected_options[i]]
    tasks: list = TaskManager.get_sorted_tasks(selected_options)

# Отображение задач
if tasks:
    df_tasks: pd.DataFrame = pd.DataFrame(tasks)
    df_tasks.columns = [
        'ID',
        'Название',
        'Описание',
        'Приоритет',
        'Дедлайн',
        'Статус',
        'Создано']

    st.write(df_tasks)
else:
    st.write("Нет задач для отображения.")
