import streamlit as st
import pandas as pd 
from app_pages.registrar import pagina_registrar
from app_pages.consultar import pagina_consultar
from app_pages.filtros import pagina_filtros
from app_pages.graficas import pagina_graficos
from app_pages.estadisticas import pagina_estadisticas
from utils.funciones import cargar_datos #Se impotan las librerias y se llama a cada pagina sus funciones especificas

st.set_page_config(page_title="Accidentes Viales",page_icon="🚧", layout="wide") #Configuramos la pagina web con el titulo un icono y que sea expandido para verlo ancho 


if "opcion" not in st.session_state: #Aca le damos un condicional para entrar a la pagina por primera vez que le da una clave "opcion" 
    st.session_state["opcion"] = "Inicio"#verifica si esta en el almacenamiento yle asigna un valor si no existia que sera "Inicio" entonces inicia desde esa pagina


def pagina_inicio(): #Creamos una funcion para la pagina de inicio 
    st.title("Sistema de Accidentes Viales ") #Creamos el titulo de nuestra pagina de inicio
    st.image(
        "https://media.istockphoto.com/id/466327320/es/foto/car-crash-colisi%C3%B3n-en-urban-street.jpg?s=612x612&w=0&k=20&c=jVNAuAW6hOGeD07CoS5jiFg5QdqbOGQm5d6o3fOrnhg=",
        width="stretch") #Agregamos una imagen representativa de lo que estamos trabajando
    st.write()

opcion = st.sidebar.radio( #Se crea un menu lateral con boton de opciones donde se puede seleccionar cada una de las paginas, se inicia en opcion y como opcion al cargar la pagina esta en Inicio entonces comeinza desde ahi y ya el usuario puede comenzar a seleccionar las paginas que desee
    "Seleccione una opcion:",
    ["🏠 Inicio", "🪪 Registrar Accidente", "🔎 Consultar / Modificar", "⚙️ Filtros", "📊 Graficos", "📈 Estadisticas"],
    index=["Inicio", "Registrar Accidente", "Consultar / Modificar", "Filtros", "Graficos", "Estadisticas"].index(st.session_state["opcion"]),
    key="menu")

st.session_state["opcion"] = opcion #Se guarda la opcion que el usuario eligio

df = cargar_datos() #Se llama a la funcion que anteriormente importamos y ella lee y ls carga en df 

st.session_state["df"] = df #Guarda ese dataframecon la clave de df, eso permite que todas las paginas de la app accedan al mismo dataframe 


if opcion == "Inicio": #Se ponen unas condiciones que segun lo que el usuario haya esocgido en el menu lateral es a la funcion que se va a ejecutar para mostar la pagina y todas las funciones reciben el dtaframe cuando necesitan los datos para trabajar 
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


