# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class FormapagoDao:

    def getFormapagos(self):

        formapagoSQL = """
        SELECT id, descripcion
        FROM formapagos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(formapagoSQL)
            formapagos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': formapago[0], 'descripcion': formapago[1]} for formapago in formapagos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los forma de pagos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getFormapagoById(self, id):

        formapagoSQL = """
        SELECT id, descripcion
        FROM formapagos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(formapagoSQL, (id,))
            formapagoEncontrado = cur.fetchone()  # Obtener una sola fila
            if formapagoEncontrado:
                return {
                    "id": formapagoEncontrado[0],
                    "descripcion": formapagoEncontrado[1]
                }  # Retornar los datos del formapago
            else:
                return None  # Retornar None si no se encuentra formapago
        except Exception as e:
            app.logger.error(f"Error al obtener forma de pago: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarFormapago(self, descripcion):

        insertFormapagoSQL = """
        INSERT INTO formapagos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertFormapagoSQL, (descripcion,))
            formapago_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return formapago_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar forma de pago: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateFormapago(self, id, descripcion):

        updateFormapagoSQL = """
        UPDATE formapagos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateFormapagoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar forma de pago: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteFormapago(self, id):

        deleteFormapagoSQL = """
        DELETE FROM formapagos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteFormapagoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar forma de pago: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
