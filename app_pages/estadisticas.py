import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt


def pagina_estadisticas(df):

    df = st.session_state.get("df", df)
    st.title("📈 Estadísticas Generales de Accidentes")
    st.info("☠️ Resumen estadístico según los datos cargados")

    columnas_nuevas = ["Causa probable", "Estado de la vía", "Clima"]#Se crea las columnas nuevas que tendra el dataframe
    for col in columnas_nuevas: #Hace un ciclo el cual mira en el dataframe cada una de las columnas y mira si estan si no las crea en el df y las crea vacia
        if col not in df.columns:
            df[col] = None

    df["Fecha_Ocurrencia"] = pd.to_datetime(df["Fecha_Ocurrencia"], format="mixed", errors="coerce")#Se convierte los valores de fecha de ocurrencia y las convierte en la fecha 
    df["Hora"] = df["Fecha_Ocurrencia"].dt.hour #Se extrae solo la hora
    df["Dia"] = df["Fecha_Ocurrencia"].dt.date #Se extrae solo el dia

    df["Muertes"] = df["Muertes"].replace("NO APLICA", None)#Se cambia el texto NO APLICA por un none
    df["Muertes"] = pd.to_numeric(df["Muertes"], errors="coerce")#Se convierte la columna a numeros enteros, si hay alguno que no se pueda convertir se vuelve nan

    df["Heridos"] = df["Heridos"].replace("NO APLICA", None)
    df["Heridos"] = pd.to_numeric(df["Heridos"], errors="coerce")


    st.subheader("📊 Indicadores clave")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🚑 Total de Accidentes", len(df))#Se muestra un cuadro con el valor de accidentes del df

    with col2:
        st.metric("👨‍🦼‍➡️ Promedio de Heridos", round(df["Heridos"].mean(), 2))#Muestra el promedio de heridos cn 2 decimales

    with col3:
        st.metric("⚰️ Promedio de Muertos", round(df["Muertes"].mean(), 2))#Muestra el promedio de muerte con 2 decimales

    col4, col5 = st.columns(2)

    dia_top = df["Dia"].value_counts().idxmax()#Devuelve el dia con mas accidentes
    total_dia_top = df["Dia"].value_counts().max()#Devuelve cuantos accidentes hubo en ese dia 

    with col4:
        st.metric("📅 Día con más accidentes", f"{dia_top} ({total_dia_top})")#Muestra junto el dia con mas accidentes 

    hora_top = df["Hora"].value_counts().idxmax()#Devuelve la hora con mas accidentes 
    total_hora_top = df["Hora"].value_counts().max()#Devuelve cuantos accidentes paso en esa hora

    with col5:
        st.metric("🕒 Hora con más accidentes", f"{hora_top}:00 ({total_hora_top})")#Muestra junto la hora con mas accidentes

    st.markdown("---")#Linea que divide 

    st.subheader("Seleccione un tipo de gráfico")

    tipo_grafico = st.selectbox(#Se despliega para seleccionar que tipo de grafica ver 
        "Tipo de gráfico",
        [
            "Barras: Accidentes por tipo",
            "Barras: Accidentes por barrio",
            "Línea: Accidentes en el tiempo",
            "Línea: Accidentes por hora",
        ],
    )

    if st.button("📊 Generar gráfico"):#Cuando el usuario hace click comienza los condicionales
        if tipo_grafico == "Barras: Accidentes por tipo":
            conteo = df["Clase de Accidente"].value_counts()#Cuenta cuantas veces aparece cada clase de accidente
            fig, ax = plt.subplots()#Se crea una figura para el grafico
            conteo.plot(kind="bar", ax=ax)#Se producen las barras agrupadas, cada columna aparece como una serie diferente de barras 
            ax.set_title("Accidentes por tipo")#Se crea el titulo 
            ax.set_xlabel("Clase de Accidente")#La etiqueta del eje x
            ax.set_ylabel("Número de accidentes")#La etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico

        elif tipo_grafico == "Barras: Accidentes por barrio":
            conteo = df["Barrio"].value_counts().head(15)#Cuenta por cada barrio cuantos accidentes hubo y saca el top 15
            fig, ax = plt.subplots(figsize=(10, 5))#Se crea una figura para el grafico y ajusta su tamaño
            conteo.plot(kind="bar", ax=ax)#Se producen las barras agrupadas, cada columna aparece como una serie diferente de barras
            ax.set_title("Accidentes por barrio (Top 20)")#Se crea el titulo
            ax.set_xlabel("Barrios")#La etiqueta del eje x
            ax.set_ylabel("Número de accidentes")#La etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico

        elif tipo_grafico == "Línea: Accidentes en el tiempo":
            conteo = df["Dia"].value_counts().sort_index()#Cuenta cuantos accidentes hubo por dia y los ordena cronologicamente
            fig, ax = plt.subplots(figsize=(12, 4))#Se crea una figura para el grafico y ajusta su tamaño
            ax.plot(conteo.index, conteo.values)#Las fechas en el eje x y la cantidad en el eje y
            ax.set_title("Accidentes por día")#Se crea el titulo
            ax.set_xlabel("Fecha")#La etiqueta del eje x
            ax.set_ylabel("Cantidad")#La etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico

        elif tipo_grafico == "Línea: Accidentes por hora":#Cuenta cuantos accidentes hubo por dia y los ordena cronologicamente
            conteo = df["Hora"].value_counts().sort_index()
            fig, ax = plt.subplots()#Se crea una figura para el grafico
            ax.plot(conteo.index, conteo.values)#Las horas en el eje x y la cantidad en el eje y
            ax.set_title("Accidentes por hora del día")#Se crea el titulo
            ax.set_xlabel("Hora")#La etiqueta del eje x
            ax.set_ylabel("Cantidad")#La etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico

    if st.button("🔙Volver al menú principal"):#Hay un boton para volver al inicio
        st.session_state["opcion"] = "Inicio"
        st.rerun()