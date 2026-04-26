from django_plotly_dash import DjangoDash
from dash import html, dcc
import pandas as pd
from survey.models import SatisfactionSurvey




# ==========================
# LOAD DATA
# ==========================
def load_data():
    qs = SatisfactionSurvey.objects.all().values()
    df = pd.DataFrame(qs)

    if df.empty:
        return df

    df["note_globale"] = pd.to_numeric(df["note_globale"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    return df


# ==========================
# APP DASH
# ==========================
app = DjangoDash("SatisfactionDashboard")


app.layout = html.Div([

    dcc.Tabs([

        # ================= KPI =================
        dcc.Tab(label="KPI", children=[

            html.Br(),

            html.Div([
                dcc.Dropdown(id="kpi-sexe-filter", options=[], multi=True, placeholder="Sexe"),
                dcc.Dropdown(id="kpi-region-filter", options=[], multi=True, placeholder="Région"),
            ], style={"display": "flex", "gap": "10px"}),

            html.Br(),

            html.Div([
                html.Div(id="total-respondants"),
                html.Div(id="satisfaction-moyenne"),
                html.Div(id="nps-score"),
            ], style={"display": "flex", "gap": "20px"})
        ]),

        # ================= AGENTS =================
        dcc.Tab(label="Agents", children=[

            html.Br(),

            dcc.Dropdown(id="agent-filter", options=[], placeholder="Agent"),

            html.Br(),

            dcc.Graph(id="agent-performance-chart"),
            dcc.Graph(id="agent-satisfaction-chart"),
        ]),

        # ================= GRAPHIQUES =================
        dcc.Tab(label="Graphiques", children=[

            html.Br(),

            html.Div([
                dcc.Dropdown(id="graph-sexe-filter", options=[], multi=True, placeholder="Sexe"),
                dcc.Dropdown(id="graph-region-filter", options=[], multi=True, placeholder="Région"),
            ], style={"display": "flex", "gap": "10px"}),

            html.Br(),

            dcc.Graph(id="region-chart"),
            dcc.Graph(id="service-chart"),
            dcc.Graph(id="age-chart"),

        ])

    ])

])