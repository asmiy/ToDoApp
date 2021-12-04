import unittest
import os
from flask import Flask
from app import app


class TestToDoApp(unittest.TestCase):

    def test_database(self):
        tester = os.path.exists("tasks.db")
        self.assertTrue(tester)

    def test_index(self):
        tester = app.test_client(self)
        pages = ['/']
        for page in pages:
            response = tester.get(page, content_type='html/text')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
