# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ClienteDao:

    def getClientes(self):

        clienteSQL = """
        SELECT id, descripcion
        FROM clientes
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(clienteSQL)
            clientes = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': cliente[0], 'descripcion': cliente[1]} for cliente in clientes]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las clientes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getClienteById(self, id):

        clienteSQL = """
        SELECT id, descripcion
        FROM clientes WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(clienteSQL, (id,))
            clienteEncontrada = cur.fetchone() # Obtener una sola fila
            if clienteEncontrada:
                return {
                        "id": clienteEncontrada[0],
                        "descripcion": clienteEncontrada[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener cliente: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCliente(self, descripcion):

        insertClienteSQL = """
        INSERT INTO clientes(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertClienteSQL, (descripcion,))
            cliente_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return cliente_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar cliente: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateCliente(self, id, descripcion):

        updateClienteSQL = """
        UPDATE clientes
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateClienteSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar cliente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCliente(self, id):

        updateClienteSQL = """
        DELETE FROM clientes
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateClienteSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar cliente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()