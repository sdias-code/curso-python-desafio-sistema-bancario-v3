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


def exibir_extrato(saldo, extrato):

    print("\nExibindo extrato")

    for operacao in extrato:

        item_valor = "R$ {:,.2f}".format(operacao["Valor"])
        print("---------------------------------------------------------------------")
        print(f"Tipo Operação: {operacao["Operacao"]}, Valor: {item_valor}")        
        print("---------------------------------------------------------------------")
        
    saldo_formatado = "Saldo em conta: R$ {:,.2f}".format(saldo)

    print(saldo_formatado)

def validar_saque(valor, valor_maximo, saldo):
    
    if valor >  valor_maximo:
        print("Limite superior a R$ 500,00, operação não realizada")
        return True

    if valor > saldo:
        print("Valor digitado é maior que o saldo na conta, operação não realizada")   
        return True     

def validar_quantidade_saque(qtde_saques, limite_saques):
    
    if qtde_saques >= limite_saques:
        print("Limite de saque superior ao permitido, operação não realizada")
        return True

def validar_valor_negativo(valor): # Validar entrada de valores negativos
    
    if valor <= 0:
        print("Não é permitido valores negativos, operação não realizada")
        return True  

def sacar(saldo, valor, extrato, valor_maximo, numero_saques, limite_saques): 
    if validar_saque(valor, valor_maximo, saldo):
        return saldo, numero_saques

    if validar_quantidade_saque(numero_saques, limite_saques):
        return saldo, numero_saques
    
    if validar_valor_negativo(valor):
        return  saldo, numero_saques  
    
    saldo -= valor

    numero_saques += 1  

    extrato.append({"Operacao": "Saque", "Valor": valor})    

    valor_formatado = "R$ {:,.2f}".format(valor)
    exibir_saque = f"""
    ------------------------------------------------------------------
                 você sacou: {valor_formatado}    

                Operação realizada com sucesso
"""
    print(exibir_saque)

    return float(saldo), numero_saques    

def depositar(saldo, valor, extrato, /):

    if validar_valor_negativo(valor):
        return
        
    saldo += valor

    extrato.append({"Operacao": "Depósito", "Valor": valor,})

    valor_formatado = "R$ {:,.2f}".format(valor)
    
    exibir_saque = f"""
    ------------------------------------------------------------------
                  você depositou: {valor_formatado}    

                  Operação realizada com sucesso
    ------------------------------------------------------------------
"""
    print(exibir_saque)

    return saldo

def valida_cpf(cpf): # Validar CPF  

    for usuario in usuarios:
        if usuario["Cpf"] == cpf:
            return True

    return False
    
def exibir_usuario_cadastrado(usuario): # Exibir usuário cadastrado
    
    print("\nUsuário cadastrado:")    
    print("----------------------------------------------------------------------------------------")
    print(f"Nome: {usuario["Nome"]}")
    print(f"Cpf: {usuario["Cpf"]}")
    print(f"Endereço: {usuario["Endereco"][0]["Logradouro"]}, {usuario["Endereco"][0]["Numero"]}, {usuario["Endereco"][0]["Bairro"]}, {usuario["Endereco"][0]["Cidade"]}")
    print("----------------------------------------------------------------------------------------")

def listar_usuarios():
    print("\nExibindo usuários cadastrados:")    
    
    for usuario in usuarios:
        print("-------------------------------------------------")
        print(usuario)
        print("-------------------------------------------------")

def cadastrar_usuario(): # Cadastrar Usuário
    
    # armazenar usuário numa lista, exemplo: nome, data nascimento, cpf e endereço (string separado por virgula)
    # endereço composto por logradouro, numero, bairro, cidade/sigla estado
    # validar cpf duplicado

    print("Digite o CPF:")
    cpf = input()

    if valida_cpf(cpf):
        print("CPF digitado já existe, digite outro CPF")
        cpf = input()
        valida_cpf(cpf)

    print("Digite o nome: ")
    nome = input()

    print("Digite data de nascimento, exemplo: dd/mm/aaaa")
    nascimento = input()       
    
    print("Digite o endereço, exemplo: logradouro, número, bairro, cidade/sigla estado")
    endereco = input()

    logradouro = endereco.split(",")[0]
    numero = endereco.split(",")[1]
    bairro = endereco.split(",")[2]
    cidade = endereco.split(",")[3]

    usuario = dict(Nome = nome, Nascimento = nascimento, Cpf = cpf, Endereco = [dict(Logradouro = logradouro, Numero = numero, Bairro = bairro, Cidade = cidade)],)

    usuarios.append(usuario)
    print("================================================")
    exibir_usuario_cadastrado(usuario)
    print("================================================")

