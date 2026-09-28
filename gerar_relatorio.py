import webbrowser
from pathlib import Path

from database import carregar_dados
from descritiva import tabela_descritiva
from graficos import heatmap_correlacao
from builder import card_tabela, card_grafico, gerar_html

print("Carregando dados...")
df = carregar_dados()
print(f"Total de registros: {len(df)}")

cards = (
    card_tabela("Estatísticas Descritivas", tabela_descritiva(df))
    + card_grafico("Matriz de Correlação", heatmap_correlacao(df))
)

output = Path(__file__).parent / "relatorio.html"
output.write_text(gerar_html(cards, len(df)), encoding="utf-8")
print(f"Relatório gerado: {output}")
webbrowser.open(output.as_uri())
