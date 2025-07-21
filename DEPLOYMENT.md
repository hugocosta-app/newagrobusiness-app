# Guia de Deploy e Publicação - Sistema New Agrobusiness

Este guia fornece instruções sobre como publicar (fazer o deploy) do Sistema New Agrobusiness para que ele fique acessível online através do seu domínio `newagrobusiness.com.br`.

## 1. Recomendações de Hospedagem (Custo-Benefício para Flask)

Para hospedar uma aplicação Flask como esta, existem várias opções. Considerando facilidade de uso e custo-benefício, recomendamos plataformas do tipo PaaS (Platform-as-a-Service):

1.  **PythonAnywhere:**
    *   **Prós:** Muito fácil de usar para iniciantes em Flask, possui um plano gratuito funcional (com limitações) e planos pagos acessíveis. Configuração simplificada para domínios personalizados.
    *   **Contras:** Menos flexibilidade que um VPS, pode ter limitações de recursos nos planos mais baratos.
    *   **Ideal para:** Quem busca a forma mais simples de colocar a aplicação no ar rapidamente.

2.  **Render:**
    *   **Prós:** Interface moderna, planos gratuitos para web services (com limitações, como "dormir" após inatividade), deploy via Git ou Docker, bancos de dados gerenciados (PostgreSQL gratuito).
    *   **Contras:** O plano gratuito pode ser lento para iniciar após inatividade. Configuração pode exigir um pouco mais de conhecimento que o PythonAnywhere.
    *   **Ideal para:** Quem quer um bom equilíbrio entre facilidade, recursos modernos e um plano gratuito inicial.

3.  **Heroku:**
    *   **Prós:** Plataforma muito popular e madura, vasta documentação, muitos add-ons (serviços extras). Deploy via Git.
    *   **Contras:** Descontinuou os planos gratuitos em 2022. Seus planos pagos podem ser um pouco mais caros que alternativas como Render ou PythonAnywhere para o mesmo nível de performance inicial.
    *   **Ideal para:** Projetos que podem precisar de integrações específicas disponíveis como add-ons Heroku.

4.  **DigitalOcean App Platform / AWS Elastic Beanstalk / Google App Engine:**
    *   **Prós:** Plataformas de nuvem robustas, escaláveis e com muitos recursos.
    *   **Contras:** Geralmente mais complexas de configurar e gerenciar que as opções anteriores. Podem ter custos mais variáveis dependendo do uso.
    *   **Ideal para:** Aplicações maiores ou que já fazem parte de um ecossistema maior nessas nuvens.

**Recomendação Inicial:** Para facilidade e custo-benefício, **PythonAnywhere** ou **Render** são excelentes pontos de partida.

## 2. Preparação para o Deploy

Antes de fazer o deploy, alguns ajustes são necessários para o ambiente de produção:

1.  **Banco de Dados:**
    *   O SQLite (`app.db`) funciona bem localmente, mas **não é recomendado para produção** em muitas plataformas (especialmente aquelas com sistemas de arquivos efêmeros como Heroku ou Render). Ele pode levar à perda de dados ou problemas de concorrência.
    *   **Recomendado:** Migrar para um banco de dados mais robusto como **PostgreSQL**. A maioria das plataformas PaaS oferece planos de PostgreSQL gerenciado (inclusive gratuitos ou de baixo custo).
    *   **Ajuste no Código:** Se migrar, você precisará:
        *   Instalar o driver: `pip install psycopg2-binary` (adicione ao `requirements.txt`).
        *   Configurar a `DATABASE_URL` no seu ambiente de produção (a plataforma de hospedagem geralmente fornece essa URL). Veja o exemplo comentado no arquivo `.env` ou `config.py`.

2.  **Servidor WSGI:**
    *   O servidor de desenvolvimento do Flask (`flask run`) **não é adequado para produção**.
    *   Você precisará de um servidor WSGI como **Gunicorn** ou **uWSGI**.
    *   **Instalação:** `pip install gunicorn` (adicione ao `requirements.txt`).

3.  **Variáveis de Ambiente:**
    *   **SECRET_KEY:** Defina uma chave secreta forte e única no ambiente de produção. Não use a chave padrão.
    *   **DATABASE_URL:** (Se aplicável) Defina a URL do seu banco de dados de produção.
    *   As plataformas de hospedagem possuem mecanismos para configurar essas variáveis de ambiente de forma segura.

