# ProyectoVG_Final_DiegoMu-oz
# La epidemia de lesiones: El verdadero costo del fútbol moderno

## Descripción del proyecto
Este proyecto es un análisis de datos y un panel interactivo construido con **Streamlit**. Explora la correlación directa entre la saturación del calendario en el fútbol de élite, el incremento de las lesiones y el impacto directo que estas bajas médicas tienen en el rendimiento y la clasificación final de los equipos.
El análisis se centra en las tres principales ligas europeas (Premier League, LaLiga y Serie A) y competiciones internacionales de la UEFA.

## La narrativa de datos
El proyecto está dividido en tres "actos" visuales:
1. **La carga física:** Compara la evolución histórica de los minutos jugados frente a la cantidad de lesiones registradas por temporada.
2. **El quiebre:** Analiza la densidad de lesiones por mes, cruzando el volumen mensual de minutos jugados para encontrar los "picos" de colapso físico.
3. **El costo deportivo:** A través de un gráfico de dispersión, se demuestra cómo la acumulación de días de lesión castiga competitivamente a los clubes, alejándolos de los primeros puestos de la tabla.
---

## Estructura del proyecto
El proyecto está organizado de la siguiente manera, separando claramente la extracción/limpieza de datos de la visualización:
📁 Proyecto_Lesiones/
│
├── 📁 Datasets/
│   ├── 📁 baseDatos_Transfermark/   #Archivos CSV crudos (minutos, juegos, clubes)
│   ├── 📁 salarios/                 #Bases de datos complementarias
│   ├── Dataset_lesiones_ligas.csv   #Historial médico de los jugadores
│   ├── premier.xlsx                 #Historial de posiciones por temporada
│   ├── laLiga.xlsx
│   └── serieA.xlsx
│
├── limpiezaBasesDatos.py  #Motor principal (ETL): Limpia, estandariza y fusiona bases
├── app.py                 #Aplicación principal de Streamlit
├── analisis.py            #Script de diagnóstico estadístico (nulos, info, describe)
├── auditoriaNombres.py    #Script de auditoría para el cruce exacto de nombres de clubes
└── README.md              #Documentación del proyecto

## Funciones principales de los scripts
* **limpiezaBasesDatos.py:** Es el núcleo. Procesa los datos, transforma fechas, estandariza formatos y cruza las bases usando diccionarios para asegurar consistencia. Retorna 4 DataFrames listos.
* **app.py:** Usa @st.cache_data para almacenar los datos limpios y genera los gráficos interactivos usando Plotly Express.
* **analisis.py y auditoriaNombres.py:** Herramientas de diagnóstico para garantizar la integridad de los datos, detectar valores nulos y auditar el cruce relacional de los nombres de los equipos.

## Cómo ejecutar el proyecto localmente
**1. Clonar el repositorio**
Asegúrate de tener la carpeta `Datasets` con los archivos originales en la ruta correcta.
**2. Instalar dependencias**
Necesitas Python instalado y las siguientes librerías:
```bash
pip install pandas streamlit plotly openpyxl
```
**3. Ejecutar aplicación**: streamlit run app.py