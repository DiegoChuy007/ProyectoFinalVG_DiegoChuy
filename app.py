import streamlit as st
import pandas as pd
import plotly.express as px # Usaremos Plotly para gráficas interactivas increíbles

# 1. Importamos tus funciones maestras desde tu archivo de limpieza
from limpiezaBasesDatos import (
    limpiar_lesiones, 
    unificar_excel_posiciones, 
    generar_tabla_carga_fisica, 
    generar_costo_deportivo
)

# 2. Configuración inicial de la página (La pestaña del navegador)
st.set_page_config(
    page_title="La Epidemia de Lesiones | IA",
    page_icon="⚽",
    layout="wide" # Para que las gráficas ocupen toda la pantalla
)

# 3. El Motor de Caché (¡La clave del éxito!)
# Este decorador hace que Streamlit solo limpie los datos la primera vez que abres la app.
@st.cache_data
def cargar_todos_los_datos():
    # Nota: Asegúrate de que las rutas coincidan con tus carpetas
    df_lesiones = limpiar_lesiones('Datasets/Dataset_lesiones_ligas.csv')
    df_posiciones = unificar_excel_posiciones('Datasets')
    df_carga = generar_tabla_carga_fisica('Datasets/baseDatos_Transfermark')
    df_costo = generar_costo_deportivo(df_lesiones, df_posiciones)
    
    return df_lesiones, df_posiciones, df_carga, df_costo

# 4. Cargamos los datos en la memoria de la app
try:
    with st.spinner('Procesando millones de datos... Por favor espera.'):
        df_lesiones, df_posiciones, df_carga, df_costo = cargar_todos_los_datos()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# 5. Encabezado Principal de tu Narrativa
st.title("⚽🏥 La Epidemia de Lesiones")
st.subheader("El verdadero costo del fútbol moderno")

st.markdown("""
A través de este análisis de datos, exploraremos si la saturación de los calendarios 
en el fútbol de élite está llevando a los jugadores a un punto de quiebre físico, 
y cómo esto impacta directamente en el fracaso deportivo de sus equipos.
""")

st.divider() # Una línea separadora elegante

# Aquí abajo irán nuestras 3 gráficas...
st.info("¡Datos cargados correctamente! Listos para graficar.")

import plotly.express as px

# ==========================================
# ACTO 1: LA CARGA Y SU CONSECUENCIA 
# ==========================================
st.header("Acto 1: La Carga Física vs Las Lesiones ⏱️🏥")
st.markdown("¿Cómo ha incrementado la exigencia física en las últimas temporadas y qué impacto directo ha tenido en los jugadores? Observamos la evolución de minutos frente a la cantidad de bajas médicas.")

# 1. Definimos nuestros "paquetes" de torneos
paquete_premier = ['premier-league', 'fa-cup', 'efl-cup', 'community-shield']
paquete_laliga = ['laliga', 'copa-del-rey', 'supercopa']
paquete_serie_a = ['serie-a', 'italy-cup', 'supercoppa-italiana']
paquete_uefa = ['uefa-champions-league', 'uefa-super-cup', 'europa-league']

todas_las_de_clubes = paquete_premier + paquete_laliga + paquete_serie_a + paquete_uefa

# 2. Menú desplegable
opciones_filtro = {
    "Todas las Competiciones de Élite": todas_las_de_clubes,
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League y Copas Inglesas": paquete_premier,
    "🇪🇸 LaLiga y Copas Españolas": paquete_laliga,
    "🇮🇹 Serie A y Copas Italianas": paquete_serie_a,
    "🌍 Torneos Internacionales (UEFA)": paquete_uefa
}
seleccion_usuario = st.selectbox("Filtra por Torneo / Liga:", options=list(opciones_filtro.keys()))

