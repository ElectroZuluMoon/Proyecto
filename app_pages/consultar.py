import streamlit as st
import pandas as pd 
from utils.funciones import guardar_datos
def pagina_consultar(df):
    st.title(" Consultar / Modificar Accidente")
    st.write("Ingrese el código del accidente para consultarlo o modificar sus datos")
    codigo_buscar = st.text_input("Código del accidente", "")
    buscar = st.button("Buscar")

    if buscar:
       if codigo_buscar not in df["Codigo_Accidente"].values:
           st.error("No existe un accidente con ese código.")
           st.session_state["codigo_no_existente"] = True
       else:
           st.session_state["codigo_no_existente"] = False
           st.session_state["codigo_encontrado"] = codigo_buscar

    if st.session_state.get("codigo_no_existente",False):
        if st.button("Registrar uno nuevo"):
            st.session_state["opcion"] = "Registrar Accidente"
            st.rerun()
        return
    if "codigo_encontrado" in st.session_state:
        codigo_encontrado = st.session_state["codigo_encontrado"]
        

        fila = df[df["Codigo_Accidente"] == codigo_buscar].iloc[0]
        st.success("Registro encontrado. Puede modificar todos los datos")

        fecha_dt = pd.to_datetime(fila["Fecha_Ocurrencia"], errors="coerce")
        fecha_valor = fecha_dt.date() if not pd.isna(fecha_dt) else pd.Timestamp.now().date()
        hora_valor = fecha_dt.time() if not pd.isna(fecha_dt) else pd.Timestamp.now().time()

        with st.form("form_editar"):

            col1, col2 = st.columns(2)

            with col1:
                fecha = st.date_input("Fecha del accidente", fecha_valor)

            with col2:
                hora = st.time_input("Hora del accidente", hora_valor)

            codigo_nuevo = st.text_input("Código del accidente", fila["Codigo_Accidente"])

            col3, col4 = st.columns(2)

            with col3:
                direccion = st.text_input("Dirección", fila["Direccion"])

            with col4:
                lista_barrios = sorted(df["Barrio"].dropna().unique())
                barrio = st.selectbox("Barrio", lista_barrios,
                                      index=lista_barrios.index(fila["Barrio"]))

            col5, col6, col7 = st.columns(3)

            with col5:
                vehiculos = st.number_input("Vehículos involucrados", min_value=0, step=1,
                                            value=int(fila["Vehiculos Involucrados"]))

            with col6:
                heridos = st.number_input("Heridos", min_value=0, step=1,
                                          value=int(fila["Heridos"]))

            with col7:
                muertes = st.number_input("Muertes", min_value=0, step=1,
                                          value=int(fila["Muertes"]))

            col8, col9 = st.columns(2)
            with col8:
                lista_acc_con = sorted(df["Accidente con"].dropna().unique())
                accidente_con = st.selectbox(
                    "Accidente con", lista_acc_con,
                    index=lista_acc_con.index(fila["Accidente con"])
                )

            with col9:
                lista_clase = sorted(df["Clase de Accidente"].dropna().unique())
                clase = st.selectbox(
                    "Tipo de accidente", lista_clase,
                    index=lista_clase.index(fila["Clase de Accidente"])
                )
            col10, col11, col12 = st.columns(3)

            with col10:
                estado_via = st.selectbox(
                    "Estado de la vía",
                    ["Seca", "Mojada", "En mantenimiento", "Desconocido"],
                    index=["Seca", "Mojada", "En mantenimiento", "Desconocido"]
                    .index(fila.get("Estado de la vía", "Desconocido"))
                )

            with col11:
                clima = st.selectbox(
                    "Clima",
                    ["Soleado", "Nublado", "Lluvioso", "Tormenta", "Desconocido"],
                    index=["Soleado", "Nublado", "Lluvioso", "Tormenta", "Desconocido"]
                    .index(fila.get("Clima", "Desconocido"))
                )

            causa = st.text_area("Causa probable", fila.get("Causa probable", ""))

            submit = st.form_submit_button("Guardar Cambios")

        if submit:
            if codigo_nuevo != codigo_buscar:
                if codigo_nuevo in df["Codigo_Accidente"].values:
                    st.error("❌ Ya existe un accidente con ese código.")
                    return
            fecha_hora = f"{fecha} {hora}"

            nueva_fila = {
                "Fecha_Ocurrencia": fecha_hora,
                "Codigo_Accidente": codigo_nuevo,
                "Direccion": direccion,
                "Barrio": barrio,
                "Vehiculos Involucrados": vehiculos,
                "Heridos": heridos,
                "Accidente con": accidente_con,
                "Muertes": muertes,
                "Clase de Accidente": clase,
                "Causa probable": causa,
                "Estado de la vía": estado_via,
                "Clima": clima
            }

            df.loc[df["Codigo_Accidente"] == codigo_buscar] = nueva_fila

            guardar_datos(df)

            st.success("Los datos se actualizaron exitosamente")
            st.balloons()

            st.write("### Registro actualizado:")
            st.json(nueva_fila)  
        
    if st.button("Volver al menú principal"):
       st.session_state["opcion"] = "Inicio"
       st.rerun()
