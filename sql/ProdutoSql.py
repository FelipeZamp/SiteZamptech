SQL_CRIAR_TABELA = """
 CREATE TABLE IF NOT EXISTS produto (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nome TEXT NOT NULL,
 desc TEXT NOT NULL,
 valor DECIMAL(9,2) NOT NULL,
 quant INTEGER NOT NULL,
 fornecedor TEXT NOT NULL
 )
"""
SQL_INSERIR = """
 INSERT INTO produto (nome, desc, valor, quant, fornecedor)
 VALUES (?, ?, ?, ?, ?)
"""
SQL_ALTERAR = """
 UPDATE produto
 SET nome=?, desc=?, valor=?, quant=?, fornecedor=?
 WHERE id=?
"""
SQL_EXCLUIR = """
 DELETE FROM produto
 WHERE id=?
"""
SQL_OBTER_TODOS = """
 SELECT id, nome, desc, valor, quant, fornecedor
 FROM produto
 ORDER BY nome
"""
SQL_OBTER_POR_ID = """
 SELECT id, nome, desc, valor, quant, fornecedor
 FROM produto
 WHERE id=?
"""