# 3. Lógica de Filtrado para MINUTOS
df_carga['torneo_temp'] = df_carga['Liga/Torneo'].astype(str).str.lower()
torneos_elegidos = opciones_filtro[seleccion_usuario]
df_carga_filtrada = df_carga[df_carga['torneo_temp'].isin(torneos_elegidos)]
carga_por_temporada = df_carga_filtrada.groupby(['Temporada', 'Tipo_Competicion'])['Minutos_Totales'].sum().reset_index()

# 4. Lógica de Filtrado para LESIONES
# Las lesiones están atadas a la liga principal del club, así que filtramos según lo seleccionado
if "Premier" in seleccion_usuario:
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('Premier', case=False, na=False)]
elif "LaLiga" in seleccion_usuario:
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('LaLiga|La Liga', case=False, na=False)]
elif "Serie A" in seleccion_usuario:
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('Serie A', case=False, na=False)]
else: 
    # Para "Todas" o "UEFA", mostramos el global de las top 3 ligas
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('Premier|LaLiga|La Liga|Serie A', case=False, na=False)]

lesiones_por_temporada = df_les_acto1.groupby('Season').size().reset_index(name='Total_Lesiones')

# 5. Dibujamos en dos columnas
col_izq, col_der = st.columns(2)

with col_izq:
    fig_carga = px.bar(
        carga_por_temporada, 
        x='Temporada', 
        y='Minutos_Totales', 
        color='Tipo_Competicion',
        title="Evolución de Minutos Jugados",
        labels={'Minutos_Totales': 'Minutos Acumulados', 'Tipo_Competicion': 'Tipo de Torneo'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig_carga, use_container_width=True)

with col_der:
    # Usamos una gráfica de líneas/área para resaltar la tendencia en el tiempo
    fig_lesiones_año = px.line(
        lesiones_por_temporada,
        x='Season',
        y='Total_Lesiones',
        title="Evolución de Lesiones Registradas",
        labels={'Season': 'Temporada', 'Total_Lesiones': 'Cantidad de Lesiones'},
        markers=True, # Pone puntitos en cada año
        color_discrete_sequence=['#d62728'] # Color rojo para el tema médico
    )
    # Sombreamos la parte de abajo de la línea para darle un toque más pro
    fig_lesiones_año.update_traces(fill='tozeroy')
    st.plotly_chart(fig_lesiones_año, use_container_width=True)

st.divider()

# ==========================================
# ACTO 2: EL QUIEBRE (Lesiones vs Minutos)
# ==========================================
st.header("Acto 2: El Quiebre 💥")
st.markdown("¿Los jugadores se rompen cuando juegan más? Comparamos directamente la carga física de cada mes con los ingresos al hospital.")

# 1. Filtro Maestro de Ligas (Aplica para ambas gráficas)
opciones_liga_acto2 = [
    "🏆 Top 3 Ligas (Premier, LaLiga, Serie A)", 
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", 
    "🇪🇸 LaLiga", 
    "🇮🇹 Serie A"
]
liga_seleccionada_acto2 = st.selectbox("Filtra el análisis por liga:", opciones_liga_acto2)

# 2. Lógica de Filtrado para AMBAS tablas
if liga_seleccionada_acto2 == "🏆 Top 3 Ligas (Premier, LaLiga, Serie A)":
    filtro_les = df_lesiones['league'].str.contains('Premier|LaLiga|La Liga|Serie A', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('premier-league|laliga|serie-a', case=False, na=False)
elif liga_seleccionada_acto2 == "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League":
    filtro_les = df_lesiones['league'].str.contains('Premier', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('premier-league', case=False, na=False)
elif liga_seleccionada_acto2 == "🇪🇸 LaLiga":
    filtro_les = df_lesiones['league'].str.contains('LaLiga|La Liga', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('laliga', case=False, na=False)
else: # Serie A
    filtro_les = df_lesiones['league'].str.contains('Serie A', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('serie-a', case=False, na=False)

df_les_filtrado = df_lesiones[filtro_les].copy()
df_car_filtrado = df_carga[filtro_car].copy()

# Mapeo de meses
nombres_meses = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
orden_meses = ['Ago', 'Sep', 'Oct', 'Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul']

# 3. Dividimos la pantalla en 2 columnas
col1, col2 = st.columns(2)

# --- GRÁFICA IZQUIERDA: MINUTOS ---
with col1:
    st.subheader("⏱️ Minutos Acumulados")
    # Agrupamos minutos por Mes usando la tabla que ya trae el mes
    df_car_filtrado['Mes_Nombre'] = df_car_filtrado['Mes'].map(nombres_meses)
    minutos_por_mes = df_car_filtrado.groupby('Mes_Nombre')['Minutos_Totales'].sum().reset_index()
    
    # Ordenar por el calendario futbolístico
    minutos_por_mes['Mes_Nombre'] = pd.Categorical(minutos_por_mes['Mes_Nombre'], categories=orden_meses, ordered=True)
    minutos_por_mes = minutos_por_mes.sort_values('Mes_Nombre')

    fig_minutos_mes = px.bar(
        minutos_por_mes, 
        x='Mes_Nombre', 
        y='Minutos_Totales',
        title="Total de Minutos Jugados por Mes",
        labels={'Mes_Nombre': 'Mes', 'Minutos_Totales': 'Minutos'},
        color_discrete_sequence=['#1f77b4'] # Color azul profesional
    )
    st.plotly_chart(fig_minutos_mes, use_container_width=True)

# --- GRÁFICA DERECHA: LESIONES ---
with col2:
    st.subheader("🏥 Pico de Lesiones")
    # Extraemos el mes de las lesiones
    df_les_filtrado['Mes'] = df_les_filtrado['injury_from_parsed'].dt.month
    df_les_filtrado['Mes_Nombre'] = df_les_filtrado['Mes'].map(nombres_meses)
    
    # Agrupamos por Temporada y Mes
    lesiones_heatmap = df_les_filtrado.groupby(['Season', 'Mes_Nombre']).size().reset_index(name='Cantidad de Lesiones')
    matriz_lesiones = lesiones_heatmap.pivot(index='Season', columns='Mes_Nombre', values='Cantidad de Lesiones').fillna(0)
    
    columnas_validas = [m for m in orden_meses if m in matriz_lesiones.columns]
    matriz_lesiones = matriz_lesiones[columnas_validas]

    fig_quiebre = px.imshow(
        matriz_lesiones, 
        labels=dict(x="Mes", y="Temporada", color="Lesiones"),
        x=matriz_lesiones.columns,
        y=matriz_lesiones.index,
        color_continuous_scale="Reds",
        aspect="auto",
        title="Densidad de Ingresos Médicos"
    )
    st.plotly_chart(fig_quiebre, use_container_width=True)

st.divider()

# ==========================================
# ACTO 3: EL COSTO DEPORTIVO (Dispersión)
# ==========================================
st.header("Acto 3: El Costo Deportivo 📉")
st.markdown("¿Tener el hospital lleno te cuesta el campeonato? Cruzamos la cantidad de días que los equipos pierden jugadores por lesión frente a su posición final en la liga.")

# Gráfica de Dispersión
fig_costo = px.scatter(
    df_costo, 
    x='Dias_Perdidos_Totales', 
    y='Posicion_Final', 
    color='Liga', 
    hover_name='Equipo',
    hover_data=['Temporada'],
    title="Impacto de las Lesiones en la Clasificación",
    labels={
        'Dias_Perdidos_Totales': 'Total de Días de Baja Médica', 
        'Posicion_Final': 'Posición en la Tabla (1 = Campeón)'
    },
    size='Dias_Perdidos_Totales',
    size_max=15
)

# Invertimos el eje Y para que el 1er lugar esté hasta arriba (lo lógico en el fútbol)
fig_costo.update_yaxes(autorange="reversed")

st.plotly_chart(fig_costo, use_container_width=True)

st.success("¡Análisis visual completado! La narrativa de datos está lista para ser presentada.")