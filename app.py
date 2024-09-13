from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Route for retrieving tasks with filtering and sorting
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Filtering based on 'done' status
    done_param = request.args.get('done')
    query = Task.query

    if done_param is not None:
        done_value = done_param.lower() == 'true'
        query = query.filter_by(done=done_value)

    # Sorting logic
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    if sort_order == 'desc':
        query = query.order_by(db.desc(getattr(Task, sort_by)))
    else:
        query = query.order_by(db.asc(getattr(Task, sort_by)))

    tasks = query.all()

    # Format response
    tasks_data = [{'id': task.id, 'title': task.title, 'done': task.done} for task in tasks]

    return jsonify({'tasks': tasks_data})

# Test route to check the server is running
@app.route('/test')
def test():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    with app.app_context():  # Create the app context
        db.create_all()      # Creates the database tables
    app.run(debug=True)
