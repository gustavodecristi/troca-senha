import cx_Oracle
from config import user, password, dsn

def consulta_usuario(usuario):
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    try:
        cursor = connection.cursor()
        query = """
        SELECT COUNT(U.DS_LOGIN) 
        FROM DATACENTER.CM_USUARIOS U
        WHERE U.DS_LOGIN = :login_user
        """
        cursor.execute(query, login_user=usuario)
        
        resultado = cursor.fetchone()[0]
        return resultado
    except cx_Oracle.DatabaseError as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        cursor.close()
        connection.close()

def consulta_senhas(usuario):
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    try:
        cursor = connection.cursor()
        query = """
        SELECT DS_SENHA 
        FROM (
            SELECT H.DS_SENHA 
            FROM DATACENTER.CM_USUARIOS_SENHA_HIST H 
            WHERE H.DS_LOGIN = :login_user 
            ORDER BY H.CD_SENHA_HIST DESC
        ) 
        WHERE ROWNUM <= 3
        """
        cursor.execute(query, login_user=usuario)
    
        historico = [row[0] for row in cursor]
        return historico
    except cx_Oracle.DatabaseError as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        cursor.close()
        connection.close()

def troca_senhas(usuario):
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CM_USUARIOS_SENHA_HIST WHERE CD_USUARIO = 5216")
        
        for row in cursor:
            print(row)
    except cx_Oracle.DatabaseError as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        cursor.close()
        connection.close()

