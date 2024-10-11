from Programa.funcoes.crud import cadastrar as cadastrarProduto, atualizar as atualizarDado, excluir as excluirProduto, buscarPorAtributo, buscarPorId, buscarTodos
from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.escolher import vendedor as escolherVendedor, produto as escolherProduto
from Programa.funcoes.utils.separar import separador1, separador2
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.visualizar import produto as visualizarProduto

def cadastrar(vendedor = None):
    comVendedor = False if vendedor == None else True
    if not comVendedor:
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
        vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escolherVendedor(vendedores)
        if not vendedor:
            return None

    nome = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco")
    valor = entrada("Insira o valor do produto (exemplo: 1.23)", "Float", 'Valor Inválido. Deve conter apenas o número decimal, separando por ".".')

    produto = {
        "nome_produto": nome,
        "valor_produto": valor,
    }

    produto_cadastrado = {
        "nome_produto": nome,
        "valor_produto": valor,
        "vendedor" : {
            "_id": vendedor.get("_id"),
            "nome_vendedor": vendedor.get("nome_vendedor"),
            "cnpj": vendedor.get("cnpj"),
            "email_vendedor": vendedor.get("email_vendedor"),
            "telefone_vendedor": vendedor.get("telefone_vendedor"),
            "enderecos_vendedor": vendedor.get("enderecos_vendedor")
        }
    }

    cadastrou = cadastrarProduto("Produtos", produto_cadastrado)
    if not cadastrou:
        return None
    produto["_id"] = produto_cadastrado["_id"]

    print("Produto cadastrado com sucesso!")
    if not comVendedor:
        if vendedor.get("produtos") == None:
            vendedor["produtos"] = []
        vendedor["produtos"].append(produto)
        atualizar = atualizarDado("Vendedores", vendedor)

        if not atualizar:
            excluirProduto("Produtos", produto.get("_id"))
            return None
        print("Vendedor vinculado com sucesso!")
    return produto
   
def cadastrarMultiplos(vendedor):
    produtos = []
    while True:
        limparTerminal()
        produto = cadastrar(vendedor)
        if produto:
            produtos.append(produto)
        if input("Deseja cadastrar mais algum produto? (S/N)").upper() != 'S':
            break
    return produtos

