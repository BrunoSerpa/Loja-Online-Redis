from datetime import datetime

from Programa.funcoes.utils.entrada import entrada
from Programa.funcoes.utils.escolher import usuario as escolherCliente, endereco as escolherEndereco, vendedor as escolherVendedor, produto as escolherProduto, compra as escolherCompra
from Programa.funcoes.utils.limpar import limparTerminal
from Programa.funcoes.utils.separar import separador1
from Programa.funcoes.utils.visualizar import compra as visualizarCompra

from Programa.funcoes.crud import buscarPorAtributo, buscarPorId, buscarTodos, cadastrar as cadastrarCompra, atualizar as atualizarDado, excluir as excluirCompra


def cadastrar(cliente = None):
    comCliente = False if cliente == None else True
    if not comCliente:
        nome_cliente = entrada("Insira o nome do usuario", "NaoVazio", "Insira o nome do usuario.")
        clientes = buscarPorAtributo("Usuarios", "nome_usuario", nome_cliente)
        cliente = escolherCliente(clientes)
        if not cliente:
            return None

    endereco_cliente = escolherEndereco(cliente.get('enderecos_usuario'))
    if not endereco_cliente:
        return None

    nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
    vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)

    vendedor = escolherVendedor(vendedores)
    if not vendedor:
        return None

    endereco_vendedor = escolherEndereco(vendedor.get("enderecos_vendedor"))
    if not endereco_vendedor:
        return None
    
    produtos_disponiveis = vendedor.get("produtos")
    if not produtos_disponiveis:
        return None

    produtos = []
    valor_total = 0
    while len(produtos_disponiveis) > 0:
        produto = escolherProduto(produtos_disponiveis)
        if not produto:
            return None
        
        produtos_disponiveis.remove(produto)
        produtos.append(produto)

        valor_total += float(produto.get("valor_produto"))
        if produtos_disponiveis == 0:
            break
        elif entrada("Deseja comprar mais algum produto? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() != 'S':
            break

    if not produtos:
        return None

    compra_realizada={
        "data_compra": datetime.utcnow(),
        "cliente": {
            "_id": cliente.get("_id"),
            "nome_usuario": cliente.get("nome_usuario"),
            "cpf": cliente.get("cpf"),
            "email_usuario": cliente.get("email_usuario"),
            "telefone_usuario": cliente.get("telefone_usuario")
        },
        "remetente": {
            "cep": endereco_vendedor.get("cep"),
            "pais": endereco_vendedor.get("pais"),
            "estado": endereco_vendedor.get("estado"),
            "cidade": endereco_vendedor.get("cidade"),
            "bairro": endereco_vendedor.get("bairro"),
            "rua": endereco_vendedor.get("rua"),
            "numero": endereco_vendedor.get("numero"),
            "descricao": endereco_vendedor.get("descricao")
        },
        "destinatario": {
            "cep": endereco_cliente.get("cep"),
            "pais": endereco_cliente.get("pais"),
            "estado": endereco_cliente.get("estado"),
            "cidade": endereco_cliente.get("cidade"),
            "bairro": endereco_cliente.get("bairro"),
            "rua": endereco_cliente.get("rua"),
            "numero": endereco_cliente.get("numero"),
            "descricao": endereco_cliente.get("descricao")},
        "vendedor": {
            "_id": vendedor.get("_id"),
            "nome_vendedor": vendedor.get("nome_vendedor"),
            "cnpj": vendedor.get("cnpj"),
            "email_vendedor": vendedor.get("email_vendedor"),
            "telefone_vendedor": vendedor.get("telefone_vendedor")
        },
        "produtos": produtos,
        "valor_total": valor_total,
    }
    
    cadastrarCompra("Compras", compra_realizada)
    
    if compra_realizada:
        print("Compra cadastrada com sucesso")

        venda = {
            "_id": compra_realizada.get("_id"),
            "data_compra": compra_realizada.get("data_compra"),
            "cliente": compra_realizada.get("cliente"),
            "remetente": compra_realizada.get("remetente"),
            "destinatario": compra_realizada.get("destinatario"),
            "produtos": compra_realizada.get("produtos"),
            "valor_total": compra_realizada.get("valor_total"),
        }

        if not vendedor.get("vendas"):
            vendedor["vendas"] = []
        vendedor["vendas"].append(venda)
        vendedor["produtos"] = produtos_disponiveis
        atualizar = atualizarDado("Vendedores", vendedor)
        if not atualizar:
            return None
        print("Vendedor vinculado com sucesso!")

        compra = {
            "_id": compra_realizada.get("_id"),
            "data_compra": compra_realizada.get("data_compra"),
            "vendedor": compra_realizada.get("vendedor"),
            "remetente": compra_realizada.get("remetente"),
            "destinatario": compra_realizada.get("destinatario"),
            "produtos": compra_realizada.get("produtos"),
            "valor_total": compra_realizada.get("valor_total"),
        }
        if not comCliente:
            if not cliente.get("compras"):
                cliente["compras"] = []
            cliente["compras"].append(compra)
            atualizar = atualizarDado("Usuarios", cliente)
            if not atualizar:
                return None
            print("Cliente vinculado com sucesso!")
        return compra

def cadastrarMultiplos(cliente):
    if not cliente.get("compras"):
        compras = []
    else:
        compras = [*cliente["compras"]]
    while True:
        limparTerminal()
        compra = cadastrar(cliente)
        if compra:
            compras.append(cliente)
        if entrada("Deseja cadastrar mais alguma compra? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() != 'S':
            break
    return compras

def deletar(vendedor = None):
    comVendedor = False if vendedor == None else True
    if not comVendedor:
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome não pode estar em branco.")
        vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escolherVendedor(vendedores)
        if not vendedor:
            return None

    if not vendedor.get("vendas"):
        print("Este vendedor não possui vendas")
        return None
    venda = escolherCompra(vendedor.get("vendas"))
    if not venda:
        return None

    visualizarCompra(venda, True, False, True)
    
    if entrada("Deseja realmente deletar esta venda específica? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        compra_realizada = buscarPorId("Compras", venda.get("_id"))

        cliente = buscarPorId("Usuarios", compra_realizada.get("cliente")["_id"])
        if cliente:
            for compra_cliente in cliente.get("compras"):
                if compra_cliente.get("_id") == venda.get("_id"):
                    cliente["compras"].remove(compra_cliente)
            atualizar = atualizarDado("Usuarios", cliente)
            if not atualizar:
                return None
            print("Compra removida do cliente!")

        if not vendedor.get("produtos"):
            vendedor["produtos"] = []

        for produto in venda.get("produtos"):
            vendedor["produtos"].append(produto)

        vendedor["vendas"].remove(venda)
        if not comVendedor:
            atualizar = atualizarDado("Vendedores", vendedor)
            if not atualizar:
                return None
        print("Produtos e compras corrigidas com sucesso!")

        excluir = excluirCompra("Compras", venda.get("_id"))
        if not excluir:
            return None
        print("Compra deletada com sucesso!")

    return vendedor

def listarCompras():
    compras = []
    if entrada("Deseja procurar as compras de um vendedor específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        nome_vendedor = entrada("Insira o nome do vendedor", "NaoVazio", "Nome do vendedor não pode estar em branco.")
        vendedores = buscarPorAtributo("Vendedores", "nome_vendedor", nome_vendedor)
        vendedor = escolherCliente(vendedores)
        if vendedor:
            compras = vendedor.get("Vendas")
    else:
        compras = buscarTodos("Compras")

    limparTerminal()
    if not compras:
        print("Nenhuma compra encontrada!")
    elif len(compras) == 0:
        print("Nenhuma compra encontrada!")
    elif len(compras) == 1:
        print(separador1)        
        visualizarCompra(compras[0], comUsuario = True)
        print(separador1)
    else:
        for numeroCompra, compra in enumerate(compras, start = 1):
            print(separador1)
            print(f'{numeroCompra}ª compra:')
            visualizarCompra(compra, comUsuario = True)
        print(separador1)


def listarVendas():
    vendas = []
    if entrada("Deseja procurar as vendas de um usuário específico? (S/N)", "SimOuNao", "Insira 'S' para sim, ou 'N' para não").upper() == 'S':
        usuarios = buscarPorAtributo("Usuarios", "nome_usuario", entrada("Insira o nome do usuario", "NaoVazio", "Insira o nome do usuario"))
        cliente = escolherCliente(usuarios)
        if cliente:
            vendas = cliente.get("compras")
    else:
        vendas = buscarTodos("Compras")

    limparTerminal()
    if not vendas:
        print("Nenhuma venda encontrada!")
    elif len(vendas) == 0:
        print("Nenhuma venda encontrada!")
    elif len(vendas) == 1:
        print(separador1)        
        visualizarCompra(vendas[0], comVendedor = True)
        print(separador1)
    else:
        for numeroVenda, venda in enumerate(vendas, start = 1):
            print(separador1)
            print(f'{numeroVenda}ª venda:')
            visualizarCompra(venda, comVendedor = True)
        print(separador1)