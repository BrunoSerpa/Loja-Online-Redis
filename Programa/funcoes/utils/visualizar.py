from Programa.funcoes.utils.formatar import cep, cnpj, cpf, telefone
from Programa.funcoes.utils.separar import separador2, separador3

def usuario(usuario, comId = False, comFavoritos = False, comCompras = False, basico = False):
    if comId:
        print(f"ID: {usuario.get('_id')}")

    print(f"Nome: {usuario.get('nome_usuario')}")
    print(f"CPF: {cpf(usuario.get('cpf'))}")

    if not basico:
        print(f"Telefone: {telefone(usuario.get('telefone_usuario'))}")
        print(f"Email: {usuario.get('email_usuario')}")
        quantEnderecos = enderecos(usuario.get('enderecos_usuario'))

    if comFavoritos:
        quantFavoritos = produtos(usuario.get('favoritos'), favoritos = True)

    if comCompras:
        quantCompras = compras(usuario.get('compras'))

    fechaSeparador = not basico
    if fechaSeparador == True:
        fechaSeparador = quantEnderecos > 0
    if fechaSeparador == False and comFavoritos:
        fechaSeparador = quantFavoritos > 0
    if fechaSeparador == False and comCompras:
        fechaSeparador = quantCompras > 0
    if fechaSeparador:
        print(separador2)

def vendedor(vendedor, comId = False, comProdutos = False, comVendas = False, basico = False):
    if comId:
        print(f'ID: {vendedor.get("_id")}')

    print(f"Nome: {vendedor.get('nome_vendedor')}")
    print(f"CNPJ: {cnpj(vendedor.get('cnpj'))}")

    if not basico:
        print(f"Telefone: {telefone(vendedor.get('telefone_vendedor'))}")
        print(f"Email: {vendedor.get('email_vendedor')}")
        quantEnderecos = enderecos(vendedor.get('enderecos_vendedor'))

    if comProdutos:
        quantProdutos = produtos(vendedor.get('produtos'))

    if comVendas:
        quantVendas = compras(vendedor.get('vendas'), vendas = True)
    fechaSeparador = not basico
    if fechaSeparador == True:
        fechaSeparador = quantEnderecos > 0
    if fechaSeparador == False and comProdutos:
        fechaSeparador = quantProdutos > 0
    if fechaSeparador == False and comVendas:
        fechaSeparador = quantVendas > 0
    if fechaSeparador:
        print(separador2)

def compra(compra, comId = False, comVendedor = False, comUsuario = False):
    if comId:
        print(f'ID: {compra.get("_id")}')

    print(f'Data da Compra: {compra.get("data_compra")}')

    if comUsuario:
        print(separador2)
        print("Cliente:")
        usuario(compra.get('cliente'), basico = True)

    print(separador2)
    print("Destinatário:")
    endereco(compra.get('destinatario'))

    if comVendedor:
        print(separador2)
        print("Vendedor:")
        vendedor(compra.get('vendedor'), basico = True)

    """    
    print(separador2)
    print("Remetente:")
    endereco(compra.get('remetente'))
    """

    print(separador2)
    produtos(compra.get("produtos"))

    print("Total:", compra.get("valor_total"))

def produto(produto, comId=False, comVendedor=False):    
    if comId:
        print(f'ID: {produto.get("_id")}')

    print(f"Produto: {produto.get('nome_produto')}")
    print(f"Valor: R${float(produto.get('valor_produto')):.2f}")

    if comVendedor:
        print(separador2)
        vendedor(produto.get('vendedor'), basico=True)
        print(separador2)

def endereco(endereco):
    print(f'{endereco.get("rua")}, {endereco.get("numero")} ({endereco.get("descricao")}) - {endereco.get("bairro")}')
    print(f'CEP: {cep(endereco.get("cep"))}')
    print(f'{endereco.get("cidade")} - {endereco.get("estado")} ({endereco.get("pais")})')

def enderecos(enderecos):
    if enderecos == None:
        print("Endereços: Nenhum endereço encontrado")
        return 0
    quantidade = len(enderecos)
    if quantidade == 0:
        print("Endereços: Nenhum endereço encontrado")
    else:
        print(separador2)
        print(f"Endereço{'s' if quantidade > 1 else ''}:")
        for endereco_item in enderecos:
            print(separador3)
            endereco(endereco_item)
        print(separador3)
    return quantidade

def produtos(produtos, comId = False, favoritos = False):
    titulo = "Produto" if not favoritos else "Favorito"
    if produtos == None:
        print(f"{titulo}: Nenhum {titulo.lower()} encontrado")
        return 0
    quantidade = len(produtos)
    if quantidade == 0:
        print(f"{titulo}: Nenhum {titulo.lower()} encontrado")
    else:
        print(separador2)
        print(f"{titulo}{'s' if quantidade > 1 else ''}:")
        
        for produto_item in produtos:
            print(separador3)
            produto(produto_item, comId)
        print(separador3)
    return quantidade

def compras(compras, vendas = False):
    titulo = "Compra" if not vendas else "Venda"
    if compras == None:
        print(f"{titulo}: Nenhuma {titulo.lower()} encontrada")
        return 0
    quantidade = len(compras)
    if quantidade == 0:
        print(f"{titulo}: Nenhuma {titulo.lower()} encontrada")
    else:
        print(separador2)
        print(f"{titulo}{'s' if quantidade > 1 else ''}:")
        for compra_item in compras:
            print(separador3)
            compra(compra_item, False, not vendas, vendas)
        print(separador3)
    return quantidade