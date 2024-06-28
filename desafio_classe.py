# Desafio sistema bancário versão 3.0
## Implementar UML fornecido como exemplo usando estrutura de classes e interface

# Operações: depósito, saque, extrato
# Obs. Não permitir lançamento de valores negativos, exibir os valores  depositados no extrato
# O sistema deve permitir 3 saques diarios com limite máximo de R$ 500,00
# Os valores devem estar formatados com base na moeda atual (Real)

# Incluir funcoes: Saque, Depósito, visualizar extrato
# Criar usuário
# Criar conta corrente e vincular com usuário

# Dica: vincular usuário a uma conta, filtre a lista de usuários buscando o numero do cpf
# Resumo: vincular conta por cpf

from abc import ABC, abstractclassmethod, abstractproperty
import datetime

# Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)    

# Pessoa física
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Conta
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
        saldo = self._saldo
        saldo_excedido = valor > saldo

        if saldo_excedido:
            print("Valor do saque superior ao saldo em conta.")

        elif valor  > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso.")  
            return True

        else:
            print("Operação falhou, o valor informado é inválido.")
                
        return False    

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
            return True
        else:
            print("Operação falhou, o valor informado é inválido.")
            return False        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limite_saques    

        if excedeu_limite:
            print("Operação falhou, limite de R$ 500,00 excedido.")

        elif excedeu_saque:
            print("Operação falhou, Número máximo de saques excedido.")    

        else:
            return super().sacar(valor)

        return False    

    def __str__(self):
            return f"""
            Agencia: {self.agencia}
            C/C {self.numero}
            Titular: {self.cliente.nome}
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
                "tipo": transacao.__class__.__name__ ,
                "valor": transacao.valor,
                "data": datetime.date.today() #.strftime('%d-%m-%Y %H:%M:%s'),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
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
 
# Validar entrada de valores negativos
def validar_valor_negativo(valor):    
    if valor <= 0:  
        print("Não é permitido valores negativos ou igual a zero, operação não realizada")      
        return True

# Validar CPF
def valida_cpf(cpf, clientes):   

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("CPF já existe cadastrado")
        return True

    return False
    
# Filtrar Cliente
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf] 
    return clientes_filtrados[0] if clientes_filtrados else None

# Recuperar conta cliente
def recuperar_conta_cliente(cliente):    
    if not cliente.contas:
        print("Cliente não possui conta")
        return 

    return cliente.contas[0]

# Depositar
def depositar(clientes):
    operacao("deposito", clientes)

# Sacar
def sacar(clientes): 
    operacao("saque", clientes)

def operacao(tipo, clientes):
    cpf = input("Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    entrada_valor = input(f"Informe o valor para {tipo}: ")   

    if entrada_valor.isdigit():
        valor = float(entrada_valor)

        if validar_valor_negativo(valor):
            return

        conta = recuperar_conta_cliente(cliente)

        if not conta:
            return

        transacao = 0

        if tipo == "deposito":
            transacao = Deposito(valor)
        elif tipo == "saque":
            transacao = Saque(valor)

        cliente.realizar_transacao(conta, transacao)

    else:
        print("Valor digitado inválido")
        return  
    
# Exibir usuário cadastrado    
def exibir_cliente_cadastrado(cliente): 

    print("\nCliente cadastrado:")    
    print("-" * 40)
    print(f"Nome: {cliente.nome}")
    print(f"Cpf: {cliente.cpf}")
    print(f"Endereço: {cliente.endereco[0]['logradouro']}, {cliente.endereco[0]['numero']}, {cliente.endereco[0]['bairro']}, {cliente.endereco[0]['cidade']}")
    print("-" * 40)

# Listar clientes
def listar_clientes(clientes):
    print("\nExibindo clientes cadastrados:")    
    
    for cliente in clientes:
        print("-" * 40)    
        info_cliente = f"""
        Nome: {cliente.nome}
        Data de Nascimento: {cliente.data_nascimento}
        CPF: {cliente.cpf}
        Endereço: {cliente.endereco[0]['logradouro']}, {cliente.endereco[0]['numero']}, {cliente.endereco[0]['bairro']}, {cliente.endereco[0]['cidade']}
        """    
        print(info_cliente)
        print("-" * 40)
 
# Criar Clientes 
def criar_cliente(clientes): # Cadastrar Usuário
    
    # armazenar usuário numa lista, exemplo: nome, data nascimento, cpf e endereço (string separado por virgula)
    # endereço composto por logradouro, numero, bairro, cidade/sigla estado
    # validar cpf duplicado

    cpf = input("Informe o CPF do cliente: ")

    while valida_cpf(cpf, clientes):
        cpf = input("Informe um CPF válido: ")
        valida_cpf(cpf, clientes)       

    nome = input("Digite o nome do cliente: ")

    nascimento = input("Digite data de nascimento, exemplo: dd/mm/aaaa: ")       
    
    endereco = input("Digite o endereço, exemplo: logradouro, número, bairro, cidade/sigla estado: ")

    logradouro = endereco.split(",")[0]
    numero = endereco.split(",")[1]
    bairro = endereco.split(",")[2]
    cidade = endereco.split(",")[3]

    cliente = PessoaFisica(
        nome = nome, 
        data_nascimento = nascimento, 
        cpf = cpf, 
        endereco = [dict(logradouro = logradouro, numero = numero, bairro = bairro, cidade = cidade)],)

    clientes.append(cliente)

    print("=" * 40)
    exibir_cliente_cadastrado(cliente)
    print("=" * 40)

# Criar conta
def criar_conta(numero_conta, clientes, contas): 
    cpf = input("Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)

    cliente.contas.append(conta)

    print("Conta criada com sucesso")

def listar_contas(contas):
    print("\nListando contas cadastradas:")

    for conta in contas:
        print("-" * 40)
        info_conta = f"""
        Agencia: {conta.agencia}
        C/C: {conta.numero}
        Cliente: {conta.cliente.nome}
        """
        print(info_conta)
        print("-" * 40)

# Exibir extrato
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    if not cliente.contas:
        print("Conta não encontrada.")
        return            

    print("\nExibindo extrato")

    transacoes = cliente.contas[0].historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \n\tR$ {transacao['valor']:.2f}" 
    print(extrato)
    print(f"\nSaldo: \n\tR$ {cliente.contas[0].saldo:.2f}")    
    print("=" * 40)

def exibir_menu():
    menu = """
    ===========================================================    
    ============ Sistema bancário Versão 2.0 ==================
    ===========================================================
    Opção [1] Saque
    Opção [2] Depósito
    Opção [3] Cadastrar clientes
    Opção [4] Listar clientes
    Opção [5] Cadastrar contas
    Opção [6] Listar contas
    Opção [7] Extrato
    Opção [8] Sair
    """
    print(menu)
    print()    

def main(): 

    clientes = []
    contas = []

    # Sistema com dois clientes e duas contas pré-preenchidos
    cliente1 = PessoaFisica(
        nome = "Silvio Dias",
        data_nascimento = "26/02/1980", 
        cpf = '12345', 
        endereco = [dict(logradouro = "Rua Barata Ribeiro", numero = 35, bairro = "Copacabana", cidade = "Rio de Janeiro/RJ")],)

    clientes.append(cliente1)

    cliente2 = PessoaFisica(
    nome = "Marcos Dias", 
    data_nascimento = "22/05/1990", 
    cpf = '123456', 
    endereco = [dict(logradouro = "Rua São Clemente", numero = 104, bairro = "Botafogo", cidade = "Rio de Janeiro/RJ")],)

    clientes.append(cliente2)

    conta1 = ContaCorrente.nova_conta(cliente=cliente1, numero=1)
    contas.append(conta1)
    cliente1.contas.append(conta1)

    conta2 = ContaCorrente.nova_conta(cliente=cliente2, numero=2)
    contas.append(conta2)
    cliente2.contas.append(conta2)


    while True:
        exibir_menu()

        entrada = input("Escolha uma opção: ")

        opcao = int(entrada)

        if opcao == 8:
            break

        elif opcao == 1: # Saque
            sacar(clientes)          

        elif opcao == 2: # Depósito
           depositar(clientes)                 

        elif opcao == 3: # Cadastrar clientes
            criar_cliente(clientes)

        elif opcao == 4: # Listar clientes
            listar_clientes(clientes)   

        elif opcao == 5: # Cadastrar contas
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)  

        elif opcao == 6: # Listar contas cadastradas
            listar_contas(contas)
            
        elif opcao == 7: # Extrato
            exibir_extrato(clientes)

        else:
            print ("Operação inválida, por favor selecione novamente a operação desejada.")   

main()