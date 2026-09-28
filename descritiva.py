import pandas as pd


def tabela_descritiva(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[["preco", "ano", "quilometragem"]]
        .describe()
        .round(2)
        .rename(index={
            "count": "Registros",
            "mean":  "Média",
            "std":   "Desvio Padrão",
            "min":   "Mínimo",
            "25%":   "Percentil 25%",
            "50%":   "Mediana",
            "75%":   "Percentil 75%",
            "max":   "Máximo",
        })
        .rename(columns={
            "preco":         "Preço (R$)",
            "ano":           "Ano",
            "quilometragem": "Quilometragem (km)",
        })
    )
