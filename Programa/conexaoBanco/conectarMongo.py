from Programa.funcoes.utils.salvarErro import salvarErro

from pymongo import MongoClient

def conectarMongo():
    try:
        cliente = MongoClient("linkmongodb")
        return cliente.Loja_Online
    except Exception as e:  
        salvarErro("Erro ao conectar ao Mongo", e)
        return None