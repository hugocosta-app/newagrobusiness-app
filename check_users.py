
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    print("Verificando usuários no banco de dados...")
    users = User.query.all()
    if users:
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Nickname: {user.nickname}, Admin: {user.is_admin}")
    else:
        print("Nenhum usuário encontrado.")

    print("\nVerificando usuário 'beto':")
    beto_user = User.query.filter_by(username='beto').first()
    if beto_user:
        print(f"ID: {beto_user.id}, Username: {beto_user.username}, Email: {beto_user.email}, Nickname: {beto_user.nickname}, Admin: {beto_user.is_admin}")
    else:
        print("Usuário 'beto' não encontrado.")

print("Verificação concluída.")
