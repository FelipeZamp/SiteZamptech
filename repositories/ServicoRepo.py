import sqlite3
from typing import List, Optional
from models.Servico import Servico
from sql.ServicoSql import *
from util.bancodedados import criar_conexao

class ServicoRepo:
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
    def inserir(cls, servico: Servico) -> Optional[Servico]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (servico.nome, servico.desc, servico.valor))
                if cursor.rowcount > 0:
                    servico.id = cursor.lastrowid
                    return servico
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def obter_todos(cls) -> List[Servico]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                servicos = cursor.execute(SQL_OBTER_TODOS).fetchall()
                return [Servico(*s) for s in servicos]
        except sqlite3.Error as e:
            print(e)
            return []

    @classmethod
    def alterar(cls, servico: Servico) -> Optional[Servico]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR, (servico.nome, servico.desc, servico.valor, servico.id))
                if cursor.rowcount > 0:
                    return servico
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def excluir(cls, id_servico: int) -> bool or False:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id_servico,))
                if cursor.rowcount > 0:
                    return True
        except sqlite3.Error as e:
            print(e)
            return False

    @classmethod
    def obter_por_id(cls, id_servico: int) -> Servico or None:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                servico = cursor.execute(SQL_OBTER_POR_ID, (id_servico,)).fetchone()
                return Servico(*servico) if servico else None
        except sqlite3.Error as e:
            print(e)
            return None
