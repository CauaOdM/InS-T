import yfinance as yf
import numpy as np

def dados_calculate(acao):
    print(f"Processando {acao}...")

    dados = yf.download(acao,period="6mo", progress=False)

    if len(dados)==0:
        print("Dados não encontrados!")
        return
    
    precos = dados['Close'].values.flatten()

    #Vamos calculas a média móvel de 20 dias:

    window = 20
    weights = np.ones(window)/window
    media_movel = np.convolve(precos,weights, mode='valid')

    #dados mais atuais:

    preco_atual = precos[-1]
    media_atual = media_movel[-1]

    diferenca = preco_atual - media_atual

    if diferenca > 0:
        STATUS = 'ACIMA'
    else:
        STATUS = 'ABAIXO'
    
    print("-="*30)
    print(f"Preço Atual: R$ {preco_atual:.2f}")
    print(f"Média Móvel (20d): R$ {media_atual:.2f}")
    print(f"Status : O preço está {STATUS} da média.")
    print("-=" * 30)

    return dados, media_movel

if __name__ == "__main__":
    acao = input("Digite o código da ação (ex: PETR4.SA): ").upper()
    dados_calculate(acao)



