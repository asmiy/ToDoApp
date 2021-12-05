import unittest
import os
from app import app, db, Task


class TestToDoApp(unittest.TestCase):
    def setUp(self):
        db.create_all()
        db.session.add(Task(title="test", state=False))
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_database(self):
        tester = os.path.exists("tasks.db")
        self.assertTrue(tester)

    def test_display(self):
        self.assertTrue(
            db.session.query(Task).filter(Task.title == "test").first() is not None)

    def test_update(self):
        task = db.session.query(Task).filter(Task.title == "test").first()
        old_state = task.state
        task.update_state()
        db.session.commit()
        self.assertTrue(db.session.query(Task).filter(Task.state != old_state).first() is not None)

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
