# La epidemia de lesiones: El verdadero costo del fútbol moderno

## Autor
Diego de Jesús Muñoz González, estudiante de Licenciatura en Ingeniería en Inteligencia Artificial.

## Fuente de los datos
Los datos utilizados para el desarrollo del proyecto se obtuvieron de las siguientes fuentes:
1. **Dataset_lesiones_ligas.csv**
* Link de descarga: https://www.kaggle.com/datasets/sananmuzaffarov/european-football-injuries-2020-2025. 
* Fecha de descarga: 15/04/2026
* Formato original: .csv
* Lugar de origen: Kaggle

2. **Datasets: laLiga.xlsx, premier.xlsx, serieA.xlsx**
* Link de descarga: https://fbref.com/ 
* Fecha de descarga: 15/04/2026
* Formato original: .xlsx
* Lugar de origen: FBREF

3. **baseDatos_Transfermark**
* Link de descarga: https://www.kaggle.com/datasets/davidcariboo/player-scores 
* Fecha de descarga: 15/04/2026
* Formato original: .csv
* Lugar de origen: Kaggle

## Descripción del proyecto
Este proyecto consiste en la creación de una narrativa visual interactiva desarrollada con Streamlit, basada en el análisis de datos. Su objetivo es explorar la relación entre la saturación del calendario en el fútbol de élite, el aumento en la incidencia de lesiones y el impacto que estas ausencias tienen en el rendimiento deportivo y la clasificación final de los equipos.
El análisis se enfoca en las principales ligas europeas (la Premier League, LaLiga y la Serie A) así como en competiciones internacionales organizadas por la UEFA.

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
**3. Ejecutar aplicación**: python -m streamlit run app.py