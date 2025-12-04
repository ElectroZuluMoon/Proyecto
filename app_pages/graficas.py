import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt #Se importan las librerias 


def pagina_graficos(df):#Se crea la funcion de graficos 

    df = st.session_state.get("df", df)
    st.title("📊 Graficos")
    st.info("Graficos segun los filtros")

    columnas_nuevas = ["Causa probable", "Estado de la vía", "Clima"]#Se crea las columnas nuevas que tendra el dataframe
    for col in columnas_nuevas: #Hace un ciclo el cual mira en el dataframe cada una de las columnas y mira si estan si no las crea en el df y las crea vacia
        if col not in df.columns:
            df[col] = None

    df["Fecha_Ocurrencia"] = pd.to_datetime(df["Fecha_Ocurrencia"], format="mixed", errors="coerce")#Se convierte los valores de fecha de ocurrencia y las convierte en la fecha 


    st.subheader("🔎 Filtros")

    col1, col2 = st.columns(2)#Se crean dos columnas 

    with col1:
        fecha_min = df["Fecha_Ocurrencia"].min()#Se calcula la fecha mas antigua registrada
        fecha_max = df["Fecha_Ocurrencia"].max()#Se calcula la fecha mas reciente

        fecha_inicio, fecha_fin = st.date_input(
            "Rango de fechas",
            [fecha_min, fecha_max]#Se crea un selector de fechas que sera un rango de esas dos fechas

        )


    with col2:
        tipos = sorted(df["Clase de Accidente"].dropna().unique())#Se selecciona la columna de clase de accidentes y elimina los duplicados y los valores nulos, luego se ponen alfabeticamente
        tipo_accidente = st.multiselect("Tipo de accidente", tipos)


        climas = sorted(df["Clima"].dropna().unique())
        clima = st.multiselect("Clima", climas)


        estados = sorted(df["Estado de la vía"].dropna().unique())
        estado_via = st.multiselect("Estado de la vía", estados)


    df_f = df.copy()#Se crea una copia del df original para hacer los filtros sin modificar el original 


    df_f = df_f[#Se aplica solo con loa filtros anteriores y que tambien esten en el rango de fechas seleccionado
        (df_f["Fecha_Ocurrencia"] >= pd.to_datetime(fecha_inicio)) &
        (df_f["Fecha_Ocurrencia"] <= pd.to_datetime(fecha_fin))
    ]

    if tipo_accidente:#Se verifica si el usuario selecciono algun tipo de accidente devuelve true si lo marco y aplica el filtro solo dejando las filas que coinciden con los tipos seleccionados
        df_f = df_f[df_f["Clase de Accidente"].isin(tipo_accidente)]

    if clima:
        df_f = df_f[df_f["Clima"].isin(clima)]

    if estado_via:
        df_f = df_f[df_f["Estado de la vía"].isin(estado_via)]

    st.info(f"Registros filtrados: **{len(df_f)}**")#Sale un mensaje informativo con el numero de registros filtrados


    st.subheader("🎨 Tema de color")

    tema = st.radio(#Se crean las opciones para marcar el color que queramos ver en los graficos
        "Seleccione un tema:",
        ["Tema 1 (Claro)", "Tema 2 (Oscuro)"]
    )

    if tema == "Tema 1 (Claro)":#Se elige el tema segun la opcion otros temas podrian ser "bmh" "fivethirtyeight" "classic"
        plt.style.use("fivethirtyeight")
    else:
        plt.style.use("dark_background")


    st.subheader("📌 Tipo de gráfico")

    tipo_grafico = st.selectbox( #Se crea un menu plegable para seleccionar que tipo de grafico elegir y que sera filtrado
        "Seleccione el tipo de gráfico:",
        ["Dispersión (Vehículos vs Heridos)",
         "Barras (Barrio vs Clase de accidente)",
         "Histograma (Accidentes por hora)",
         "Histograma (Accidentes por día)"]
    )

    if st.button("📊 Generar gráfico"):#El ususario le da generar grafico y comiena el condicional
        if tipo_grafico == "Dispersión (Vehículos vs Heridos)":#Si el usuario eligio dispersion...
            fig, ax = plt.subplots()#Se crea una figura y un eje donde se va a dibujar
            ax.scatter(df_f["Vehiculos Involucrados"], df_f["Heridos"])#Dibuja un grafico de dispersion usando los datos filtrados, el eje x como vehiculos involucrados y el eje y como heridos
            ax.set_title("Vehículos involucrados vs Heridos")#Se crea el titulo 
            ax.set_xlabel("Vehículos involucrados")#La etiqueta del eje x
            ax.set_ylabel("Heridos")#L etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico 

        elif tipo_grafico == "Barras (Barrio vs Clase de accidente)":
            conteo = df_f.groupby(["Barrio", "Clase de Accidente"]).size().unstack(fill_value=0)#Se crea una tabla que cuenta cuantos accidentes hubo por cada cobinacion

            fig, ax = plt.subplots(figsize=(10,5))#Se crea una figura para el grafico y ajusta su tamaño
            conteo.plot(kind="bar", ax=ax)#Se producen las barras agrupadas, cada columna aparece como una serie diferente de barras dentro de cada barrio 
            ax.set_title("Barrio vs Clase de accidente")#Se crea el titulo 
            ax.set_xlabel("Barrios")#La etiqueta del eje x
            ax.set_ylabel("Cantidad de accidentes")#La etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico

        elif tipo_grafico == "Histograma (Accidentes por hora)":
            df_f["Hora"] = df_f["Fecha_Ocurrencia"].dt.hour#De la columna de fecha ocurrencia del df se extrae solamente la hora y se guarda en la variable 

            fig, ax = plt.subplots()#Se crea una figura y un eje donde se va a dibujar
            ax.hist(df_f["Hora"], bins=24)#Se ponen los valores que se van a graficar y una barra por cada hora (24) 
            ax.set_title("Accidentes por hora del día")#Se crea el titulo 
            ax.set_xlabel("Hora")#La etiqueta del eje x
            ax.set_ylabel("Frecuencia")#La etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico


        elif tipo_grafico == "Histograma (Accidentes por día)":
            df_f["Dia"] = df_f["Fecha_Ocurrencia"].dt.date#De la columna de fecha ocurrencia del df se extrae solamente el dia y se guarda en la variable 

            fig, ax = plt.subplots()#Se crea una figura y un eje donde se va a dibujar
            ax.hist(df_f["Dia"], bins=30)#Se ponen los valores que se van a graficar
            ax.set_title("Accidentes por día")#Se crea el titulo 
            ax.set_xlabel("Día")#La etiqueta del eje x
            ax.set_ylabel("Frecuencia")#La etiqueta del eje y
            st.pyplot(fig)#Muestra el grafico


        
    if st.button("🔙Volver al menú principal"): #Hay un boton para volver al inicio 
       st.session_state["opcion"] = "Inicio"
       st.rerun()

