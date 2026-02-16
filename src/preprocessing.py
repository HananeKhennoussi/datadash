import pandas as pd
import numpy as np

def detect_column_types(df):
    """
    Sépare les colonnes numériques et catégorielles.
    """
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return numeric_cols, categorical_cols

def handle_missing_values(df, strategy="none"):
    """
    Gestion des valeurs manquantes.
    """
    if strategy == "drop":
        return df.dropna()
    elif strategy == "mean":
        return df.fillna(df.mean(numeric_only=True))
    elif strategy == "median":
        return df.fillna(df.median(numeric_only=True))
    elif strategy == "mode":
        return df.fillna(df.mode().iloc[0])
    return df

def detect_outliers(df, numeric_cols):
    """
    Détecte les outliers selon l'intervalle interquartile.
    Retourne un dictionnaire avec les colonnes et indices des outliers.
    """
    outliers = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        mask = (df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))
        outliers[col] = df.index[mask].tolist()
    return outliers

