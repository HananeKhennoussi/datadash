import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file):
    """
    Charge un fichier CSV avec gestion des erreurs et mise en cache.
    """
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement du fichier : {e}")

