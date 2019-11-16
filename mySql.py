import pymysql



class Base_datos():
    def __init__(self, hosting, usuario, contraseña, basededatos):
        self.conexion = pymysql.connect(
            host=hosting, user=usuario, password=contraseña, db=basededatos)

    # método Execute - Leer en Login, Leer en Registrarse
    def query(self, sql):
        with self.conexion.cursor() as cursor:
            cursor.execute(sql)
            self.conexion.commit()
            return cursor.fetchall()

    # Cerrar base de datos
    def close(self):
        self.conexion.close()