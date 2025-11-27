import streamlit as st
import pandas as pd 
from app_pages.registrar import pagina_registrar
from app_pages.consultar import pagina_consultar
from app_pages.filtros import pagina_filtros
from app_pages.graficas import pagina_graficos
from app_pages.estadisticas import pagina_estadisticas
from utils.funciones import cargar_datos

st.set_page_config(page_title="Accidentes Viales",page_icon="🚧", layout="wide")


if "opcion" not in st.session_state:
    st.session_state["opcion"] = "Inicio"


def pagina_inicio():
    st.title("Sistema de Accidentes Viales ")
    st.image(
        "https://media.istockphoto.com/id/466327320/es/foto/car-crash-colisi%C3%B3n-en-urban-street.jpg?s=612x612&w=0&k=20&c=jVNAuAW6hOGeD07CoS5jiFg5QdqbOGQm5d6o3fOrnhg=",
        width="stretch")

opcion = st.sidebar.radio(
    "Seleccione una opcion:",
    ["Inicio", "Registrar Accidente", "Consultar / Modificar", "Filtros", "Graficos", "Estadisticas"],
    index=["Inicio", "Registrar Accidente", "Consultar / Modificar", "Filtros", "Graficos", "Estadisticas"].index(st.session_state["opcion"]),
    key="menu")

st.session_state["opcion"] = opcion

df = cargar_datos()

st.session_state["df"] = df


if opcion == "Inicio":
    pagina_inicio()
elif opcion == "Registrar Accidente":
    pagina_registrar(df)
elif opcion == "Consultar / Modificar":
    pagina_consultar(df)
elif opcion == "Filtros":
    pagina_filtros(df)
elif opcion == "Graficos":
    pagina_graficos(df)
elif opcion == "Estadisticas":
    pagina_estadisticas(df)


