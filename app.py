import streamlit as st
import pandas as pd 
import os

st.set_page_config(page_title="Accidentes Viales",page_icon="🚧", layout="wide")

RUTA_EXCEL = "data/Accidentes_50.xlsx"

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel(RUTA_EXCEL)
        return pd.read_excel(RUTA_EXCEL)
    except FileNotFoundError:
        st.error("No se encontró el archivo")
        return pd.DataFrame()


def guardar_datos(df):
    df.to_excel(RUTA_EXCEL, index=False)

def pagina_inicio():
    st.title("Sistema de Accidentes Viales ")
    st.image(
        "https://media.istockphoto.com/id/466327320/es/foto/car-crash-colisi%C3%B3n-en-urban-street.jpg?s=612x612&w=0&k=20&c=jVNAuAW6hOGeD07CoS5jiFg5QdqbOGQm5d6o3fOrnhg=",
        use_container_width=True)

def pagina_registrar(df):
    st.title("Registrar Accidente")
    st.info("Formulario")

def pagina_consultar_modificar(df):
    st.title("Consultar / Modificar Accidente")
    st.info("Busqueda y edicion de Accidentes")

def pagina_filtros(df):
    st.title("Filtros")
    st.info("Filtros de Accidentes")

def pagina_graficos(df):
    st.title("Graficos")
    st.info("Graficos segun los filtros")

def estadisticas(df):
    st.title("Estadisticas")
    st.info("Estadisticas avanzadas")

    


st.sidebar.title("Menu")
opcion = st.sidebar.radio(
    "Seleccione una opcion:",
    ["Inicio", "Registrar Accidente", "Consultar / Modificar", "Filtros", "Graficos", "Estadisticas"]
)