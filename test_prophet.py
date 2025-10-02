import pandas as pd

CSV_PATH = r"C:\Users\ivonn\Desktop\Mi proyecto azure\datos\sentimiento_2025-09-30_22-00-03.csv"

# Cargar CSV
try:
    df = pd.read_csv(CSV_PATH)
    print("✅ CSV cargado correctamente")
    print(df.head())  # muestra las primeras filas
except FileNotFoundError:
    print(f"❌ Archivo no encontrado: {CSV_PATH}")


# Revisar las primeras filas y tipos de datos
print(df.head())
print(df.dtypes)

# Intentar convertir la columna Fecha a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# Revisar si hay nulos o problemas de conversión
print(df['Fecha'].isnull().sum())
print(df['Fecha'].head())
print(df['Fecha'].min(), df['Fecha'].max())

# Revisar cantidad de registros por día
df_daily = df.groupby(df['Fecha'].dt.date).size()
print(df_daily)
