import sqlite3
from datetime import datetime


class TaskManager:
    """ Класс, описывающий планировщик задач."""

    @staticmethod
    def add_task(title: str, description: str,
                 priority: str, deadline: datetime, status: str):
        """ Добавление задачи.

        Args:
            title: Название задачи.
            description: Описание задачи.
            priority: Приоритет задачи.
            deadline: Дедлайн.
            status: Статус задачи.

        """
        now = datetime.now()
        created_at: datetime = now.strftime("%d.%m.%Y %H:%M:%S")

        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO tasks (title, description, priority, deadline,
            status, created_at) VALUES(?, ?, ?, ?, ?, ?)""",
            (title, description, priority, deadline, status, created_at))

        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_tasks_all() -> list:
        """ Получение всех задач.

        Returns:
            Список всех задач.

        """
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM tasks')
        tasks: list = cursor.fetchall()

        cursor.close()
        connection.close()

        return tasks

    @staticmethod
    def search_tasks(filter: str = '') -> list:
        """ Фильтрация задач по условию фильтрации.

        Args:
            filter: Условие фильтрации.

        Returns:
            Список отфильтрованных задач.

        """
        if filter.strip() == '':
            tasks: list = TaskManager.get_tasks_all()
        else:
            connection = sqlite3.connect('task_manager.db')
            cursor = connection.cursor()

            sql_query: str = """
            SELECT * FROM tasks t WHERE t.title LIKE ?
            OR t.description LIKE ?
            OR t.priority LIKE ?
            OR t.status LIKE ?
            """

            cursor.execute(sql_query, [f"%{filter}%"] * 4)
            tasks: list = cursor.fetchall()

            cursor.close()
            connection.close()

        return tasks

    @staticmethod
    def get_sorted_tasks(fields: list, ascending: bool = True) -> list:
        """ Сортировка задач по заданному полю или нескольким полям.
            По умолчанию - по возрастанию.

        Args:
            fields: Список полей.
            ascending: Тип сортировки - по возрастанию или по убыванию.

        Returns:
            Список отсортированных задач.

        """
        if len(fields) == 0:
            return TaskManager.get_tasks_all()
        else:
            connection = sqlite3.connect('task_manager.db')
            cursor = connection.cursor()

            if ascending:
                rule_sort = 'ASC'
            else:
                rule_sort = 'DESC'

            sql_query: str = (f'SELECT * FROM tasks ORDER BY '
                              f'{", ".join(fields)} {rule_sort}')

            cursor.execute(sql_query)
            tasks: list = cursor.fetchall()

            cursor.close()
            connection.close()
            return tasks

    @staticmethod
    def delete_task(ident: int):
        """ Удаление записи по id записи.

        Args:
            ident: id записи.

        """
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()

        cursor.execute('DELETE FROM tasks WHERE id = ?', [ident])

        connection.commit()
        cursor.close()
        connection.close()
