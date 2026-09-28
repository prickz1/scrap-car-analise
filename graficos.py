import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


def heatmap_correlacao(df: pd.DataFrame) -> plt.Figure:
    df_enc = df.copy()
    le = LabelEncoder()
    for col in ["marca", "combustivel", "cambio", "cor", "tipo_veiculo", "direcao"]:
        df_enc[col] = df_enc[col].fillna("Desconhecido")
        df_enc[col] = le.fit_transform(df_enc[col])

    corr = df_enc[["preco", "ano", "quilometragem", "marca", "combustivel",
                   "cambio", "cor", "tipo_veiculo", "direcao"]].corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, linewidths=0.5, ax=ax)
    ax.set_title("Matriz de Correlação entre Atributos", fontsize=14, pad=12)
    plt.tight_layout()
    return fig
