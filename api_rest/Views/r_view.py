

from flask import Blueprint, jsonify, request
from api_rest.Controller.r_control import consulta_grupos
from api_rest.Controller.r_control_2 import consulta_rest_mesa

rest_blueprint = Blueprint('rest', __name__)

@rest_blueprint.route('/consulta-grupos', methods=['POST'])
def consultaGrupos():
    print(request.data.decode('utf-8'))
    data = consulta_grupos(request.data.decode('utf-8'))
    response = jsonify(data)
    print(response)
    return response


@rest_blueprint.route('/consulta-usuarios', methods=['POST'])
def consultaUsuarios():
    ##consulta_rest_mesa
    print(request.data.decode('utf-8'))
    data = consulta_rest_mesa(request.data.decode('utf-8'))
    response = jsonify(data)
    print(response)
    return response
