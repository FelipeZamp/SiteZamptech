import sqlite3
from typing import List, Optional
from models.Ordem import Ordem
from sql.OrdemSql import *
from util.bancodedados import criar_conexao

class OrdemRepo:
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
    def inserir(cls, ordem: Ordem) -> Optional[Ordem]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (ordem.cliente, ordem.servico, ordem.status, ordem.desc))
                if cursor.rowcount > 0:
                    ordem.id = cursor.lastrowid
                    return ordem
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def obter_todos(cls) -> List[Ordem]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                ordens = cursor.execute(SQL_OBTER_TODOS).fetchall()
                return [Ordem(*o) for o in ordens]
        except sqlite3.Error as e:
            print(e)
            return []

    @classmethod
    def alterar(cls, ordem: Ordem) -> Optional[Ordem]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR, (ordem.cliente, ordem.servico, ordem.status, ordem.desc, ordem.id))
                if cursor.rowcount > 0:
                    return ordem
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def excluir(cls, id_ordem: int) -> bool or False:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id_ordem,))
                if cursor.rowcount > 0:
                    return True
        except sqlite3.Error as e:
            print(e)
            return False

    @classmethod
    def obter_por_id(cls, id_ordem: int) -> Ordem or None:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                ordem = cursor.execute(SQL_OBTER_POR_ID, (id_ordem,)).fetchone()
                return Ordem(*ordem) if ordem else None
        except sqlite3.Error as e:
            print(e)
            return None
