# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DiseñoDao:

    def getDiseños(self):

        diseñoSQL = """
        SELECT id, descripcion
        FROM diseños
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(diseñoSQL)
            diseños = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': diseño[0], 'descripcion': diseño[1]} for diseño in diseños]

        except Exception as e:
            app.logger.error(f"Error al obtener todas los diseños: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDiseñoById(self, id):

        diseñoSQL = """
        SELECT id, descripcion
        FROM diseños WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(diseñoSQL, (id,))
            diseñoEncontrada = cur.fetchone() # Obtener una sola fila
            if diseñoEncontrada:
                return {
                        "id": diseñoEncontrada[0],
                        "descripcion": diseñoEncontrada[1]
                    }  # Retornar los datos del diseño
            else:
                return None # Retornar None si no se encuentra diseño
        except Exception as e:
            app.logger.error(f"Error al obtener diseño: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDiseño(self, descripcion):

        insertDiseñoSQL = """
        INSERT INTO diseños(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertDiseñoSQL, (descripcion,))
            diseño_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return diseño_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar diseño: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateDiseño(self, id, descripcion):

        updateDiseñoSQL = """
        UPDATE diseños
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDiseñoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar diseño: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDiseño(self, id):

        updateDiseñoSQL = """
        DELETE FROM diseños
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDiseñoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar diseño: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()