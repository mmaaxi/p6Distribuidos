from flask import Flask, request, jsonify, abort
from collections import defaultdict

app = Flask(__name__)

# Almacenaremos las tareas en memoria
tasks = [
    {'id': 1, 'title': 'Aprender Flask', 'completed': False},
    {'id': 2, 'title': 'Hacer ejercicio', 'completed': True},
    {'id': 3, 'title': 'Leer un libro', 'completed': False},
    {'id': 4, 'title': 'Comprar víveres', 'completed': True},
    {'id': 5, 'title': 'Trabajar en el proyecto', 'completed': False},
    {'id': 6, 'title': 'Llamar a la familia', 'completed': True},
    {'id': 7, 'title': 'Actualizar CV', 'completed': False},
]
task_counter = 1  # Contador para asignar IDs únicos a las tareas

# Filtros posibles para las tareas
VALID_FILTERS = ['completed', 'pending']

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Obtener lista de tareas con paginación y filtros opcionales.
    """
    # Paginación
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    
    # Filtro de estado
    status_filter = request.args.get('status', None)
    if status_filter and status_filter not in VALID_FILTERS:
        abort(400, description="Invalid filter. Use 'completed' or 'pending'.")
    
    # Filtrar tareas
    filtered_tasks = tasks
    if status_filter == 'completed':
        filtered_tasks = [task for task in tasks if task['completed']]
    elif status_filter == 'pending':
        filtered_tasks = [task for task in tasks if not task['completed']]
    
    # Paginación
    start = (page - 1) * per_page
    end = start + per_page
    paginated_tasks = filtered_tasks[start:end]
    
    return jsonify(paginated_tasks)


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Crear una nueva tarea.
    """
    global task_counter
    data = request.get_json()
    
    if not data or 'title' not in data:
        abort(400, description="Title is required.")
    
    task = {
        'id': task_counter,
        'title': data['title'],
        'completed': False
    }
    tasks.append(task)
    task_counter += 1
    
    return jsonify(task), 201


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Obtener una tarea por su ID.
    """
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found.")
    
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Actualizar una tarea por su ID.
    """
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found.")
    
    data = request.get_json()
    if 'title' in data:
        task['title'] = data['title']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Eliminar una tarea por su ID.
    """
    global tasks
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found.")
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return jsonify({'message': 'Task deleted successfully'})


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': error.description}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': error.description}), 404


if __name__ == '__main__':
    app.run(debug=True)
