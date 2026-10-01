import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.preprocessing import LabelEncoder


def _iqr_limite(dados: pd.Series):
    q3 = dados.quantile(0.75)
    iqr = q3 - dados.quantile(0.25)
    return q3 + 1.5 * iqr


def _box_horizontal(
    df: pd.DataFrame, coluna: str,
    cor_fill: str, cor_linha: str,
    hover_prefix: str = "", hover_suffix: str = "",
) -> go.Box:
    subset = df.dropna(subset=[coluna])
    modelo_ano = list(zip(
        subset["modelo"].fillna("—"),
        subset["ano"].fillna(0).astype(int).astype(str).replace("0", "—"),
    ))
    return go.Box(
        x=subset[coluna], name="", orientation="h",
        customdata=modelo_ano,
        hovertemplate=f"{hover_prefix}%{{x:,.0f}}{hover_suffix}<br>%{{customdata[0]}} %{{customdata[1]}}<extra></extra>",
        hoverlabel=dict(align="left"),
        marker_color=cor_linha, fillcolor=cor_fill,
        line_color=cor_linha, marker_outliercolor="#EF9A9A",
        marker_size=3,
    )


def boxplot_preco_bruto(df: pd.DataFrame) -> go.Figure:
    dados = df["preco"].dropna()
    limite = _iqr_limite(dados)
    outliers = dados[dados > limite]
    fig = go.Figure(_box_horizontal(df, "preco", "#90CAF9", "#1565C0", hover_prefix="R$ "))
    fig.update_layout(
        title=f"Distribuição de Preços — Dados Brutos<br>"
              f"<sup>Mediana: R$ {dados.median():,.0f} | Outliers acima de R$ {limite:,.0f}: {len(outliers):,} registros</sup>",
        height=350, showlegend=False, hoverlabel=dict(align="left"),
    )
    fig.update_xaxes(tickprefix="R$ ", tickformat=",.0f")
    return fig


def boxplot_km_bruto(df: pd.DataFrame) -> go.Figure:
    dados = df["quilometragem"].dropna()
    limite = _iqr_limite(dados)
    outliers = dados[dados > limite]
    fig = go.Figure(_box_horizontal(df, "quilometragem", "#A5D6A7", "#2E7D32", hover_suffix=" km"))
    fig.update_layout(
        title=f"Distribuição de Quilometragem — Dados Brutos<br>"
              f"<sup>Mediana: {dados.median():,.0f} km | Outliers acima de {limite:,.0f} km: {len(outliers):,} registros</sup>",
        height=350, showlegend=False, hoverlabel=dict(align="left"),
    )
    fig.update_xaxes(ticksuffix=" km", tickformat=",.0f")
    return fig


def boxplot_km_sem_outliers(df: pd.DataFrame) -> go.Figure:
    dados = df["quilometragem"].dropna()
    limite = _iqr_limite(dados)
    subset_limpo = df[df["quilometragem"] <= limite]
    dados_limpos = subset_limpo["quilometragem"]
    q1 = dados_limpos.quantile(0.25)
    med = dados_limpos.median()
    q3 = dados_limpos.quantile(0.75)
    fig = go.Figure(_box_horizontal(subset_limpo, "quilometragem", "#A5D6A7", "#2E7D32", hover_suffix=" km"))
    fig.update_layout(
        title=f"Distribuição de Quilometragem — Sem Outliers Extremos<br>"
              f"<sup>{len(dados_limpos):,} registros | Q1: {q1:,.0f} km | Mediana: {med:,.0f} km | Q3: {q3:,.0f} km</sup>",
        height=350, showlegend=False, hoverlabel=dict(align="left"),
    )
    fig.update_xaxes(ticksuffix=" km", tickformat=",.0f")
    return fig




def _heatmap_fig(corr, title: str) -> go.Figure:
    labels = ["Preço", "Ano", "Quilometragem", "Marca", "Combustível",
              "Câmbio", "Cor", "Tipo Veículo", "Direção"]
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=labels, y=labels,
        colorscale="RdBu_r", zmid=0, zmin=-1, zmax=1,
        text=corr.round(2).values, texttemplate="%{text:.2f}",
        colorbar=dict(title="Correlação"),
        hoverinfo="none",
    ))
    fig.update_layout(
        title=title, height=600, hovermode="closest",
        xaxis=dict(ticklen=12, side="top"),
        yaxis=dict(ticklen=12),
    )
    return fig


def heatmap_correlacao(df: pd.DataFrame) -> go.Figure:
    df_enc = df.copy()
    le = LabelEncoder()
    for col in ["marca", "combustivel", "cambio", "cor", "tipo_veiculo", "direcao"]:
        df_enc[col] = df_enc[col].fillna("Desconhecido")
        df_enc[col] = le.fit_transform(df_enc[col])

    corr = df_enc[["preco", "ano", "quilometragem", "marca", "combustivel",
                   "cambio", "cor", "tipo_veiculo", "direcao"]].corr()

    labels = ["Preço", "Ano", "Quilometragem", "Marca", "Combustível",
              "Câmbio", "Cor", "Tipo Veículo", "Direção"]

    return _heatmap_fig(corr, "Matriz de Correlação — Dados Brutos")


_COLUNAS = ["preco", "ano", "quilometragem", "marca", "combustivel",
            "cambio", "cor", "tipo_veiculo", "direcao"]


