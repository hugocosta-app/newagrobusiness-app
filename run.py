from app import create_app, db
from app.models.user import User
import os

app = create_app()

# Define a lista de usuários a serem criados
users_to_add = [
    {"username": "beto", "password": "beto123", "nickname": "Betão"},
    {"username": "luiz-andrade", "password": "luiz123", "nickname": "Luiz Mineiro"},
    {"username": "veronica", "password": "veronica123", "nickname": "Veronica"},
    {"username": "lourival", "password": "lourival123", "nickname": "Lourival"},
    {"username": "paulo", "password": "paulo123", "nickname": "Paulinho"},
    {"username": "ricardo", "password": "ricardo123", "nickname": "Ricardo"},
    {"username": "aldo", "password": "aldo123", "nickname": "Aldinho"},
    {"username": "hugo", "password": "hugo123", "nickname": "Hugão"},
    {"username": "fabio", "password": "fabio123", "nickname": "Fabinho"},
    {"username": "luciano", "password": "luciano123", "nickname": "Luciano"}
]

# Configurações para o usuário admin
admin_username = "admin"
admin_password = "admin123"
admin_email = "admin@newagrobusiness.com.br"

with app.app_context():
    # Cria o banco de dados se ele não existir
    db.create_all()

    # Cria o usuário administrador se ele não existir
    existing_admin = User.query.filter_by(username=admin_username).first()
    if not existing_admin:
        User.create_user(username=admin_username, email=admin_email, password=admin_password, is_admin=True, nickname="Admin")
        print(f"Usuário administrador {admin_username} criado com sucesso.")
    else:
        print(f"Usuário administrador {admin_username} já existe. Pulando.")

    # Cria os usuários vendedores se eles não existirem
    for user_data in users_to_add:
        username = user_data["username"]
        password = user_data["password"]
        nickname = user_data["nickname"]
        email = f"{username}@example.com"

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Usuário {username} já existe. Pulando.")
        else:
            User.create_user(username=username, email=email, password=password, nickname=nickname)
            print(f"Usuário {username} ({nickname}) criado com sucesso.")

    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
