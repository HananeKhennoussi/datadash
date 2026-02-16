import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.preprocessing import detect_column_types, handle_missing_values, detect_outliers
from src.visualization import plot_scatter, plot_histogram, plot_correlation, plot_box

st.set_page_config(page_title="DataDash", layout="wide")
st.title("📊 DataDash - Dashboard Dynamique Avancé")
st.write("💡 Chargez un CSV et explorez vos données avec EDA automatique !")

uploaded_file = st.file_uploader("📂 Choisir un fichier CSV", type="csv")

if uploaded_file is not None:

    try:
        df = load_data(uploaded_file)
        st.success("Fichier chargé avec succès ✅")
    except ValueError as e:
        st.error(e)
        st.stop()

    # Infos générales
    st.subheader("ℹ️ Informations générales")
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", df.shape[0])
    col2.metric("Colonnes", df.shape[1])
    col3.metric("Valeurs manquantes", int(df.isna().sum().sum()))

    st.subheader("📋 Aperçu des données")
    st.dataframe(df.head(10))

    # Détection colonnes
    numeric_cols, categorical_cols = detect_column_types(df)
    st.write(f"🔢 Colonnes numériques : {numeric_cols}")
    st.write(f"🏷 Colonnes catégorielles : {categorical_cols}")

    # Gestion des valeurs manquantes
    st.subheader("🧹 Gestion des valeurs manquantes")
    strategy = st.selectbox(
        "Choisir une stratégie",
        ["none", "drop", "mean", "median", "mode"]
    )
    df = handle_missing_values(df, strategy)

    # Détection outliers
    if numeric_cols:
        st.subheader("⚠️ Outliers détectés")
        outliers = detect_outliers(df, numeric_cols)
        for col, idx in outliers.items():
            st.write(f"{col}: {len(idx)} outliers")

    # Filtrage
    if categorical_cols:
        st.subheader("🎯 Filtrer les données")
        filter_col = st.selectbox("Colonne à filtrer", categorical_cols)
        filter_values = st.multiselect("Valeurs à garder", df[filter_col].unique())
        if filter_values:
            df = df[df[filter_col].isin(filter_values)]
            st.info(f"{len(df)} lignes après filtrage")

    # Stats descriptives
    st.subheader("📈 Statistiques descriptives")
    st.dataframe(df.describe(include="all"))

    # Visualisations automatiques
    if numeric_cols:
        st.subheader("🔍 Analyse visuelle")
        # Corrélation
        fig_corr = plot_correlation(df, numeric_cols)
        st.pyplot(fig_corr)
        # Histogrammes
        for col in numeric_cols:
            st.pyplot(plot_histogram(df, col))
        # Boxplots
        for col in numeric_cols:
            st.pyplot(plot_box(df, col))

    # Scatter plot interactif
    if len(numeric_cols) >= 2:
        st.subheader("📊 Scatter plot interactif")
        x_axis = st.selectbox("Axe X", numeric_cols)
        y_axis = st.selectbox("Axe Y", numeric_cols, index=1)
        st.pyplot(plot_scatter(df, x_axis, y_axis))

    # Télécharger le CSV filtré
    st.subheader("⬇️ Télécharger les données filtrées")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger CSV", csv, "datadash_export.csv", "text/csv")

else:
    st.info("⬆️ Uploade un fichier CSV pour commencer.")

