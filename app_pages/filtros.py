import streamlit as st
import pandas as pd 

def pagina_filtros(df):
    st.title("Filtros de accidentes")
    st.write("Seleccione uno o varios criterios para filtrar los accidentes registrados.")

    columnas_necesarias = ["Causa probable", "Estado de la vía", "Clima"]
    for col in columnas_necesarias:
        if col not in df.columns:
            df[col] = None
    for col in ["Heridos", "Muertes", "Vehiculos Involucrados"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    with st.expander("⚙️ Opciones de Filtro", expanded=True):

        lista_tipos = sorted(df["Clase de Accidente"].dropna().unique())
        tipo_accidente = st.multiselect("Tipo de accidente:", lista_tipos)

        lista_clima = sorted(df["Clima"].dropna().unique())
        clima = st.multiselect("Clima:", lista_clima)

        lista_estado = sorted(df["Estado de la vía"].dropna().unique())
        estado_via = st.multiselect("Estado de la vía:", lista_estado)

        filtro_heridos = st.checkbox("Heridos > promedio")
        filtro_muertes = st.checkbox("Accidentes con muertes")

        df["Fecha_Ocurrencia"] = pd.to_datetime(df["Fecha_Ocurrencia"], format="mixed", errors="coerce")
        min_fecha = df["Fecha_Ocurrencia"].min()
        max_fecha = df["Fecha_Ocurrencia"].max()

        fecha_inicio, fecha_fin = st.date_input(
            "Rango de fechas", [min_fecha, max_fecha]
        )

    df_filtrado = df.copy()

    if tipo_accidente:
        df_filtrado = df_filtrado[df_filtrado["Clase de Accidente"].isin(tipo_accidente)]

    if clima:
        df_filtrado = df_filtrado[df_filtrado["Clima"].isin(clima)]

    if estado_via:
        df_filtrado = df_filtrado[df_filtrado["Estado de la vía"].isin(estado_via)]

    if filtro_heridos:
        promedio = df["Heridos"].mean()
        df_filtrado = df_filtrado[df_filtrado["Heridos"] > promedio]

    if filtro_muertes:
        df_filtrado = df_filtrado[df_filtrado["Muertes"] > 0]

    df_filtrado = df_filtrado[
        (df_filtrado["Fecha_Ocurrencia"] >= pd.to_datetime(fecha_inicio)) &
        (df_filtrado["Fecha_Ocurrencia"] <= pd.to_datetime(fecha_fin))
    ]

    st.subheader(f"Resultados encontrados: {len(df_filtrado)} registros")
    st.dataframe(df_filtrado, width="stretch")

    if st.button("Volver al menú principal"):
       st.session_state["opcion"] = "Inicio"
       st.rerun()


    
