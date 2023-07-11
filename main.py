import os

from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
stack = []

SWAGGER_URL = '/swagger'  # URL de l'interface Swagger UI
current_dir = os.path.dirname(os.path.abspath(__file__))
swagger_file = os.path.join(current_dir, 'swagger.yaml')
# Utiliser le chemin d'accès absolu dans la configuration de Swagger
API_URL = swagger_file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Calculatrice RPN"
    }
)

# Obtenir le chemin d'accès absolu au répertoire contenant le fichier YAML
swagger_dir = os.path.join(os.getcwd(), 'path/to/your/swagger/files/directory')


@app.route('/swagger.yaml')
def serve_swagger():
    return send_from_directory(swagger_dir, 'swagger.yaml')


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/stack', methods=['GET'])
def get_stack():
    return jsonify(stack)


@app.route('/stack', methods=['POST'])
def add_to_stack():
    element = request.get_json()['element']
    stack.append(element)
    return jsonify(stack)


@app.route('/stack', methods=['DELETE'])
def clear_stack():
    stack.clear()
    return jsonify(stack)


@app.route('/add', methods=['PUT'])
def add_numbers():
    if len(stack) >= 2:
        num2 = stack.pop()
        num1 = stack.pop()
        result = num1 + num2
        stack.append(result)
        return jsonify(stack)
    else:
        return jsonify({'error': 'Not enough numbers in the stack'})


@app.route('/subtract', methods=['PUT'])
def subtract_numbers():
    if len(stack) >= 2:
        num2 = stack.pop()
        num1 = stack.pop()
        result = num1 - num2
        stack.append(result)
        return jsonify(stack)
    else:
        return jsonify({'error': 'Not enough numbers in the stack'})


@app.route('/multiply', methods=['PUT'])
def multiply_numbers():
    if len(stack) >= 2:
        num2 = stack.pop()
        num1 = stack.pop()
        result = num1 * num2
        stack.append(result)
        return jsonify(stack)
    else:
        return jsonify({'error': 'Not enough numbers in the stack'})


@app.route('/divide', methods=['PUT'])
def divide_numbers():
    if len(stack) >= 2:
        num2 = stack.pop()
        num1 = stack.pop()
        if num2 != 0:
            result = num1 / num2
            stack.append(result)
            return jsonify(stack)
        else:
            return jsonify({'error': 'Division by zero'})
    else:
        return jsonify({'error': 'Not enough numbers in the stack'})


if __name__ == '__main__':
    app.run()
