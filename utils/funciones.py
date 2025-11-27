import streamlit as st
import pandas as pd 
import os

RUTA_EXCEL = "data/Accidentes_50.xlsx"


def cargar_datos():
    try:
        return pd.read_excel(RUTA_EXCEL)
    except FileNotFoundError:
        st.error("No se encontró el archivo. Se creará uno nuevo cuando registre datos.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error leyendo el archivo: {e}")
        return pd.DataFrame()

def guardar_datos(df):
    df.to_excel(RUTA_EXCEL, index=False)