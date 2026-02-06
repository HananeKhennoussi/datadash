import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DataDash", layout="wide")

st.title("📊 DataDash - Dashboard Dynamique")
st.write("💡 Chargez n'importe quel fichier CSV et explorez vos données !")

# Étape 1 : Charger un CSV depuis l'ordinateur
uploaded_file = st.file_uploader("📂 Choisir un fichier CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Fichier chargé avec succès ✅")

    # Infos générales
    st.subheader("ℹ️ Informations générales")
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", df.shape[0])
    col2.metric("Colonnes", df.shape[1])
    col3.metric("Valeurs manquantes", int(df.isna().sum().sum()))

    st.subheader("📋 Aperçu des données")
    st.dataframe(df.head(10))

    # Détection automatique des colonnes
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    st.write(f"🔢 Colonnes numériques : {numeric_cols}")
    st.write(f"🏷 Colonnes catégorielles : {categorical_cols}")

    # Filtrage simple
    if categorical_cols:
        st.subheader("🎯 Filtrer les données")
        filter_col = st.selectbox("Choisir une colonne pour filtrer", categorical_cols)
        filter_values = st.multiselect("Valeurs à garder", df[filter_col].unique())

        if filter_values:
            df = df[df[filter_col].isin(filter_values)]
            st.info(f"{len(df)} lignes après filtrage")

    # Stats descriptives
    st.subheader("📈 Statistiques descriptives")
    st.dataframe(df.describe(include="all"))

    # Bar chart (ta fonctionnalité conservée)
    if categorical_cols and numeric_cols:
        cat_col = st.selectbox("Choisir la colonne catégorielle", categorical_cols)
        num_col = st.selectbox("Choisir la colonne numérique", numeric_cols)
        
        st.subheader(f"📊 Bar chart : {num_col} par {cat_col}")
        st.bar_chart(df.set_index(cat_col)[num_col])

    # Scatter plot (ta fonctionnalité conservée)
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Axe X (numérique)", numeric_cols, index=0)
        y_axis = st.selectbox("Axe Y (numérique)", numeric_cols, index=1)
        
        st.subheader(f"📈 Scatter plot : {y_axis} vs {x_axis}")
        fig, ax = plt.subplots()
        ax.scatter(df[x_axis], df[y_axis], color='green')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{y_axis} vs {x_axis}")
        st.pyplot(fig)

    # Histogramme
    if numeric_cols:
        st.subheader("📊 Histogramme")
        hist_col = st.selectbox("Choisir une colonne numérique pour l'histogramme", numeric_cols)
        fig2, ax2 = plt.subplots()
        ax2.hist(df[hist_col].dropna(), bins=30)
        ax2.set_title(f"Distribution de {hist_col}")
        st.pyplot(fig2)

    # Télécharger le CSV filtré
    st.subheader("⬇️ Télécharger les données filtrées")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger CSV", csv, "datadash_export.csv", "text/csv")

else:
    st.info("⬆️ Uploade un fichier CSV pour commencer.")

