# -*- coding: utf-8 -*-
"""
SQLib sirve como soporte a las principales funciones de SQlite3 sobre python
para futuras actualizaciones, comunicarse a jeraver@eafit.edu.co
"""

import pandas as pd
import sqlite3
import os

def archivo_a_sql(ruta_archivo, nombre_db):
    """
    Convierte archivo de excel o csv con todas sus hojas 
    en una base de datos con sus respectivas tablas

    Parameters
    ----------
    ruta_archivo : string(str), ruta al archivo que se desea convertir 
    en base de datos
    nombre_db : string(str), nombre de la base de datos que almacenara la informacion
    transformada


    Returns
    -------
    archivo.db (db) con la base de datos en formato sqlite3
    """
    try:
        #conectamos a la base de datos
        #creamos un conector llamado conn
        conn = sqlite3.connect(nombre_db)
        #Generamos un cursor que es un puente a la conexion
        cursor = conn.cursor()
        
        #Revisamos la extension del archivo del usuario
        extension = os.path.splitext(ruta_archivo)[1].lower()
        
        if extension in ['.xslx','.xls']:
            #procesamos el archivo en excel
            #almacenamos en la variable xls los datos del achivo 
            xls = pd.ExcelFile(ruta_archivo)
            #Hacemos un ciclo que recorra cada hoja de calculo
            for sheet_name in xls.sheet_names:
                # Almacenamos el contenido de cada hoja de calculo en la varible df
                df = pd.read_excel(ruta_archivo,sheet_name = sheet_name)
                #Guardamos el nombre de la hoja de calculo para convertirlo en
                #el nombre de la tabla
                table_name = sheet_name.strip().replace(' ', '_').replace('-','_')
                # Llevamos el contenido de df  la tabla de sql
                df.to_sql(table_name, conn, if_exists = 'replace',index = False)
                print(f"Hoja '{sheet_name}' importada con exito")
        
        elif extension == '.csv':
            #procesamos el archivo CSV
            #llevamos el contenido del archivo a la variable df
            df = pd.read_csv(ruta_archivo)
            #generamos el nombre de la tabla
            table_name = os.path.splitext(os.path.basename(ruta_archivo))[0].replace(' ', '_').replace('-','_')
            # Llevamos el contenido de df a la tabla de sql
            df.to_sql(table_name,conn,if_exists='replace', index = False)
            print(f"La tabla '{table_name} fue importada con exito")
            
        else:
            print("El formato de archivo no es compatible")
    except:
        print("Error durante la conversion")
        
    finally:
        #Cerramos la conexion de la base de datos
        conn.close()
        print("Conexion cerrada")
        

def ejecutar_consulta(consulta_sql, nombre_db):
    """
    ejecuta una consulta sql sobre una base de datos SQLite3

    Parameters
    ----------
    consulta_sql : string(str) consulta que se quiere ejecutar.
    nombre_db : string(str) nombre de la base de datos SQLite3
        DESCRIPTION.

    Returns
    -------
    resultado_consulta: string, dataframe como resultado de la consulta
    """
    
    try:
        # Conectamos con la base de datos
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()
        
        #ejecutamos la consulta ingresada por el usuario
        cursor.execute(consulta_sql)
        
        #Verificamos si es una consulta tipo select
        if consulta_sql.strip().lower().startswith('select'):
            resultado_consulta = cursor.fetchall()
            return resultado_consulta
        else:
            # confirmamos los cambios parq INSERT, UPDATE, DELETE
            conn.commit()
            return None
    except:
        print("Error en la ejecucion")
        return None
    finally:
        # Cerramos la conexion
        conn.close()
        print("Conexion cerrada")
        

def mostrar_tablas(nombre_db):
    """
    Muestra todas las tablas de la base de datos nombre_db

    Parameters
    ----------
    nombre_db : string(str) nombre de la base de datos

    Returns
           : list lista con los nombres de las tablas de la base de datos
    """
    try:
      # Establecemos la conexion con la base de datos
      conn = sqlite3.connect(nombre_db)
      cursor = conn.cursor()
      
      #Ejecutamos una consulta
      cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
      tablas = cursor.fetchall()
      #Retornamos la lista
      return [tabla[0]for tabla in tablas]
      
    except:
         print("Error en la consulta de las tablas")
         
    finally:
        conn.close()
        print("Conexion finalizada")