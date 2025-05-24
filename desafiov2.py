import textwrap

def menu():
    try:
        menu = """\n
        ==================== Sistema Bancário RM ====================
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Novo Usuario
        [nc] Nova Conta
        [lc] Listar Contas
        [q] Sair\n
        Digite a Opção: """
        return input(textwrap.dedent(menu))
    except KeyboardInterrupt:
        print("\nDigite 'q' para encerrar o programa!")
        return "q"  # Retorna 'q' para sair do programa


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o Valor do Deposito: "))

            saldo, extrato = Depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o Valor do Saque: "))

            saldo, extrato, numero_saques = Sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saque=LIMITE_SAQUES,
            )

        elif opcao == "e":
            Extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            Criar_Usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = Criar_Conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            Listar_Contas(contas)

        elif opcao == "q":
            print("\nSistema Bancário V2.0")
            print("Desenvolvido por Rafael Mendes para DIO")
            print("Saindo do sistema...")
            break

        else:
            print("\nERRO: Comando inválido, tente novamente!")

def Depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"\nDeposito: R$ {valor:.2f}"
        print(f"\nDeposito de R$ {valor:.2f} Realizado com Sucesso!")
    else:
        print("\nERRO: VALOR INCORRETO")

    return saldo, extrato

def Sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saque):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saque

    if excedeu_saldo:
        print("\nERRO: Saldo Insuficiente!!")

    elif excedeu_limite:
        print("\nERRO: o Valor do Saque excede o Limite!!")

    elif excedeu_saques:
        print("\nERRO: Numero de Saques Excedido!!")

    elif valor > 0:
        saldo -= valor
        extrato += f"\nSaque: R$ {valor:.2f}"
        numero_saques += 1
        print(f"\nVocê Sacou R$ {valor:.2f} Com Sucesso!")
    else:
        print("\nERRO: Operação Invalida!!")

    return saldo, extrato, numero_saques

def Extrato(saldo, /, *, extrato):
    print("\n==================== EXTRATO ====================")
    print("Não foram realizadas Movimentaçoes." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==================================================")

def Criar_Usuario(usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nCPF Ja Cadastrado!!")
        return
    
    nome = input("Informe seu Nome: ")
    data_nascimento = input("Informe a Data de Nascimento(Dia/Mes/Ano): ")
    endereco = input("Informe o Endereço(logradouro, nro, bairro, cidade e sigla Estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print(f"\nUsuario {nome} Criado com Sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def Criar_Conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(f"\nConta: {numero_conta} Criada com Sucesso!!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print(f"\nUsuario {cpf} Não Encontrado!!")

def Listar_Contas(contas):
    for conta in contas:
        linha = f"""
            Agencia: {conta['agencia']}
            Conta: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


main()