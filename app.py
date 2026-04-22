import streamlit as st
import pandas as pd
import plotly.express as px #Usaremos plotly para gráficas interactivas

#Importamos funciones del archivo de limpieza
from limpiezaBasesDatos import (
    limpiar_lesiones, 
    unificar_excel_posiciones, 
    generar_tabla_carga_fisica, 
    generar_costo_deportivo
)

#Configuración inicial de la página
st.set_page_config(
    page_title="La Epidemia de Lesiones",
    page_icon="⚽",
    layout="wide" 
)

#El Motor de Caché
#Este decorador hace que Streamlit solo limpie los datos la primera vez que abres la app.
@st.cache_data
def cargar_todos_los_datos():
    df_lesiones = limpiar_lesiones('Datasets/Dataset_lesiones_ligas.csv')
    df_posiciones = unificar_excel_posiciones('Datasets')
    df_carga = generar_tabla_carga_fisica('Datasets/baseDatos_Transfermark')
    df_costo = generar_costo_deportivo(df_lesiones, df_posiciones)
    return df_lesiones, df_posiciones, df_carga, df_costo

#Cargamos los datos en la memoria de la app
try:
    with st.spinner('Procesando millones de datos... Por favor espera.'):
        df_lesiones, df_posiciones, df_carga, df_costo = cargar_todos_los_datos()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

#Encabezado principal 
st.title("La epidemia de lesiones: El verdadero costo del fútbol moderno")
st.subheader("Más torneos, más partidos, más minutos, más exigencia. El límite físico de los jugadores frente a un calendario que no se detiene.")
st.markdown("""
El fútbol de élite ha evolucionado hacia un espectáculo de máxima intensidad, pero el cuerpo humano tiene un límite. Hoy, los sindicatos de jugadores en todo el mundo levantan la voz ante una realidad innegable: 
el calendario está saturado. A través de los datos, exploramos la pregunta crítica del fútbol actual: 
¿Estamos rompiendo a los protagonistas del juego?
""")
st.divider()
st.info("¡Datos cargados correctamente! Listos para graficar.")
import plotly.express as px

#==========================================
#Acto 1
#==========================================
st.header("1. La carga física: El peso de los minutos y la factura en el cuerpo")
st.markdown("""
¿Cómo ha incrementado la exigencia física en las últimas temporadas y qué impacto directo ha tenido en los jugadores? 

A la izquierda, la acumulación de minutos pone en evidencia un calendario de partidos que ha ido en aumento a lo largo de los años. A la derecha, observamos una clara tendencia al alza en el número de lesiones desde el año 2022 hasta el 2025. 

Es importante destacar que los picos elevados en el gráfico de la derecha de 2020-2021 y 2021-2022 representan datos atípicos influenciados por la pandemia:
1. **Los contagios de COVID-19** se registraban directamente como bajas médicas que alejaban a los jugadores varios días.
2. **El desajuste físico:** volver al ritmo de máxima competencia tras meses de inactividad disparó los problemas musculares.
3. **La saturación extrema:** la urgencia por terminar las temporadas pausadas comprimió los calendarios, obligando a disputar partidos con muy pocos días de descanso.

*(Nota: Los registros de la temporada 2024-2025 no están completos y contabilizan únicamente hasta enero).*
""")
#Definimos nuestros "paquetes" de torneos
paquete_premier = ['premier-league', 'fa-cup', 'efl-cup', 'community-shield']
paquete_laliga = ['laliga', 'copa-del-rey', 'supercopa']
paquete_serie_a = ['serie-a', 'italy-cup', 'supercoppa-italiana']
paquete_uefa = ['uefa-champions-league', 'uefa-super-cup', 'europa-league']
todas_las_de_clubes = paquete_premier + paquete_laliga + paquete_serie_a + paquete_uefa
#Menú desplegable
opciones_filtro = {
    "Todas las competiciones": todas_las_de_clubes,
    "Premier League y Copas Inglesas": paquete_premier,
    "LaLiga y Copas Españolas": paquete_laliga,
    "Serie A y Copas Italianas": paquete_serie_a,
    "Torneos Internacionales (UEFA)": paquete_uefa
}
seleccion_usuario = st.selectbox("Filtra por Torneo / Liga:", options=list(opciones_filtro.keys()))
#Lógica de Filtrado para minutos
df_carga['torneo_temp'] = df_carga['Liga/Torneo'].astype(str).str.lower()
torneos_elegidos = opciones_filtro[seleccion_usuario]
df_carga_filtrada = df_carga[df_carga['torneo_temp'].isin(torneos_elegidos)]
carga_por_temporada = df_carga_filtrada.groupby(['Temporada', 'Tipo_Competicion'])['Minutos_Totales'].sum().reset_index()
#Lógica de Filtrado para lesiones
#Las lesiones están atadas a la liga principal del club, así que filtramos según lo seleccionado
if "Premier" in seleccion_usuario:
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('Premier', case=False, na=False)]
elif "LaLiga" in seleccion_usuario:
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('LaLiga|La Liga', case=False, na=False)]
elif "Serie A" in seleccion_usuario:
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('Serie A', case=False, na=False)]
else: 
    #Para "Todas", mostramos el global de las top 3 ligas
    df_les_acto1 = df_lesiones[df_lesiones['league'].str.contains('Premier|LaLiga|La Liga|Serie A', case=False, na=False)]
