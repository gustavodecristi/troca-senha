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

def trocar_senha(usuario, senha):
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    try:
        cursor = connection.cursor()
        query = """
        UPDATE DATACENTER.CM_USUARIOS S
        SET S.FG_ATIVO = 1, S.FG_SITUACAO = 1, S.DS_SENHA = :password, S.NR_TENTATIVAS = 0
        WHERE S.DS_LOGIN = :login_user
        """
        cursor.execute(query, login_user=usuario, password=senha)
        
        query2 = """
        UPDATE DATACENTER.CM_USUARIO_BLOQUEIOS B
        SET B.FG_ATIVO = 0, B.CD_USUARIO_DESBLOQUEO = 5595, B.DT_DESBLOQUEO = SYSDATE
        WHERE B.CD_USUARIO = (SELECT CD_USUARIO FROM DATACENTER.CM_USUARIOS S WHERE S.DS_LOGIN = :login_user)
        AND B.FG_ATIVO = 1
        """
        cursor.execute(query2, login_user=usuario)
        
        connection.commit()
        
    except cx_Oracle.DatabaseError as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        cursor.close()
        connection.close()


