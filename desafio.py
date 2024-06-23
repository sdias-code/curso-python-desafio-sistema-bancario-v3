# Desafio sistema bancário versão 1.0
# Operações: depósito, saque, extrato
# Obs. Não permitir lançamento de valores negativos, exibir os valores  depositados no extrato
# O sistema deve permitir 3 saques diarios com limite máximo de R$ 500,00
# Os valores devem estar formatados com base na moeda atual (Real)

saldo_bancario = 0
registro_extrato = []
registro_saque = 0
LIMITE_SAQUE = 3
valor_maximo_saque = 500

def ConsultaExtrato():
    print(list(registro_extrato))

def ValidarSaque(valor_digitado):
    if valor_digitado >  valor_maximo_saque:
        print("Limite superior a R$ 500,00, operação não realizada")
        return True

    if valor_digitado > saldo_bancario:
        print("Valor digitado é maior que o saldo na conta, operação não realizada")   
        return True

def ValidarQuantidadeSaque():
    if registro_saque >= 3:
        print("Limite de saque superior ao permitido, operação não realizada")
        return True

def ValidarValorNegativo(valor_digitado):
    if valor_digitado <= 0:
        print("Não é permitido valores negativos, operação não realizada")
        return True        


while True:
    menu = """
    ===========================================================    
    ============ Sistema bancário Versão 1.0 ==================
    ===========================================================
    Opção [1] Saque
    Opção [2] Depósito
    Opção [3] Extrato
    Opção [4] Sair
    """
    print(menu)
    print()
    print("Escolha uma opção:")

    opcao = int(input())
    if opcao == 4:
        break

    elif opcao == 1:
        print("Digite um valor para saque: ")
        valor_digitado = float(input())   

        if ValidarSaque(valor_digitado):
            continue

        if ValidarQuantidadeSaque():
            continue

        if ValidarValorNegativo(valor_digitado):
            continue

        saldo_bancario -= valor_digitado

        registro_saque = registro_saque + 1        

        registro_extrato.append({"Operacao": "Saque", "Valor": valor_digitado})

        valor_formatado = "R$ {:,.2f}".format(valor_digitado)

        print(f"Você sacou: {valor_formatado}")

        print("Operação realizada com sucesso")


    elif opcao == 2:
        print("Digite um valor para depósito: ")

        valor_digitado = float(input())
         
        if ValidarValorNegativo(valor_digitado):
            continue
        
        saldo_bancario += valor_digitado

        registro_extrato.append({"Operacao": "Depósito", "Valor": valor_digitado})

        valor_formatado = "R$ {:,.2f}".format(valor_digitado)

        print(f"Você depositou: {valor_formatado}")

        print("Operação realizada com sucesso")


    elif opcao == 3:
        print("Exibindo extrato")

        for item in registro_extrato:

            item_valor = "R$ {:,.2f}".format(item["Valor"])

            print(f"Tipo Operação: {item["Operacao"]}, Valor: {item_valor}")        
        
        saldo_em_conta = "Saldo em conta: R$ {:,.2f}".format(saldo_bancario)

        print(saldo_em_conta)

    else:
        print ("Operação inválida, por favor selecione novamente a operação desejada.")   






     




