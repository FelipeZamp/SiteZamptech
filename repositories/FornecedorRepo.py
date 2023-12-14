import sqlite3
from typing import List, Optional
from models.Fornecedor import Fornecedor
from sql.FornecedorSql import *
from util.bancodedados import criar_conexao

class FornecedorRepo:
    @classmethod
    def criar_tabela(cls) -> bool:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_CRIAR_TABELA)
                return True
        except sqlite3.Error as e:
            print(e)
            return False

    @classmethod
    def inserir(cls, fornecedor: Fornecedor) -> Optional[Fornecedor]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (fornecedor.nome, fornecedor.endereco, fornecedor.telefone, fornecedor.email))
                if cursor.rowcount > 0:
                    fornecedor.id = cursor.lastrowid
                    return fornecedor
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def obter_todos(cls) -> List[Fornecedor]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                fornecedores = cursor.execute(SQL_OBTER_TODOS).fetchall()
                return [Fornecedor(*f) for f in fornecedores]
        except sqlite3.Error as e:
            print(e)
            return []

    @classmethod
    def alterar(cls, fornecedor: Fornecedor) -> Optional[Fornecedor]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR, (fornecedor.nome, fornecedor.endereco, fornecedor.telefone, fornecedor.email, fornecedor.id))
                if cursor.rowcount > 0:
                    return fornecedor
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def excluir(cls, id_fornecedor: int) -> bool or False:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id_fornecedor,))
                if cursor.rowcount > 0:
                    return True
        except sqlite3.Error as e:
            print(e)
            return False

    @classmethod
    def obter_por_id(cls, id_fornecedor: int) -> Fornecedor or None:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                fornecedor = cursor.execute(SQL_OBTER_POR_ID, (id_fornecedor,)).fetchone()
                return Fornecedor(*fornecedor) if fornecedor else None
        except sqlite3.Error as e:
            print(e)
            return None
