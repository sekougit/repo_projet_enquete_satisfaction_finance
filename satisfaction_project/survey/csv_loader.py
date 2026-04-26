import pandas as pd
from io import StringIO

from .models import SatisfactionSurvey


# =========================
# NETTOYAGE VALEURS
# =========================
def clean_value(val):
    if pd.isna(val):
        return None
    if str(val).strip().lower() in ["nan", "none", "null", ""]:
        return None
    return val


# =========================
# DATE PARSING
# =========================
def parse_date(val):
    try:
        if pd.isna(val):
            return None
        return pd.to_datetime(val)
    except:
        return None


# =========================
# IMPORT CSV ROBUSTE
# =========================
def import_survey_csv(file):

    # 🔥 FIX IMPORTANT : gérer bytes Django
    file.seek(0)
    content = file.read()

    try:
        content = content.decode("utf-8")
    except UnicodeDecodeError:
        content = content.decode("latin1")

    df = pd.read_csv(StringIO(content), sep=None, engine="python")

    created_count = 0
    updated_count = 0

    for _, row in df.iterrows():

        # 🔥 sécuriser id_soummission
        id_soummission = clean_value(row.get("id_soummission"))

        if id_soummission is None:
            continue  # skip ligne invalide

        obj_data = {
            "agent_appel": clean_value(row.get("agent_appel")),
            "numero_telephone": clean_value(row.get("numero_telephone")),
            "nom_client": clean_value(row.get("nom_client")),
            "prenom_nom": clean_value(row.get("prenom_nom")),

            "consentement_enquete": clean_value(row.get("consentement_enquete")),
            "nombre_services_utilises": clean_value(row.get("nombre_services_utilises")),

            "service_principal": clean_value(row.get("service_principal")),
            "frequence_service_principal": clean_value(row.get("frequence_service_principal")),

            "service_secondaire": clean_value(row.get("service_secondaire")),
            "frequence_service_secondaire": clean_value(row.get("frequence_service_secondaire")),

            "accessibilite_service": clean_value(row.get("accessibilite_service")),
            "rapidite_service": clean_value(row.get("rapidite_service")),

            "satisfaction_globale": clean_value(row.get("satisfaction_globale")),
            "qualite_service": clean_value(row.get("qualite_service")),
            "confiance_service": clean_value(row.get("confiance_service")),
            "satisfaction_support_client": clean_value(row.get("satisfaction_support_client")),

            "problemes_rencontres": clean_value(row.get("problemes_rencontres")),
            "propositions_amelioration": clean_value(row.get("propositions_amelioration")),

            "note_globale": clean_value(row.get("note_globale")),

            "mois_enquete": clean_value(row.get("mois_enquete")),
            "annee_enquete": clean_value(row.get("annee_enquete")),

            "date_soumission": parse_date(row.get("date_soumission")),

            "sexe": clean_value(row.get("sexe")),
            "age": clean_value(row.get("age")),

            "region": clean_value(row.get("region")),
            "departement": clean_value(row.get("departement")),
        }

        obj, created = SatisfactionSurvey.objects.update_or_create(
            id_soummission=id_soummission,
            defaults=obj_data
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    return {
        "total_lignes": len(df),
        "created": created_count,
        "updated": updated_count
    }