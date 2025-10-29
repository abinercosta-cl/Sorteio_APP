# database.py (ATUALIZADO COM PAPÉIS DE USUÁRIO)

import sqlite3
import datetime
import hashlib
import sys
import os

def get_base_path():
    """ Obtém o caminho base, funcione para script ou .exe PyInstaller """
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como um .exe 'congelado'
        return os.path.dirname(sys.executable)
    else:
        # Se estiver rodando como um script normal
        return os.path.dirname(os.path.abspath(__file__))

# Define o DB_NAME como um caminho absoluto ao lado do script/exe
DB_NAME = os.path.join(get_base_path(), 'sorteio.db')

def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    return conn, conn.cursor()

def validar_usuario(usuario, senha):
    """
    Verifica as credenciais do usuário e retorna seu papel ('admin', 'locutor') se for válido,
    caso contrário, retorna None.
    """
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    conn, cursor = conectar_db()
    # Agora selecionamos a coluna 'role'
    cursor.execute("SELECT role FROM usuarios WHERE usuario = ? AND senha_hash = ?", (usuario, senha_hash))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return resultado[0] # Retorna a string do papel, ex: 'admin'
    return None

# O resto das funções permanece o mesmo...

def adicionar_participante(nome, cpf, telefone):
    try:
        conn, cursor = conectar_db()
        cursor.execute("INSERT INTO participantes (nome, cpf, telefone) VALUES (?, ?, ?)", (nome, cpf, telefone))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Erro ao adicionar participante: {e}")
        return False

def buscar_todos_participantes():
    conn, cursor = conectar_db()
    cursor.execute("SELECT id, nome, cpf, telefone, vezes_sorteado FROM participantes ORDER BY nome")
    participantes = cursor.fetchall()
    conn.close()
    return participantes

def excluir_participante(id_participante):
    try:
        conn, cursor = conectar_db()
        cursor.execute("DELETE FROM participantes WHERE id = ?", (id_participante,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao excluir participante: {e}")
        return False
    
def buscar_participantes_elegiveis():
    conn, cursor = conectar_db()
    cursor.execute("SELECT id, nome FROM participantes WHERE vezes_sorteado < 2")
    elegiveis = cursor.fetchall()
    conn.close()
    return elegiveis

def registrar_vencedor(id_vencedor, nome_vencedor):
    try:
        conn, cursor = conectar_db()
        cursor.execute("UPDATE participantes SET vezes_sorteado = vezes_sorteado + 1 WHERE id = ?", (id_vencedor,))
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO historico_sorteios (participante_id, nome_vencedor, data_sorteio) VALUES (?, ?, ?)", 
                       (id_vencedor, nome_vencedor, data_atual))
        conn.commit()
        conn.close()
        return True
    except Exception as e: 
        print(f"Erro ao registrar vencedor: {e}")
        return False

def buscar_historico_recente():
    conn, cursor = conectar_db()
    cursor.execute("SELECT nome_vencedor, data_sorteio FROM historico_sorteios ORDER BY data_sorteio DESC LIMIT 5")
    historico = cursor.fetchall()
    conn.close()
    return historico

def buscar_ganhadores_por_mes(ano, mes_numero):
    periodo_busca = f"{ano}-{mes_numero}-%"
    conn, cursor = conectar_db()
    cursor.execute("SELECT DISTINCT participante_id FROM historico_sorteios WHERE data_sorteio LIKE ?", (periodo_busca,))
    ganhadores_ids = cursor.fetchall()
    if not ganhadores_ids:
        conn.close()
        return []
    ids_planos = [item[0] for item in ganhadores_ids]
    placeholders = ','.join(['?'] * len(ids_planos))
    query = f"SELECT id, nome, cpf, telefone FROM participantes WHERE id IN ({placeholders})"
    cursor.execute(query, ids_planos)
    info_ganhadores = cursor.fetchall()
    conn.close()
    return info_ganhadores