import streamlit as st
import pandas as pd
from utils.funciones import guardar_datos

def pagina_registrar(df):
    st.title("Registrar Accidente")
    st.write("Complete todos los campos para registrar un nuevo accidente")


    columnas_nuevas = ["Causa probable", "Estado de la vía", "Clima"]
    for col in columnas_nuevas:
        if col not in df.columns:
            df[col] = None
               
    with st.form("form_registro"):
        col1, col2 = st.columns(2)

        with col1:
            fecha = st.date_input("Fecha del accidente")
            hora = st.time_input("Hora del accidente")
        
        with col2:
            codigo = st.text_input("Código del accidente")
        col3, col4 = st.columns(2)  

        with col3:
            direccion = st.text_input("Dirección")

        with col4:
            lista_barrios = sorted(df["Barrio"].dropna().unique())
            barrio = st.selectbox("Barrio", lista_barrios)
        
        col5, col6, col7 = st.columns(3)

        with col5:
            vehiculos = st.number_input("Vehículos involucrados", min_value=0, step=1)

        with col6:
            heridos = st.number_input("Heridos", min_value=0, step=1)

        with col7:
            muertes = st.number_input("Muertes", min_value=0, step=1)

        col8, col9 = st.columns(2)

        with col8:
             lista_acc_con = sorted(df["Accidente con"].dropna().unique())
             accidente_con = st.selectbox("Accidente con", lista_acc_con)

        with col9:
             lista_clase = sorted(df["Clase de Accidente"].dropna().unique())
             tipo_accidente = st.selectbox("Tipo de accidente", lista_clase)
        col10, col11, col12 = st.columns(3)

        with col10:
            estado_via = st.selectbox(
                "Estado de la vía",
                ["Seca", "Mojada", "En mantenimiento", "Desconocido"]
            )
        
        with col11:
            clima = st.selectbox(
                "Clima",
                ["Soleado", "Nublado", "Lluvioso", "Tormenta", "Desconocido"]
            )
        with col12:
            pass  # para estética

        causa = st.text_area("Causa probable (descripción)")
        submit = st.form_submit_button("Guardar Registro")

    if submit:
        if codigo in df["Codigo_Accidente"].values:
           st.error("Ya existe un accidente con ese código")
           return
     
        if not codigo or not direccion:
            st.error("Por favor llene todos los campos obligatorios")
        fecha_hora = f"{fecha} {hora}"

        nueva_fila = {
            "Fecha_Ocurrencia": fecha_hora,
            "Codigo_Accidente": codigo,
            "Direccion": direccion,
            "Barrio": barrio,
            "Vehiculos Involucrados": vehiculos,
            "Heridos": heridos,
            "Accidente con": accidente_con,
            "Muertes": muertes,
            "Clase de Accidente": tipo_accidente,
            "Causa probable": causa,
            "Estado de la vía": estado_via,
            "Clima": clima
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

        guardar_datos(df)
        st.success("Accidente registrado correctamente")
        st.balloons()

        st.write("### Último registro agregado:")
        st.json(nueva_fila)

    if st.button("Volver al menú principal"):
       st.session_state['opcion'] = "Inicio"