lesiones_por_temporada = df_les_acto1.groupby('Season').size().reset_index(name='Total_Lesiones')
#Dibujamos en dos columnas
col_izq, col_der = st.columns(2)
with col_izq:
    fig_carga = px.bar(
        carga_por_temporada, 
        x='Temporada', 
        y='Minutos_Totales', 
        color='Tipo_Competicion',
        title="Evolución de minutos jugados",
        labels={'Minutos_Totales': 'Minutos Acumulados', 'Tipo_Competicion': 'Tipo de Torneo'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig_carga, use_container_width=True)
with col_der:
    fig_lesiones_año = px.line(
        lesiones_por_temporada,
        x='Season',
        y='Total_Lesiones',
        title="Evolución de lesiones registradas",
        labels={'Season': 'Temporada', 'Total_Lesiones': 'Cantidad de Lesiones'},
        markers=True, 
        color_discrete_sequence=['#d62728']
    )
    st.plotly_chart(fig_lesiones_año, use_container_width=True)
st.divider()

#==========================================
#Acto 2
#==========================================
st.header("2. El quiebre: Cuando el calendario supera al físico")
st.markdown("¿Los jugadores se rompen cuando juegan más? Comparamos directamente la carga física con el número de lesiones cada mes. " \
"A la izquierda, el volumen mensual de minutos jugados expone los periodos de mayor asfixia competitiva. A la derecha, el mapa de calor revela la consecuencia: las zonas rojas más oscuras evidencian que los picos de lesiones estallan precisamente durante esos tramos de máxima exigencia sostenida. La fatiga acumulada no perdona."
"Como excepción visible, en el mapa de calor se observa un bloque más claro (con un número atípicamente bajo de lesiones) entre noviembre y diciembre de la temporada 2022-2023. Esto se debe a la pausa sin precedentes de las ligas de clubes provocada por la Copa del Mundo de Qatar 2022.")

#Filtro de ligas (Aplica para ambas gráficas)
opciones_liga_acto2 = [
    "Todas las competiciones", 
    "Premier League", 
    "LaLiga", 
    "Serie A"
]
liga_seleccionada_acto2 = st.selectbox("Filtra el análisis por liga:", opciones_liga_acto2)
#Lógica de filtrado para ambas tablas
if liga_seleccionada_acto2 == "Todas las competiciones":
    filtro_les = df_lesiones['league'].str.contains('Premier|LaLiga|La Liga|Serie A', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('premier-league|laliga|serie-a', case=False, na=False)
elif liga_seleccionada_acto2 == "Premier League":
    filtro_les = df_lesiones['league'].str.contains('Premier', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('premier-league', case=False, na=False)
elif liga_seleccionada_acto2 == "LaLiga":
    filtro_les = df_lesiones['league'].str.contains('LaLiga|La Liga', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('laliga', case=False, na=False)
else: # Serie A
    filtro_les = df_lesiones['league'].str.contains('Serie A', case=False, na=False)
    filtro_car = df_carga['Liga/Torneo'].str.contains('serie-a', case=False, na=False)
df_les_filtrado = df_lesiones[filtro_les].copy()
df_car_filtrado = df_carga[filtro_car].copy()
#Mapeo de meses
nombres_meses = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
orden_meses = ['Ago', 'Sep', 'Oct', 'Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul']
#Dividimos la pantalla en 2 columnas
col1, col2 = st.columns(2)
with col1:
    st.subheader("Minutos acumulados por mes")
    #Agrupamos minutos por mes usando la tabla que ya trae el mes
    df_car_filtrado['Mes_Nombre'] = df_car_filtrado['Mes'].map(nombres_meses)
    minutos_por_mes = df_car_filtrado.groupby('Mes_Nombre')['Minutos_Totales'].sum().reset_index()
    #Ordenar por el calendario futbolístico
    minutos_por_mes['Mes_Nombre'] = pd.Categorical(minutos_por_mes['Mes_Nombre'], categories=orden_meses, ordered=True)
    minutos_por_mes = minutos_por_mes.sort_values('Mes_Nombre')
    fig_minutos_mes = px.bar(
        minutos_por_mes, 
        x='Mes_Nombre', 
        y='Minutos_Totales',
        title="Total de minutos jugados",
        labels={'Mes_Nombre': 'Mes', 'Minutos_Totales': 'Minutos'},
        color_discrete_sequence=['#1f77b4'] # Color azul profesional
    )
    st.plotly_chart(fig_minutos_mes, use_container_width=True)
with col2:
    st.subheader("Pico de lesiones por mes")
    #Extraemos el mes de las lesiones
    df_les_filtrado['Mes'] = df_les_filtrado['injury_from_parsed'].dt.month
    df_les_filtrado['Mes_Nombre'] = df_les_filtrado['Mes'].map(nombres_meses)
    #Agrupamos por temporada y mes
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
        title="Densidad de lesiones"
    )
    st.plotly_chart(fig_quiebre, use_container_width=True)
st.divider()

#==========================================
#Acto 3
#==========================================
st.header("3. El costo deportivo")
st.markdown("¿Tener el hospital lleno te cuesta el campeonato? Relacionamos la cantidad de días que los equipos pierden jugadores por lesión frente a su posición final en la liga. " \
"En esta gráfica de dispersión, la tendencia es reveladora: a medida que los clubes se desplazan hacia la derecha por acumular más días en la enfermería, sus opciones de pelear por los primeros puestos disminuyen. El desgaste físico trasciende la salud individual del atleta; se convierte en un ancla que frena directamente el éxito deportivo de todo el equipo.")
#Creamos el filtro dinámico leyendo las ligas exactas que tienes en tu tabla
ligas_acto3 = ["Todas las Ligas"] + list(df_costo['Liga'].unique())
#Agregamos un 'key' único para que Streamlit no lo confunda con los otros filtros
liga_seleccionada_acto3 = st.selectbox("Filtra el impacto por Liga:", options=ligas_acto3, key="filtro_costo")
#Lógica de filtrado
if liga_seleccionada_acto3 != "Todas las Ligas":
    df_costo_filtrado = df_costo[df_costo['Liga'] == liga_seleccionada_acto3]
else:
    df_costo_filtrado = df_costo
#Gráfica de Dispersión interactiva
fig_costo = px.scatter(
    df_costo_filtrado, 
    x='Dias_Perdidos_Totales', 
    y='Posicion_Final', 
    color='Liga', 
    hover_name='Equipo',
    hover_data=['Temporada'],
    title=f"Impacto de las Lesiones en la Clasificación: {liga_seleccionada_acto3}",
    labels={
        'Dias_Perdidos_Totales': 'Total de Días de Baja Médica', 
        'Posicion_Final': 'Posición en la Tabla (1 = Campeón)'
    },
    size='Dias_Perdidos_Totales',
    size_max=15
)
#Invertimos el eje Y para que el 1er lugar (Campeón) esté en la cima de la gráfica
fig_costo.update_yaxes(autorange="reversed")
st.plotly_chart(fig_costo, use_container_width=True)
st.success("¡Análisis visual completado! La narrativa de datos está lista para ser presentada.")