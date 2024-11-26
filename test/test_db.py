import os
import unittest

from src import db


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_database()

    # @classmethod
    # def tearDownClass(cls):
    #     os.remove('task_manager.db')

    def test_create_database(self):
        self.assertTrue(
            os.path.exists('task_manager.db'),
            'Путь до файла базы данных не существует.')
        self.assertTrue(
            os.path.isfile('task_manager.db'),
            'Файл базы данных не существует.')


if __name__ == '__main__':
    unittest.main()
