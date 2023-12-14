SQL_CRIAR_TABELA = """
 CREATE TABLE IF NOT EXISTS fornecedor (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nome TEXT NOT NULL,
 endereco TEXT NOT NULL,
 telefone TEXT NOT NULL,
 email TEXT NOT NULL
 )
"""
SQL_INSERIR = """
 INSERT INTO fornecedor (nome, endereco, telefone, email)
 VALUES (?, ?, ?, ?)
"""
SQL_ALTERAR = """
 UPDATE fornecedor
 SET nome=?, endereco=?, telefone=?, email=?
 WHERE id=?
"""
SQL_EXCLUIR = """
 DELETE FROM fornecedor
 WHERE id=?
"""
SQL_OBTER_TODOS = """
 SELECT id, nome, endereco, telefone, email
 FROM fornecedor
 ORDER BY nome
"""
SQL_OBTER_POR_ID = """
 SELECT id, nome, endereco, telefone, email
 FROM fornecedor
 WHERE id=?
"""