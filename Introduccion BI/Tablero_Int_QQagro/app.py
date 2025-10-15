# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 08:35:47 2025

@author: Juan Esteban
"""

#Importamos las librerias necesarias
import sqlite3 as sq3
import pandas as pd
import numpy as np
import streamlit as st
import SQLib as sq
from datetime import date

# Nombre de la pagina
st.set_page_config(page_title = "QuimQuinAgro", layout = "wide")

# Configuramos el titulo principal
st.title("Consultas Info Financiera")

#Base de datos 
DB = 'contabilidad.db'

#Lista de socios para la consulta Q3
socios_query = """
SELECT DISTINCT socio FROM (
    SELECT socio FROM cxc2020
    UNION ALL
    SELECT s.socio FROM cxc2024 c JOIN socios2022 s ON c.socio = s.codigo
    UNION ALL
    SELECT s.socio FROM cxc2025 c JOIN socios2022 s ON c.codigo_cliente = s.codigo
);
"""
socios_result = sq.ejecutar_consulta(socios_query, DB)
socios_list = ['Todos'] + [row[0] for row in socios_result] if socios_result else ['Todos']

#Pestañas donde se visualizaran los resultados
tab1, tab2, tab3 = st.tabs(["Q1. Resumen Caja Mensual", "Q2. Top 10 Egresos", "Q3. Ingresos Por Socio"])

#Configuracion de la Q1 en la pestaña 1
with tab1:
    st.header("Q1. Resumen Caja Mensual")
    with st.form("q1_form"):
        start_date_q1 = st.date_input("Fecha inicio", value=date(2020, 1, 1))
        end_date_q1 = st.date_input("Fecha fin", value=date(2025, 12, 31))
        submit_q1 = st.form_submit_button("Consultar")

    if submit_q1:
        start_str = start_date_q1.strftime('%Y-%m-%d')
        end_str = end_date_q1.strftime('%Y-%m-%d')
        q1_query = f"""
        SELECT strftime('%Y-%m', fecha) AS Año_Mes, SUM(entrada) AS Ingresos, SUM(salida) AS Egresos
        FROM (
            SELECT fecha, entrada, salida FROM caja2020
            UNION ALL
            SELECT fecha, entrada, salida FROM caja2022
            UNION ALL
            SELECT fecha, entrada, salida FROM caja2023
            UNION ALL
            SELECT fecha, entrada, salida FROM caja2024
            UNION ALL
            SELECT fecha, prestamo AS entrada, abono AS salida FROM caja2025
        ) AS cajas
        WHERE fecha BETWEEN '{start_str}' AND '{end_str}'
        GROUP BY Año_Mes
        ORDER BY Año_Mes;
        """
        result_q1 = sq.ejecutar_consulta(q1_query, DB)
        if result_q1:
            df_q1 = pd.DataFrame(result_q1, columns=['Año_Mes', 'Ingresos', 'Egresos'])
            df_q1['Egresos'] = -df_q1['Egresos']
            st.dataframe(df_q1)
            st.bar_chart(df_q1.set_index('Año_Mes'))
        else:
            st.write("No hay resultados para el rango seleccionado.")
    st.write("""
             Esta consulta muestra los totales o sumatoria de los ingresos y egresos de manera mensual, ayudando a identificar patrones estacionales en la caja.
             Analizando la grafica se encontro que hay varios meses dentro del rango de años donde no se registran ingresos ni egresos ademas haciendo una inspeccion
             en la mayoria de los años hay un deficit claro con mayor egreseos que ingresos especialmente en los años 2022 y 2023 si emabrgo se puede ver que el 2024 y 2025
             se ha mejorado con respecto a los primeros años, sin embargo se requiere mejorar en la gestion y control de cuentas para poder tener mayores ingresos y poder cubrir por completo los egresos por año.
             """)



#Configuracion de la Q2 en la Pestaña 2
with tab2:
    st.header("Q2. Top 10 Egresos")
    with st.form("q2_form"):
        start_date_q2 = st.date_input("Fecha inicio", value=date(2020, 1, 1))
        end_date_q2 = st.date_input("Fecha fin", value=date(2025, 12, 31))
        submit_q2 = st.form_submit_button("Consultar")

    if submit_q2:
        start_str = start_date_q2.strftime('%Y-%m-%d')
        end_str = end_date_q2.strftime('%Y-%m-%d')
        q2_query = f"""
        SELECT detalle, SUM(salida) AS total_egresos
        FROM (
            SELECT fecha, detalle, salida FROM caja2020
            UNION ALL
            SELECT fecha, detalle, salida FROM caja2022
            UNION ALL
            SELECT fecha, detalle, salida FROM caja2023
            UNION ALL
            SELECT fecha, detalle, salida FROM caja2024
            UNION ALL
            SELECT fecha, detalle, abono AS salida FROM caja2025
        ) AS cajas
        WHERE fecha BETWEEN '{start_str}' AND '{end_str}'
        GROUP BY detalle
        ORDER BY total_egresos DESC
        LIMIT 10;
        """
        result_q2 = sq.ejecutar_consulta(q2_query, DB)
        if result_q2:
            df_q2 = pd.DataFrame(result_q2, columns=['detalle', 'total_egresos'])
            df_q2['total_egresos'] = -df_q2['total_egresos']
            st.dataframe(df_q2)
            st.bar_chart(df_q2.set_index('detalle'))
        else:
            st.write("No hay resultados para el rango seleccionado.")
    st.write("""
             Esta consulta identifica los principales conceptos de gasto, permitiendo priorizar reducciones y analizar en que se esta gastando mayormente. 
             Revisando los resultados se puede evidenciar que del top 10 hay varios egresos relacionados a pagos de interes y abonos de deuda de varios de los socio 
             ademas se evidencian varios egresos con respecto a pagos de obligaciones con entidades del estado como invima, camara de comercio y otros tramites legales y por ultimo algunas registros con respecto
             a temas el negocio como lo son facturas  de plasticos y agricolas del quindio. Esto evidencia que se necesita una mejora en el manejo de estos mismos debido a que la mayoria de los egresos estan concentrados en 
             pagar intereses y abonos a deudas de los socios y no ha temas relacionados a la produccion y core del negocio.
             """)

#Configuracion de la Q3 en la Pestaña 3
with tab3:
    st.header("Q3. Ingresos Por Socio")
    with st.form("q3_form"):
        start_date_q3 = st.date_input("Fecha inicio", value=date(2020, 1, 1))
        end_date_q3 = st.date_input("Fecha fin", value=date(2025, 12, 31))
        selected_socio = st.selectbox("Socio", options=socios_list)
        submit_q3 = st.form_submit_button("Consultar")

    if submit_q3:
        start_str = start_date_q3.strftime('%Y-%m-%d')
        end_str = end_date_q3.strftime('%Y-%m-%d')
        if selected_socio == 'Todos':
            q3_query = f"""
            SELECT socio, SUM(entrada) AS total_ingresos
            FROM (
                SELECT socio, valor AS entrada, '2020-01-01' AS fecha FROM cxc2020 WHERE socio != 'total'
                UNION ALL
                SELECT s.socio, entrada, fecha FROM cxc2024 c JOIN socios2022 s ON c.socio = s.codigo
                UNION ALL
                SELECT s.socio, entrada, fecha FROM cxc2025 c JOIN socios2022 s ON c.codigo_cliente = s.codigo
            ) AS cxc_unificada
            WHERE fecha BETWEEN '{start_str}' AND '{end_str}'
            GROUP BY socio
            ORDER BY total_ingresos DESC;
            """
            result_q3 = sq.ejecutar_consulta(q3_query, DB)
            if result_q3:
                df_q3 = pd.DataFrame(result_q3, columns=['socio', 'total_ingresos'])
                st.dataframe(df_q3)
                st.bar_chart(df_q3.set_index('socio'))
            else:
                st.write("No hay resultados para el rango seleccionado.")
        else:
            q3_query = f"""
            SELECT socio , SUM(entrada) AS ingresos_mensuales
            FROM (
                SELECT socio, valor AS entrada, '2020-01-01' AS fecha FROM cxc2020 WHERE socio != 'total'
                UNION ALL
                SELECT s.socio, entrada, fecha FROM cxc2024 c JOIN socios2022 s ON c.socio = s.codigo
                UNION ALL
                SELECT s.socio, entrada, fecha FROM cxc2025 c JOIN socios2022 s ON c.codigo_cliente = s.codigo
            ) AS cxc_unificada
            WHERE fecha BETWEEN '{start_str}' AND '{end_str}' AND socio = '{selected_socio}'
            GROUP BY socio
            ORDER BY ingresos_mensuales;
            """
            result_q3 = sq.ejecutar_consulta(q3_query, DB)
            if result_q3:
                df_q3 = pd.DataFrame(result_q3, columns=['socio', 'ingresos_mensuales'])
                st.dataframe(df_q3)
                st.bar_chart(df_q3.set_index('socio'))
            else:
                st.write("No hay resultados para el socio y rango seleccionados.")
    st.write("""
             Esta consulta muestra la concentración de ingresos por socio, facilitando el análisis de contribuciones individuales o grupales.
             Como se puede ver en la grafica la socia con mayores ingresos es Yamile Vera acumula la mayoria de los ingresos junto con Luz Mary y German lopez que tienen 
             Una proporcion menor respecto a esta. Esto nos da cuenta de que los ingresos estan altamente concentrados en un solo socio lo que es preocupante de cara a la
             distribucion de los mismos y quiere decir que se tiene gran dependencia de estos.
             """)



