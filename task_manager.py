import sqlite3
from datetime import datetime


class TaskManager:
    """ Класс, описывающий планировщик задач.

    """
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
        created_at: datetime = datetime.now()

        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO tasks (title, description, priority, deadline,
                status, created_at)
                VALUES(?, ?, ?, ?, ?, ?)""", (title, description, priority,
                deadline, status, created_at)
                )

        connection.commit()
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

        connection.close()

        return tasks

    @staticmethod
    def search_tasks(filter: str = ''):
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

            sql_query = """
            SELECT * FROM tasks t WHERE t.title LIKE ?
            OR t.description LIKE ?
            OR t.priority LIKE ?
            OR t.status LIKE ?
            """

            cursor.execute(sql_query, [f"%{filter}%"] * 4)
            tasks: list = cursor.fetchall()

            connection.close()

        return tasks

    @staticmethod
    def get_sorted_tasks(fields: list) -> list:
        """ Сортировка задач по заданному полю или нескольким полям.
            По умолчанию - по возрастанию.

        Args:
            fields: Список полей.

        Returns:
            Список отсортированных задач.

        """
        if len(fields) == 0:
            return TaskManager.get_tasks_all()
        else:
            connection = sqlite3.connect('task_manager.db')
            cursor = connection.cursor()

            sql_query = f'SELECT * FROM tasks ORDER BY {", ".join(fields)}'

            cursor.execute(sql_query)
            tasks: list = cursor.fetchall()

            connection.close()
            return tasks
        