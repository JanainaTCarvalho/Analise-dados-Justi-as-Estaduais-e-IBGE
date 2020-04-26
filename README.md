# Comparativa de dados nas justiças estaduais com dados populacionais fornecidos pelo IBGE.

##Análise exploratória de dados - Trabalho proposto na AceleraDev em Data Science da Codenation

Um dos problemas mais comentados quando se trata de justiça no Brasil é o longo tempo de tramitação do processo. Nesse breve trabalho de exploração de dados procuro relacionar os dados das Justiças Estaduais, incluindo tempo médio dos processos, com dados populacionais do mesmo estado, procurando entender se o tempo médio do processo pode estar relacionado com o desenvolvimento do estado, quantidade de habitantes, densidade populacional, investimento financeiro na justiça e outros dados.

### Dados utilizados:

- Os dados relativos às Justiças Estaduais foram retirados do site do CNJ (Conselho Nacional de Justiça) no relatório dos números da Justiça de 2019, ano base 2018.
- Os dados relativos aos estados foram retirados do site do IBGE em abril de 2020, baseados em estimativas populacionais de 2019 e no senso de 2010.'

### Conclusões

	Em uma primeira análise, diante do gráfico de correlação linear acima, nota-se que não há uma forte correlação entre o tempo médio processual e os demais indicadores considerados.
	Entretanto, nota-se uma correlação moderada entre o tempo levado em um processo na fase de conhecimento e valor gasto por habitante em cada justiça (Custo por habitante e Custo por habitante sem os inativos). Também encontramos uma correlação levemente moderada entre o tempo médio levado no processo em fase de conhecimento e o IDH e o Rendimento mensal domiciliar per capita.  Todas essas correlações moderadas apontadas são negativas, que significa que quanto maior o tempo gasto no processo, menor são os demais indicadores (Investimento na justiça, IDH e Rendimento mensal domiciliar per capita do estado).
	Importante ressaltar que, a despeito de ter-se encontrado uma correlação moderada em dados relevantes, essas análises guardam limitações metodológicas. A principal delas está no uso da média como medida estatística para representar o tempo. A média é fortemente influenciada por valores extremos e, ao resumir em um único indicador os resultados de informações extremamente heterogêneas, pode apresentar distorções. Para uma análise de tempo mais adequada, seria importante recorrer aos quantis, boxplots e curvas de sobrevivência, considerando, por exemplo, o agrupamento de processos semelhantes, segundo classe e assunto, de forma a diminuir a heterogeneidade e a dispersão. Para essas análises, seria imprescindível recorrer aos dados de cada processo e não de forma agregada.

###Visualizações
	
- Análise de correlação em um heatmap
- Gráfico de barras
- Gráfico de dispersão combinada à regressão linear e regressão polinomial(graus em 5 e 8)
- Dados apresentados por estados brasileiros
