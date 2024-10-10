from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.pedido.PedidoDao import PedidoDao

pedapi = Blueprint('pedapi', __name__)

# Trae todos los pedidos
@pedapi.route('/pedidos', methods=['GET'])
def getPedidos():
    pedDao = PedidoDao()

    try:
        pedidos = pedDao.getPedidos()

        return jsonify({
            'success': True,
            'data': pedidos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los pedidos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pedapi.route('/pedidos/<int:pedido_id>', methods=['GET'])
def getPedido(pedido_id):
    peddao = PedidoDao()

    try:
        pedido = peddao.getPedidoById(pedido_id)

        if pedido:
            return jsonify({
                'success': True,
                'data': pedido,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el pedido con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener pedido: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo pedido
@pedapi.route('/pedidos', methods=['POST'])
def addPedido():
    data = request.get_json()
    peddao = PedidoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        pedido_id = peddao.guardarPedido(descripcion)
        if pedido_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': pedido_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el pedido. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar pedido: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pedapi.route('/pedidos/<int:pedido_id>', methods=['PUT'])
def updatePedido(pedido_id):
    data = request.get_json()
    peddao = PedidoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if peddao.updatePedido(pedido_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': pedido_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el pedido con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar pedido: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pedapi.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def deletePedido(pedido_id):
    peddao = PedidoDao()

    try:
        # Usar el retorno de eliminarPedido para determinar el éxito
        if peddao.deletePedido(pedido_id):
            return jsonify({
                'success': True,
                'mensaje': f'Pedido con ID {pedido_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el pedido con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar pedido: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
