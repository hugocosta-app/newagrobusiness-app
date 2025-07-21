# Sistema de Gestão New Agrobusiness

Este é um aplicativo web desenvolvido em Flask para gerenciar Pedidos, Despesas, Viagens e Agenda para a equipe da New Agrobusiness.

## Funcionalidades Principais

*   **Autenticação:** Login seguro para Vendedores e Administradores.
*   **Perfis:**
    *   **Admin:** Gerencia produtos, visualiza todos os pedidos, despesas, visitas e agendas.
    *   **Vendedor:** Cria pedidos, registra despesas, relata visitas e gerencia sua própria agenda.
*   **Pedidos:** Criação de pedidos com dados do cliente, busca de produtos, aplicação de descontos por item e geração de relatório TXT.
*   **Despesas:** Registro de despesas de viagem (combustível, pedágio, refeições, hotel, diversos) com upload de nota fiscal, cálculo de KM e geração de relatórios (TXT implementado).
*   **Viagens:** Registro de visitas a clientes com resumo, destaques, observações e upload de fotos.
*   **Agenda:** Vendedores registram sua localização/compromissos futuros; Gestores visualizam a agenda da equipe.

## Configuração e Execução Local

**Pré-requisitos:**

*   Python 3.8+
*   pip (gerenciador de pacotes Python)

**Passos:**

1.  **Clonar o repositório (ou descompactar os arquivos):**
    ```bash
    # Se estivesse em um repositório git
    # git clone <url_do_repositorio>
    # cd newagrobusiness_app
    cd /home/ubuntu/newagrobusiness_app 
    ```

2.  **Criar um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate    # Windows
    ```

3.  **Instalar as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variáveis de ambiente (opcional, mas recomendado para produção):**
    *   Crie um arquivo `.env` na raiz do projeto (`/home/ubuntu/newagrobusiness_app/.env`).
    *   Adicione a seguinte linha (mude a chave secreta para algo seguro):
        ```
        SECRET_KEY=\'sua_chave_secreta_super_segura_aqui\'
        # DATABASE_URL=\'postgresql://user:password@host:port/database\' # Exemplo para PostgreSQL em produção
        ```
    *   Se o arquivo `.env` não for criado, uma chave secreta padrão será usada para desenvolvimento, e o banco de dados será um arquivo `app.db` SQLite na raiz.

5.  **Executar a aplicação:**
    ```bash
    flask run
    ```
    *   A aplicação estará acessível em `http://127.0.0.1:5000` (ou o endereço indicado no terminal).

6.  **Acesso Inicial:**
    *   Um usuário **admin** padrão é criado na primeira execução:
        *   **Email:** `admin@newagrobusiness.com.br`
        *   **Senha:** `adminpassword`
    *   **IMPORTANTE:** Altere a senha do admin imediatamente após o primeiro login por questões de segurança (funcionalidade de troca de senha não implementada neste escopo, mas essencial para produção).
    *   Novos usuários (vendedores) precisam ser cadastrados pelo administrador (funcionalidade de cadastro não implementada neste escopo).

## Estrutura do Projeto

```
/newagrobusiness_app
|-- app/                  # Módulo principal da aplicação Flask
|   |-- models/           # Modelos SQLAlchemy (user.py, product.py, etc.)
|   |-- routes/           # Blueprints para as rotas (auth.py, orders.py, etc.)
|   |-- static/           # Arquivos estáticos (CSS, JS, Imagens)
|   |   |-- css/
|   |   |-- js/
|   |   |-- images/
|   |-- templates/        # Templates HTML (Jinja2)
|   |   |-- auth/
|   |   |-- orders/
|   |   |-- expenses/
|   |   |-- visits/
|   |   |-- agenda/
|   |   |-- base.html     # Template base
|   |   |-- dashboard.html
|   |-- utils/            # Utilitários (decorators.py)
|   |-- __init__.py       # Fábrica da aplicação Flask (create_app)
|-- uploads/              # Diretório para uploads (notas fiscais, fotos de visitas)
|   |-- visits/           # Subdiretório para fotos de visitas
|-- venv/                 # Ambiente virtual (se criado)
|-- .env                  # Arquivo de variáveis de ambiente (opcional)
|-- config.py             # Configurações da aplicação
|-- requirements.txt      # Dependências Python
|-- run.py                # Script para iniciar a aplicação (usado por `flask run`)
|-- todo.md               # Lista de tarefas (desenvolvimento)
|-- README.md             # Este arquivo
|-- USER_GUIDE.md         # Guia do Usuário
|-- DEPLOYMENT.md         # Instruções de Deploy
```

