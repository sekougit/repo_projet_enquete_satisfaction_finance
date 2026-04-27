from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# ==========================
# GROUPES
# ==========================
admin_group, _ = Group.objects.get_or_create(name="Admin")
agent_group, _ = Group.objects.get_or_create(name="Agent")
manager_group, _ = Group.objects.get_or_create(name="Manager")


# ==========================
# ADMIN
# ==========================
if not User.objects.filter(username="admin").exists():
    admin = User.objects.create_superuser(
        username="admin",
        email="admin@gmail.com",
        password="admin1234"
    )
    admin.role = "admin"
    admin.save()
    admin.groups.add(admin_group)
    print("✅ Admin créé")


# ==========================
# 5 AGENTS
# ==========================
for i in range(1, 6):
    username = f"agent{i}"

    user, created = User.objects.get_or_create(username=username)

    if created:
        user.set_password("123456")
        user.email = f"{username}@mail.com"
        user.role = "agent"
        user.save()

    user.groups.add(agent_group)
    print(f"✅ Agent créé : {username}")


# ==========================
# 5 MANAGERS
# ==========================
for i in range(1, 6):
    username = f"manager{i}"

    user, created = User.objects.get_or_create(username=username)

    if created:
        user.set_password("123456")
        user.email = f"{username}@mail.com"
        user.role = "manager"
        user.save()

    user.groups.add(manager_group)
    print(f"✅ Manager créé : {username}")


print("🎯 Tous les utilisateurs ont été créés")