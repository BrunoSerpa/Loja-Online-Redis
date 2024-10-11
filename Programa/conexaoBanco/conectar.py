from Programa.conexaoBanco.configuracao import carregarConfiguracao
from Programa.funcoes.utils.salvarErro import salvarErro

from pymongo import MongoClient

def conectar():
    try:
        cliente = MongoClient("linkMongo")
        return cliente.Loja_Online
    except Exception as e:
        salvarErro("Erro ao conectar ao Mongo", e)
        return None