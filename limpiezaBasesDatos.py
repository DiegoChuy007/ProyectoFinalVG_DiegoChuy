import pandas as pd
import os

#DATASET LESIONES
def limpiar_lesiones(ruta_archivo):
    #Leer el archivo
    df = pd.read_csv(ruta_archivo)
    #Limpiar la columna 'Days' (quitar texto y convertir a entero)
    df['Days'] = df['Days'].astype(str).str.replace(' days', '', regex=False)
    df['Days'] = df['Days'].str.replace(' day', '', regex=False)
    df['Days'] = pd.to_numeric(df['Days'], errors='coerce').fillna(0).astype(int)
    #Formatear las columnas de fechas
    df['injury_from_parsed'] = pd.to_datetime(df['injury_from_parsed'], errors='coerce')
    df['injury_until_parsed'] = pd.to_datetime(df['injury_until_parsed'], errors='coerce')
    #Estandarizar la columna 'Season' ("20/21" = "2020-2021")
    def estandarizar_temporada(season_str):
        if pd.isna(season_str):
            return season_str
        season_str = str(season_str).strip()
        if '/' in season_str:
            partes = season_str.split('/')
            # Solo aplica si tiene exactamente dos partes numéricas cortas
            if len(partes) == 2 and len(partes[0]) == 2 and len(partes[1]) == 2:
                return f"20{partes[0]}-20{partes[1]}"
        return season_str
    df['Season'] = df['Season'].apply(estandarizar_temporada)
    # 5. Filtrar para la narrativa: Enfocarnos en lesiones musculares/fatiga
    # (Descomenta la siguiente línea si quieres enfocar la app solo en ese tipo de lesiones)
    # df = df[df['Injury'].str.contains('Muscle|Hamstring|Tear|Strain', case=False, na=False)]
    return df
#Prueba rápida para ver si funciona
if __name__ == "__main__":
    df_lesiones_limpio = limpiar_lesiones('Datasets/Dataset_lesiones_ligas.csv')
    print("Muestra de las lesiones limpias:")
    print(df_lesiones_limpio[['player_name', 'Season', 'Injury', 'Days','club','league']].head())

#DATASET POSICIONES
def unificar_excel_posiciones(ruta_carpeta):
    #Definimos los nombres exactos de tus 3 archivos Excel
    archivos_excel = ['premier.xlsx', 'laLiga.xlsx', 'serieA.xlsx']
    lista_tablas = []
    for archivo in archivos_excel:
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        #Sacamos el nombre de la liga quitando el ".xlsx"
        liga = archivo.replace('.xlsx', '') 
        #sheet_name=None lee TODAS las pestañas a la vez
        #Esto crea un diccionario donde la llave es el nombre de la pestaña (ej. "2020-2021")
        try:
            todas_las_temporadas = pd.read_excel(ruta_completa, sheet_name=None)
            for nombre_pestaña, df_pestaña in todas_las_temporadas.items():
                # Agregamos las columnas clave que necesitas
                df_pestaña['League'] = liga
                df_pestaña['Season'] = str(nombre_pestaña).strip()
                lista_tablas.append(df_pestaña)
        except FileNotFoundError:
            print(f"No se encontró el archivo: {ruta_completa}")
    #Pegamos todas las pestañas de todas las ligas en una sola tabla gigante
    if lista_tablas:
        df_final = pd.concat(lista_tablas, ignore_index=True)
        #Filtramos SOLO las columnas que te importan: Temporada, Equipo y Posición
        #Nota: Asumo que en FBref la posición viene como 'Rk' y el equipo como 'Squad'
        columnas_deseadas = ['Season', 'League', 'Rk', 'Squad']
        # Esta línea asegura que no marque error si una columna se llama distinto
        columnas_existentes = [col for col in columnas_deseadas if col in df_final.columns]
        return df_final[columnas_existentes]
    else:
        return pd.DataFrame()
#Prueba del código
if __name__ == "__main__":
    df_posiciones_limpio = unificar_excel_posiciones('Datasets')
    print("--- MUESTRA DE TABLA DE POSICIONES UNIFICADA ---")
    print(df_posiciones_limpio.head(10))

#DATASET minutos
def generar_tabla_carga_fisica(ruta_data):
    """
    Une los 5 archivos de Transfermarkt para obtener los minutos totales
    por jugador, temporada y tipo de competencia.
    """
    print("Cargando y procesando minutos (esto puede tardar con los archivos originales)...")
    #Cargar Archivos (Usando solo las columnas necesarias para ahorrar RAM)
    #Nota: Asegúrate de que los nombres coincidan con tus archivos .csv reales
    df_app = pd.read_csv(f'{ruta_data}/appearances.csv', usecols=['player_id', 'game_id', 'minutes_played', 'player_name'])
    df_games = pd.read_csv(f'{ruta_data}/games.csv', usecols=['game_id', 'competition_id', 'season'])
    df_players = pd.read_csv(f'{ruta_data}/players.csv', usecols=['player_id', 'current_club_id'])
    df_clubs = pd.read_csv(f'{ruta_data}/clubs.csv', usecols=['club_id', 'name', 'domestic_competition_id'])
    df_comp = pd.read_csv(f'{ruta_data}/competitions.csv', usecols=['competition_id', 'type', 'name'])
    #Renombrar columnas para evitar confusiones
    df_clubs = df_clubs.rename(columns={'name': 'club_name'})
    df_comp = df_comp.rename(columns={'name': 'competition_name', 'type': 'comp_type'})
    #El Gran Cruce (Pipeline de Merges)
    #A) Unir apariciones con juegos para tener la Temporada y el ID de competencia
    df_unido = pd.merge(df_app, df_games, on='game_id', how='left')
    #B) Unir con competiciones para saber si es Liga, Copa o Selección
    df_unido = pd.merge(df_unido, df_comp, on='competition_id', how='left')
    #C) Unir con jugadores para obtener su club actual
    df_unido = pd.merge(df_unido, df_players, on='player_id', how='left')
    # D) Unir con clubs para tener el nombre del equipo
    df_unido = pd.merge(df_unido, df_clubs, left_on='current_club_id', right_on='club_id', how='left')
    #Agrupación y Limpieza Final
    #Sumamos los minutos por la combinación que definimos
    tabla_carga = df_unido.groupby(
        ['player_name', 'club_name', 'competition_name', 'season', 'comp_type']
    )['minutes_played'].sum().reset_index()
    #Renombrar para que sea amigable con Streamlit
    tabla_carga.columns = ['Jugador', 'Club', 'Liga/Torneo', 'Temporada', 'Tipo_Competicion', 'Minutos_Totales']
    #Estandarizar temporada a string (ej. "2022")
    tabla_carga['Temporada'] = tabla_carga['Temporada'].astype(str)
    print("Tabla de Carga Física generada con éxito.")
    return tabla_carga

