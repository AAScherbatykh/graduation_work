import sqlite3
from datetime import datetime


class TaskManager:
    """ Класс, описывающий планировщик задач.

    """

    def add_task(self, title: str, description: str,
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
            f'''INSERT INTO tasks (title, description, priority, deadline, status, created_at)
                    VALUES('{title}', '{description}', '{priority}', '{deadline}', '{status}', '{created_at}'
                    ) ''')

        connection.commit()
        connection.close()

    def get_tasks_all(self) -> list:
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

    def search_tasks(self, filter: str):
        """ Фильтрация задач по условию фильтрации.

        Args:
            filter: Условие фильтрации.

        Returns:
            Список отфильтрованных задач.

        """

        if filter.strip() == '':
            tasks: list = self.get_tasks_all()

        else:
            connection = sqlite3.connect('task_manager.db')
            cursor = connection.cursor()

            sql_query = (
                f"""SELECT * FROM tasks t WHERE t.title LIKE '%{filter}%'
            OR t.description LIKE '%{filter}%'
            OR t.priority LIKE '%{filter}%'
            OR t.status LIKE '%{filter}%'""")
            # print(sql_query)
            cursor.execute(sql_query)
            tasks: list = cursor.fetchall()

            connection.close()

        return tasks

    def get_sorted_tasks(self, fields: list) -> list:
        """ Сортировка задач по заданному полю или нескольким полям.
            По умолчанию - по возрастанию.

        Args:
            fields: Список полей.

        Returns:
            Список отсортированных задач.

        """
        if len(fields) == 0:
            return self.get_tasks_all()
        else:
            connection = sqlite3.connect('task_manager.db')
            cursor = connection.cursor()

            sql_query = f'SELECT * FROM tasks ORDER BY {", ".join(fields)}'
            print(sql_query)
            cursor.execute(sql_query)
            tasks: list = cursor.fetchall()

            connection.close()
            return tasks


#if __name__ == '__main__':

    #task1: TaskManager = TaskManager()
    # task1.add_task('Проект 1', 'Закупка канцтоваров', 'высокий', '30.11.2024', 'в работе')
    # task1.add_task('Проект 2', 'День охраны труда', 'высокий', '01.12.2024', 'запланирован')
    # task1.add_task('Проект 3', 'Встреча с банком', 'средний', '05.12.2024', 'запланирован')
    # print(task1.search_tasks('охраны'))
    #print(task1.get_sorted_tasks(['description', 'title']))
    #print(task1.search_tasks(' '))