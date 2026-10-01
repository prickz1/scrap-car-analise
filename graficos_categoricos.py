import pandas as pd
import plotly.graph_objects as go


def _boxplot_por_categoria(
    df: pd.DataFrame,
    valor_col: str,
    categoria_col: str,
    titulo: str,
    top_n: int | None = 15,
    ordem_por: str = "mediana",   # "mediana" | "frequencia"
    mostrar_contagem: bool = False,
    excluir_valores: list[str] | None = None,
    largura_auto: bool = False,
    y_prefix: str = "",
    y_suffix: str = "",
    y_format: str = ",.0f",
    custom_cols: list[str] | None = None,
    hover_extra: str = "",
    cor_fill: str = "#90CAF9",
    cor_linha: str = "#1565C0",
) -> go.Figure:
    if excluir_valores:
        df = df[~df[categoria_col].isin(excluir_valores)]
    contagem = df[categoria_col].value_counts()
    top = contagem.head(top_n).index if top_n is not None else contagem.index
    dados = df[df[categoria_col].isin(top)].dropna(subset=[valor_col])

    if ordem_por == "frequencia":
        ordem = [c for c in contagem.index if c in top]
    else:
        ordem = dados.groupby(categoria_col)[valor_col].median().sort_values(ascending=False).index.tolist()

    custom_cols = custom_cols or []
    fig = go.Figure()
    for cat in ordem:
        subset = dados[dados[categoria_col] == cat]
        name = f"{cat} ({contagem[cat]})" if mostrar_contagem else str(cat)
        custom = list(zip(*[subset[c].fillna("—").astype(str) for c in custom_cols])) if custom_cols else None
        extra = hover_extra.replace("{cat}", str(cat))
        fig.add_trace(go.Box(
            y=subset[valor_col], name=name,
            customdata=custom,
            hovertemplate=f"<b>{cat}</b><br>{y_prefix}%{{y:{y_format}}}{y_suffix}{extra}<extra></extra>",
            hoverlabel=dict(align="left"),
            marker_color=cor_linha, fillcolor=cor_fill,
            line_color=cor_linha, marker_outliercolor="#EF9A9A",
            marker_size=3,
        ))

    largura = max(900, len(ordem) * 60) if largura_auto else None
    layout = dict(
        title=titulo,
        yaxis_title=f"{valor_col.capitalize()} ({y_prefix.strip()}{y_suffix.strip()})",
        xaxis_title=categoria_col.replace("_", " ").capitalize(),
        height=500, showlegend=False, hoverlabel=dict(align="left"),
    )
    if largura:
        layout["width"] = largura
    fig.update_layout(**layout)
    fig.update_yaxes(tickprefix=y_prefix, ticksuffix=y_suffix, tickformat=y_format)
    return fig


# ── Preço por marca ───────────────────────────────────────────────────────────

def boxplot_preco_todas_marcas(df: pd.DataFrame) -> go.Figure:
    return _boxplot_por_categoria(
        df, "preco", "marca",
        titulo="Distribuição de Preços — Todas as Marcas",
        top_n=None, ordem_por="frequencia",
        mostrar_contagem=True, excluir_valores=["ERRO"],
        largura_auto=True, y_prefix="R$ ",
        custom_cols=["modelo", "ano"],
        hover_extra="<br>%{customdata[0]} %{customdata[1]}",
    )


# ── Preço por categoria ────────────────────────────────────────────────────────

def boxplot_preco_combustivel(df: pd.DataFrame) -> go.Figure:
    return _boxplot_por_categoria(
        df, "preco", "combustivel",
        titulo="Distribuição de Preços por Combustível",
        top_n=10, y_prefix="R$ ",
        custom_cols=["modelo", "ano"],
        hover_extra="<br>%{customdata[0]} %{customdata[1]}",
    )


def boxplot_preco_cambio(df: pd.DataFrame) -> go.Figure:
    return _boxplot_por_categoria(
        df, "preco", "cambio",
        titulo="Distribuição de Preços por Câmbio",
        top_n=10, y_prefix="R$ ",
        custom_cols=["modelo", "ano"],
        hover_extra="<br>%{customdata[0]} %{customdata[1]}",
    )


def boxplot_preco_tipo_veiculo(df: pd.DataFrame) -> go.Figure:
    return _boxplot_por_categoria(
        df, "preco", "tipo_veiculo",
        titulo="Distribuição de Preços por Tipo de Veículo",
        top_n=10, y_prefix="R$ ",
        custom_cols=["modelo", "ano"],
        hover_extra="<br>%{customdata[0]} %{customdata[1]}",
    )


def boxplot_preco_direcao(df: pd.DataFrame) -> go.Figure:
    return _boxplot_por_categoria(
        df, "preco", "direcao",
        titulo="Distribuição de Preços por Direção",
        top_n=10, y_prefix="R$ ",
        custom_cols=["modelo", "ano"],
        hover_extra="<br>%{customdata[0]} %{customdata[1]}",
        cor_fill="#CE93D8", cor_linha="#6A1B9A",
    )


# ── Preço por modelo (por marca) ──────────────────────────────────────────────


def boxplot_preco_modelos_marca(df: pd.DataFrame, marca: str) -> go.Figure:
    dados = df[df["marca"].str.upper() == marca.upper()].dropna(subset=["preco", "modelo"]).copy()
    ordem = dados.groupby("modelo")["preco"].median().sort_values(ascending=False).index.tolist()

    fig = go.Figure()
    contagem = dados["modelo"].value_counts()
    for modelo in ordem:
        subset = dados[dados["modelo"] == modelo]
        try:
            ano_med = int(subset["ano"].dropna().median())
        except Exception:
            ano_med = "—"
        anos = subset["ano"].fillna(0).astype(int).astype(str).replace("0", "—").tolist()
        ids = subset["id"].astype(str).tolist()
        fig.add_trace(go.Box(
            y=subset["preco"],
            name=f"{modelo} · {ano_med} ({contagem[modelo]})",
            customdata=[[a, i] for a, i in zip(anos, ids)],
            hovertemplate=f"<b>{modelo}</b><br>R$ %{{y:,.0f}}<br>%{{customdata[0]}} | id: %{{customdata[1]}}<extra></extra>",
            hoverlabel=dict(align="left"),
            marker_color="#1565C0", fillcolor="#90CAF9",
            line_color="#1565C0", marker_outliercolor="#EF9A9A",
            marker_size=3,
        ))

    largura = max(900, len(ordem) * 80)
    fig.update_layout(
        title=f"Distribuição de Preços por Modelo — {marca.upper()} ({len(dados):,} anúncios)",
        yaxis_title="Preço (R$)", xaxis_title="Modelo",
        height=500, width=largura, showlegend=False,
    )
    fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
    return fig


