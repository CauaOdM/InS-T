from dotenv import load_dotenv
import os
import google.generativeai as genai
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

load_dotenv(".env.local")
genai.configure(api_key=os.getenv("API_KEY"))

def dados_calculate(acao):
    print(f"Iniciando a análise de {acao}...")

    print("Carregando cotações...")
    dados = yf.download(acao,period="6mo", progress=False)

    if len(dados)==0:
        print("Ação não encontrada!")
        return
    
    precos = dados['Close'].values.flatten()

    print("Calculando Indicadores...")

    #Média móvel de 20 dias:

    window = 20
    weights = np.ones(window)/window
    media_movel = np.convolve(precos,weights, mode='valid')

    #ATUAL:
    preco_atual = precos[-1]
    media_atual = media_movel[-1]

    #VOLATILIDADE (DESVIO PADRÃO):
    retornos = np.diff(precos) / precos[:-1]
    volatilidade = np.std(retornos) * 100

    print(f"Volatilidade: {volatilidade:.2f}%")

    print("-="*30)
    print("Gerando gráfico...")
    print("-="*30)

    plt.figure(figsize=(10, 5))

    #Preço real

    plt.plot(dados.index[window-1:], precos[window-1:], label='Preço Real', color='blue', alpha=0.5)

    #Média móvel

    plt.plot(dados.index[window-1:], media_movel, label='Média Móvel (20d)', color='orange', linewidth=2)

    plt.title(f'Análise de {acao}')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.legend()
    plt.grid(True)
    plt.show()

    nome_arquivo = f"grafico_{acao}.png"
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"✅ Gráfico salvo: {nome_arquivo}")

    print("Consultando Agente AI...")

    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Você é um Analista Técnico de Investimentos Sênior.
    Analise os dados técnicos abaixo para a ação {acao}:
    
    1. Preço Atual: R$ {preco_atual:.2f}
    2. Média Móvel (20 dias): R$ {media_atual:.2f}
    3. Volatilidade do período: {volatilidade:.2f}% (Considerar > 2% como alta).
    
    Tarefa:
    - Compare o Preço com a Média (Se preço > média = Tendência de Alta/Baixa).
    - Avalie o risco baseado na volatilidade.
    - Dê um veredito final curto: COMPRA, VENDA ou AGUARDAR.
    
    Responda em tópicos curtos e diretos.
    """
    
    response = model.generate_content(prompt)
    
    print("\n" + "="*40)
    print(response.text)
    print("="*40)


if __name__ == "__main__":
    acao = input("Digite o ticker (ex: PETR4.SA): ").upper()
    dados_calculate(acao)