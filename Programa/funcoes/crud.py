from Programa.conexaoBanco.conectar import conectar
from Programa.funcoes.utils.salvarErro import salvarErro

from bson.objectid import ObjectId

sessao = conectar()

def escolherColecao(nome):
    if sessao is None:
        salvarErro("Erro na sessão", "Sessão de banco de dados não estabelecida")
        return None

    colecoes = {
        "Usuarios": sessao.Usuarios,
        "Vendedores": sessao.Vendedores,
        "Produtos": sessao.Produtos,
        "Compras": sessao.Compras
    }
    return colecoes.get(nome)

def cadastrar(nomeColecao, dados):
    colecao = escolherColecao(nomeColecao)
    if colecao is None:
        return None
    try:
        colecao.insert_one(dados)
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
        return id
    except Exception as e:
        salvarErro(f"Erro ao excluir em {nomeColecao}", e)
        return None

def buscarTodos(nomeColecao):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        resultados = colecao.find().sort("_id")
        return list(resultados)
    except Exception as e:
        salvarErro("Erro ao buscar todos os registros", e)
    return None

def buscarPorId(nomeColecao, id):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        resultado = colecao.find_one({"_id": ObjectId(id)})
        if resultado:
            return resultado
        else:
            salvarErro("Registro não encontrado", f'ID {id} não encontrado na coleção {nomeColecao}')
            return None
    except Exception as e:
        salvarErro("Erro ao buscar registro por ID", e)
        return None

def buscarPorAtributo(nomeColecao, nomeCampo, atributo):
    colecao = escolherColecao(nomeColecao)
    if colecao == None:
        return None
    try:
        resultados = colecao.find({nomeCampo: {"$regex":atributo, "$options": "i"}})
        return list(resultados)
    except Exception as e:
        salvarErro("Erro ao buscar registro por atributo semelhante", e)
        return None