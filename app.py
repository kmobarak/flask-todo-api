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

# Route for retrieving paginated tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Query tasks with pagination
    tasks = Task.query.paginate(page, per_page, error_out=False)
    
    # Format response
    tasks_data = [{'id': task.id, 'title': task.title, 'done': task.done} for task in tasks.items]

    return jsonify({
        'tasks': tasks_data,
        'total': tasks.total,
        'pages': tasks.pages,
        'current_page': tasks.page
    })

# Test route to check the server is running
@app.route('/test')
def test():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    with app.app_context():  # Create the app context
        db.create_all()      # Creates the database tables
    app.run(debug=True)
