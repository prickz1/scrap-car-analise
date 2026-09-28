import base64
import io

import matplotlib.pyplot as plt
import pandas as pd

DESCRICOES = {
    "Estatísticas Descritivas": (
        "Resumo estatístico das variáveis numéricas do dataset. "
        "Registros = total de valores não nulos; Média = valor médio; Desvio Padrão = o quanto os valores variam em torno da média; "
        "Mínimo/Máximo = menor e maior valor encontrado; Percentis 25%, 50% (Mediana) e 75% indicam a distribuição dos dados. "
        "<strong>Regras aplicadas:</strong> apenas registros com preço e marca preenchidos. "
        "Nenhum filtro aplicado em quilometragem — dados brutos conforme coletados."
    ),
    "Matriz de Correlação": (
        "Mostra a correlação entre todas as variáveis numéricas e categóricas do dataset. "
        "Cada célula contém um valor entre -1 e +1: valores próximos de +1 (vermelho) indicam que as duas variáveis sobem juntas; "
        "valores próximos de -1 (azul) indicam que quando uma sobe a outra desce; valores próximos de 0 (branco) indicam ausência de relação. "
        "A diagonal principal é sempre 1.00 pois representa cada variável correlacionada consigo mesma. "
        "<strong>Atenção:</strong> variáveis categóricas foram convertidas para números via LabelEncoder — "
        "a numeração é arbitrária, por isso a correlação delas deve ser interpretada com cautela."
    ),
}


def fig_to_base64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{encoded}"


def card_tabela(titulo: str, tabela: pd.DataFrame) -> str:
    return f"""
    <div class="card">
        <h2>{titulo}</h2>
        <p class="desc">{DESCRICOES.get(titulo, "")}</p>
        {tabela.to_html(classes="tabela", border=0)}
    </div>
    """


def card_grafico(titulo: str, fig: plt.Figure) -> str:
    return f"""
    <div class="card">
        <h2>{titulo}</h2>
        <p class="desc">{DESCRICOES.get(titulo, "")}</p>
        <img src="{fig_to_base64(fig)}" alt="{titulo}">
    </div>
    """


def gerar_html(cards: str, total_registros: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Análise — Scrap Carros</title>
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
