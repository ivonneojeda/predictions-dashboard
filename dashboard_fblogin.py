# dashboard_fblogin.py
import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import dash
from dash import html

# -----------------------------
# Configurar Flask
# -----------------------------
server = Flask(__name__)
server.secret_key = os.environ.get("FLASK_SECRET_KEY", "default-secret")  # Cambia a algo seguro en producción

# -----------------------------
# Configurar Facebook OAuth
# -----------------------------
facebook_bp = make_facebook_blueprint(
    client_id=os.environ.get("facebook_oauth_client_id"),
    client_secret=os.environ.get("facebook_oauth_client_secret"),
    redirect_to="dashboard"  # Nombre de la función a redirigir tras login
)
server.register_blueprint(facebook_bp, url_prefix="/facebook_login")

# -----------------------------
# Configurar Dash
# -----------------------------
app = dash.Dash(__name__, server=server, url_base_pathname='/')
app.title = "Dashboard de Opiniones"

app.layout = html.Div(id="content")

# -----------------------------
# Callback para mostrar contenido solo si hay login
# -----------------------------
@server.route("/")
def dashboard():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    resp = facebook.get("/me?fields=name,email")
    if not resp.ok:
        return redirect(url_for("facebook.login"))
    user_info = resp.json()
    return f"""
    <h1>Bienvenido {user_info.get('name')}</h1>
    <p>Tu correo: {user_info.get('email')}</p>
    <p>📊 Aquí irá el contenido del dashboard</p>
    """

# -----------------------------
# Ejecutar servidor
# -----------------------------
if __name__ == "__main__":
    app.run(port=8050, debug=True)
