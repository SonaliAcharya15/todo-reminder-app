from flask import request
from flask_restful import Resource
from models import Task
from database import db

class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get(task_id)
        if task:
            return {
                'id': task.id,
                'title': task.title,
                'completed': task.completed,
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        return {'message': 'Task not found'}, 404

    def put(self, task_id):
        task = Task.query.get(task_id)
        if task:
            data = request.get_json()
            if 'title' in data and data['title'].strip() == '':
                return {'message': 'Task title cannot be empty'}, 400
            
            task.completed = data.get('completed', task.completed)  # Only update completed status if provided
            if 'title' in data and data['title'].strip() != '':
                task.title = data['title']
            db.session.commit()
            return {'message': 'Task updated'}, 200
        return {'message': 'Task not found'}, 404

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted'}, 200
        return {'message': 'Task not found'}, 404

class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return [{
            'id': task.id,
            'title': task.title,
            'completed': task.completed,
            'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for task in tasks]

    def post(self):
        data = request.get_json()
        if Task.query.filter_by(title=data['title']).first():
            return {'message': 'Task title already exists'}, 400  # Check for duplicate titles
        
        new_task = Task(title=data['title'])
        db.session.add(new_task)
        db.session.commit()
        return {'message': 'Task added', 'id': new_task.id}, 201

    def delete(self):
        Task.query.delete()
        db.session.commit()
        return {'message': 'All tasks deleted'}, 200
