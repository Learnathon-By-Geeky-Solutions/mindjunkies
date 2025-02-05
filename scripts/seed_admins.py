from django.contrib.auth import get_user_model
from decouple import config


def run() -> None:
    user = get_user_model()

    # Define superusers
    superusers = [
        {"username": config("U_SHAFAYET"), "email": config("E_SHAFAYET"), "password": config("P_SHAFAYET")},
        {"username": config("U_JIFAT"), "email": config("E_JIFAT"), "password": config("P_JIFAT")},
        {"username": config("U_FARHANA"), "email": config("E_FARHANA"), "password": config("P_FARHANA")},
    ]

    for user_data in superusers:
        username = user_data["username"]
        email = user_data["email"]
        password = user_data["password"]
        role = "teacher"

        if not user.objects.filter(username=username).exists():
            user.objects.create_superuser(username=username, email=email, password=password, role=role)
            print(f"✅ Superuser {username} created.")
        else:
            print(f"⚠️ Superuser {username} already exists.")

    print("🎉 Superuser creation script completed!")
