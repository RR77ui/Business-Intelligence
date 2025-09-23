# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 12:06:31 2025

@author: Juan Esteban
"""

#Cargamos las librerias
import streamlit as st #Libreria para prototipado de la app
import pandas as pd #Libreria para el manejo de dataframes
import sqlite3 #Framework de sql
import plotly.express as px #Para graficos dinamicos

DB_PATH = "contabilidad.db" #Ruta Base de datos

#Configurar la pagina de la app
st.set_page_config(page_title = "Informacion Financiera QuimQuinAgro", layout = "wide")

#Configuramos el titulo principal
st.title("Consultas Info Financiera")

#Declaramos la funcion que nos permitira realizar las consultas en sql.La funcion se llama 
def ejecutar_sql(consulta):
    conn = sqlite3.connect(DB_PATH) #Conexion con la base de datos 
    resultado = pd.read_sql_query(consulta, conn) #En resultado vamos a almacenar la respuesta a la consulta realizada y almacenada en consulta
    conn.close() #Por seguridad despues de realizar la consulta cierre la conexion
    return resultado #Retorno resultado (salida dela funcion)

#Posibles elecciones del usuario en la app, eleccion sera un diccionario
eleccion = {
    "¿Cuál es el total de las cuentas por pagar (CXP) que la asociación tiene con cada socio en el año 2022?":
        "SELECT socio, SUM(valor) AS total_deuda_2022 FROM cxp2022 WHERE socio!='' GROUP BY socio ORDER BY total_deuda_2022;",
    "movimientos mas recientes registrados en el estado de resultados 2025":
        "SELECT fecha,categoria,detalle,entrada,salida FROM edr2025 WHERE fecha >= '2025-01-01' ORDER BY fecha DESC, entrada DESC;",
    "Registros de 2023 donde hubo pérdida (gastos mayores que ingresos)":
        "SELECT fecha,detalle,entrada,salida,saldo FROM caja2023 WHERE saldo > 0 ORDER BY fecha;",
    "el total de dinero que la asociación tiene por cobrar a cada socio en 2024.":
        "SELECT socio, SUM(entrada) AS total_por_cobrar FROM cxc2024 GROUP BY socio ORDER BY total_por_cobrar DESC;",
    "¿Cuál es el balance total de préstamos y abonos de los cliente en el año 2025?":
        "SELECT codigo_cliente,SUM(prestamo) AS total_prestado,SUM(abono) AS total_abonado,SUM(prestamo) - SUM(abono) AS saldo_neto FROM cxp2025 GROUP BY codigo_cliente HAVING saldo_neto > 0 ORDER BY saldo_neto DESC;",
    "Top 5 de Socios con Mayor Deuda (Cuentas por Cobrar) en 2024":
        "SELECT socio, SUM(salida) AS total_deuda_2024 FROM cxc2024 GROUP BY socio ORDER BY total_deuda_2024 DESC LIMIT 5;"
            }

# Configuramos panel al lado izquierdo con las opciones de consulta
st.sidebar.header("Opciones")
#Configuramos un select box con las opciones de usuario
opcion=st.sidebar.selectbox("Elige una opción", list(eleccion.keys()))
sql = eleccion[opcion]

#Configuramos el boton para ejecutar la consulta
if st.sidebar.button("Buscar"):
    resultado = ejecutar_sql(sql)
    
    # Vizualizamos la informacion
    st.dataframe(resultado, use_container_width=True)
    st.markdown("---")
    st.subheader("Conclusión de la Consulta")

    # Creamos un condicional para que cuando el usuario seleccione cada una de as consultas del diccionario le aparezca su respectiva conclusion
    if opcion == "¿Cuál es el total de las cuentas por pagar (CXP) que la asociación tiene con cada socio en el año 2022?":
        st.write("Esta tabla identifica las deudas de la asociación con sus socios en 2022. El resultado muestra que la asociación tiene una deuda total de 2,300,000 con María Piedad Horta, la más alta de todas. Este tipo de análisis es fundamental para la gestión de la liquidez, ya que permite a la asociación planificar los pagos, priorizar las deudas más grandes y mantener una relación transparente con sus socios. El resultado evidencia la importancia de un registro contable preciso para la toma de decisiones financieras")
    
    elif opcion == "movimientos mas recientes registrados en el estado de resultados 2025":
        st.write("1. Dinámica del Flujo de Caja:Los registros muestran un ciclo de operación y reinversión. La venta de pescado (INGRESOS OPERACIONALES) por $1,500,000 genera los fondos necesarios para la compra de concentrado, un insumo esencial para la producción. Esta relación directa entre ingresos y gastos operacionales es un indicador clave de la salud del negocio. Por ejemplo, se observa que la venta del 24 de enero precede a un gasto de concentrado el 28 de enero. Un seguimiento más riguroso podría evaluar si el volumen de ventas justifica los costos de insumos y si hay oportunidades para negociar mejores precios con proveedores.2. Eficiencia Operacional y Rentabilidad:Los registros muestran que las entradas operacionales (venta de pescado) son significativamente mayores que las salidas operacionales (compra de concentrado). Esta diferencia, si se mantiene, indica una rentabilidad positiva en la operación principal de la asociación. Los gerentes pueden usar esta información para proyectar la rentabilidad futura y asignar recursos a áreas que impulsen aún más los ingresos operacionales, como expandir la capacidad de producción o invertir en tecnología de acuicultura.3. Evaluación de Gastos No Operacionales:El gasto de $250,000 en el MANTENIMIENTO TANKES clasificado como GASTOS NO OPERACIONALES resalta la necesidad de considerar los gastos imprevistos. Aunque estos gastos no están directamente relacionados con la producción diaria, son esenciales para el buen funcionamiento de la infraestructura. La gerencia debe evaluar la frecuencia y el costo de estos gastos no operacionales. Un plan de mantenimiento preventivo podría ayudar a reducir estos costos a largo plazo y evitar interrupciones en la producción.4. Oportunidades de Venta Adicionales:La VENTA DE CONCENTRADO por $800,000, categorizada como INGRESOS NO OPERACIONALES, sugiere una posible oportunidad de negocio. Vender insumos a otros productores podría diversificar las fuentes de ingresos de la asociación. Los líderes de la asociación podrían analizar si esta actividad es rentable y si justifica una inversión en la compra de concentrado a granel para su posterior reventa.")
    
    elif opcion == "Registros de 2023 donde hubo pérdida (gastos mayores que ingresos)":
        st.write(" la Toma de Decisiones:Identificación de los Gastos Recurrentes: Los registros del 26 de enero de 2023 muestran que la nómina y los servicios públicos (gas y agua) son los gastos que más contribuyen al saldo negativo. Esto sugiere que el flujo de efectivo del mes de enero fue insuficiente para cubrir los costos operativos esenciales. Para mitigar esto, se deben explorar opciones como la optimización de los costos de servicios o la revisión de la estructura de nómina, quizás ajustando los pagos a los ingresos generados.Impacto de los Reembolsos: Los reembolsos de préstamos en febrero también contribuyen a un saldo negativo. Aunque estos gastos son necesarios para honrar las obligaciones, la gerencia debe evaluar la capacidad de la caja para manejar estos pagos. Si la asociación no puede cubrir los reembolsos con sus ingresos actuales, podría ser necesario renegociar las condiciones de los préstamos o buscar fuentes de financiación a corto plazo para evitar un problema de liquidez.Gestión del Flujo de Caja: El hecho de que todos los saldos mostrados sean negativos es una señal de alarma. Una estrategia administrativa debe centrarse en la gestión proactiva del flujo de caja. Esto incluye:Proyección de Ingresos y Gastos: Anticipar cuándo se esperan los ingresos principales (por ejemplo, ventas de pescado) y programar los pagos de gastos grandes (como la nómina o el mantenimiento) para que coincidan con esas entradas de dinero.Políticas de Crédito y Cobro: Si el saldo negativo se debe a que los clientes no pagan a tiempo, es crucial endurecer las políticas de cobro para asegurar que el dinero entre en la caja de manera oportuna.En resumen, este análisis resalta la necesidad de una planificación financiera más rigurosa. La asociación debe enfocarse en aumentar sus ingresos, reducir sus gastos operativos y gestionar los pagos de manera estratégica para evitar que los gastos superen a los ingresos, lo cual es vital para su sostenibilidad a largo plazo.")

    elif opcion == "el total de dinero que la asociación tiene por cobrar a cada socio en 2024.":
        st.write("En 2024, la asociación tiene dos socios deudores, siendo el socio 9 el más crítico con más de $5,5 millones pendientes, frente a $480.000 del socio 8.La gestión de cobro debe enfocarse principalmente en el socio 9 para evitar problemas de liquidez, mientras que al socio 8 conviene darle seguimiento para que no aumente su saldo pendiente.")
    
    elif opcion == "¿Cuál es el balance total de préstamos y abonos de los cliente en el año 2025?":
        st.write("En 2025, el único cliente registrado (código 5) concentra un préstamo de $1.000.000 sin ningún abono. Esto implica que la exposición al riesgo está en un solo cliente y que la asociación debe dar seguimiento prioritario a este caso para evitar problemas de recuperación de cartera")

    elif opcion == "Top 5 de Socios con Mayor Deuda (Cuentas por Cobrar) en 2024":
        st.write("Socio 9 → tiene una deuda pendiente de $3.500.000 en 2024.Socio 8 → aparece con deuda $0, es decir, no registra cuentas por cobrar pendientes en ese año.Solo se listaron 2 socios (aunque el enunciado decía Top 5), lo cual indica que en la base de datos solo hay 2 con registros de deuda en 2024.Concentración del riesgo de cartera:Toda la deuda en 2024 está altamente concentrada en un solo socio (socio 9). Esto representa un riesgo financiero para la asociación, porque depende de que ese único socio pague.Situación del socio 8:Aunque aparece en el ranking, su deuda es cero → lo que sugiere que está al día en pagos, o no tuvo transacciones de cuentas por cobrar ese año.Debilidad en la diversificación:Que solo un socio concentre deudas es un punto de alerta. En términos de gestión de cartera, sería recomendable monitorear la capacidad de pago de ese socio.Oportunidad para decisiones estratégicas:La asociación podría implementar políticas de crédito más estrictas con el socio 9.También conviene incentivar la diversificación de ventas a otros socios/clientes para reducir la dependencia.")
