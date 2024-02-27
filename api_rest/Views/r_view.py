

from flask import Blueprint, request
from Controller.tickets.grupos.r_control_g import consulta_grupos
from Controller.tickets.usuarios.r_control_u import consulta_rest_mesa

rest_blueprint = Blueprint('rest', __name__)

@rest_blueprint.route('/consulta-grupos', methods=['POST'])
def consultaGrupos():
    print(request.data.decode('utf-8'))
    result = consulta_grupos(request.data.decode('utf-8'))
    return result


@rest_blueprint.route('/consulta-usuarios', methods=['POST'])
def consultaUsuarios():
    ##consulta_rest_mesa
    print(request.data.decode('utf-8'))
    result = consulta_rest_mesa(request.data.decode('utf-8'))
    return result
