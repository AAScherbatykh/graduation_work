import sqlite3
import unittest
from datetime import datetime

# import os
from src import db
from src.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_database()

    # @classmethod
    # def tearDownClass(cls):
    #     os.remove('task_manager.db')

    def test_add_task(self):
        TaskManager.add_task(
            'Тест', 'Тестовое описание', 'Высокий',
            datetime.combine(datetime.now(), datetime.min.time()),
            'Новая')

        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()

        # проверка наличия записи по названию задачи
        cursor.execute(
            "SELECT * FROM tasks WHERE title=? AND description=? AND "
            "priority=? AND ""status=?",
            ('Тест',
             'Тестовое описание',
             'Высокий',
             'Новая',
             ))
        task = cursor.fetchone()

        self.assertIsNotNone(task, 'Тестовая запись не обнаружена.')
        self.assertEqual(task[1], 'Тест', 'Тестовая запись не верна.')
        self.assertEqual(
            task[2],
            'Тестовое описание',
            'Тестовая запись не верна.')
        self.assertEqual(task[3], 'Высокий', 'Тестовая запись не верна.')
        self.assertEqual(task[5], 'Новая', 'Тестовая запись не верна.')

        cursor.close()
        connection.close()

    def test_delete_task(self):
        connection = sqlite3.connect('task_manager.db')
        cursor = connection.cursor()

        # найти ID удаляемой записи
        cursor.execute(
            "SELECT id FROM tasks WHERE title=? AND description=? AND "
            "priority=? AND status=?",
            ('Тест',
             'Тестовое описание',
             'Высокий',
             'Новая',
             ))
        task = cursor.fetchone()
        ident = task[0]

        TaskManager.delete_task(int(ident))

        # проверка наличия записи по названию задачи
        cursor.execute(
            "SELECT * FROM tasks WHERE title=? AND description=? AND "
            "priority=? AND status=?",
            ('Тест',
             'Тестовое описание',
             'Высокий',
             'Новая',
             ))
        task = cursor.fetchone()
        self.assertIsNone(task, 'Тестовая запись не удалена.')

        cursor.close()
        connection.close()


if __name__ == '__main__':
    unittest.main()
