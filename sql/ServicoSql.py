SQL_CRIAR_TABELA = """
 CREATE TABLE IF NOT EXISTS servico (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nome TEXT NOT NULL,
 desc TEXT NOT NULL,
 valor DECIMAL(9,2) NOT NULL
 )
"""
SQL_INSERIR = """
 INSERT INTO servico (nome, desc, valor)
 VALUES (?, ?, ?)
"""
SQL_ALTERAR = """
 UPDATE servico
 SET nome=?, desc=?, valor=?
 WHERE id=?
"""
SQL_EXCLUIR = """
 DELETE FROM servico
 WHERE id=?
"""
SQL_OBTER_TODOS = """
 SELECT id, nome, desc, valor
 FROM servico
 ORDER BY nome
"""
SQL_OBTER_POR_ID = """
 SELECT id, nome, desc, valor
 FROM servico
 WHERE id=?
"""