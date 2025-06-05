import textwrap
from abc import ABC, abstractmethod
from datetime import datetime, timezone

clientes = []
contas = []


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência: {conta.agencia}
            Número: {conta.numero}
            Titular: {conta.cliente.nome}
            Saldo: {conta.saldo:.2f}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\nVocê excedeu as transações diárias!")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return f"{self.nome} | CPF: {self.cpf} | Nascimento: {self.data_nascimento}"


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len([
            transacao
            for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        ])

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now(timezone.utc).date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d-%m-%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado

    return envelope


def menu(cliente):
    try:
        menu = f"""\n
        ==================== Bem Vindo {cliente.nome} ====================
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nc] Nova Conta
        [lc] Listar Contas
        [nu] Novo Usuário
        [q] Sair\n
        Digite a Opção: """
        return input(textwrap.dedent(menu))
    except KeyboardInterrupt:
        print("\nDigite 'q' para encerrar o programa!")
        return "q"  # Retorna 'q' para sair do programa

def MenuInicial():
    while True:
        print("==================== Sistema Bancário RM ====================\n")
        print("lo - Login")
        print("re - Registro")
        print("d - Depositar")
        print("q - Sair")
        opcao = input("Escolha: ")

        if opcao == "lo":
            cliente = TelaLogin(clientes)
            if cliente:
                main(cliente)  # <-- Agora com o cliente logado
        
        elif opcao == "re":
            criar_cliente(clientes)
            
        elif opcao == "d":
            depositar(clientes)
        
        elif opcao == "q":
            print("\nSistema Bancário V2.0")
            print("Desenvolvido por Rafael Mendes para DIO")
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!!")

def TelaLogin(clientes):
    nome = input("Digite seu nome completo: ")
    cpf = input("Digite seu CPF: ")

    for cliente in clientes:
        if cliente.nome.lower() == nome.lower() and cliente.cpf == cpf:
            print(f"\n Login realizado com sucesso! Bem-vindo, {cliente.nome}!")
            return cliente

    print("\n❌ Nome ou CPF incorretos.")
    return None


def main(cliente_logado):

    while True:
        opcao = menu(cliente_logado)

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            extrato(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "q":
            print("\nSistema Bancário V2.0")
            print("Desenvolvido por Rafael Mendes para DIO")
            print("Saindo do sistema...")
            exit()

        else:
            print("\nERRO: Comando inválido, tente novamente!")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nERRO: Cliente não possui conta!")
        return None
    
    # Permite selecionar conta se houver mais de uma
    if len(cliente.contas) > 1:
        print("\nContas disponíveis:")
        for i, conta in enumerate(cliente.contas):
            print(f"{i+1} - Agência: {conta.agencia} Número: {conta.numero}")
        
        opcao = int(input("Selecione o número da conta: ")) - 1
        return cliente.contas[opcao]
    
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\nCliente {cpf} não encontrado!")
        return

    try:
        valor = float(input("Informe o valor do Deposito: "))
        transacao = Deposito(valor)
    except ValueError:
        print("Valor inválido!")

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\nCliente {cpf} não encontrado!")
        return

    try:
        valor = float(input("Informe o valor do Deposito: "))
        transacao = Saque(valor)
    except ValueError:
        print("Valor inválido!")

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\nCliente {cpf} não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n==================== EXTRATO ====================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:R$ {transacao['valor']:.2f}\n"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações!"

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==================================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(f"\nCliente {cpf} já cadastrado!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (Rua, Número - Cidade/Estado): ")

    cliente = PessoaFisica(
        nome=nome, 
        data_nascimento=data_nascimento, 
        cpf=cpf, 
        endereco=endereco
    )

    clientes.append(cliente)

    print(f"\nCliente {nome} cadastrado com sucesso!")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\nCliente {cpf} não encontrado!")
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente,
        numero=numero_conta,
        limite=500,
        limite_saques=3  # Valor padrão mais razoável
    )
    
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f"\nConta {numero_conta} criada com sucesso!")


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))



MenuInicial()