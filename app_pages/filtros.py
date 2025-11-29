import streamlit as st
import pandas as pd #Se importan las librerias

def pagina_filtros(df): #Se crea la funcion de filtros

    df = st.session_state.get("df", df)
    st.title("🔤 Filtros de accidentes")
    st.write("📝 Seleccione uno o varios criterios para filtrar los accidentes registrados.")

    columnas_necesarias = ["Causa probable", "Estado de la vía", "Clima"]#Revsa que las columnas esten en el df, si no estan las agrega vacias
    for col in columnas_necesarias:
        if col not in df.columns:
            df[col] = None

    for col in ["Heridos", "Muertes", "Vehiculos Involucrados"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)#Se convierte en esas columnas a numeros enteros para poder realizar los filtros bien, si hay un valor que no es numero lo pone en nan y luego reemplaza nan por 0

    with st.expander("⚙️ Opciones de Filtro", expanded=True):#Se crea un panel desplegable 

        lista_tipos = sorted(df["Clase de Accidente"].dropna().unique())#Selecciona clase de accidente, quita los valores vacios y tamnbien solo deja valores unicos y que guardado en la variable lista_tipos
        tipo_accidente = st.multiselect("Tipo de accidente:", lista_tipos)#Se permiten seleccionar los tipos que hayan 

        lista_clima = sorted(df["Clima"].dropna().unique())#Pasa lo mismo asi para el resto como en Clase de accidentes
        clima = st.multiselect("Clima:", lista_clima)

        lista_estado = sorted(df["Estado de la vía"].dropna().unique())
        estado_via = st.multiselect("Estado de la vía:", lista_estado)

        filtro_heridos = st.checkbox("Heridos > promedio")#Se crea una casilla donde el usuario define si la marca o no 
        filtro_muertes = st.checkbox("Accidentes con muertes")

        df["Fecha_Ocurrencia"] = pd.to_datetime(df["Fecha_Ocurrencia"], format="mixed", errors="coerce")#Se convierte todo a un formato de fehca y hora
        min_fecha = df["Fecha_Ocurrencia"].min().date()#Busca la fehca mas antigua 
        max_fecha = df["Fecha_Ocurrencia"].max().date()#Busca la fecha mas reciente

        fecha_inicio, fecha_fin = st.date_input( #Se crea un selector de fechas que sera un rango de esas dos fechas
            "Rango de fechas", [min_fecha, max_fecha]
        )


    df_filtrado = df.copy()#Se crea una copia del df original para hacer los filtros sin modificar el original 

    if tipo_accidente:#Se verifica si el usuario selecciono algun tipo de accidente devuelve true si lo marco y aplica el filtro solo dejando las filas que coinciden con los tipos seleccionados
        df_filtrado = df_filtrado[df_filtrado["Clase de Accidente"].isin(tipo_accidente)]

    if clima:#Pasa lo mismo que con tipo de accidentes 
        df_filtrado = df_filtrado[df_filtrado["Clima"].isin(clima)]

    if estado_via:
        df_filtrado = df_filtrado[df_filtrado["Estado de la vía"].isin(estado_via)]

    if filtro_heridos:#Si el usuario marca esta casilla se revisa la columna de heridos y se saca un promedio y se guarda en la variable 
        promedio = df["Heridos"].mean()
        df_filtrado = df_filtrado[df_filtrado["Heridos"] > promedio] #Se filtra donde solo las filas donde el numero de heridos sea mayor al promedio y se devuelve 

    if filtro_muertes:#Si se marca la casilla se revisa la columna de muertes y se elige cuales son mayores a 0
        df_filtrado = df_filtrado[df_filtrado["Muertes"] > 0]


    df_filtrado["Fecha_Ocurrencia"] = df_filtrado["Fecha_Ocurrencia"].dt.date


    df_filtrado = df_filtrado[ #Se aplica solo con loa filtros anteriores y que tambien esten en el rango de fechas seleccionado
        (df_filtrado["Fecha_Ocurrencia"] >= fecha_inicio) &
        (df_filtrado["Fecha_Ocurrencia"] <= fecha_fin)
    ]

    st.subheader(f"➡️ Resultados encontrados: {len(df_filtrado)} registros") #Se muestra cuantas filas tiene el df filtrado 
    st.dataframe(df_filtrado, width="stretch")#Se muestra el dataframe y se ajusta a la pagina

    if st.button("🔙Volver al menú principal"): #Hay un boton para volver al inicio 
       st.session_state["opcion"] = "Inicio"
       st.rerun()


    
