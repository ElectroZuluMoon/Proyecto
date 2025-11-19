import streamlit as st
import pandas as pd 
import os

st.set_page_config(page_title="Accidentes Viales",page_icon="🚧", layout="wide")

RUTA_EXCEL = "data/Accidentes_50.xlsx"

@st.cache_data
def cargar_datos():
    return pd.read_excel(RUTA_EXCEL)

def guardar_datos(df):
    df.to_excel(RUTA_EXCEL, index=False)


st.sidebar.title("Menu")
opcion = st.sidebar.radio(
    "Seleccione una opcion:",
    ["Inicio", "Registrar Accidente", "Consultar / Modificar", "Filtros", "Graficos", "Estadisticas"]
)
