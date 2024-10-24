from Programa.conexaoBanco.conectarMongo import conectarMongo
from Programa.conexaoBanco.conectarRedis import conectarRedis
from Programa.funcoes.utils.salvarErro import salvarErro
from Programa.funcoes.utils.converter import JsonParaObjeto, ObjetoParaJson

from bson.objectid import ObjectId
from json import dumps, loads

cacheRedis = conectarRedis()
sessaoMongo = conectarMongo()

def escolherColecao(nome):
    if sessaoMongo is None:
        salvarErro("Erro na sessão", "Sessão de banco de dados não estabelecida")
        return None

    colecoes = {
        "Usuarios": sessaoMongo.Usuarios,
        "Vendedores": sessaoMongo.Vendedores,
        "Produtos": sessaoMongo.Produtos,
        "Compras": sessaoMongo.Compras
    }
    return colecoes.get(nome)

def cacheResultado(chave, resultado):
    dadoJson = dumps(resultado, default=ObjetoParaJson)
    cacheRedis.set(chave, dadoJson)

def obterCache(chave):
    resultado = cacheRedis.get(chave)
    return loads(resultado, object_hook=JsonParaObjeto) if resultado else None

def limparCache(chave=None):
    if chave:
        cacheRedis.delete(chave)
    else:
        cacheRedis.flushall()

def cadastrar(nomeColecao, dados):
    colecao = escolherColecao(nomeColecao)
    if colecao is None:
        return None
    try:
        colecao.insert_one(dados)
        chave = f"{nomeColecao}:{dados['_id']}"
        cacheResultado(chave, dados)
        limparCache(f"{nomeColecao}:todos")
        return dados
    except Exception as e:
        salvarErro(f"Erro ao cadastrar em {nomeColecao}", e)
        return None

def atualizar(nomeColecao, dados):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        colecao.update_one({"_id": ObjectId(dados["_id"])}, {"$set": dados})
        chave = f"{nomeColecao}:{dados['_id']}"
        cacheResultado(chave, dados)
        limparCache(f"{nomeColecao}:todos")
        return dados
    except Exception as e:
        salvarErro(f"Erro ao atualizar {nomeColecao}", e)
        return None

def excluir(nomeColecao, id):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        colecao.delete_one({"_id": id})
        chave = f"{nomeColecao}:{id}"
        limparCache(chave)
        limparCache(f"{nomeColecao}:todos")
        return id
    except Exception as e:
        salvarErro(f"Erro ao excluir em {nomeColecao}", e)
        return None

def buscarTodos(nomeColecao):
    chave = f"{nomeColecao}:todos"
    cache = obterCache(chave)
    
    if cache:
        return cache

    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        resultados = colecao.find().sort("_id")
        resultados = list(resultados)
        cacheResultado(chave, resultados)
        return resultados
    except Exception as e:
        salvarErro("Erro ao buscar todos os registros", e)
    return None

def buscarPorId(nomeColecao, id):
    chave = f"{nomeColecao}:{id}"
    cache = obterCache(chave)

    if cache:
        return cache

    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        resultado = colecao.find_one({"_id": ObjectId(id)})
        if resultado:
            cacheResultado(chave, resultado)
            return resultado
        else:
            salvarErro("Registro não encontrado", f'ID {id} não encontrado na coleção {nomeColecao}')
            return None
    except Exception as e:
        salvarErro("Erro ao buscar registro por ID", e)
        return None

def buscarPorAtributo(nomeColecao, nomeCampo, atributo):
    chave = f"{nomeColecao}:{nomeCampo}:{atributo}"
    cache = obterCache(chave)

    if cache:
        return cache

    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        resultados = colecao.find({nomeCampo: {"$regex": atributo, "$options": "i"}})
        resultados = list(resultados)
        cacheResultado(chave, resultados)
        return resultados
    except Exception as e:
        salvarErro("Erro ao buscar registro por atributo semelhante", e)
        return None