import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
import os

User = get_user_model()

# ==========================
# EXCEL PATH
# ==========================
file_path = os.path.join(settings.BASE_DIR, 'media', 'users.xlsx')

# ==========================
# READ EXCEL
# ==========================
df = pd.read_excel(file_path)

# ==========================
# GROUPS
# ==========================
admin_group, _ = Group.objects.get_or_create(name="Admin")
agent_group, _ = Group.objects.get_or_create(name="Agent")
manager_group, _ = Group.objects.get_or_create(name="Manager")

# ==========================
# IMPORT USERS
# ==========================
for _, row in df.iterrows():

    username = str(row["username"]).strip()
    email = str(row["email"]).strip()
    password = str(row["password"]).strip()
    role = str(row["role"]).strip().lower()

    # Vérifie si user existe déjà
    if User.objects.filter(username=username).exists():

        print(f"Déjà existant : {username}")
        continue

    # Création user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    user.role = role

    # Assignation groupes
    if role == "admin":
        user.is_staff = True
        user.is_superuser = True
        user.groups.add(admin_group)

    elif role == "agent":
        user.groups.add(agent_group)

    elif role == "manager":
        user.groups.add(manager_group)

    user.save()

    print(f"Créé : {username}")

print("Import terminé")