SQL_CRIAR_TABELA = """
 CREATE TABLE IF NOT EXISTS ordem (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 cliente TEXT NOT NULL,
 servico TEXT NOT NULL,
 status TEXT NOT NULL,
 desc TEXT NOT NULL
 )
"""
SQL_INSERIR = """
 INSERT INTO ordem (cliente, servico, status, desc)
 VALUES (?, ?, ?, ?)
"""
SQL_ALTERAR = """
 UPDATE ordem
 SET cliente=?, servico=?, status=?, desc=?
 WHERE id=?
"""
SQL_EXCLUIR = """
 DELETE FROM ordem
 WHERE id=?
"""
SQL_OBTER_TODOS = """
 SELECT id, cliente, servico, status, desc
 FROM ordem
 ORDER BY id
"""
SQL_OBTER_POR_ID = """
 SELECT id, cliente, servico, status, desc
 FROM ordem
 WHERE id=?
"""