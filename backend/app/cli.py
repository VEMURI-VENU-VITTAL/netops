import getpass

from app.auth import hash_password
from app.db import SessionLocal
from app.models import User


def main():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    role = input("Role [admin]: ") or "admin"
    with SessionLocal() as db:
        db.add(User(username=username, password_hash=hash_password(password), role=role))
        db.commit()
    print(f"Created user {username} ({role})")


if __name__ == "__main__":
    main()