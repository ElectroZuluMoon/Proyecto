import streamlit as st
import pandas as pd
from utils.funciones import guardar_datos #Se importan las librerias y se llama a la funcion de guardar datos

def pagina_registrar(df): #Se crea la funcion de registrar usando el dataframe cargado
    st.title("Registrar Accidente")#Titulo de la pagina 
    st.write("Complete todos los campos para registrar un nuevo accidente")#Un texto que le indica al usuario que debe hacer en esa pagina


    columnas_nuevas = ["Causa probable", "Estado de la vía", "Clima"] #Se crea las columnas nuevas que tendra el dataframe
    for col in columnas_nuevas: #Hace un ciclo el cual mira en el dataframe cada una de las columnas y mira si estan si no las crea en el df y las crea vacia
        if col not in df.columns:
            df[col] = None
               
    with st.form("form_registro"):#Se crea un formulario con el nombre form_registro

        col1, col2 = st.columns(2) #Se orgniza el formulario en dos columnas para distribuir los campos a registrar


        with col1: #En la primera columna tenemos la fecha y hora, aca el usuario registra esoa valores y se guardan en las variabes fecha y hora para usarlos despues al registrar la informacion
            fecha = st.date_input("Fecha del accidente")
            hora = st.time_input("Hora del accidente")
        
        with col2:#En la segunda columna el usuario crea el codigo para que asi sea unico su registro y se guarda en la variable codigo
            codigo = st.text_input("Código del accidente")

        col3, col4 = st.columns(2)#Se crean otras dos columnas mas para seguir organizando el formulario

        with col3:
            direccion = st.text_input("Dirección")#Se crea un campo donde el usurio registra la direccion del acciedente y se guarda en la variable direccion

        with col4: 
            lista_barrios = sorted(df["Barrio"].dropna().unique())#Se selecciona la columna barrios del dataframe, dropna elimina los posibles valores nulos y unique devuelve los valores unicos
            #sorted ordena los valores que resultan en orden alfabetico y todo lo guarda en la variable lista_barrios
            barrio = st.selectbox("Barrio", lista_barrios) #Se crea un menu desplegable de barrios donde el usuario al desplegarla encontrara la lista de barrios y la eleccion se guardara en barrio
        
        col5, col6, col7 = st.columns(3)#Se crean tres columnas nuevas para seguir llenando el formulario 

        with col5: 
            vehiculos = st.number_input("Vehículos involucrados", min_value=0, step=1)#Se crea el campo para ingresar el numero de vehi invo con el valor minimo 0 y este se suma de 1 en 1 y se guarda en vehiculos

        with col6:
            heridos = st.number_input("Heridos", min_value=0, step=1) 

        with col7:
            muertes = st.number_input("Muertes", min_value=0, step=1)

        col8, col9 = st.columns(2)

        with col8:
             lista_acc_con = sorted(df["Accidente con"].dropna().unique())#Se hace lo mismo que con los barrios, recorre la columna del df saca los nulos y duplicdos y los pone en orden alfabetico, los guarda en lista_acc_con
             accidente_con = st.selectbox("Accidente con", lista_acc_con)#Se crea un menu desplegable donde el usuario elige la opcion y se guarda en accidentes_con

        with col9:
             lista_clase = sorted(df["Clase de Accidente"].dropna().unique())
             tipo_accidente = st.selectbox("Tipo de accidente", lista_clase)
             
        col10, col11 = st.columns(2)

        with col10: 
            estado_via = st.selectbox(
                "Estado de la vía",
                ["Seca", "Mojada", "En mantenimiento", "Desconocido"]
            ) #Se crea un menu desplegable donde el usuario elige a condicion de la via en el momento del accidente y esta se guarda en estado_via
        
        with col11:
            clima = st.selectbox(
                "Clima",
                ["Soleado", "Nublado", "Lluvioso", "Tormenta", "Desconocido"]
        )

        causa = st.text_area("Causa probable (descripción)") #Se crea una area donde el usuario describe cuales fueron esas causas problemas del accidente
        submit = st.form_submit_button("Guardar Registro")#Se crea un boton para finalizar el formulario y guardarlo 

    if submit: #Solo se registra todo cuando el boton registrar haya sido presionado por el usuario
        if codigo in df["Codigo_Accidente"].values:#Se inicia una busqueda de que si codigo esta en el df este devuelva un error que ya existe el codigo
           st.error("Ya existe un accidente con ese código")#Para que cada codigo sea unico 
           return
     
        if not codigo or not direccion:#Si los campos de codigo y direccion estan vacios mandara un mensaje de llenar todos los campos 
            st.error("Por favor llene todos los campos obligatorios")
            return
        
        fecha_hora = f"{fecha} {hora}"#Se convierte la fecha y hora en una sola para ponerla en la variable fecha_hora

        nueva_fila = { #Se crea la nueva lista donde se le asigna la clave que es nombre de la columna de df y el valor que es lo que el usuario escogio en el formulario 
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

        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)#Se convierte la nueva_fila en un dataframe, pd.contact une los dos dataframes, ignore_index organiza los indices para que no se repitan 

        guardar_datos(df)#Se llama a la funcion guardar_datos para guardar los datos en el excel permanentemente 
        st.session_state["df"] = df#Actualiza la copia del dataframe dentro de streamlit


        st.success("Accidente registrado correctamente")#Se manda un mensaje al usuario que el registro se guardo y salen unos globos flotando  
        st.balloons()

        st.write("### Último registro agregado:")#
        st.json(nueva_fila)

    if st.button("Volver al menú principal"):
       st.session_state["opcion"] = "Inicio"
       st.rerun()