# --- PRUEBA DEL CÓDIGO ---
if __name__ == "__main__":
    # Cambia 'Datasets' por la carpeta donde tengas tus archivos reales
    ruta = 'Datasets/baseDatos_Transfermark' 
    df_carga = generar_tabla_carga_fisica(ruta)
    
    print("\nPrimeras filas de la tabla unificada:")
    print(df_carga.head())
    
    # Verificamos qué tipos de competencia hay (esto servirá para tus filtros en Streamlit)
    print("\nTipos de competencia encontrados:")
    print(df_carga['Tipo_Competicion'].unique())

    # --- DATASET COSTO DEPORTIVO (Gráfica 3) ---
# --- DATASET COSTO DEPORTIVO (Gráfica 3) ---
def generar_costo_deportivo(df_lesiones, df_posiciones):
    print("Generando tabla de Costo Deportivo...")
    
    # 1. Sumar todos los días de baja médica por equipo y temporada
    df_dias_perdidos = df_lesiones.groupby(['club', 'Season'])['Days'].sum().reset_index()

    # --- EL FILTRO "QUITA-ESPACIOS" ---
    # Esto elimina cualquier espacio en blanco invisible al inicio o final
    df_dias_perdidos['Season'] = df_dias_perdidos['Season'].astype(str).str.strip()
    df_posiciones['Season'] = df_posiciones['Season'].astype(str).str.strip()
    df_dias_perdidos['club'] = df_dias_perdidos['club'].astype(str).str.strip()
    df_posiciones['Squad'] = df_posiciones['Squad'].astype(str).str.strip()

    # --- BLOQUE DE DIAGNÓSTICO (Para ver qué está fallando) ---
    print("\n[DIAGNÓSTICO] Temporadas en Lesiones:", df_dias_perdidos['Season'].unique())
    print("[DIAGNÓSTICO] Temporadas en Posiciones:", df_posiciones['Season'].unique())
    print("\n[DIAGNÓSTICO] Equipos en Lesiones (Ejemplo):", df_dias_perdidos['club'].head(3).tolist())
    print("[DIAGNÓSTICO] Equipos en Posiciones (Ejemplo):", df_posiciones['Squad'].head(3).tolist())
    print("-" * 50)

    # 2. Diccionario de corrección de nombres
    diccionario_equipos = {
        'Manchester Utd': 'Manchester United',
        'Nott\'ham Forest': 'Nottingham Forest',
        'Newcastle Utd': 'Newcastle United',
        'Sheffield Utd': 'Sheffield United',
        'Alavés': 'Deportivo Alavés',
        'Cádiz': 'Cádiz CF'
    }
    df_posiciones['Squad'] = df_posiciones['Squad'].replace(diccionario_equipos)

    # 3. El Gran Cruce (Merge)
    df_costo = pd.merge(
        df_dias_perdidos, 
        df_posiciones, 
        left_on=['club', 'Season'], 
        right_on=['Squad', 'Season'], 
        how='inner' 
    )

    # 4. Limpieza final si el cruce funcionó
    if not df_costo.empty:
        df_costo = df_costo[['Season', 'League', 'Squad', 'Days', 'Rk']]
        df_costo.columns = ['Temporada', 'Liga', 'Equipo', 'Dias_Perdidos_Totales', 'Posicion_Final']
        print("✅ Tabla de Costo Deportivo generada con éxito.")
    else:
        print("⚠️ ALERTA: El Merge sigue vacío. Revisa el diagnóstico de arriba.")

    return df_costo

# --- PRUEBA FINAL DEL CÓDIGO ---
if __name__ == "__main__":
    # Generamos las dos tablas base que necesitamos
    lesiones_limpias = limpiar_lesiones('Datasets/Dataset_lesiones_ligas.csv')
    posiciones_limpias = unificar_excel_posiciones('Datasets')
    
    # Probamos nuestra nueva función
    if not posiciones_limpias.empty and not lesiones_limpias.empty:
        df_impacto = generar_costo_deportivo(lesiones_limpias, posiciones_limpias)
        print("\n--- MUESTRA DEL COSTO DEPORTIVO ---")
        # Mostrar los equipos con más días perdidos y su posición
        print(df_impacto.sort_values(by='Dias_Perdidos_Totales', ascending=False).head(10))