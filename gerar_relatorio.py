import webbrowser
from pathlib import Path

from database import carregar_dados
from descritiva import tabela_descritiva
from graficos import (heatmap_correlacao, heatmap_correlacao_filtrado, heatmap_correlacao_misto,
                      boxplot_preco_bruto, boxplot_km_bruto, boxplot_km_sem_outliers)
from graficos_categoricos import (boxplot_preco_todas_marcas,
                                   boxplot_preco_combustivel, boxplot_preco_cambio,
                                   boxplot_preco_tipo_veiculo, boxplot_preco_direcao,
                                   boxplot_preco_modelos_marca)
from builder import card_tabela, card_grafico, card_grafico_scroll, card_heatmap, gerar_html

MARCAS = ["VOLKSWAGEN", "FIAT", "CHEVROLET", "HYUNDAI", "FORD", "TOYOTA", "RENAULT", "BYD"]

# IDs excluídos manualmente da segunda matriz de correlação (Amarok outliers confirmados)
IDS_IGNORAR_MATRIZ2 = [79641, 159336, 794481, 79645, 76207, 76183, 79626, 79521,
                        79214, 79623, 79627, 79497, 79646, 79628, 79630, 71351,
                        64802, 79624, 79629, 79351, 79631, 79659]

_DESC_MODELOS = (
    "Distribuição de preços para cada modelo {marca}, separado por modelo. "
    "Cada caixa representa um modelo: a linha central é a mediana, a caixa cobre Q1–Q3 e os pontos isolados são outliers. "
    "O rótulo inclui o ano mediano e a quantidade de anúncios."
)


def _cards_marca(df, marca: str) -> str:
    m = marca.upper()
    return card_grafico_scroll(
        f"Distribuição de Preços por Modelo — {m}",
        boxplot_preco_modelos_marca(df, marca),
        desc=_DESC_MODELOS.format(marca=m),
    )


print("Carregando dados...")
df = carregar_dados()
print(f"Total de registros: {len(df)}")

cards = (
    card_tabela("Estatísticas Descritivas", tabela_descritiva(df))
    # Boxplot de preço geral
    + card_grafico("Boxplot — Dados Brutos", boxplot_preco_bruto(df))
    # Marca — todas juntas
    + card_grafico_scroll("Distribuição de Preços — Todas as Marcas", boxplot_preco_todas_marcas(df))
    + "".join(_cards_marca(df, m) for m in MARCAS)
    # Preço por outras categorias
    + card_grafico("Distribuição de Preços por Combustível", boxplot_preco_combustivel(df))
    + card_grafico("Distribuição de Preços por Câmbio", boxplot_preco_cambio(df))
    + card_grafico("Distribuição de Preços por Tipo de Veículo", boxplot_preco_tipo_veiculo(df))
    + card_grafico("Distribuição de Preços por Direção", boxplot_preco_direcao(df))
    # Quilometragem
    + card_grafico("Boxplot — Quilometragem Bruta", boxplot_km_bruto(df))
    + card_grafico("Boxplot — Quilometragem Sem Outliers", boxplot_km_sem_outliers(df))
    # Matrizes de correlação
    + card_heatmap("Matriz de Correlação — Dados Brutos", heatmap_correlacao(df), div_id="heatmap-bruto")
    + card_heatmap("Matriz de Correlação — Quilometragem sem outliers", heatmap_correlacao_filtrado(df, IDS_IGNORAR_MATRIZ2), div_id="heatmap-filtrado")
    + card_heatmap("Matriz de Correlação — Método Misto", heatmap_correlacao_misto(df, IDS_IGNORAR_MATRIZ2), div_id="heatmap-misto")
)

output = Path(__file__).parent / "relatorio.html"
output.write_text(gerar_html(cards, len(df)), encoding="utf-8")
print(f"Relatório gerado: {output}")
webbrowser.open(output.as_uri())
