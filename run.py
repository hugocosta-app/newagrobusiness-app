# /home/ubuntu/newagrobusiness_app/run.py
from app import create_app

app = create_app()

# A linha abaixo é apenas para execução local com `python run.py` ou `flask run`
# Em produção, o Gunicorn/uWSGI chamará diretamente o objeto `app` importado.
if __name__ == "__main__":
    # O Flask detecta automaticamente este arquivo e a instância `app`
    # ao usar `flask run`. Para executar com `python run.py`, 
    # descomente a linha abaixo, mas lembre-se que este não é o modo de produção.
    # app.run(debug=False) # Certifique-se que debug=False para produção
    pass # Deixe pass ou remova o if __name__... para `flask run` funcionar

