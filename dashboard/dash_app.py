import pandas as pd
import plotly.express as px
import os

from django.conf import settings
from django_plotly_dash import DjangoDash
from dash import dcc, html
import dash_bootstrap_components as dbc
from survey.models import SatisfactionSurvey



# ==========================
# CHARGEMENT DES DONNEES
# ==========================
def load_data():

    qs = SatisfactionSurvey.objects.all().values()
    df = pd.DataFrame(list(qs))

    if df.empty:
        return df

    if "note_globale" in df.columns:
        df["note_globale"] = pd.to_numeric(
            df["note_globale"],
            errors="coerce"
        )

    if "age" in df.columns:
        df["age"] = pd.to_numeric(
            df["age"],
            errors="coerce"
        )

    return df


# ==========================
# DATA
# ==========================
file_path = os.path.join(settings.BASE_DIR, 'data', 'base_clients_enquete.xlsx')
data = pd.read_excel(file_path)

data.columns = data.columns.str.strip().str.lower()

for col in ["satisfaction_globale", "confiance_service", "service_principal"]:
    if col in data.columns:
        data[col] = data[col].fillna("")




# ==========================
# KPI VALUES
# ==========================
total = len(data)
note = round(data["note_globale"].mean(), 2)
age = round(data["age"].mean(), 1)

sat = round((data["satisfaction_globale"].str.lower() == "satisfait").mean() * 100, 1)

service = data["service_principal"].mode().iloc[0] if not data["service_principal"].mode().empty else "N/A"

conf = round((data["confiance_service"].str.lower() == "oui").mean() * 100, 1)


# ==========================
# GRAPHIQUES RESPONSIVE
# ==========================
fig_box = px.box(data, y="age", title="Distribution de l'âge")
fig_box.update_layout(margin=dict(l=20, r=20, t=40, b=20))

df_sexe = data["sexe"].value_counts().reset_index()
df_sexe.columns = ["sexe", "count"]
fig_pie = px.pie(df_sexe, names="sexe", values="count", title="Sexe")
fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20))

df_sat = data["satisfaction_globale"].value_counts().reset_index()
df_sat.columns = ["satisfaction", "count"]
fig_bar = px.bar(df_sat, x="satisfaction", y="count", title="Satisfaction")
fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))

df_region = data["region"].value_counts().reset_index()
df_region.columns = ["region", "count"]
fig_region = px.bar(df_region, x="region", y="count", title="Région")
fig_region.update_layout(margin=dict(l=20, r=20, t=40, b=20))


# ==========================
# APP
# ==========================
app = DjangoDash(
    "SatisfactionDashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Données exemple
df_exemple = pd.DataFrame({
    "Mois": ["Jan", "Fev", "Mar", "Avr"],
    "Valeur": [10, 20, 15, 30]
})

# Graphique
fig_exemple = px.bar(df_exemple, x="Mois", y="Valeur")

# ==========================
# KPI CARDS FIXED (NO OVERFLOW)
# ==========================
kpi_cards = dbc.Row([

    dbc.Col(dbc.Card([dbc.CardBody([html.H4(total), html.P("Répondants")])],
                     color="primary", inverse=True), width=4),

    dbc.Col(dbc.Card([dbc.CardBody([html.H4(f"{note}/10"), html.P("Note")])],
                     color="success", inverse=True), width=4),

    dbc.Col(dbc.Card([dbc.CardBody([html.H4(f"{age} ans"), html.P("Âge")])],
                     color="info", inverse=True), width=4),

    dbc.Col(dbc.Card([dbc.CardBody([html.H4(f"{sat}%"), html.P("Satisfaction")])],
                     color="warning", inverse=True), width=4),

    dbc.Col(dbc.Card([dbc.CardBody([html.H4(service), html.P("Service")])],
                     color="dark", inverse=True), width=4),

    dbc.Col(dbc.Card([html.H4(f"{conf}%"), html.P("Confiance")],
                     style={"textAlign": "center"}), width=4),

], className="g-2", style={"flexWrap": "wrap"})


# ==========================
# LAYOUT FINAL
# ==========================
app.layout = html.Div([

    html.H2(
        "Dashboard Satisfaction Client",
        style={"textAlign": "center", "color": "#0d6efd"}
    ),

    kpi_cards,

    html.Hr(),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_box), width=6),
        dbc.Col(dcc.Graph(figure=fig_pie), width=6),
    ], className="g-2"),

    html.Br(),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_bar), width=6),
        dbc.Col(dcc.Graph(figure=fig_region), width=6),
    ], className="g-2"),

    html.Br(),

    dcc.Graph(figure=fig_exemple)

], style={
    "width": "100%",
    "height": "100%",
    "overflow": "hidden",
    "padding": "10px"
})