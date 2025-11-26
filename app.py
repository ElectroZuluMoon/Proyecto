import streamlit as st
import pandas as pd 
import os
from pages.registrar import pagina_registrar
from pages.consultar import pagina_consultar
from pages.filtros import pagina_filtros
from pages.graficas import pagina_graficos
from pages.estadisticas import pagina_estadisticas

from utils.funciones import cargar_datos, guardar_datos

st.set_page_config(page_title="Accidentes Viales",page_icon="🚧", layout="wide")

def pagina_inicio():
    st.title("Sistema de Accidentes Viales ")
    st.image(
        "https://media.istockphoto.com/id/466327320/es/foto/car-crash-colisi%C3%B3n-en-urban-street.jpg?s=612x612&w=0&k=20&c=jVNAuAW6hOGeD07CoS5jiFg5QdqbOGQm5d6o3fOrnhg=",
        width="stretch")

st.sidebar.title("Menu")
opcion = st.sidebar.radio(
    "Seleccione una opcion:",
    ["Inicio", "Registrar Accidente", "Consultar", "Filtros", "Graficos", "Estadisticas"]
)

df = cargar_datos()

if opcion == "Inicio":
    pagina_inicio()
elif opcion == "Registrar Accidente":
    st.switch_page("pages/registrar.py")
elif opcion == "Consultar":
    st.switch_page("pages/consultar.py")
elif opcion == "Filtros":
    st.switch_page("pages/filtros.py")
elif opcion == "Graficos":
    st.switch_page("pages/graficas.py")
elif opcion == "Estadisticas":
    st.switch_page("pages/estadisticas.py")
