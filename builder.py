import pandas as pd

DESCRICOES = {
    "Estatísticas Descritivas": (
        "Resumo estatístico das variáveis numéricas do dataset. "
        "Registros = total de valores não nulos; Média = valor médio; Desvio Padrão = o quanto os valores variam em torno da média; "
        "Mínimo/Máximo = menor e maior valor encontrado; Percentis 25%, 50% (Mediana) e 75% indicam a distribuição dos dados. "
        "<strong>Regras aplicadas:</strong> apenas registros com preço e marca preenchidos. "
        "Nenhum filtro aplicado em quilometragem — dados brutos conforme coletados."
    ),
    "Boxplot — Dados Brutos": (
        "Distribuição completa de preços sem nenhum filtro. "
        "A caixa fica comprimida à esquerda porque poucos anúncios com preços absurdos (até R$ 7 milhões) esticam o eixo, "
        "tornando a distribuição da maioria dos carros invisível. "
        "Os pontos isolados à direita são <strong>outliers estatísticos</strong> (acima de Q3 + 1,5×IQR) — candidatos a remoção."
    ),
    "Boxplot — Quilometragem Bruta": (
        "Distribuição completa da quilometragem sem nenhum filtro. "
        "Evidencia a presença de valores absurdos (como 999.999.999 km) que distorcem o eixo e comprimem a caixa à esquerda. "
        "Os pontos isolados são outliers estatísticos — candidatos a remoção ou investigação."
    ),
    "Boxplot — Quilometragem Sem Outliers": (
        "Mesma distribuição após remover registros acima do limite IQR (Q3 + 1,5×IQR). "
        "Permite visualizar os três quartis reais: Q1, Mediana e Q3. "
        "Compare com o gráfico anterior para quantificar o impacto dos dados incorretos."
    ),
    "Distribuição de Preços por Combustível": (
        "Compara a distribuição de preços entre os tipos de combustível mais frequentes. "
        "Permite verificar se carros flex, gasolina, diesel ou elétrico têm faixas de preço distintas."
    ),
    "Distribuição de Preços por Câmbio": (
        "Compara preços entre câmbio manual e automático. "
        "Espera-se que automáticos tenham mediana mais alta, pois agregam valor ao veículo."
    ),
    "Distribuição de Preços por Tipo de Veículo": (
        "Mostra como o preço varia entre categorias como SUV, Hatch, Sedan e Picape. "
        "Caixas mais altas indicam maior variação de preço dentro da categoria."
    ),
    "Distribuição de Preços por Direção": (
        "Compara preços entre tipos de direção (hidráulica, elétrica, mecânica). "
        "Direção elétrica tende a aparecer em carros mais novos e caros."
    ),
    "Distribuição de Preços — Todas as Marcas": (
        "Mesmo gráfico do Top 15, mas com todas as marcas presentes no dataset. "
        "Role horizontalmente para ver todas. Ordenadas pela mediana de preço."
    ),
    "Matriz de Correlação — Dados Brutos": (
        "Correlação calculada sobre todos os registros sem nenhum filtro. "
        "Cada célula contém um valor entre -1 e +1: vermelho = variáveis sobem juntas, azul = relação inversa, branco = sem relação. "
        "A diagonal é sempre 1.00. Correlações fracas aqui indicam que os outliers estão distorcendo os resultados. "
        "<strong>Atenção:</strong> variáveis categóricas foram convertidas para números via LabelEncoder — numeração arbitrária, interprete com cautela."
    ),
    "Matriz de Correlação — Quilometragem sem outliers": (
        "Correlação calculada após remover apenas os outliers de quilometragem (acima de Q3 + 1,5×IQR). "
        "Nenhum outro campo foi alterado — preço, marca e demais variáveis permanecem com dados brutos. "
        "Compare com a matriz bruta para ver o impacto isolado dos outliers de km nas correlações."
    ),
}


def card_tabela(titulo: str, tabela: pd.DataFrame) -> str:
    return f"""
    <div class="card">
        <h2>{titulo}</h2>
        <p class="desc">{DESCRICOES.get(titulo, "")}</p>
        {tabela.to_html(classes="tabela", border=0)}
    </div>
    """


