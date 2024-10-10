# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EmpleadoDao:

    def getEmpleados(self):

        empleadoSQL = """
        SELECT id, descripcion
        FROM empleados
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(empleadoSQL)
            empleados = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': empleado[0], 'descripcion': empleado[1]} for empleado in empleados]

        except Exception as e:
            app.logger.error(f"Error al obtener todas los empleados: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEmpleadoById(self, id):

        empleadoSQL = """
        SELECT id, descripcion
        FROM empleados WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(empleadoSQL, (id,))
            empleadoEncontrada = cur.fetchone() # Obtener una sola fila
            if empleadoEncontrada:
                return {
                        "id": empleadoEncontrada[0],
                        "descripcion": empleadoEncontrada[1]
                    }  # Retornar los datos del diseño
            else:
                return None # Retornar None si no se encuentra diseño
        except Exception as e:
            app.logger.error(f"Error al obtener empleado: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEmpleado(self, descripcion):

        insertEmpleadoSQL = """
        INSERT INTO empleados(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEmpleadoSQL, (descripcion,))
            empleado_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return empleado_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar empleado: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEmpleado(self, id, descripcion):

        updateEmpleadoSQL = """
        UPDATE empleados
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEmpleadoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar empleado: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEmpleado(self, id):

        updateEmpleadoSQL = """
        DELETE FROM empleado
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEmpleadoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar empleado: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()