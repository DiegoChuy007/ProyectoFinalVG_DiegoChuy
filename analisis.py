import pandas as pd
from limpiezaBasesDatos import (
    limpiar_lesiones, 
    unificar_excel_posiciones, 
    generar_tabla_carga_fisica, 
    generar_costo_deportivo
)

def ejecutar_analisis(df, nombre_tabla):
    print(f"\n\n{'='*60}")
    print(f" Análisis de la tabla: {nombre_tabla.upper()}")
    print(f"{'='*60}")
    #Información General
    print("\n Información general (.info())")
    print("-" * 30)
    df.info()
    #Valores Nulos
    print("\n Valores nulos por columna (isnull().sum())")
    print("-" * 30)
    nulos = df.isnull().sum()
    print(nulos[nulos > 0] if nulos.sum() > 0 else "¡Todo limpio! No hay valores nulos.")
    #Resumen Estadístico
    print("\n Resumen estadístico (.describe())")
    print("-" * 30)
    #include='all' para que también nos dé info de las columnas de texto (cuántas ligas únicas, etc.)
    print(df.describe(include='all').fillna('-')) 

#EJECUCIÓN
#Definimos las rutas
ruta_lesiones = 'Datasets/Dataset_lesiones_ligas.csv'
ruta_posiciones = 'Datasets'
ruta_transfermarkt = 'Datasets/baseDatos_Transfermark'
#Generamos los 4 DataFrames usando las propias funciones
df_lesiones = limpiar_lesiones(ruta_lesiones)
df_posiciones = unificar_excel_posiciones(ruta_posiciones)
df_carga = generar_tabla_carga_fisica(ruta_transfermarkt)
#Hacemos el cruce final solo si las tablas base cargaron bien
if not df_lesiones.empty and not df_posiciones.empty:
    df_costo = generar_costo_deportivo(df_lesiones, df_posiciones)
else:
    df_costo = pd.DataFrame()
#Mandamos a analizar las 4 tablas
ejecutar_analisis(df_lesiones, "Lesiones (Hospital)")
ejecutar_analisis(df_posiciones, "Posiciones (Clasificación)")
ejecutar_analisis(df_carga, "Carga Física (Desgaste)")
if not df_costo.empty:
    ejecutar_analisis(df_costo, "Costo Deportivo (Impacto)")
else:
    print("\n No se pudo analizar el costo deportivo porque la tabla está vacía.")