4.  **Arquivo `Procfile` (Para Heroku/Render):**
    *   Se usar Heroku ou Render, crie um arquivo chamado `Procfile` (sem extensão) na raiz do projeto.
    *   Conteúdo (exemplo usando Gunicorn):
        ```Procfile
        web: gunicorn run:app
        ```
        *   Isso informa à plataforma como iniciar sua aplicação. `run:app` refere-se à variável `app` dentro do arquivo `run.py` (ou onde quer que sua instância Flask seja criada/importada).
        *   **Ajuste:** O arquivo `run.py` atual está vazio. Precisamos configurá-lo para importar e executar `create_app`:
            ```python
            # /home/ubuntu/newagrobusiness_app/run.py
            from app import create_app
            
            app = create_app()
            
            # A linha abaixo é apenas para execução local com `python run.py`
            # Em produção, o Gunicorn/uWSGI chamará diretamente o objeto `app`.
            if __name__ == \"__main__\":
                app.run(debug=False) # Certifique-se que debug=False para produção
            ```

5.  **Debug Mode:** Certifique-se de que `debug=False` ao executar em produção (geralmente o padrão se não for definido explicitamente ou se `FLASK_ENV` não for `development`).

## 3. Processo Geral de Deploy (Exemplo com Render)

O processo varia um pouco entre as plataformas, mas geralmente envolve:

1.  **Criar Conta:** Registre-se na plataforma escolhida (ex: Render.com).
2.  **Código Fonte:** Envie seu código para um repositório Git (GitHub, GitLab, Bitbucket). Render e outras plataformas se conectam diretamente a esses repositórios.
3.  **Criar Novo Serviço Web:**
    *   Na plataforma (Render), escolha "New" > "Web Service".
    *   Conecte seu repositório Git.
    *   **Configurações:**
        *   **Nome:** Escolha um nome (ex: `newagrobusiness-app`).
        *   **Região:** Escolha a mais próxima.
        *   **Branch:** `main` ou a branch que contém o código final.
        *   **Build Command:** `pip install -r requirements.txt`
        *   **Start Command:** `gunicorn run:app` (ou o comando do seu `Procfile`).
        *   **Plano:** Escolha o plano (comece com o gratuito, se disponível).
4.  **Variáveis de Ambiente:**
    *   Na seção "Environment" ou "Config Vars", adicione suas variáveis de produção (`SECRET_KEY`, `DATABASE_URL` se aplicável).
5.  **Banco de Dados (Se usar PostgreSQL):**
    *   Crie um serviço de banco de dados PostgreSQL na plataforma.
    *   Copie a "Internal Database URL" fornecida.
    *   Adicione essa URL como a variável de ambiente `DATABASE_URL` no seu Web Service.
6.  **Deploy:** Clique em "Create Web Service" ou "Deploy". A plataforma buscará o código, instalará dependências e iniciará a aplicação.
7.  **Acesso:** A plataforma fornecerá uma URL pública (ex: `newagrobusiness-app.onrender.com`). Teste o acesso.

## 4. Configuração do Domínio (`newagrobusiness.com.br`)

Após a aplicação estar rodando na URL fornecida pela hospedagem:

1.  **Adicionar Domínio Personalizado:**
    *   Na plataforma de hospedagem (Render, PythonAnywhere, etc.), procure a seção "Custom Domains" ou "Domains".
    *   Adicione seu domínio: `newagrobusiness.com.br` (e talvez `www.newagrobusiness.com.br`).
2.  **Configurar DNS:**
    *   A plataforma de hospedagem fornecerá instruções de configuração de DNS. Geralmente, isso envolve adicionar um registro `CNAME` ou `A` no painel de controle onde seu domínio está registrado (Registro.br, GoDaddy, Cloudflare, etc.).
    *   **Exemplo (CNAME):** Você pode precisar criar um registro CNAME para `www` apontando para a URL fornecida pela hospedagem (ex: `www CNAME newagrobusiness-app.onrender.com`).
    *   **Exemplo (A Record):** Para o domínio raiz (`newagrobusiness.com.br`), algumas plataformas fornecem um endereço IP para criar um registro `A`. Outras (como Render) podem usar um registro `ALIAS` ou `ANAME` se o seu provedor de DNS suportar, apontando para a URL da hospedagem.
    *   **Siga as instruções específicas da sua plataforma de hospedagem.**
3.  **Propagação DNS:** Pode levar de alguns minutos a 48 horas para que as alterações de DNS se propaguem pela internet.
4.  **SSL/HTTPS:** A maioria das plataformas PaaS (Render, PythonAnywhere) oferece certificados SSL gratuitos e automáticos para domínios personalizados (Let's Encrypt). Verifique se a opção está ativada.

## 5. Manutenção e Atualizações

*   Para atualizar a aplicação, basta enviar as novas alterações para o seu repositório Git (na branch configurada). A plataforma de hospedagem geralmente detecta as mudanças e faz o deploy automaticamente (ou você pode acioná-lo manualmente).
*   Monitore os logs da aplicação através do painel da plataforma de hospedagem para identificar erros.
*   Faça backups regulares do banco de dados (muitas plataformas oferecem backups automáticos para bancos de dados gerenciados).

Este guia fornece uma visão geral. Consulte sempre a documentação específica da plataforma de hospedagem escolhida para obter detalhes precisos.