def atualizar(produto = None):
    comVendedor = True if produto == None else False
    if not produto:
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("Produtos", "nome_produto", nome_produto)
        produto = escolherProduto(produtos)
        if not produto:
            return None
        vendedor = buscarPorId("Vendedores", produto.get("vendedor").get("_id"))
        if not vendedor:
            return None
        elif not vendedor.get("produtos"):
            print("Este produto foi vendido, não podendo ser alterado!")
            return None
        
        vendido = True
        for produto_a_venda in vendedor.get("produtos"):
            if produto_a_venda.get("_id") == produto.get("_id"):
                vendido = False
                break

        if vendido:
            print("Este produto foi vendido, não podendo ser alterado!")
            return None

    while True:
        print(separador1)
        print("Produto atual:")
        visualizarProduto(produto, True)
        print(f'{separador1}\n')

        print(separador1)
        print("O que deseja alterar?")
        print(separador2)
        print("1 - Nome")
        print("2 - Preço")
        print(separador2)
        print("0 - Salvar e sair")
        print(f'{separador1}\n')

        print("Qual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        limparTerminal()
        if opcaoEscolhida == '0':
            if comVendedor:
                for produto_a_venda in vendedor["produtos"]:
                    if produto_a_venda.get("_id") == produto.get("_id"):
                        produto_a_venda["nome_produto"] = produto["nome_produto"]
                        produto_a_venda["valor_produto"] = produto["valor_produto"]
                        break
                atualizar = atualizarDado("Vendedores", vendedor)
                if not atualizar:
                    return None
            print("Produto atualizado no vendedor!")
            atualizar = atualizarDado("Produtos", produto)
            if not atualizar:
                return None
            print("Produto atualizado com sucesso!")
            return produto
        elif opcaoEscolhida == '1':
            produto["nome_produto"] = entrada("Insira o novo nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        elif opcaoEscolhida == '2':
            produto["valor_produto"] = entrada("Insira o novo valor do produto", "Float", "Valor Inválido. Deve conter apenas o número decimal.")
        else:
            print("Insira uma opção válida.")

def deletar(produto = None):
    comVendedor = True if produto == None else False
    if not produto:
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("Produtos", "nome_produto", nome_produto)
        produto = escolherProduto(produtos)
        if not produto:
            return None
        vendedor = buscarPorId("Vendedores", produto.get("vendedor").get("_id"))
        if not vendedor:
            return None
        elif not vendedor.get("produtos"):
            print("Este produto foi vendido, não podendo ser deletado!")
            return None
        
        vendido = True
        for produto_a_venda in vendedor.get("produtos"):
            if produto_a_venda.get("_id") == produto.get("_id"):
                vendido = False
                break

        if vendido:
            print("Este produto foi vendido, não podendo ser deletado!")
            return None

    visualizarProduto(produto, True, comVendedor)
    if entrada("Deseja realmente deletar este produto específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        if comVendedor:
            for produto_a_venda in vendedor.get("produtos"):
                if produto_a_venda.get("_id") == produto.get("_id"):
                    vendedor["produtos"].remove(produto_a_venda)
            atualizar = atualizarDado("Vendedores", vendedor)
            if not atualizar:
                return None
            print("Produto removido do vendedor!")

        excluir = excluirProduto("Produtos", produto.get("_id"))
        if not excluir:
            return None
        print("Produto deletado com sucesso!")

    return id
    return True

def listar():
    produtos = []
    if entrada("Deseja procurar um produto específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        nome_produto = entrada("Insira o nome do produto", "NaoVazio", "Nome não pode estar em branco.")
        produtos = buscarPorAtributo("Produtos", "nome_produto", nome_produto)
    else:
        produtos = buscarTodos("Produtos")

    if not produtos:
        print("Nenhum produto encontrado!")
    elif len(produtos) == 0:
        print("Nenhum produto encontrado!")
    elif len(produtos) == 1:
        print(separador1)
        visualizarProduto(produtos[0], comVendedor = True)
        print(separador1)
    else:
        for numeroProduto, produto in enumerate(produtos, start = 1):
            print(separador1)
            print(f'{numeroProduto}º produto:')
            visualizarProduto(produto, comVendedor = True)
        print(separador1)

def gerenciar(vendedor):
    if not vendedor.get("produtos"):
        produto = []
    else:
        produtos = vendedor.get("produtos")
    while True:
        quantidade = len(produtos)

        print(separador1)
        print("Produtos atuais:")
        if quantidade > 0:
            for produto in produtos:
                print(separador2)
                visualizarProduto(produto)
            print(separador2)
        else:
            print("Produto: Nenhum produto encontrado")
        print(f'{separador1}\n')

        print(separador1)
        print("O que deseja fazer?")
        print(separador2)
        print("1 - Adicionar um produto")
        if quantidade > 0:
            print("2 - Atualizar um produto")
            print("3 - Deletar um produto")
        print(separador2)
        print("0 - Salvar e sair")
        print(separador1)
        
        print("\nQual ação deseja realizar?")
        opcaoEscolhida = entrada("Insira uma opção", "Numero", "Insira uma opção válida")
        if opcaoEscolhida == "0":
            break
        elif opcaoEscolhida == "1":
            produto = cadastrar(vendedor)
            if produto:
                produtos.append(produto)
        elif opcaoEscolhida == "2" and quantidade > 0:
            produtoEscolhido = escolherProduto(produtos)
            if not produtoEscolhido:
                continue
            for produto in produtos:
                if produto == produtoEscolhido:
                    produto = atualizar(produto)
        elif opcaoEscolhida == "3" and quantidade > 0:
            produtoEscolhido = escolherProduto(produtos)
            if not produtoEscolhido:
                continue
            else:
                deletou = deletar(produtoEscolhido)
                if deletou:
                    produtos.remove(produtoEscolhido)
        else:
            print("Insira uma opção válida.")
    return produtos

def atualizarVendedor(vendedor):
    if not vendedor.get("produtos"):
        return
    for produto in vendedor.get("produtos"):
        produto["vendedor"] = {
            "_id": vendedor.get("_id"),
            "nome_vendedor": vendedor.get("nome_vendedor"),
            "cnpj": vendedor.get("cnpj"),
            "email_vendedor": vendedor.get("email_vendedor"),
            "telefone_vendedor": vendedor.get("telefone_vendedor"),
            "enderecos_vendedor": vendedor.get("enderecos_vendedor")
        }
        atualizar = atualizarDado("Produtos", produto)
        if not atualizar:
            return
    print("Produtos atualizado com sucesso!")