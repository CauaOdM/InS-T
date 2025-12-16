from dotenv import load_dotenv
import os
import google.generativeai as genai
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

load_dotenv(".env.local")
genai.configure(api_key=os.getenv("API_KEY"))

# Calculo do RSI 
def calcular_rsi(dados, janela=14):
    delta = dados.diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=janela).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=janela).mean()
    
    rs = ganho / perda
    rsi = 100 - (100 / (1 + rs))
    return rsi

def dados_calculate(acao):
    print(f"Iniciando a análise de {acao}...")

    print("Carregando cotações...")
    
    dados = yf.download(acao, period="6mo", progress=False)

    if len(dados) == 0:
        print("Ação não encontrada!")
        return
    
    # Seleciona a coluna de preços
    if 'Close' in dados.columns:
        series_precos = dados['Close']
    else:
        series_precos = dados.iloc[:, 0]

    
    print("Calculando Indicadores...")
    rsi = calcular_rsi(series_precos)

    
    precos_numpy = series_precos.values.flatten()

    # Média móvel de 20 dias
    janela = 20
    weights = np.ones(janela) / janela
    media_movel = np.convolve(precos_numpy, weights, mode='valid')

    # ATUAL
    preco_atual = precos_numpy[-1]
    media_atual = media_movel[-1]
    rsi_atual = rsi.iloc[-1].item()

    # TENDÊNCIA
    if preco_atual > media_atual:
        tendencia = "ALTA"
    else:
        tendencia = "BAIXA"

    # VOLATILIDADE
    retornos = np.diff(precos_numpy) / precos_numpy[:-1]
    volatilidade = np.std(retornos) * 100

    print(f"Volatilidade: {volatilidade:.2f}%")

    # GRÁFICOS feitos com auxilio de IA generativa
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    # Gráfico 1: Preço e Média
    
    ax1.plot(dados.index, precos_numpy, label='Preço', color='blue', alpha=0.6)
    ax1.plot(dados.index[janela-1:], media_movel, label='Média (20)', color='orange', linestyle='--')
    ax1.set_title(f"Análise Técnica: {acao}")
    ax1.legend()
    ax1.grid(True)
    
    # Gráfico 2: RSI
    ax2.plot(dados.index, rsi, label='RSI (14)', color='purple')
    ax2.axhline(70, color='red', linestyle='--', alpha=0.5)
    ax2.axhline(30, color='green', linestyle='--', alpha=0.5)
    ax2.set_ylabel('RSI')
    ax2.grid(True)
    
    nome_arquivo = f"analise_pro_{acao}.png"
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Gráfico salvo: {nome_arquivo}")

    print("Consultando Agente AI...")

    
    model = genai.GenerativeModel('gemini-2.5-flash')

    #Prompt feito com auxilio de IA generativa

    prompt = f"""
    Atue como um Analista Financeiro Quantitativo.
    Analise os indicadores técnicos de {acao}:
    
    1. Preço vs Média (Tendência):
       - Preço: {preco_atual:.2f}
       - Média (20): {media_atual:.2f}
       - Status: {tendencia}
       
    2. RSI (Momentum/Velocidade):
       - Valor Atual: {rsi_atual:.2f}
       - Regra: RSI > 70 é Sobrecompra (risco de queda). RSI < 30 é Sobrevenda (chance de subida).
       - Volatilidade: {volatilidade:.2f}%
    
    TAREFA:
    Cruze as informações.
    - Exemplo: Se Tendência é BAIXA mas RSI < 30, pode ser uma chance de reversão (compra arriscada).
    - Exemplo: Se Tendência é ALTA e RSI > 70, o preço pode estar esticado demais (cuidado).
    
    Dê um veredito final: COMPRA FORTE, COMPRA, NEUTRO, VENDA ou VENDA FORTE.
    Justifique em 3 linhas.
    """
    
    response = model.generate_content(prompt)
    
    print("\n" + "="*40)
    print(response.text)
    print("="*40)


if __name__ == "__main__":
    acao = input("Digite o ticker (ex: PETR4.SA): ").upper()
    dados_calculate(acao)