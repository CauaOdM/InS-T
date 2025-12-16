# InS&T – Analista Técnico Junior para S&T (powered by IA)

> ⚠️ Este README foi escrito por IA generativa, e o código também conta com trechos assistidos por IA (marcados ao longo do arquivo). Use com senso crítico.

Autor: [CauaOdM](https://github.com/CauaOdM) — estudante de Engenharia de Computação no Insper.


## O que é o InS&T?
Um “analista técnico júnior” de linha de comando com foco na área de Sales & Trading (S&T), projetado como suporte técnico à tomada de decisão. Ele:
- Baixa cotações de qualquer ticker via `yfinance` (ex.: PETR4.SA, AAPL, TSLA).
- Calcula rapidamente indicadores clássicos: RSI, média móvel simples (20) e volatilidade dos retornos.
- Gera um gráfico elegante (preço + média em cima; RSI embaixo) salvo como `analise_pro_<TICKER>.png`.
- Conversa com o modelo Gemini para fornecer um veredito textual (COMPRA/NEUTRO/VENDA), funcionando como apoio sintético e objetivo para decisões rápidas.

## Por que é útil? 
- Suporte técnico à tomada de decisão para mesas de S&T, traders e sales: consolida sinais de tendência e momentum em segundos.
- Gráfico pronto para compartilhar ou embutir em relatórios e briefs intra‑day.
- Uma opinião resumida via IA para complementar (não substituir) a leitura humana do mercado.

## Como o fluxo acontece (passo a passo)
1) Você informa o ticker no terminal.
2) O script baixa 6 meses de preços de fechamento com `yfinance`.
3) Calcula indicadores:
	 - RSI de 14 períodos (força/momentum).
	 - Média móvel simples de 20 períodos (tendência suave).
	 - Volatilidade: desvio padrão dos retornos diários em % (nervosismo do ativo).
4) Cria dois painéis no gráfico: preço vs. média e RSI com faixas de 30/70.
5) Monta um prompt com os números atuais e pede ao Gemini (`gemini-2.5-flash`) um veredito curto e justificado.
6) Salva o PNG e imprime a análise do modelo no terminal.

## Indicadores, em português claro
- **RSI (Relative Strength Index)**: escala 0–100 que mede velocidade/força dos movimentos. Acima de 70 = sobrecompra (pode esfriar); abaixo de 30 = sobrevenda (pode reagir). É calculado comparando ganhos e perdas médios nos últimos 14 períodos.
- **Média Móvel Simples (20)**: a “linha de tendência” curta. Preço acima dela sugere viés de alta; abaixo, viés de baixa.
- **Volatilidade (% dos retornos)**: quanto o preço oscila dia a dia. Alta volatilidade = mais risco e mais oportunidade; baixa volatilidade = movimentos mais suaves.

## Sobre o código 
- `load_dotenv` + `genai.configure`: carrega `API_KEY` do arquivo `.env.local` e configura o cliente Gemini.
- `calcular_rsi(dados, janela=14)`: pega a série de preços, calcula variações, separa ganhos/perdas, aplica médias móveis e devolve o RSI.
- `dados_calculate(acao)`: o maestro da orquestra.
	- Baixa 6 meses de dados com `yf.download`.
	- Extrai `Close` e calcula RSI, média móvel 20 e volatilidade dos retornos.
	- Lê o estado atual: preço do último dia, média do último dia, RSI atual e a tendência (ALTA/BAIXA) baseada na posição do preço vs. média.
	- Plota dois subgráficos (preço+média e RSI), salva a figura e fecha para não vazar memória.
	- Monta o prompt com os números e chama o modelo `gemini-2.5-flash` para um veredito curto.
	- Imprime o texto retornado.
- `if __name__ == "__main__"`: ponto de entrada; pergunta o ticker e chama `dados_calculate`.

## Entradas e saídas
- Entrada: ticker digitado (ex.: `PETR4.SA`).
- Saídas:
	- PNG: `analise_pro_<TICKER>.png` com preço, média e RSI.
	- Texto no terminal: resumo com veredito da IA.

## Como rodar
1. Crie `.env.local` com `API_KEY=<sua_chave_gemini>`.
2. Instale dependências: `pip install -r requirements.txt`.
3. Rode: `python junior.py` e digite o ticker.
4. Confira o PNG gerado na raiz e leia a análise impressa.

## Possíveis próximas melhorias
- Alinhar perfeitamente séries e índices para evitar qualquer descompasso entre preço e médias (usar rolling direto no DataFrame).
- Incluir mais indicadores (MACD, Bandas de Bollinger, OBV) e permitir ligar/desligar via flags.
- Registrar histórico das análises em CSV/SQLite para acompanhar decisões ao longo do tempo.
- Criar uma interface web simples para visualizar gráficos e laudos em segundos.

Obrigado pelo tempo e por experimentar o InS&T! 🚀🎉
