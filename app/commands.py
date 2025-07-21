import click
from flask.cli import with_appcontext
from flask import current_app
from app import db

@click.group()
def cli():
    """Comandos personalizados para a aplicação."""
    pass

@cli.command()
@with_appcontext
def init_db():
    """Inicializa o banco de dados e cria usuário admin padrão."""
    # Import models here to ensure they are known to SQLAlchemy
    from app.models import user, product, order, expense, visit, agenda
    from app.models.user import User
    
    db.drop_all()
    db.create_all()
    
    # Criar usuário admin padrão
    if not User.query.filter_by(email='admin@newagrobusiness.com.br').first():
        User.create_user('admin', 'admin@newagrobusiness.com.br', 'adminpassword', is_admin=True)
        click.echo('Usuário admin criado com sucesso!')
    
    # Criar alguns usuários vendedores de exemplo
    if not User.query.filter_by(email='vendedor1@newagrobusiness.com.br').first():
        User.create_user('vendedor1', 'vendedor1@newagrobusiness.com.br', 'vendedor123', is_admin=False, nickname='João Silva')
        click.echo('Vendedor 1 criado com sucesso!')
    
    if not User.query.filter_by(email='vendedor2@newagrobusiness.com.br').first():
        User.create_user('vendedor2', 'vendedor2@newagrobusiness.com.br', 'vendedor123', is_admin=False, nickname='Maria Santos')
        click.echo('Vendedor 2 criado com sucesso!')
    
    click.echo('Banco de dados inicializado com sucesso!')

