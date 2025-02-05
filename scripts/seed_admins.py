from django.contrib.auth import get_user_model


def run():
    user = get_user_model()

    # Define superusers
    superusers = [
        {"username": "admin_shafayet", "email": "shafayet@example.com", "password": "12shafayet09"},
        {"username": "admin_tonmay", "email": "tonmay@example.com", "password": "12tonmay09"},
        {"username": "admin_farhana", "email": "farhana@example.com", "password": "12farhana09"},
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
