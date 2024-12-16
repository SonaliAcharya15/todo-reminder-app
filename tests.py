import unittest
import json
from app import app, db
from models import Task

class ToDoAppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and create a new database for each test."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:superuser@localhost/todo_app_test'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.app = app.test_client()  # Move this below config
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the database after each test."""
        with app.app_context():
            db.drop_all()

    def test_add_task(self):
        """Test adding a new task."""
        response = self.app.post('/tasks', data=json.dumps({'title': 'Test Task'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Task added', response.data)

    def test_get_tasks(self):
        """Test retrieving the list of tasks."""
        self.app.post('/tasks', data=json.dumps({'title': 'Test Task'}),
                      content_type='application/json')
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_edit_task(self):
        """Test editing a task."""
        self.app.post('/tasks', data=json.dumps({'title': 'Test Task'}),
                      content_type='application/json')
        response = self.app.put('/tasks/1', data=json.dumps({'title': 'Updated Task', 'completed': False}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task updated', response.data)

    def test_delete_task(self):
        """Test deleting a task."""
        self.app.post('/tasks', data=json.dumps({'title': 'Test Task'}),
                      content_type='application/json')
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task deleted', response.data)

    def test_clear_all_tasks(self):
        """Test deleting all tasks."""
        self.app.post('/tasks', data=json.dumps({'title': 'Test Task 1'}),
                      content_type='application/json')
        self.app.post('/tasks', data=json.dumps({'title': 'Test Task 2'}),
                      content_type='application/json')
        response = self.app.delete('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All tasks deleted', response.data)

if __name__ == '__main__':
    unittest.main()
