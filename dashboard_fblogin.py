# dashboard_fblogin.py
import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import dash
from dash import html, dcc

# -----------------------------
# Configurar Flask y Dash
# -----------------------------
server = Flask(__name__)

# Secret key para sesiones (leer de variable de entorno)
server.secret_key = os.environ.get("FLASK_SECRET_KEY", "default-secret")

# -----------------------------
# Configurar login con Facebook
# -----------------------------
facebook_blueprint = make_facebook_blueprint(
    client_id=os.environ.get("FACEBOOK_APP_ID", "TU_APP_ID_AQUI"),
    client_secret=os.environ.get("FACEBOOK_APP_SECRET", "TU_APP_SECRET_AQUI"),
    redirect_to="dashboard"
)
server.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")

# -----------------------------
# Crear app Dash
# -----------------------------
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

app.layout = html.Div(id="content")

# -----------------------------
# Función para mostrar dashboard solo si hay login
# -----------------------------
@server.route('/')
def index():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    return redirect("/dashboard/")

@app.callback(
    dash.dependencies.Output("content", "children"),
    dash.dependencies.Input("content", "id")  # Dummy input para disparar callback
)
def display_dashboard(_):
    if facebook.authorized:
        resp = facebook.get("/me?fields=name,email")
        if resp.ok:
            user_data = resp.json()
            return html.Div([
                html.H1(f"Bienvenido, {user_data.get('name')}!"),
                html.P(f"Tu email: {user_data.get('email')}"),
                html.Hr(),
                html.H2("📊 Dashboard de Opiniones"),
                html.P("Aquí se pueden mostrar gráficos y tablas.")
            ])
    return html.Div([
        html.P("No autorizado. Por favor, inicia sesión con Facebook.")
    ])

# -----------------------------
# Ejecutar servidor
# -----------------------------
if __name__ == "__main__":
    app.run(port=8050, debug=True)