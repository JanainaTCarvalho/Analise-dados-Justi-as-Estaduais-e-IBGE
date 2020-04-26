# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:07:43 2020

@author: Janaina Teixeira Carvalho

Análise exploratória de dados - Terceira semana AceleraDev Codenation

Comparativa do tempo médio do processo nas justiças estaduais com dados populacionais fornecidos pelo IBGE.
"""

import pandas as pd
import altair as alt
import streamlit as st


def criar_barras(coluna_cat, coluna_num, df):
    bars = alt.Chart(df, width = 600).mark_bar().encode(
        x=alt.X(coluna_cat),
        y=alt.Y(coluna_num, stack='zero'),
        tooltip=[coluna_num, coluna_cat]
    ).interactive()
    return bars

def criar_scatterplot(x, y, df):
    graus = [1, 5, 8]

    base = alt.Chart(df, width=800, height=400).mark_circle(color="black").encode(
        alt.X(x), alt.Y(y))

    polynomial_fit = [
        base.transform_regression(
            x, y, method="poly", order=order, as_=[x, str(order)]
        )
        .mark_line()
        .transform_fold([str(order)], as_=["Graus", y])
        .encode(alt.Color("Graus:N"))
        for order in graus
    ]
    return alt.layer(base, *polynomial_fit)

#Criação do mapa de correlação
def cria_correlationplot(df, colunas_numericas):
    dados = (df[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlacao', 'level_0': 'variavel1', 'level_1': 'variavel2'})
    dados['aba_correlacao'] = dados['correlacao'].map('{:.2f}'.format) #Arredondar para 2 decimal
    base = alt.Chart(dados, width=900, height=900).encode( x = 'variavel2:O', y = 'variavel1:O')
    text = base.mark_text().encode(text = 'aba_correlacao',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
    alt.value('black')))

    # Mapa de correlação
    cor_plot = base.mark_rect().encode(
    color = 'correlacao:Q')

    return cor_plot + text

def main():
    st.title('Análise exploratória de dados - AceleraDev Data Science')
    st.header('Comparativa de dados nas justiças estaduais com dados populacionais fornecidos pelo IBGE.')
    st.image('BrasilMartelo.jpg')
    
    #Importação dos dados
    ibge = pd.read_csv('Estados_IBGE.csv', sep = ';')
    custo = pd.read_csv('Estadual_custo.csv', sep = ';')
    execucao = pd.read_csv('Estadual_Execucao.csv', sep = ';')
    porte = pd.read_csv('Estadual_porte.csv', sep = ';')
    sentenca = pd.read_csv('Estadual_Sentenca.csv', sep = ';')
    perc_pop = pd.read_csv('Estadual_PercentualPopResidenteMunicipioSede.csv', sep = ';')
    
     #Transformação das tabelas em um único dataframe
    df = pd.merge(ibge, custo, on  = 'Estados')
    df = pd.merge(df, sentenca, on  = 'Estados')
    df = pd.merge(df, execucao, on  = 'Estados')
    df = pd.merge(df, porte, on  = 'Estados')
    df = pd.merge(df, perc_pop, on  = 'Estados')
    
    #Visualização das tabelas importadas
    st.sidebar.title('Justiça Estaduais e dados do IBGE por estado')
    st.sidebar.subheader('Conheça os dados utilizados na análise')
    tabelas_individuais = st.sidebar.selectbox('Selecione a tabela', ('Dados Gerais', 'Dados IBGE', 'Custo da Justiça por habitante', 'Tempo médio conhecimento e execução', 
                                                'Tempo médio sentença', 'Percentual população em sede de comarca', 'Outros dados', 'Tabela completa')
                                               )
    if tabelas_individuais:
        if tabelas_individuais == 'Dados Gerais':
            st.write('Um dos problemas mais comentados quando se trata de justiça no Brasil é o longo tempo de tramitação do processo. Nesse breve trabalho de exploração de dados procuro relacionar os dados das Justiças Estaduais, incluindo tempo médio dos processos, com dados populacionais do mesmo estado, procurando entender se o tempo médio do processo pode estar relacionado com o desenvolvimento do estado, quantidade de habitantes, densidade populacional, investimento financeiro na justiça e outros dados.')
            st.write('-> Esse trabalho foi desenvolvido para o desafio de Análise exploratória de dados proposto na Aceleração em Data Science da Codenation pelo professor Túlio Vieira de Souza.')
            st.write('*Os dados relativos às Justiças Estaduais foram retirados do site do CNJ (Conselho Nacional de Justiça) no relatório dos números da Justiça de 2019, ano base 2018.')
            st.write('*Os dados relativos aos estados foram retirados do site do IBGE em abril de 2020, baseados em estimativas populacionais de 2019 e no senso de 2010.') 
        if tabelas_individuais == 'Dados IBGE':
            st.subheader('Dados dos estados fornecido pelo IBGE')
            st.dataframe(ibge)
            st.markdown('Informativo dos dados mostrados:')
            st.write('-> População estimada em 2019.')
            st.write('-> Densidade demográfica pelo senso IBGE 2010, hab/km².')
            st.write('-> IDH - Índice de Desenvolvimento Humano pelo senso IBGE 2010.')
            st.write('-> Receitas realizadas em Reais (X1000) em 2017.')
            st.write('-> Renda mensal domiciliar per capita em 2019, em Reais')
            st.write('*Dados retirados do site do IBGE em abril de 2020.')
        if tabelas_individuais == 'Custo da Justiça por habitante':
            st.subheader('Custo da Justiça por habitante em Reais')
            st.dataframe(custo)
            st.write('-> Valor gasto por habitante pela Justiça Estadual, em Reais.')
            st.write('*Dados retirados do site do CNJ em abril de 2020. Análise de 2019, ano-base 2018.')
        if tabelas_individuais == 'Tempo médio conhecimento e execução':
            st.subheader('Tempo médio do processo dividido entre fase de execução e de conhecimento em meses')
            st.dataframe(execucao)
            st.write('-> Tempo médio gasto nos processos da Justiça Estadual, divididos entre fase de conhecimento e fase de execução do processo, em meses.')
            st.write('*Dados retirados do site do CNJ em abril de 2020. Análise de 2019, ano-base 2018.')
        if tabelas_individuais == 'Tempo médio sentença':
            st.subheader('Tempo médio do processo até a data da sentença em 1° e 2° grau de jurisdição, em meses')
            st.dataframe(sentenca)
            st.write('-> Tempo médio gasto nos processos da Justiça Estadual até a data da sentença, divididos entre 1° e 2° graus de jurisdição, em meses.')
            st.write('*Dados retirados do site do CNJ em abril de 2020. Análise de 2019, ano-base 2018.')
        if tabelas_individuais == 'Percentual população em sede de comarca':
            st.subheader('Percentual da população residente em cidade com sede de comarca')
            st.dataframe(perc_pop)
            st.write('-> Percentual da população residente em cidade sede de comarca se refere à facilidade de acesso à justiça da população do estado.')
            st.write('*Dados retirados do site do CNJ em abril de 2020. Análise de 2019, ano-base 2018.')
        if tabelas_individuais == 'Outros dados':
            st.subheader('Outros dados da Justiça Estadual')
            st.dataframe(porte)
            st.write('-> Despesa total da justiça estadual, em Reais.')
            st.write('-> Quantidade de casos novos que entraram no ano de 2018.')
            st.write('-> Quantidade de casos ainda pendentes (não baixados) no ano de 2018.')
            st.write('-> Quantidade de magistrados (juízes) ativos.')
            st.write('-> Quantidade de servidores e auxiliares ativos.')
            st.write('*Dados retirados do site do CNJ em abril de 2020. Análise de 2019, ano-base 2018.')
        if tabelas_individuais == 'Tabela completa':
            st.subheader('Tabela completa de dados analisados')
            st.dataframe(df)
            st.markdown('Informativo dos dados mostrados:')
            st.write('-> População estimada em 2019.')
            st.write('-> Densidade demográfica pelo senso IBGE 2010, hab/km².')
            st.write('-> IDH - Índice de Desenvolvimento Humano pelo senso IBGE 2010.')
            st.write('-> Receitas realizadas em Reais (X1000) em 2017.')
            st.write('-> Renda mensal domiciliar per capita em 2019, em Reais')
            st.write('-> Valor gasto por habitante pela Justiça Estadual, em Reais.')
            st.write('-> Tempo médio gasto nos processos da Justiça Estadual, divididos entre fase de conhecimento e fase de execução do processo, em meses.')
            st.write('-> Tempo médio gasto nos processos da Justiça Estadual até a data da sentença, divididos entre 1° e 2° graus de jurisdição, em meses.')
            st.write('-> Percentual da população residente em cidade sede de comarca se refere à facilidade de acesso à justiça da população do estado.')
            st.write('-> Percentual da população residente em cidade sede de comarca se refere à facilidade de acesso à justiça da população do estado.')
            st.write('-> Percentual da população residente em cidade sede de comarca se refere à facilidade de acesso à justiça da população do estado.')
            st.write('-> Despesa total da justiça estadual, em Reais.')
            st.write('-> Quantidade de casos novos que entraram no ano de 2018.')
            st.write('-> Quantidade de casos ainda pendentes (não baixados) no ano de 2018.')
            st.write('-> Quantidade de magistrados (juízes) ativos.')
            st.write('-> Quantidade de servidores e auxiliares ativos.')
            st.write('*Dados retirados do site do CNJ em abril de 2020. Análise de 2019, ano-base 2018.')
            st.write('*Dados retirados do site do IBGE em abril de 2020.')
    
    
    #Criação de listas de acordo com o tipo da coluna
    aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})
    colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
    colunas_estados = list(df['Estados'])
    estado = 'Estados'
    
    #Análise da correlação dos dados
    st.sidebar.subheader('Correlação dos dados:')
    corrl = st.sidebar.checkbox('Análise de correlação linear dos dados')
    if corrl:
        st.subheader('Correlação dos dados:')
        st.write(cria_correlationplot(df, colunas_numericas))
        st.write('Em uma primeira análise, diante do gráfico de correlação linear acima, nota-se que não há uma forte correlação entre o tempo médio processual e os demais indicadores considerados.')
        st.write('Entretanto, nota-se uma correlação moderada entre o tempo levado em um processo na fase de conhecimento e valor gasto por habitante em cada justiça (Custo por habitante e Custo por habitante sem os inativos). Também encontramos uma correlação levemente moderada entre o tempo médio levado no processo em fase de conhecimento e o IDH e o Rendimento mensal domiciliar per capita.  Todas essas correlações moderadas apontadas são negativas, que significa que quanto maior o tempo gasto no processo, menor são os demais indicadores (Investimento na justiça, IDH e Rendimento mensal domiciliar per capita do estado).')
        st.write('Importante ressaltar que, a despeito de ter-se encontrado uma correlação moderada em dados relevantes, essas análises guardam limitações metodológicas. A principal delas está no uso da média como medida estatística para representar o tempo. A média é fortemente influenciada por valores extremos e, ao resumir em um único indicador os resultados de informações extremamente heterogêneas, pode apresentar distorções. Para uma análise de tempo mais adequada, seria importante recorrer aos quantis, boxplots e curvas de sobrevivência, considerando, por exemplo, o agrupamento de processos semelhantes, segundo classe e assunto, de forma a diminuir a heterogeneidade e a dispersão. Para essas análises, seria imprescindível recorrer aos dados de cada processo e não de forma agregada.')
    #Outras análises
    st.sidebar.subheader('Outras visualizações de dados')
    st.sidebar.markdown('Selecione a visualizacao')
    
    #Gráfico de barras
    barras = st.sidebar.checkbox('Gráfico de barras')
    if barras:
        st.subheader('Comparativo de dados por estados')
        colunas_barras = st.selectbox('Selecione a coluna: ', colunas_numericas, key = 'unique')
        st.markdown('Comparativo de estados com base na coluna ' + colunas_barras)
        st.write('*Ver significado dos dados selecionados em "Conheça os dados utilizados na análise"')
        st.write(criar_barras(estado, colunas_barras, df))
    
    scatter = st.sidebar.checkbox('Gráfico de dispersão')
    if scatter:
        st.subheader('Dispersão combinada à regressão linear e regressão polinomial')
        col_num_x = st.selectbox('Selecione o valor de x ', colunas_numericas, key = 'unique')
        col_num_y = st.selectbox('Selecione o valor de y ', colunas_numericas, key = 'unique')
        st.write('*Ver significado dos dados selecionados em "Conheça os dados utilizados na análise"')
        st.write(criar_scatterplot(col_num_x, col_num_y, df))
        
    #Dados por estado
    estado_index = df.set_index('Estados')
    conheca = st.sidebar.checkbox('Conheça seu estado')
    if conheca:
        st.subheader('Conheça seu estado')
        col_estado = st.selectbox('Selecione o Estado: ', colunas_estados, key = 'unique')
        linha_estado = estado_index.loc[col_estado]
        
        st.subheader('Dados da população e da Justiça Estadual: ' + col_estado)
        st.write('População estimada: ' + str(linha_estado['Populacao estimada']))
        st.write('Densidade demográfica em 2010: ' + str(linha_estado['Densidade demografica_2010']) + ' hab/km²')
        st.write('IDH (indice de desenvolvimento humano) em 2010: ' + str(linha_estado['IDH _2010']))
        st.write('Rendimento mensal domiciliar per capita em 2019: R$' + str(linha_estado['Rendimento mensal domiciliar per capita_2019']))
        st.write('Tempo médio de duração do processo em fase de primeiro grau: ' + str(int(linha_estado['Tempo_1_Grau'])) + ' meses')
        st.write('Tempo médio de duração do processo em fase de segundo grau: ' + str(int(linha_estado['Tempo_2_Grau'])) + ' meses')
        st.write('Tempo médio de duração do processo em fase de conhecimento(até a sentença): ' + str(int(linha_estado['Tempo_Conhecimento'])) + ' meses')
        st.write('Tempo médio de duração do processo em fase de execução: ' + str(int(linha_estado['Tempo_Execucao'])) + ' meses')
        st.write('Custo da Justiça Estadual do estado por habitante em 2018: R$' + str(linha_estado['Custo por habitante']))
        st.write('Custo da Justiça Estadual do estado por habitante em 2018(sem inativos): R$' + str(linha_estado['Custo por hab sem_inativos']))
        st.write('Custo total da Justiça Estadual do estado em 2018: R$' + str(linha_estado['Despesa Total']))
        st.write('Quantidade de novos casos na Justiça Estadual em 2018: ' + str(int(linha_estado['Casos novos'])))
        st.write('Quantidade de casos pendentes na Justiça Estadual em 2018: ' + str(int(linha_estado['Casos pendentes'])))
        st.write('Quantidade de magistrados atuantes na Justiça Estadual em 2018: ' + str(int(linha_estado['Magistrados'])))
        st.write('Quantidade de servidores e auxiliares atuantes na Justiça Estadual em 2018: ' + str(int(linha_estado['Servidores e Aux'])))
        st.write('Percentual da população residente em sede de comarca em 2018: ' + str(linha_estado['Percentual_populacao']) + '%')

    st.sidebar.subheader('Sobre a autora')
    st.sidebar.image('SobreAutor.png', width=90)
    st.sidebar.markdown('Janaína Teixeira Carvalho')
    st.sidebar.markdown('Advogada, Tecnóloga em Análise e Desenvolvimento de Sistemas, Estudante de Gestão de Projetos (MBA USP/Esalq) e de Ciência de Dados.')
    st.sidebar.markdown('Linkedin: https://www.linkedin.com/in/janainatcarvalho/')
    st.sidebar.markdown('Github: https://github.com/JanainaTCarvalho')

if __name__ == '__main__':
    main()
