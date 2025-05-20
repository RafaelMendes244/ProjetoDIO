menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
"""

saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o Valor para Deposito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Deposito: R$ {valor:.2f}\n"

        else:
            print("ERRO: Informe um Valor Valido!")

    elif opcao == "s":
        valor = float(input("Informa o Valor para Saque: "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saque >= LIMITE_SAQUE

        if excedeu_saldo:
            print(f"Seu Saldo Atual é R$ {saldo}")

        elif excedeu_limite:
            print(f"ERRO: Seu Limite de Saque é {limite}")

        elif excedeu_saques:
            print("Você Efetuou os 3 Saque Diario!")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saque += 1
        
        else:
            print("ERRO: Informe um Valor Valido!")

    elif opcao == "e":
        print("\n==================== EXTRATO ====================")
        print("Não foram realizadas Movimentaçoes." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==================================================")

    elif opcao == "q":
        print("Desenvolvido por Rafael Mendes para Digital Innovation One")
        print("Saindo do Sistema...")
        break

    else:
        print("ERRO: Operação Invalida, Tente Novamente!!")