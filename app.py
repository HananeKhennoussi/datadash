import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 DataDash - Dashboard Dynamique")
st.write("💡 Chargez n'importe quel fichier CSV et explorez vos données !")

# Étape 1 : Charger un CSV depuis l'ordinateur
uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📋 Aperçu des données")
    st.dataframe(df.head(10))  # Affiche les 10 premières lignes

    # Détection automatique des colonnes numériques et catégorielles
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    st.write(f"Colonnes numériques : {numeric_cols}")
    st.write(f"Colonnes catégorielles : {categorical_cols}")

    # Étape 2 : Choix de l'axe pour le graphique en barres
    if categorical_cols and numeric_cols:
        cat_col = st.selectbox("Choisir la colonne catégorielle", categorical_cols)
        num_col = st.selectbox("Choisir la colonne numérique", numeric_cols)
        
        st.subheader(f"📊 Bar chart : {num_col} par {cat_col}")
        st.bar_chart(df.set_index(cat_col)[num_col])

    # Étape 3 : Scatter plot interactif
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

