from flask import Flask, render_template
from flask_restful import Api
from resources import TaskResource, TaskListResource
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:superuser@localhost/todo_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api = Api(app)

# Add resources to the API
api.add_resource(TaskListResource, '/tasks')  # List of tasks
api.add_resource(TaskResource, '/tasks/<int:task_id>')  # Specific task

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
