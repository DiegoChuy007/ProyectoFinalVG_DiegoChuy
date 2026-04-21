import pandas as pd

print("⏳ Encogiendo appearances.csv...")

# 1. Leemos el archivo grande, pero SOLO las 4 columnas que usa tu proyecto
columnas_necesarias = ['player_id', 'game_id', 'minutes_played', 'player_name']
ruta = 'Datasets/baseDatos_Transfermark/appearances.csv'

df = pd.read_csv(ruta, usecols=columnas_necesarias)

# 2. Lo sobreescribimos. Como ya no tiene las columnas inútiles, pesará muchísimo menos.
df.to_csv(ruta, index=False)

print("✅ ¡Listo! El archivo ahora es peso pluma y está listo para GitHub.")