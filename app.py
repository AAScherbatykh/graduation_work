from datetime import datetime

import pandas as pd
import streamlit as st

from src import db
from src.task_manager import TaskManager

# Интерфейс Streamlit
st.set_page_config(page_title="Список дел")
st.title('Список дел')


# Создание базы данных
try:
    db.create_database()
except Exception as ex:
    st.error(f'Возникла ошибка создания базы данных: {ex}')

# Форма для добавления задачи
with st.form(key='add_task_form', clear_on_submit=True):
    title: str | None = st.text_input('Название задачи')
    description: str | None = st.text_area('Описание задачи')
    priority = st.selectbox('Приоритет', ['Низкий', 'Средний', 'Высокий'])
    deadline = st.date_input('Дедлайн', datetime.today())
    status = st.selectbox('Статус', ['Новая', 'В процессе', 'Завершена'])

    submit_button: bool = st.form_submit_button(label='Добавить задачу')

    if submit_button:
        try:
            TaskManager.add_task(
                title,
                description,
                priority,
                datetime.combine(
                    deadline,
                    datetime.min.time()),
                status)
            st.success('Задача добавлена!')
        except Exception as ex:
            st.error(f'Возникла ошибка добавления задачи: {ex}')

# Фильтрация и поиск задач
tasks: list = []
search_query: str | None = st.text_input('Поиск задач')
if search_query:
    tasks: list = TaskManager.search_tasks(search_query)
else:
    selected_options: list = st.multiselect(
        'Сортировать по', ['Название', 'Описание', 'Приоритет',
                           'Дедлайн', 'Статус', 'Создано'])
    descending = st.checkbox('Сортировка по убыванию')
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
    tasks: list = TaskManager.get_sorted_tasks(
        selected_options, not descending)


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

    # Удаление записей
    event = st.dataframe(
        df_tasks,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="multi-row",
    )
    rows = event.selection.rows
    ids: list = df_tasks.iloc[rows]['ID'].values.tolist()

    del_button = st.button(label='Удалить')

    if del_button and len(ids) > 0:
        for i in range(len(ids)):
            TaskManager.delete_task(ids[i])
        st.rerun()

else:
    st.write("Нет задач для отображения.")