def card_grafico(titulo: str, fig, desc: str = "") -> str:
    div = fig.to_html(include_plotlyjs=False, full_html=False, config={"responsive": True, "displayModeBar": False})
    descricao = desc or DESCRICOES.get(titulo, "")
    return f"""
    <div class="card">
        <h2>{titulo}</h2>
        <p class="desc">{descricao}</p>
        {div}
    </div>
    """


def card_grafico_scroll(titulo: str, fig, desc: str = "") -> str:
    div = fig.to_html(include_plotlyjs=False, full_html=False, config={"displayModeBar": False})
    descricao = desc or DESCRICOES.get(titulo, "")
    return f"""
    <div class="card">
        <h2>{titulo}</h2>
        <p class="desc">{descricao}</p>
        <div style="overflow-x: auto;">{div}</div>
    </div>
    """


def card_heatmap(titulo: str, fig, div_id: str = "heatmap-corr") -> str:
    div = fig.to_html(
        include_plotlyjs=False, full_html=False,
        div_id=div_id,
        config={"responsive": True, "displayModeBar": False},
    )
    labels = '["Preço","Ano","Quilometragem","Marca","Combustível","Câmbio","Cor","Tipo Veículo","Direção"]'
    script = f"""
    <script>
    (function() {{
        var el = document.getElementById('{div_id}');
        var labels = {labels};
        var n = labels.length;
        el.on('plotly_hover', function(data) {{
            var pt = data.points[0];
            var xi = labels.indexOf(pt.x);
            var yi = labels.indexOf(pt.y);
            Plotly.relayout(el, {{shapes: [
                // braço esquerdo — linha até o label da linha
                {{type:'rect', xref:'x', yref:'y', layer:'above',
                 x0:-0.5, x1:xi-0.5, y0:yi-0.5, y1:yi+0.5,
                 fillcolor:'rgba(0,0,0,0.22)', line:{{width:0}}}},
                // braço inferior — coluna abaixo da célula
                {{type:'rect', xref:'x', yref:'y', layer:'above',
                 x0:xi-0.5, x1:xi+0.5, y0:yi+0.5, y1:n-0.5,
                 fillcolor:'rgba(0,0,0,0.22)', line:{{width:0}}}},
                // célula atual — mais destaque
                {{type:'rect', xref:'x', yref:'y', layer:'above',
                 x0:xi-0.5, x1:xi+0.5, y0:yi-0.5, y1:yi+0.5,
                 fillcolor:'rgba(255,255,255,0.18)',
                 line:{{width:2, color:'rgba(0,0,0,0.55)'}}}}
            ]}});
        }});
        el.on('plotly_unhover', function() {{
            Plotly.relayout(el, {{shapes: []}});
        }});
    }})();
    </script>
    """
    return f"""
    <div class="card">
        <h2>{titulo}</h2>
        <p class="desc">{DESCRICOES.get(titulo, "")}</p>
        {div}
        {script}
    </div>
    """


def gerar_html(cards: str, total_registros: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Análise — Scrap Carros</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  body {{ font-family: sans-serif; background: #f0f0f0; margin: 0; padding: 24px; color: #222; }}
  h1 {{ text-align: center; margin-bottom: 6px; }}
  p.sub {{ text-align: center; color: #666; margin-bottom: 32px; }}
  .card {{ background: white; border-radius: 10px; padding: 24px; margin-bottom: 28px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
  .card h2 {{ margin-top: 0; font-size: 1.1rem; color: #444; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 10px; }}
  .desc {{ font-size: 0.9rem; color: #555; line-height: 1.6; margin-bottom: 16px; background: #f9f9f9; padding: 10px 14px; border-left: 3px solid #ccc; border-radius: 4px; }}
  img {{ width: 100%; height: auto; }}
  .tabela {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  .tabela th, .tabela td {{ padding: 8px 14px; text-align: right; border-bottom: 1px solid #eee; }}
  .tabela th {{ background: #f4f4f4; font-weight: 600; }}
  .tabela tr:hover {{ background: #fafafa; }}
</style>
</head>
<body>
<h1>Análise de Preços — Scrap Carros</h1>
<p class="sub">Total de registros: <strong>{total_registros}</strong> | Fonte: OLX Brasil (web scraping)</p>
{cards}
</body>
</html>"""
