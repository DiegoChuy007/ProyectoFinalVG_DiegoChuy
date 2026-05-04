import pandas as pd
import plotly.express as px

# Importamos tus funciones de limpieza
from limpiezaBasesDatos import (
    limpiar_lesiones, 
    unificar_excel_posiciones, 
    generar_tabla_carga_fisica, 
    generar_costo_deportivo
)

print("1. Cargando y limpiando millones de datos (esto tomará unos segundos)...")
df_lesiones = limpiar_lesiones('Datasets/Dataset_lesiones_ligas.csv')
df_posiciones = unificar_excel_posiciones('Datasets')
df_carga = generar_tabla_carga_fisica('Datasets/baseDatos_Transfermark')
df_costo = generar_costo_deportivo(df_lesiones, df_posiciones)

# Diccionario con las claves exactas que pusimos en los botones de Unity
ligas_diccionario = {
    "todas": ['premier-league', 'laliga', 'serie-a'],
    "premier": ['premier-league'],
    "laliga": ['laliga'],
    "seriea": ['serie-a']
}

print("2. Generando y tomando las 'fotos' de las gráficas...")

for clave_liga, valores_liga in ligas_diccionario.items():
    print(f"--- Exportando gráficas para: {clave_liga} ---")

    # ==========================================
    # ACTO 1: CARGA FÍSICA (Gráfico de Barras)
    # ==========================================
    df_carga['torneo_temp'] = df_carga['Liga/Torneo'].astype(str).str.lower()
    df_carga_filtrada = df_carga[df_carga['torneo_temp'].isin(valores_liga)]
    carga_por_temporada = df_carga_filtrada.groupby(['Temporada', 'Tipo_Competicion'])['Minutos_Totales'].sum().reset_index()

    fig_carga = px.bar(
        carga_por_temporada,
        x='Temporada',
        y='Minutos_Totales',
        color='Tipo_Competicion',
        title=f"Evolución de minutos jugados",
        color_discrete_sequence=['#1e293b', '#10b981', '#3b82f6', '#94a3b8']
    )
    fig_carga.write_image(f"carga_{clave_liga}.png", width=800, height=450)


    # ==========================================
    # ACTO 2: EL QUIEBRE (Mapa de Calor)
    # ==========================================
    # Corrección: Filtros exactos idénticos a tu app.py
    if clave_liga == "todas":
        texto_filtro_lesiones = 'Premier|LaLiga|La Liga|Serie A'
    elif clave_liga == "premier":
        texto_filtro_lesiones = 'Premier'
    elif clave_liga == "laliga":
        texto_filtro_lesiones = 'LaLiga|La Liga'
    elif clave_liga == "seriea":
        texto_filtro_lesiones = 'Serie A'

    filtro_les = df_lesiones['league'].str.contains(texto_filtro_lesiones, case=False, na=False)
    df_les_filtrado = df_lesiones[filtro_les].copy()

    df_les_filtrado['Mes'] = df_les_filtrado['injury_from_parsed'].dt.month
    nombres_meses = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
    df_les_filtrado['Mes_Nombre'] = df_les_filtrado['Mes'].map(nombres_meses)

    lesiones_heatmap = df_les_filtrado.groupby(['Season', 'Mes_Nombre']).size().reset_index(name='Cantidad')

    if not lesiones_heatmap.empty:
        matriz = lesiones_heatmap.pivot(index='Season', columns='Mes_Nombre', values='Cantidad').fillna(0)
        fig_quiebre = px.imshow(
            matriz, 
            aspect="auto", 
            title=f"Densidad de lesiones por mes",
            color_continuous_scale=['#f8fafc', '#6ee7b7', '#10b981', '#1e3a8a', '#020617']
        )
        fig_quiebre.write_image(f"quiebre_{clave_liga}.png", width=800, height=450)


    # ==========================================
    # ACTO 3: COSTO DEPORTIVO (Dispersión/Scatter)
    # ==========================================
    texto_filtro_costo = 'Premier League' if clave_liga == 'premier' else 'LaLiga' if clave_liga == 'laliga' else 'Serie A' if clave_liga == 'seriea' else ''
    df_costo_filtrado = df_costo[df_costo['Liga'] == texto_filtro_costo] if texto_filtro_costo else df_costo

    fig_costo = px.scatter(
        df_costo_filtrado,
        x='Dias_Perdidos_Totales',
        y='Posicion_Final',
        color='Liga' if clave_liga == 'todas' else 'Equipo',
        title=f"Lesiones vs Posición",
        range_y=[20.5, 0.5],
        color_discrete_sequence=['#0f172a', '#10b981', '#2563eb', '#38bdf8', '#64748b', '#34d399']
    )
    fig_costo.write_image(f"costo_{clave_liga}.png", width=800, height=450)

print("¡Listo! Revisa la carpeta, ahora sí deben ser 12 imágenes exactas.")