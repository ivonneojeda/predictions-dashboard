import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------
# Configuración de Flask
# -----------------------------
server = Flask(__name__)
server.secret_key = os.environ.get("FLASK_SECRET_KEY", "default-secret")

# Facebook OAuth
facebook_bp = make_facebook_blueprint(
    client_id=os.environ.get("FACEBOOK_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET"),
    redirect_url="/facebook_login/facebook/authorized"
)
server.register_blueprint(facebook_bp, url_prefix="/facebook_login")

# -----------------------------
# Configuración de Dash
# -----------------------------
app = dash.Dash(__name__, server=server, url_base_pathname='/', suppress_callback_exceptions=True)
app.title = "Dashboard de Opiniones"

# -----------------------------
# Datos de ejemplo
# -----------------------------
df_sentimientos = pd.DataFrame({
    "Fecha": pd.date_range(start="2025-01-01", periods=30),
    "Sentimiento": [0.1, 0.3, -0.2, 0.5, -0.1, 0.0, 0.2, -0.3, 0.4, 0.1,
                    0.2, 0.1, -0.2, 0.3, 0.0, 0.2, -0.1, 0.1, 0.3, -0.2,
                    0.2, 0.0, -0.1, 0.3, 0.4, 0.2, -0.3, 0.1, 0.0, 0.2]
})

df_tabla = pd.DataFrame({
    "Publicación": [f"Post {i}" for i in range(1, 11)],
    "Likes": [10, 25, 15, 30, 20, 12, 22, 18, 35, 28],
    "Comentarios": [1, 5, 2, 4, 3, 2, 1, 0, 5, 3]
})

# -----------------------------
# Layout con Tabs
# -----------------------------
app.layout = html.Div([
    html.H1("📊 Dashboard de Opiniones con Facebook Login"),
    html.Div(id='login-message'),
    dcc.Tabs([
        dcc.Tab(label='Gráficos', children=[
            dcc.Graph(
                id="grafico-sentimientos",
                figure=px.line(df_sentimientos, x="Fecha", y="Sentimiento",
                               title="Evolución del Sentimiento")
            )
        ]),
        dcc.Tab(label='Tabla', children=[
            dash_table.DataTable(
                id='tabla-publicaciones',
                columns=[{"name": i, "id": i} for i in df_tabla.columns],
                data=df_tabla.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center'},
                page_size=5
            )
        ]),
        dcc.Tab(label='Resumen', children=[
            html.Div([
                html.P(f"Total Posts: {len(df_tabla)}"),
                html.P(f"Likes Totales: {df_tabla['Likes'].sum()}"),
                html.P(f"Comentarios Totales: {df_tabla['Comentarios'].sum()}")
            ], style={'margin': '20px', 'fontSize': '18px'})
        ])
    ])
])

# -----------------------------
# Callback de login
# -----------------------------
@app.callback(
    Output('login-message', 'children'),
    Input('login-message', 'id')  # Dummy input para que Dash llame al callback
)
def check_login(_):
    if not facebook.authorized:
        return html.Div([
            html.P("No estás logueado en Facebook."),
            html.A("Inicia sesión con Facebook", href=url_for("facebook.login"))
        ])
    resp = facebook.get("/me?fields=name")
    if not resp.ok:
        return html.P("Error al obtener información de Facebook.")
    user_name = resp.json().get("name", "Usuario")
    return html.P(f"¡Bienvenido, {user_name}! Ahora puedes ver el dashboard completo.")

# -----------------------------
# Ejecutar app
# -----------------------------
if __name__ == "__main__":
    app.run(port=8050, debug=True)
