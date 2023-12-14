SQL_CRIAR_TABELA = """
 CREATE TABLE IF NOT EXISTS cliente (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nome TEXT NOT NULL,
 endereco TEXT NOT NULL,
 telefone TEXT NOT NULL,
 email TEXT NOT NULL
 )
"""
SQL_INSERIR = """
 INSERT INTO cliente (nome, endereco, telefone, email)
 VALUES (?, ?, ?, ?)
"""
SQL_ALTERAR = """
 UPDATE cliente
 SET nome=?, endereco=?, telefone=?, email=?
 WHERE id=?
"""
SQL_EXCLUIR = """
 DELETE FROM cliente
 WHERE id=?
"""
SQL_OBTER_TODOS = """
 SELECT id, nome, endereco, telefone, email
 FROM cliente
 ORDER BY nome
"""
SQL_OBTER_POR_ID = """
 SELECT id, nome, endereco, telefone, email
 FROM cliente
 WHERE id=?
"""