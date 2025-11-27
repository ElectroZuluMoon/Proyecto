import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
def pagina_estadisticas(df):

    if "df" not in st.session_state:
        st.error("No se ha cargado el DataFrame.")
        st.stop()

    df = st.session_state.df
    st.title("Estadísticas Generales de Accidentes")
    st.info("Resumen estadístico según los datos cargados")

    columnas_nuevas = ["Causa probable", "Estado de la vía", "Clima"]
    for col in columnas_nuevas:
        if col not in df.columns:
            df[col] = None

    df["Fecha_Ocurrencia"] = pd.to_datetime(
        df["Fecha_Ocurrencia"], format="mixed", errors="coerce"
    )
    df["Hora"] = df["Fecha_Ocurrencia"].dt.hour
    df["Dia"] = df["Fecha_Ocurrencia"].dt.date

    df["Muertes"] = df["Muertes"].replace("NO APLICA", None)
    df["Muertes"] = pd.to_numeric(df["Muertes"], errors="coerce")

    df["Heridos"] = df["Heridos"].replace("NO APLICA", None)
    df["Heridos"] = pd.to_numeric(df["Heridos"], errors="coerce")


    st.subheader("Indicadores clave")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Accidentes", len(df))

    with col2:
        st.metric("Promedio de Heridos", round(df["Heridos"].mean(), 2))

    with col3:
        st.metric("Promedio de Muertos", round(df["Muertes"].mean(), 2))

    col4, col5 = st.columns(2)

    dia_top = df["Dia"].value_counts().idxmax()
    total_dia_top = df["Dia"].value_counts().max()

    with col4:
        st.metric("Día con más accidentes", f"{dia_top} ({total_dia_top})")

    hora_top = df["Hora"].value_counts().idxmax()
    total_hora_top = df["Hora"].value_counts().max()

    with col5:
        st.metric("Hora con más accidentes", f"{hora_top}:00 ({total_hora_top})")

    st.markdown("---")

    st.subheader("Seleccione un tipo de gráfico")

    tipo_grafico = st.selectbox(
        "Tipo de gráfico",
        [
            "Barras: Accidentes por tipo",
            "Barras: Accidentes por barrio",
            "Línea: Accidentes en el tiempo",
            "Línea: Accidentes por hora",
        ],
    )

    if st.button("Generar gráfico"):
        if tipo_grafico == "Barras: Accidentes por tipo":
            conteo = df["Clase de Accidente"].value_counts()
            fig, ax = plt.subplots()
            conteo.plot(kind="bar", ax=ax)
            ax.set_title("Accidentes por tipo")
            ax.set_ylabel("Número de accidentes")
            st.pyplot(fig)

        elif tipo_grafico == "Barras: Accidentes por barrio":
            conteo = df["Barrio"].value_counts().head(20)
            fig, ax = plt.subplots(figsize=(10, 5))
            conteo.plot(kind="bar", ax=ax)
            ax.set_title("Accidentes por barrio (Top 20)")
            ax.set_ylabel("Número de accidentes")
            st.pyplot(fig)

        elif tipo_grafico == "Línea: Accidentes en el tiempo":
            conteo = df["Dia"].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(conteo.index, conteo.values)
            ax.set_title("Accidentes por día")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Cantidad")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        elif tipo_grafico == "Línea: Accidentes por hora":
            conteo = df["Hora"].value_counts().sort_index()
            fig, ax = plt.subplots()
            ax.plot(conteo.index, conteo.values)
            ax.set_title("Accidentes por hora del día")
            ax.set_xlabel("Hora")
            ax.set_ylabel("Cantidad")
            st.pyplot(fig)

    if st.button("Volver al menú principal"):
        st.session_state["opcion"] = "Inicio"
        st.rerun()