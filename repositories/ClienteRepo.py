import sqlite3
from typing import List, Optional
from models.Cliente import Cliente
from sql.ClienteSql import *
from util.bancodedados import criar_conexao

class ClienteRepo:
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
    def inserir(cls, cliente: Cliente) -> Optional[Cliente]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (cliente.nome, cliente.endereco, cliente.telefone, cliente.email))
                if cursor.rowcount > 0:
                    cliente.id = cursor.lastrowid
                    return cliente
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def obter_todos(cls) -> List[Cliente]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                clientes = cursor.execute(SQL_OBTER_TODOS).fetchall()
                return [Cliente(*c) for c in clientes]
        except sqlite3.Error as e:
            print(e)
            return []

    @classmethod
    def alterar(cls, cliente: Cliente) -> Optional[Cliente]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR, (cliente.nome, cliente.endereco, cliente.telefone, cliente.email, cliente.id))
                if cursor.rowcount > 0:
                    return cliente
        except sqlite3.Error as e:
            print(e)
            return None

    @classmethod
    def excluir(cls, id_cliente: int) -> bool or False:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id_cliente,))
                if cursor.rowcount > 0:
                    return True
        except sqlite3.Error as e:
            print(e)
            return False

    @classmethod
    def obter_por_id(cls, id_cliente: int) -> Cliente or None:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cliente = cursor.execute(SQL_OBTER_POR_ID, (id_cliente,)).fetchone()
                return Cliente(*cliente) if cliente else None
        except sqlite3.Error as e:
            print(e)
            return None
