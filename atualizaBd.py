# pip install mysql-connector-python
import mysql.connector
from enviaEmail import EnviaEmail
# Variaveis de ambiente

# Configurações do primeiro banco de dados (de onde os dados serão lidos)
origem_db_config = {
    'host': 'serverOrigem',
    'user': 'usuarioOrigem',
    'password': 'senhaOrigem',
    'database': 'bancoOrigem'
}

# Configurações do segundo banco de dados (onde os dados serão inseridos)
destino_db_config = {
    'host': 'serverDestino',
    'user': 'usuarioDestino',
    'password': 'senhaDestino',
    'database': 'bancoDestino'
}

# Conectando ao banco de dados de origem
origem_conn = mysql.connector.connect(**origem_db_config)
origem_cursor = origem_conn.cursor()

# Conectando ao banco de dados de destino
destino_conn = mysql.connector.connect(**destino_db_config)
destino_cursor = destino_conn.cursor()

try:
    # Exemplo: lendo dados da tabela 'exemplo_tabela' no banco de dados de origem
    origem_cursor.execute("SELECT * FROM exemplo_tabela")
    rows = origem_cursor.fetchall()

    # Exemplo: inserindo dados na tabela 'exemplo_tabela_destino' no banco de dados de destino
    for row in rows:
        query = "INSERT INTO exemplo_tabela_destino VALUES ("
        query += ", ".join(["%s"] * len(row))  # Adiciona %s para cada coluna na linha
        query += ")"
        destino_cursor.execute(query, row)
    # Commit das alterações no banco de dados de destino
    destino_conn.commit()
    EnviaEmail("Dados transferidos com sucesso!")
    print("Dados transferidos com sucesso!")

except mysql.connector.Error as err:
    print(f"Erro: {err}")

finally:
    # Fechando as conexões
    origem_cursor.close()
    destino_cursor.close()
    origem_conn.close()
    destino_conn.close()