def _encodar(df: pd.DataFrame) -> pd.DataFrame:
    le = LabelEncoder()
    df_enc = df.copy()
    for col in ["marca", "combustivel", "cambio", "cor", "tipo_veiculo", "direcao"]:
        df_enc[col] = df_enc[col].fillna("Desconhecido")
        df_enc[col] = le.fit_transform(df_enc[col])
    return df_enc


def _eta(num: pd.Series, cat: pd.Series) -> float:
    """Força de associação entre variável numérica e categórica (0 a 1)."""
    df_tmp = pd.DataFrame({"num": num, "cat": cat}).dropna()
    if df_tmp.empty or df_tmp["cat"].nunique() < 2:
        return 0.0
    grand_mean = df_tmp["num"].mean()
    ss_total = ((df_tmp["num"] - grand_mean) ** 2).sum()
    if ss_total == 0:
        return 0.0
    ss_between = sum(
        len(g) * (g.mean() - grand_mean) ** 2
        for _, g in df_tmp.groupby("cat")["num"]
    )
    return float(np.sqrt(ss_between / ss_total))


def _cramers_v(x: pd.Series, y: pd.Series) -> float:
    """Associação entre duas variáveis categóricas (0 a 1)."""
    df_tmp = pd.DataFrame({"x": x, "y": y}).dropna()
    if df_tmp.empty:
        return 0.0
    ct = pd.crosstab(df_tmp["x"], df_tmp["y"])
    chi2 = stats.chi2_contingency(ct, correction=False)[0]
    n = ct.values.sum()
    min_dim = min(ct.shape) - 1
    if min_dim == 0 or n == 0:
        return 0.0
    return float(np.sqrt(chi2 / (n * min_dim)))


def heatmap_correlacao_filtrado(df: pd.DataFrame, ids_ignorar: list[int] | None = None) -> go.Figure:
    df_f = df.copy()
    if ids_ignorar:
        df_f = df_f[~df_f["id"].isin(ids_ignorar)]
    s = df_f["quilometragem"].dropna()
    limite = s.quantile(0.75) + 1.5 * (s.quantile(0.75) - s.quantile(0.25))
    df_f = df_f[df_f["quilometragem"].isna() | (df_f["quilometragem"] <= limite)]
    corr = _encodar(df_f)[_COLUNAS].corr()
    return _heatmap_fig(corr, f"Matriz de Correlação — Quilometragem sem outliers ({len(df_f):,} registros)")


_NUMERICAS = ["preco", "ano", "quilometragem"]
_CATEGORICAS = ["marca", "combustivel", "cambio", "cor", "tipo_veiculo", "direcao"]
_LABELS_PT = ["Preço", "Ano", "Quilometragem", "Marca", "Combustível",
              "Câmbio", "Cor", "Tipo Veículo", "Direção"]


def heatmap_correlacao_misto(df: pd.DataFrame) -> go.Figure:
    df_f = df.copy()

    # Filtro IQR — quilometragem
    s_km = df_f["quilometragem"].dropna()
    lim_km = s_km.quantile(0.75) + 1.5 * (s_km.quantile(0.75) - s_km.quantile(0.25))
    df_f = df_f[df_f["quilometragem"].isna() | (df_f["quilometragem"] <= lim_km)]

    # Filtro IQR — preço (para corrigir eta de preço × direção)
    s_pr = df_f["preco"].dropna()
    lim_pr = s_pr.quantile(0.75) + 1.5 * (s_pr.quantile(0.75) - s_pr.quantile(0.25))
    df_f = df_f[df_f["preco"] <= lim_pr]

    colunas = _NUMERICAS + _CATEGORICAS
    n = len(colunas)
    matrix = np.full((n, n), np.nan)

    for i, ci in enumerate(colunas):
        for j, cj in enumerate(colunas):
            if i == j:
                matrix[i][j] = 1.0
            elif ci in _NUMERICAS and cj in _NUMERICAS:
                tmp = df_f[[ci, cj]].dropna()
                matrix[i][j] = tmp[ci].corr(tmp[cj]) if len(tmp) > 1 else 0.0
            elif ci in _NUMERICAS and cj in _CATEGORICAS:
                v = _eta(df_f[ci], df_f[cj])
                matrix[i][j] = v
                matrix[j][i] = v
            elif ci in _CATEGORICAS and cj in _NUMERICAS:
                pass  # já preenchido acima
            else:
                v = _cramers_v(df_f[ci], df_f[cj])
                matrix[i][j] = v
                matrix[j][i] = v

    corr = pd.DataFrame(matrix, index=_LABELS_PT, columns=_LABELS_PT)

    fig = go.Figure(go.Heatmap(
        z=corr.values, x=_LABELS_PT, y=_LABELS_PT,
        colorscale="RdBu_r", zmid=0, zmin=-1, zmax=1,
        text=corr.round(2).values, texttemplate="%{text:.2f}",
        colorbar=dict(title="Coeficiente"),
        hoverinfo="none",
    ))
    fig.update_layout(
        title=f"Matriz de Correlação — Método Misto ({len(df_f):,} registros)",
        height=600, hovermode="closest",
        xaxis=dict(ticklen=12, side="top"),
        yaxis=dict(ticklen=12),
    )
    return fig
