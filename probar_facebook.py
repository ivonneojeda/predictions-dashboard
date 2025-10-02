import os
import requests

# Lee las variables de entorno
page_id = os.getenv("META_PAGE_ID")
access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

print("🔎 Page ID:", page_id)
print("🔑 Access Token (primeros 15):", access_token[:15] + "..." if access_token else None)

if not page_id or not access_token:
    print("❌ Faltan variables de entorno (META_PAGE_ID o FACEBOOK_ACCESS_TOKEN)")
    exit()

# URL del endpoint de Facebook Graph
url = f"https://graph.facebook.com/v17.0/{page_id}/posts"
params = {
    "fields": "message,created_time,likes.summary(true)",
    "limit": 5,
    "access_token": access_token
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    print("✅ Respuesta correcta de Facebook")
    print(data)
except requests.exceptions.HTTPError as e:
    print(f"❌ Error HTTP: {e}")
    print("Respuesta completa:", response.text)
except Exception as e:
    print("❌ Otro error:", e)

