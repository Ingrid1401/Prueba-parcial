# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PedidoDao:

    def getPedidos(self):

        pedidoSQL = """
        SELECT id, descripcion
        FROM pedidos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pedidoSQL)
            pedidos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': pedido[0], 'descripcion': pedido[1]} for pedido in pedidos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los pedidos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPedidoById(self, id):

        pedidoSQL = """
        SELECT id, descripcion
        FROM pedidos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pedidoSQL, (id,))
            pedidoEncontrado = cur.fetchone()  # Obtener una sola fila
            if pedidoEncontrado:
                return {
                    "id": pedidoEncontrado[0],
                    "descripcion": pedidoEncontrado[1]
                }  # Retornar los datos del pedido
            else:
                return None  # Retornar None si no se encuentra el pedido
        except Exception as e:
            app.logger.error(f"Error al obtener pedido: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPedido(self, descripcion):

        insertPedidoSQL = """
        INSERT INTO pedidos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertPedidoSQL, (descripcion,))
            pedido_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return pedido_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar pedido: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updatePedido(self, id, descripcion):

        updatePedidoSQL = """
        UPDATE pedidos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePedidoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar pedido: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePedido(self, id):

        deletePedidoSQL = """
        DELETE FROM pedidos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePedidoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar pedido: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
