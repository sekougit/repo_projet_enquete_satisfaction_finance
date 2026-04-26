from django.db import models

class SatisfactionSurvey(models.Model):

    id_soummission = models.BigIntegerField(primary_key=True)

    agent_appel = models.CharField(max_length=100, null=True, blank=True)
    numero_telephone = models.CharField(max_length=30, null=True, blank=True)
    nom_client = models.CharField(max_length=255, null=True, blank=True)
    prenom_nom = models.CharField(max_length=255, null=True, blank=True)

    consentement_enquete = models.CharField(max_length=10, null=True, blank=True)

    nombre_services_utilises = models.IntegerField(null=True, blank=True)

    service_principal = models.CharField(max_length=255, null=True, blank=True)
    frequence_service_principal = models.CharField(max_length=100, null=True, blank=True)

    service_secondaire = models.CharField(max_length=255, null=True, blank=True)
    frequence_service_secondaire = models.CharField(max_length=100, null=True, blank=True)

    accessibilite_service = models.CharField(max_length=100, null=True, blank=True)
    rapidite_service = models.CharField(max_length=100, null=True, blank=True)

    satisfaction_globale = models.CharField(max_length=50, null=True, blank=True)
    qualite_service = models.CharField(max_length=50, null=True, blank=True)
    confiance_service = models.CharField(max_length=50, null=True, blank=True)
    satisfaction_support_client = models.CharField(max_length=50, null=True, blank=True)

    problemes_rencontres = models.TextField(null=True, blank=True)
    propositions_amelioration = models.TextField(null=True, blank=True)

    note_globale = models.FloatField(null=True, blank=True)

    mois_enquete = models.CharField(max_length=20, null=True, blank=True)
    annee_enquete = models.IntegerField(null=True, blank=True)

    date_soumission = models.DateTimeField(null=True, blank=True)

    sexe = models.CharField(max_length=10, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    region = models.CharField(max_length=100, null=True, blank=True)
    departement = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.id_soummission} - {self.nom_client}"