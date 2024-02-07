

from flask import Blueprint, jsonify, request
from api_rest.Controller.r_control import consulta_rest
from api_rest.Controller.r_control_2 import consulta_rest_mesa

rest_blueprint = Blueprint('rest', __name__)

@rest_blueprint.route('/consulta', methods=['POST'])
def consulta():
    print(request.data.decode('utf-8'))
    data = consulta_rest(request.data.decode('utf-8'))
    response = jsonify(data)
    print(response)
    return response


@rest_blueprint.route('/consulta2', methods=['POST'])
def consulta2():
    ##consulta_rest_mesa
    print(request.data.decode('utf-8'))
    data = consulta_rest_mesa(request.data.decode('utf-8'))
    response = jsonify(data)
    print(response)
    return response
