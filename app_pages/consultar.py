import streamlit as st
import pandas as pd 
from utils.funciones import guardar_datos#Se importan las librerias y se llama a la funcion de guardar datos


def pagina_consultar(df): #Se crea la funcion de consultar
    st.title("🔎 Consultar / Modificar Accidente") #Titulo
    st.write("🖊️Ingrese el código del accidente para consultarlo o modificar sus datos")#Indicaciones para el usuario


    if st.session_state.get("registro_eliminado", False):
        st.success("🚮 Registro eliminado exitosamente.")
        st.session_state["registro_eliminado"] = False


    codigo_buscar = st.text_input("Código del accidente", "")#Se le da un texto para que el usuario escriba y este se guarda en codigo_buscar
    buscar = st.button("🔍Buscar")#Cuando el usuario le da al boton se guarda en buscar

    if buscar: #Se hace un concional de cuando se le da al boton buscar
       if codigo_buscar not in df["Codigo_Accidente"].values: #El codigo entra y si no esta en el df sale un error diciendo que no existe un accidente con ese codigo y le da el valor de True
           st.error("❌ No existe un accidente con ese código.")
           st.session_state["codigo_no_existente"] = True
       else:
           st.session_state["codigo_no_existente"] = False #Sino el codigo se guarda en codigo_buscar
           st.session_state["codigo_encontrado"] = codigo_buscar

    if st.session_state.get("codigo_no_existente",False):#Aca entra y como tiene el valor de true se mete en el condicional
        if st.button("👤 Registrar uno nuevo"):#Se muestra el boton para poder registrar ese codigo
            st.session_state["opcion"] = "Registrar Accidente"#Cuando le damos al boton cambia a la pagina de registrar accidente
            st.rerun()
        return
    if "codigo_encontrado" in st.session_state:#Verifica que si este guardado
        codigo_encontrado = st.session_state["codigo_encontrado"]#Si lo encuentra lo guarda en la variable codigo_encontrado
        

        fila = df[df["Codigo_Accidente"] == codigo_buscar].iloc[0]#Se busca en el df el registro de codigo y iloc toma la posicion 0 para guardarlo como una fila 
        st.success("🔓 Registro encontrado. Puede modificar todos los datos")#Sale un mensaje que si fue encontrado el codigo y puede ser modificado

        fecha_dt = pd.to_datetime(fila["Fecha_Ocurrencia"], errors="coerce")#Se convierte la fecha guardada en una fecha que pueda leer streamlit
        fecha_valor = fecha_dt.date() if not pd.isna(fecha_dt) else pd.Timestamp.now().date()#Se verifica que el dia sea correcto para guardarlo en fecha_valor sino se usa la fecha actual
        hora_valor = fecha_dt.time() if not pd.isna(fecha_dt) else pd.Timestamp.now().time()

        with st.form("form_editar"):#Se crea un formulario de edicion

            col1, col2 = st.columns(2) #Se crean dos columnas

            with col1:
                fecha = st.date_input("Fecha del accidente", fecha_valor)#La primera columna sera la fecha del accidente y se ve la fecha que anteriormente ya habiamos sacado limpia

            with col2:
                hora = st.time_input("Hora del accidente", hora_valor)

            codigo_nuevo = st.text_input("Código del accidente", fila["Codigo_Accidente"])#Se crea una columna donde se pone el codigo existente, por si lo quiere cambiar o dejar aasi y se guarda en la variable codigo_nuevo

            col3, col4 = st.columns(2)#Se crean mas columnas para seguir modificando o dejar asi 

            with col3:
                direccion = st.text_input("Dirección", fila["Direccion"])

            with col4:
                lista_barrios = sorted(df["Barrio"].dropna().unique())
                barrio = st.selectbox("Barrio", lista_barrios,index=lista_barrios.index(fila["Barrio"]))

            col5, col6, col7 = st.columns(3)

            with col5:
                vehiculos = st.number_input("Vehículos involucrados", min_value=0, step=1,value=int(fila["Vehiculos Involucrados"]))

            with col6:
                heridos = st.number_input("Heridos", min_value=0, step=1, value=int(fila["Heridos"]))

            with col7:
                muertes = st.number_input("Muertes", min_value=0, step=1, value=int(fila["Muertes"]))

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

            submit = st.form_submit_button("🔒 Guardar Cambios") #Se crea un boton para guardar el formulario

        if submit:
            if codigo_nuevo != codigo_buscar:#Se entra a un condicional que si el codigo se cambia y es diferente al que habiamos buscado, entra al ciclo 
                if codigo_nuevo in df["Codigo_Accidente"].values:#Si el codigo esta en el dataframe sale un error que ya existe  
                    st.error("❌ Ya existe un accidente con ese código.")
                    return
            fecha_hora = f"{fecha} {hora}"#Se convierte la fecha y hora en una sola para ponerla en la variable fecha_hora

            nueva_fila = {#Se crea la nueva lista donde se le asigna la clave que es nombre de la columna de df y el valor que es lo que el usuario escogio en el formulario
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

            filtro = df["Codigo_Accidente"] == codigo_buscar #Nos muestra donde queda codigo_buscar y se pone a la variable filtro

            for col, value in nueva_fila.items():#Se recorre todas la filas del diccionario de nueva_fila, la fila donde el filtro sea True le cambia el valor 
                if col in df.columns:
                 df.loc[filtro, col] = value


            guardar_datos(df)#Se llama a la funcion guardar_datos para guardar los datos en el excel permanentemente 
            st.session_state["df"] = df #Actualiza la copia del dataframe dentro de streamlit


            st.success("✅Los datos se actualizaron exitosamente")#Se manda un mensaje al usuario que el registro se actualizo y salen unos globos flotando
            st.balloons()

            st.write("### Registro actualizado:")#Se le muestra al usuario lo que agrego 
            st.json(nueva_fila)  

        if st.button("❌ Borrar registro"):#Se agrega un boton de eliminar 
            df = df[df["Codigo_Accidente"] != codigo_encontrado]#Se elimina del dataframe el codigo que coincide con codigo_encontrado, filtra los otros dejando los que no tengan ese codigo
            guardar_datos(df)#Se guardan los datos 
            st.session_state["df"] = df #Se actualiza la copia del df
            st.session_state.pop("codigo_encontrado", None) #Se elimina de la memoria codigo_encontrado
            st.session_state["registro_eliminado"] =True #Se marca una bandera indicando que se elimino el regitro para cuando se vuelva a cargar la pagina, las lineas del inicio pase y ssalga que fue exitosamente borrado
            st.rerun()
        
    if st.button("🔙Volver al menú principal"):#Hay un boton para volver al inicio 
       st.session_state["opcion"] = "Inicio"
       st.rerun()
