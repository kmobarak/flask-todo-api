from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Route for retrieving all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()  

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
