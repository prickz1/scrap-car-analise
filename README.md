# scrap-car-analise

Análise Exploratória de Dados (AED) sobre anúncios de veículos coletados do portal OLX Brasil pelo projeto `scrap-car-back`. Gera um relatório HTML interativo com estatísticas descritivas, boxplots e matrizes de correlação.

## Stack

- Python 3.14
- Pandas
- Plotly
- Scikit-learn (LabelEncoder)
- SQLAlchemy

## Pré-requisitos

- Python 3.14 instalado
- Banco PostgreSQL do `scrap-car-back` rodando em `localhost:7777`
- Dependências instaladas:

```bash
pip install -r requirements.txt
```

## Executando

```bash
py -3.14 gerar_relatorio.py
```

Gera o arquivo `relatorio.html` e abre automaticamente no navegador.

## Estrutura

```
scrap-car-analise/
├── gerar_relatorio.py      ← ponto de entrada: monta e abre o relatório
├── database.py             ← conecta ao PostgreSQL e carrega os dados
├── descritiva.py           ← estatísticas descritivas (df.describe)
├── graficos.py             ← boxplots de preço/km e matrizes de correlação
├── graficos_categoricos.py ← boxplots por marca, modelo e demais categorias
└── builder.py              ← monta os cards HTML e o template da página
```

## Análises geradas

- **Estatísticas descritivas** — média, mediana, desvio padrão, percentis
- **Boxplot de preços brutos** — distribuição completa sem filtros
- **Boxplot por marca** — todas as marcas, ordenadas pela mediana
- **Boxplot por modelo** — distribuição por modelo para 8 marcas selecionadas
- **Boxplot por combustível, câmbio, tipo de veículo e direção**
- **Boxplot de quilometragem** — bruta e sem outliers (IQR)
- **Matrizes de correlação** — dados brutos, quilometragem sem outliers e método misto (Pearson + Eta + Cramér's V)
