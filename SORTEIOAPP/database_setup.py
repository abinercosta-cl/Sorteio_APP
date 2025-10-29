# database_setup.py (ATUALIZADO COM PAPÉIS DE USUÁRIO)
import sqlite3
import hashlib

NOME_BANCO_DE_DADOS = 'sorteio.db'

def setup_database():
    try:
        conn = sqlite3.connect(NOME_BANCO_DE_DADOS)
        cursor = conn.cursor()

        print("Verificando e criando tabelas...")

        # Tabela de Participantes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            vezes_sorteado INTEGER NOT NULL DEFAULT 0
        )
        ''')

        # Tabela de Administradores renomeada para Usuarios com a coluna 'role'
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            role TEXT NOT NULL 
        )
        ''')

        # Tabela de Histórico 
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_sorteios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participante_id INTEGER NOT NULL,
            nome_vencedor TEXT NOT NULL,
            data_sorteio TEXT NOT NULL,
            FOREIGN KEY (participante_id) REFERENCES participantes(id)
        )
        ''')
        print("Tabelas verificadas com sucesso.")

        # --- Adicionar usuários padrão se não existirem ---
        
        # Usuário Administrador
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ('admin',))
        if cursor.fetchone() is None:
            senha_hash_admin = hashlib.sha256('senha123'.encode()).hexdigest()
            cursor.execute("INSERT INTO usuarios (usuario, senha_hash, role) VALUES (?, ?, ?)", 
                           ('admin', senha_hash_admin, 'admin'))
            print("Usuário 'admin' padrão criado com sucesso.")

        # Usuário Locutor
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ('locutor',))
        if cursor.fetchone() is None:
            senha_hash_locutor = hashlib.sha256('locutor123'.encode()).hexdigest()
            cursor.execute("INSERT INTO usuarios (usuario, senha_hash, role) VALUES (?, ?, ?)", 
                           ('locutor', senha_hash_locutor, 'locutor'))
            print("Usuário 'locutor' padrão criado com sucesso.")

        conn.commit()
        conn.close()
        print("\nConfiguração do banco de dados concluída com sucesso!")

    except Exception as e:
        print(f"\nOcorreu um erro durante a configuração do banco de dados: {e}")

if __name__ == "__main__":
    setup_database()