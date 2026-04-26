from dash import Input, Output
import plotly.express as px
from .dash_app import app, load_data


#app = DjangoDash.get_app("SatisfactionDashboard")


# ==========================
# LOAD FILTERS
# ==========================
@app.callback(
    [
        Output("kpi-sexe-filter", "options"),
        Output("kpi-region-filter", "options"),
        Output("graph-sexe-filter", "options"),
        Output("graph-region-filter", "options"),
        Output("agent-filter", "options"),
    ],
    Input("kpi-sexe-filter", "id")
)
def load_filters(_):

    df = load_data()

    if df.empty:
        return [], [], [], [], []

    def opt(col):
        return [{"label": str(x), "value": str(x)} for x in df[col].dropna().unique()]

    return opt("sexe"), opt("region"), opt("agent_appel")


# ==========================
# KPI
# ==========================
@app.callback(
    [
        Output("total-respondants", "children"),
        Output("satisfaction-moyenne", "children"),
        Output("nps-score", "children"),
    ],
    [
        Input("kpi-sexe-filter", "value"),
        Input("kpi-region-filter", "value"),
    ]
)
def update_kpi(sexes, regions):

    df = load_data()

    if sexes:
        df = df[df["sexe"].isin(sexes)]

    if regions:
        df = df[df["region"].isin(regions)]

    total = len(df)

    if total == 0:
        return "Total: 0", "Satisfaction: 0", "NPS: 0"

    satisfaction = round(df["note_globale"].mean(), 2)

    promoters = len(df[df["note_globale"] >= 9])
    detractors = len(df[df["note_globale"] <= 6])

    nps = ((promoters - detractors) / total) * 100

    return (
        f"Total: {total}",
        f"Satisfaction: {satisfaction}",
        f"NPS: {round(nps,2)}"
    )


# ==========================
# GRAPHIQUES
# ==========================
@app.callback(
    [
        Output("region-chart", "figure"),
        Output("service-chart", "figure"),
        Output("age-chart", "figure"),
    ],
    [
        Input("graph-sexe-filter", "value"),
        Input("graph-region-filter", "value"),
    ]
)
def update_graphs(sexes, regions):

    df = load_data()

    if sexes:
        df = df[df["sexe"].isin(sexes)]

    if regions:
        df = df[df["region"].isin(regions)]

    if df.empty:
        return {}, {}, {}

    return (
        px.bar(df.groupby("region").size().reset_index(name="count"),
               x="region", y="count", title="Région"),

        px.pie(df, names="service_principal", title="Services"),

        px.histogram(df, x="age", title="Âge")
    )


# ==========================
# AGENTS
# ==========================
@app.callback(
    [
        Output("agent-performance-chart", "figure"),
        Output("agent-satisfaction-chart", "figure"),
    ],
    Input("agent-filter", "value")
)
def update_agent(agent):

    df = load_data()

    if agent:
        df = df[df["agent_appel"] == agent]

    if df.empty:
        return {}, {}

    return (
        px.histogram(df, x="note_globale", title="Performance agent"),
        px.box(df, y="note_globale", title="Satisfaction agent")
    )