def obter_usuario(cpf, usuarios):
    buscar_usuario_por_cpf = [usuario for usuario in usuarios if usuario["Cpf"] == cpf]
    return buscar_usuario_por_cpf[0] if buscar_usuario_por_cpf else None

def validar_usuario_cadastrado(cpf):
    for usuario in usuarios:
        if cpf == usuario["Cpf"]:
            return True
        
    return False

def exibir_conta_cadastrada(conta):
    
    print("\nConta cadastrada:")
    print("------------------------------------------------------------------------")
    print(f"Agencia: {conta["Agencia"]}")
    print(f"Número: {conta["Numero"]}")
    print(f"Usuario: {conta["Usuario"]}")
    print("------------------------------------------------------------------------")

def criar_conta(agencia, numero, numero_conta_sequencial, usuarios):
    print("Digite o CPF do usuário: ")

    cpf = input()

    usuario = obter_usuario(cpf, usuarios)

    if usuario:
        conta = {"Agencia": agencia, "Numero": numero, "Usuario": usuario}

        contas.append(conta)

        numero_conta_sequencial = numero_conta_sequencial + 1

        exibir_conta_cadastrada(conta)
        return False
    
    return True

def cadastrar_conta_corrent():
    # armazenar conta numa lista, composta por agencia, numero da conta e usuário da conta é sequencial, iniciando em 1
    # o número da agencia é fixo: "0001"
    # usuário pode ter mais de uma conta
    # uma conta pertence somente a um usuário
    # uma conta não existe sem estar vinculada a um usuário    

    numero_conta_temp = numero_conta_sequencial + 1

    if criar_conta(AGENCIA, numero_conta_temp, numero_conta_sequencial, usuarios):
        print("Não foi possível criar conta corrente, não existe usuário cadastrado com esse CPF")      

def listar_contas():
    print("\nListando contas cadastradas:")

    for conta in contas:
        print("----------------------------------------------------")
        print(conta)
        print("----------------------------------------------------")

def exibir_menu():
    menu = """
    ===========================================================    
    ============ Sistema bancário Versão 2.0 ==================
    ===========================================================
    Opção [1] Saque
    Opção [2] Depósito
    Opção [3] Cadastrar Usuário
    Opção [4] Listar usuários
    Opção [5] Cadastrar conta corrente
    Opção [6] Listar contas
    Opção [7] Extrato
    Opção [8] Sair
    """
    print(menu)
    print()
    print("Escolha uma opção:")    

def main():
    saldo_bancario = 0
    numero_saques = 0
    valor_digitado = 0
    valor_maximo_saque = 500
    numero_conta_sequencial = 1

    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    registro_extrato = []
    usuarios = []
    contas = []

    while True:
        exibir_menu()

        opcao = int(input())
        if opcao == 8:
            break

        elif opcao == 1: # Saque
            print("Digite um valor para saque: ")

            valor_digitado = float(input())         

            saldo_bancario, numero_saques = sacar(
                saldo = saldo_bancario, 
                valor = valor_digitado, 
                extrato = registro_extrato, 
                valor_maximo = valor_maximo_saque, 
                numero_saques = numero_saques, 
                limite_saques = LIMITE_SAQUES)              

        elif opcao == 2: # Depósito
            print("Digite um valor para depósito: ")

            valor_digitado = float(input())

            saldo_bancario =  depositar(saldo_bancario, valor_digitado, registro_extrato)                    

        elif opcao == 3: # Cadastrar Usuário
            cadastrar_usuario()

        elif opcao == 4: # Listar usuários
            listar_usuarios()   

        elif opcao == 5: # Cadastrar conta corrente
            cadastrar_conta_corrent()  

        elif opcao == 6: # Listar contas cadastradas
            listar_contas()
            
        elif opcao == 7: # Extrato
            exibir_extrato(saldo_bancario, registro_extrato)

        else:
            print ("Operação inválida, por favor selecione novamente a operação desejada.")   

main()