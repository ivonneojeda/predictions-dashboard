import os
import pandas as pd
import requests
from datetime import datetime

# -------------------------
# Variables de entorno
# -------------------------
access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
container_name = os.getenv("AZURE_CONTAINER_NAME")
azure_key = os.getenv("AZURE_TEXT_KEY")
azure_endpoint = os.getenv("AZURE_TEXT_ENDPOINT")

# -------------------------
# Parámetros Meta
# -------------------------
page_id = "tu_page_id_aqui"  # O también puedes ponerlo como variable de entorno

# -------------------------
# Función simulada para obtener posts de Meta
# -------------------------
def obtener_posts_meta(limit=5):
    url = f"https://graph.facebook.com/v17.0/{page_id}/posts"
    params = {
        "access_token": access_token,
        "fields": "message,created_time,likes.summary(true)",
        "limit": limit
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json().get("data", [])
        posts = []
        for item in data:
            mensaje = item.get("message", "")
            fecha = item.get("created_time", "")
            likes = item.get("likes", {}).get("summary", {}).get("total_count", 0)
            posts.append({"Fecha": fecha, "Post": mensaje, "Likes": likes})
        return posts
    except Exception as e:
        print("⚠️ Error obteniendo posts de Meta:", e)
        # Retornamos datos simulados si falla la API
        return [
            {"Fecha": datetime.now().isoformat(), "Post": "Prueba de post", "Likes": 0},
            {"Fecha": datetime.now().isoformat(), "Post": "Otro post de prueba", "Likes": 5}
        ]

# -------------------------
# Función para análisis de sentimiento (simulado)
# -------------------------
def analizar_sentimiento(posts):
    # Aquí conectas tu Azure Text Analytics real
    for p in posts:
        # Solo para prueba local: asignamos sentimientos aleatorios
        p["Sentimiento"] = "Neutro"
    return posts

# -------------------------
# Generar CSV
# -------------------------
posts = obtener_posts_meta(limit=5)
posts = analizar_sentimiento(posts)
df = pd.DataFrame(posts)
csv_file = "facebook_posts.csv"
df.to_csv(csv_file, index=False, encoding="utf-8-sig")
print(f">> CSV generado en {csv_file}")
print(df)

