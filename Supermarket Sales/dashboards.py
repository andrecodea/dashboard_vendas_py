import streamlit as st # interface
import pandas as pd # análise de dados
import plotly.express as px # gráficos

st.set_page_config(layout="wide")
# ====================================

# 1. Glossário:
# 2. df: DataFrame
# 3. dtype: Data Type >>> Tipo de dado
#4. lambda: Função de apenas uma linha 
    # incrementar = lambda x: x + 1
    # print(incrementar(5)) 
    # >>> 6


# ====================================

# Objetivo - Visão mensal de:
# 1 - Faturamento por unidade;
# 2 - Tipo de produto mais vendido;
# 3 - Contribuição por filial;
# 4 - Desempenho das formas de pagamento;
# 5 - Avaliações das filiais.

# ================ INICIO DO CÓDIGO ====================

# Realiza a leitura do arquivo csv por meio do pandas:
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

# Formata os dados de datas da tabela "Date" do dtype "object" para o dtype "datetime":
df["Date"] = pd.to_datetime(df["Date"])

# Ordena o conjunto de dados da tabela "Date":
df = df.sort_values(by="Date")


# Cria uma nova coluna "Month" no DataFrame onde cada valor é uma string no formato "ano-mês", derivada da coluna "Date". 
# Isso é útil para agregar ou filtrar dados por mês e ano, facilitando a análise temporal.
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Cria uma caixa de seleção de nome "Mês" na barra lateral esquerda para filtragem de dados por mês.
# A função "unique()" garante que não hajam duplicações.
month = st.sidebar.selectbox("Month", df["Month"].unique())

# Cria um filtro por meio do pandas que filtra o 'df' retornando apenas as linhas onde a coluna "Month" correspondem ao valor selecioniado na caixa de seleção.
df_filtered = df[df["Month"] == month]
# df resultante da filtragem
df_filtered

# Cria duas colunas na tela da aplicação.
col1, col2 = st.columns(2)
# Cria mais três colunas abaixo das duas colunas criadas anteriormente.
col3, col4, col5 = st.columns(3)

# Exibe um gráfico em barras por meio do plotly express a partir do DataFrame "df_filtered".
# Os dados exibidos são: Datas, filiais e o total de vendas nessas datas e filiais (diariamente).
# Os dados são divididos por cores representando as filiais da empresa.
fig_date=px.bar(df_filtered, x="Date", y="Total", color="City", title="Revenue per day" )

# Exibe o gráfico criado garantindo que o gráfico permaneça no tamanho estipulado pela coluna.
col1.plotly_chart(fig_date, use_container_width=True)


# Exibe um gráfico em barras por meio do plotly express a partir do DataFrame "df_filtered".
# Os dados exibidos são: Datas, filiais e o tipo de produto vendido nessas datas e filiais.
# Os dados são divididos por cores representando as filiais da empresa.
# A orientação do gráfico será horizontal (orientation="h")
fig_prod=px.bar(df_filtered, x="Date", y="Product line", color="City", title="Revenue by product type", orientation="h" )

# Exibe o gráfico criado garantindo que o gráfico permaneça no tamanho estipulado pela coluna.
col2.plotly_chart(fig_prod, use_container_width=True)

# Cria um DataFrame e realiza uma operação de agrupamento entre as filiais da empresa e o total de vendas.
# Resultando no total de vendas por filial.
# "reset_index()" permite-nos acessar os valores de filial e total no gráfico.
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()

# Cria um gráfico a partir do DataFrame "city_total" para exibir o total de vendas por filial a partir da operação de agrupamento.
fig_city = px.bar(city_total, x="City", y="Total", title="Revenue by branch")

# Exibe o gráfico criado garantindo que o gráfico permaneça no tamanho estipulado pela coluna.
col3.plotly_chart(fig_city, use_container_width=True)

# Cria um gráfico em forma de pizza a partir do DataFrame "df_filtered" para exibir o total de vendas por  tipo de pagamento.
# Note que não há valores "x" e "y", apenas "values" e "names".
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Revenue by payment type")

# Exibe o gráfico criado garantindo que o gráfico permaneça no tamanho estipulado pela coluna.
col4.plotly_chart(fig_kind, use_container_width=True)

# Realiza uma operação de agrupamento entre as filiais da empresa e as avaliações médias.
# A função "mean()" realiza a média das avaliações
city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()

# Cria um gráfico em forma de barras 
fig_rating = px.bar(df_filtered, y="Rating", x="City", title="Average rating")

# Exibe o gráfico criado garantindo que o gráfico permaneça no tamanho estipulado pela coluna.
col5.plotly_chart(fig_rating, use_container_width=True)