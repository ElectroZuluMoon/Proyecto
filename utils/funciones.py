import streamlit as st
import pandas as pd 
import os

RUTA_EXCEL = "data/Accidentes_50.xlsx"


def cargar_datos():
    try:
        df = pd.read_excel(RUTA_EXCEL)
        return pd.read_excel(RUTA_EXCEL)
    except FileNotFoundError:
        st.error("No se encontró el archivo")
        return pd.DataFrame()

def guardar_datos(df):
    df.to_excel(RUTA_EXCEL, index=False)