import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
def pagina_graficos(df):

    if "df" not in st.session_state:
        st.error("No se ha cargado el DataFrame.")
        st.stop()

    df = st.session_state.df
    st.title("Graficos")
    st.info("Graficos segun los filtros")

    columnas_nuevas = ["Causa probable", "Estado de la vía", "Clima"]
    for col in columnas_nuevas:
        if col not in df.columns:
            df[col] = None

    df["Fecha_Ocurrencia"] = pd.to_datetime(df["Fecha_Ocurrencia"], format="mixed", errors="coerce")


    st.subheader("Filtros")

    col1, col2 = st.columns(2)

    with col1:
        fecha_min = df["Fecha_Ocurrencia"].min()
        fecha_max = df["Fecha_Ocurrencia"].max()

        fecha_inicio, fecha_fin = st.date_input(
            "Rango de fechas",
            [fecha_min, fecha_max]

        )


    with col2:
        tipos = sorted(df["Clase de Accidente"].dropna().unique())
        tipo_accidente = st.multiselect("Tipo de accidente", tipos)


        climas = sorted(df["Clima"].dropna().unique())
        clima = st.multiselect("Clima", climas)


        estados = sorted(df["Estado de la vía"].dropna().unique())
        estado_via = st.multiselect("Estado de la vía", estados)


    df_f = df.copy()

    df_f = df_f[
        (df_f["Fecha_Ocurrencia"] >= pd.to_datetime(fecha_inicio)) &
        (df_f["Fecha_Ocurrencia"] <= pd.to_datetime(fecha_fin))
    ]

    if tipo_accidente:
        df_f = df_f[df_f["Clase de Accidente"].isin(tipo_accidente)]

    if clima:
        df_f = df_f[df_f["Clima"].isin(clima)]

    if estado_via:
        df_f = df_f[df_f["Estado de la vía"].isin(estado_via)]

    st.info(f"Registros filtrados: **{len(df_f)}**")


    st.subheader("Tema de color")

    tema = st.radio(
        "Seleccione un tema:",
        ["Tema 1 (Claro)", "Tema 2 (Oscuro)"]
    )

    if tema == "Tema 1(Claro)":
        plt.style.use("default")
    else:
        plt.style.use("dark_background")


    st.subheader("Tipo de gráfico")

    tipo_grafico = st.selectbox(
        "Seleccione el tipo de gráfico:",
        ["Dispersión (Vehículos vs Heridos)",
         "Barras (Barrio vs Clase de accidente)",
         "Histograma (Accidentes por hora)",
         "Histograma (Accidentes por día)"]
    )

    if st.button("Generar gráfico"):
        if tipo_grafico == "Dispersión (Vehículos vs Heridos)":
            fig, ax = plt.subplots()
            ax.scatter(df_f["Vehiculos Involucrados"], df_f["Heridos"])
            ax.set_title("Vehículos involucrados vs Heridos")
            ax.set_xlabel("Vehículos involucrados")
            ax.set_ylabel("Heridos")
            st.pyplot(fig)

        elif tipo_grafico == "Barras (Barrio vs Clase de accidente)":
            conteo = df_f.groupby(["Barrio", "Clase de Accidente"]).size().unstack(fill_value=0)

            fig, ax = plt.subplots(figsize=(10,5))
            conteo.plot(kind="bar", ax=ax)
            ax.set_title("Barrio vs Clase de accidente")
            ax.set_ylabel("Cantidad de accidentes")
            st.pyplot(fig)

        elif tipo_grafico == "Histograma (Accidentes por hora)":
            df_f["Hora"] = df_f["Fecha_Ocurrencia"].dt.hour

            fig, ax = plt.subplots()
            ax.hist(df_f["Hora"], bins=24)
            ax.set_title("Accidentes por hora del día")
            ax.set_xlabel("Hora")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)

        elif tipo_grafico == "Histograma (Accidentes por día)":
            df_f["Dia"] = df_f["Fecha_Ocurrencia"].dt.date

            fig, ax = plt.subplots()
            ax.hist(df_f["Dia"], bins=20)
            ax.set_title("Accidentes por día")
            ax.set_xlabel("Día")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)

        
    if st.button("Volver al menú principal"):
       st.session_state['opcion'] = "Inicio"


