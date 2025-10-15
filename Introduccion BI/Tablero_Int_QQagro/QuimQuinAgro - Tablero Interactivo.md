QuimQuinAgro - Tablero Interactivo de Consultas Financieras

Descripción del proyecto
Este proyecto es un tablero interactivo desarrollado en Streamlit para la Asociación de Piscicultores QuimQuinAgro. Permite consultar y visualizar información financiera de la base de datos contabilidad.db, incluyendo totales mensuales de caja, top 10 egresos y ingresos por socio, utilizando consultas SQL fijas con filtros interactivos controlados (fechas y selección de socio).
El código fuente está disponible en GitHub: https://github.com/RR77ui/Business-Intelligence/tree/main/Introduccion%20BI/Tablero_Int_QQagro.

Requisitos
Tener instalado python
Tener todos los archivos del repositorio en una misma carpeta

Instala las dependencias esde tu terminal:
pip install streamlit 

Cómo Ejecutar la Aplicación :
Opción 1
Asegúrate de que contabilidad.db y SQLib.py estén en el mismo directorio que app.py (o el nombre de tu archivo principal).
Ejecuta la app con Streamlit desde tu terminal:
python -m streamlit run nombre del archivo.py
La app se abrirá automáticamente en tu navegador

Opción 2
Descargar todos los archivos y correrlo desde anaconda prompt(OPCION RECOMENDADA)
Descargar anaconda desde la pagina web oficial https://www.anaconda.com/download/success
abrir anaconda prompt 
cd ruta de la carpeta donde guardaste el archivo app.py 
streamlit run nombre del archivo.py (Si guardaste el archivo con el mismo nombre del GitHub es app.py)
La app se abrirá automáticamente en tu navegador

Instrucciones de Uso
El tablero se divide en tres pestañas, cada una correspondiente a una consulta fija. Usa los formularios en cada pestaña para filtrar datos. No hay entradas de texto libre; solo selecciona fechas o opciones de listas desplegables. Presiona "Consultar" para ver resultados en tablas y gráficos.
Pestaña Q1: Resumen Caja Mensual

Descripción: Muestra totales de ingresos y egresos por mes en un rango de fechas seleccionado.
Filtros:

Fecha de inicio (predeterminado: 2020-01-01).
Fecha de fin (predeterminado: 2025-12-31). 
En esta sección podrás seleccionar las fechas que quieres analizar

Visualización: Gráfico de barras agrupadas (ingresos arriba, egresos abajo como barras negativas).
Uso:

Selecciona el rango de fechas.
Presiona "Consultar" y visualizaras el grafico y tabla con los valores de las fechas seleccionadas.
 

Pestaña Q2: Top 10 Egresos

Descripción: Identifica los 10 conceptos con mayores egresos en caja, en un rango de fechas.
Filtros:

Fecha de inicio (predeterminado: 2020-01-01).
Fecha de fin (predeterminado: 2025-12-31).


Visualización: Tabla interactiva y gráfico de barras descendentes (egresos como valores negativos para dirección descendente).
Uso:

Selecciona el rango de fechas.
Presiona "Consultar" y visualiza el grafico con los valores de las fechas seleccionadas.




[Inserte captura de pantalla de Q2 aquí, mostrando el formulario, tabla y gráfico. Ejemplo: <img src="capturas/q2_ejemplo.png" alt="Captura Q2">]
Pestaña Q3: Ingresos Por Socio

Descripción: Muestra ingresos por socio (concentración total o temporal por mes).
Filtros:

Fecha de inicio (predeterminado: 2020-01-01).
Fecha de fin (predeterminado: 2025-12-31).
Socio ("Todos" o lista de socios únicos de las tablas CXC).


Visualización:

Si "Todos": Tabla y barras por socio.
Si socio específico: Tabla y grafico de barra socio especifico.


Uso:

Selecciona el rango de fechas y el socio (o "Todos").
Presiona "Consultar" Revisa la tabla y gráfico para análisis de contribuciones.


Notas adicionales al usuario:
Si no hay datos para el filtro seleccionado, se muestra un mensaje de "No hay resultados".
Las conclusiones de cada consulta se muestran al final de cada pestaña.

Contribuciones
Si deseas contribuir, descarga el código fuente de GitHub y moldéalo a tu gusto


