from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.salvarErro import salvarErro
from Programa.funcoes.utils.separar import separador1
import Programa.funcoes.utils.visualizar as visualizar


def escolher_item(tipo, itens, descricao, visualizar, **kwargs):
    quantidade = len(itens)
    if quantidade == 0:
        print(f"Nenhuma {descricao} encontrada" if not kwargs.get('termo_feminino') else f"Nenhum {descricao} encontrado")
    elif quantidade == 1:
        return itens[0]
    else:
        print(f"Mais de uma {descricao} encontrada!" if kwargs.get('termo_feminino') else f"Mais de um {descricao} encontrado!")
        while True:
            print(f"Escolha uma {descricao}:" if kwargs.get('termo_feminino') else f"Escolha um {descricao}:")
            for posicao, item in enumerate(itens, start=1):
                print(separador1)
                print(f'{posicao} - {tipo.capitalize()}:')
                visualizar(item)
            print(separador1)
            posicao = int(entrada("Insira a opção desejada", "Numero", "Insira uma opção válida."))
            limparTerminal()

            if 0 < posicao <= len(itens):
                return itens[posicao - 1]
            elif len(itens) == 0:
                return None
            else:
                print("Insira uma opção existente.")
    return None

def usuario(usuarios):
    if not usuarios:
        print("Nenhum usuário correspondente encontrado!")
        return None
    def visualizarUsuario(usuario):
        return visualizar.usuario(usuario, True)
    return escolher_item("Usuarios", usuarios, "usuário", visualizarUsuario)

def vendedor(vendedores):
    if not vendedores:
        print("Nenhum vendedor correspondente encontrado!")
        return None
    def visualizarVendedor(vendedor):
        return visualizar.vendedor(vendedor, True)
    return escolher_item("Vendedores", vendedores, "vendedor", visualizarVendedor)

def endereco(enderecos):
    if not enderecos:
        print("Nenhum endereco correspondente encontrado!")
        return None
    def visualizarEndereco(endereco):
        return visualizar.endereco(endereco)
    return escolher_item("Enderecos", enderecos, "endereço", visualizarEndereco)

def produto(produtos, favoritos = False):
    descricao = "favorito" if favoritos else "produto"
    if not produtos:
        print(f"Nenhum {descricao} correspondente encontrado!")
        return None
    def visualizarProduto(produto):
        return visualizar.produto(produto, True, favoritos)
    return escolher_item("Produtos", produtos, descricao, visualizarProduto)

def compra(compras, vendas = False):
    descricao = "compra" if not vendas else "venda"
    if not compras:
        print(f"Nenhuma {descricao} correspondente encontrada!")
        return None
    def visualizarCompra(compra):
        return visualizar.compra(compra, True, vendas, not vendas)
    return escolher_item("Compras", compras, descricao, visualizarCompra, termo_feminino = True)