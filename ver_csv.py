import pandas as pd

# Ruta al CSV generado
csv_path = r"C:\Users\ivonn\Desktop\Mi proyecto azure\facebook_posts.csv"

# Leer el CSV
try:
    df = pd.read_csv(csv_path)
    print("✅ CSV cargado correctamente")
    print(df.head())  # Muestra las primeras filas
except FileNotFoundError:
    print("⚠️ No se encontró el CSV en la ruta indicada")
except Exception as e:
    print("⚠️ Error al leer el CSV:", e)
