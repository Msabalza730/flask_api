from flask import Flask, request, jsonify
from datetime import datetime

from database import tasks, setup

app = Flask(__name__)
setup.create_tables()


#Enlazar con la url se utiliza el decorator
@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    created_date = datetime.now().strftime('%x')

    data = (title, created_date)
    task_id = tasks.insert_task(data)

    if task_id:
        task = tasks.select_task_by_id(task_id)
        return jsonify({'task': task})
    return jsonify({'message': 'Internal Error'})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    data = tasks.select_all_tasks()

    if data:
        return jsonify({'tasks': data})
    elif data == False:
        return jsonify({'message': 'Internal Error'})
    else:
        return jsonify({'tasks': {}})


@app.route('/tasks', methods=['PUT'])
def update_task():
    title = request.json['title']
    id_arg = request.args.get('id')

    if tasks.update_task(id_arg, (title,)):
        task = tasks.select_task_by_id(id_arg)
        return jsonify(task)
    return jsonify({'message': 'Internal Error'})


@app.route('/tasks', methods=['DELETE'])
def delete_task():
    id_arg = request.args.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({'message': 'Task Deleted'})
    return jsonify({'message': 'Internal Error'})


@app.route('/tasks/completed', methods=['PUT'])
def complete_task():
    id_arg = request.args.get('id')
    completed = request.args.get('completed')

    if tasks.complete_task(id_arg, completed):
        return jsonify({'message': 'Succesfully'})
    return jsonify({'message': 'Internal Error'})


if __name__ == '__main__':
    app.run(debug=True)