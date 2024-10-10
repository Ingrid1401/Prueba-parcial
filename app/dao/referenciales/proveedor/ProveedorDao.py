# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProveedorDao:

    def getProveedores(self):

        proveedorSQL = """
        SELECT id, descripcion
        FROM proveedores
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(proveedorSQL)
            proveedores = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': proveedor[0], 'descripcion': proveedor[1]} for proveedor in proveedores]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los proveedores: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getProveedorById(self, id):

        proveedorSQL = """
        SELECT id, descripcion
        FROM proveedores WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(proveedorSQL, (id,))
            proveedorEncontrado = cur.fetchone()  # Obtener una sola fila
            if proveedorEncontrado:
                return {
                    "id": proveedorEncontrado[0],
                    "descripcion": proveedorEncontrado[1]
                }  # Retornar los datos del proveedor
            else:
                return None  # Retornar None si no se encuentra proveedor
        except Exception as e:
            app.logger.error(f"Error al obtener proveedor: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarProveedor(self, descripcion):

        insertProveedorSQL = """
        INSERT INTO proveedores(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertProveedorSQL, (descripcion,))
            proveedor_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return proveedor_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar proveedor: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateProveedor(self, id, descripcion):

        updateProveedorSQL = """
        UPDATE proveedores
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProveedorSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar proveedor: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteProveedor(self, id):

        deleteProveedorSQL = """
        DELETE FROM proveedores
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteProveedorSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar proveedor: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
