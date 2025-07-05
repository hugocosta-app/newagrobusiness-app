import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User

@click.group()
def cli():
    "Add application commands."
    pass

@cli.command("init-db")
@with_appcontext
def init_db_command():
    "Clear existing data and create new tables."
    db.drop_all()
    db.create_all()
    click.echo("Banco de dados inicializado.")

@cli.command("create-users")
@with_appcontext
def create_users_command():
    "Create initial users for the application."
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

    admin_username = "admin"
    admin_password = "admin123"
    admin_email = "admin@newagrobusiness.com.br"

    # Create admin user if not exists
    existing_admin = User.query.filter_by(username=admin_username).first()
    if not existing_admin:
        User.create_user(username=admin_username, email=admin_email, password=admin_password, is_admin=True, nickname="Admin")
        click.echo(f"Usuário administrador {admin_username} criado com sucesso.")
    else:
        click.echo(f"Usuário administrador {admin_username} já existe. Pulando.")

    # Create seller users if not exists
    for user_data in users_to_add:
        username = user_data["username"]
        password = user_data["password"]
        nickname = user_data["nickname"]
        email = f"{username}@example.com"

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            click.echo(f"Usuário {username} já existe. Pulando.")
        else:
            User.create_user(username=username, email=email, password=password, nickname=nickname)
            click.echo(f"Usuário {username} ({nickname}) criado com sucesso.")
    db.session.commit()
    click.echo("Processo de criação de usuários concluído.")

