import pandas as pd
#Importamos las funciones
from limpiezaBasesDatos import limpiar_lesiones, unificar_excel_posiciones

def auditar_nombres():
    #Cargamos las bases usando las propias funciones
    df_lesiones = limpiar_lesiones('Datasets/Dataset_lesiones_ligas.csv')
    df_posiciones = unificar_excel_posiciones('Datasets')
    #Replicamos el "quita espacios"
    df_lesiones['club'] = df_lesiones['club'].astype(str).str.strip()
    df_posiciones['Squad'] = df_posiciones['Squad'].astype(str).str.strip()
    #Aplicamos tu diccionario actual para ver qué falta
    diccionario_equipos = {
        'Manchester Utd': 'Manchester United',
        'Nott\'ham Forest': 'Nottingham Forest',
        'Newcastle Utd': 'Newcastle United',
        'Sheffield Utd': 'Sheffield United',
        'Atlético Madrid': 'Atletico Madrid',
        'Leganés': 'Leganes',
        'Almería': 'Almeria',
        'Athletic Club': 'Athletic Bilbao',
        'Cádiz CF': 'Cadiz',
        'Cádiz': 'Cadiz',
        'Deportivo Alavés': 'Deportivo Alaves',
        'Alavés': 'Deportivo Alaves',
        'Milan': 'AC Milan'
    }
    df_posiciones['Squad'] = df_posiciones['Squad'].replace(diccionario_equipos)
    #Conjuntos (Sets) para encontrar las diferencias
    equipos_posiciones = set(df_posiciones['Squad'].unique())
    equipos_lesiones = set(df_lesiones['club'].unique())
    huerfanos_posiciones = equipos_posiciones - equipos_lesiones
    huerfanos_lesiones = equipos_lesiones - equipos_posiciones
    #Imprimimos los resultados
    print("\n" + "="*80)
    print("[DIAGNÓSTICO] Equipos en Posiciones que NO cruzaron:")
    print(huerfanos_posiciones if huerfanos_posiciones else "¡Todos cruzaron perfectamente!")
    print("\n[DIAGNÓSTICO] Equipos en Lesiones que NO cruzaron:")
    print(huerfanos_lesiones if huerfanos_lesiones else "¡Todos cruzaron perfectamente!")
    print("="*80)

auditar_nombres()