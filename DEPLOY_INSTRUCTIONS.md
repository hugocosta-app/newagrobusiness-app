# Instruções de Deploy - New Agro Business

Este documento contém as instruções para fazer o deploy da aplicação New Agro Business no Render.

## Pré-requisitos

- Conta no [Render](https://render.com/)
- Conta no [GitHub](https://github.com/)
- Repositório do projeto no GitHub

## Passos para Deploy

### 1. Preparação do Repositório

1. Certifique-se de que todos os arquivos estão atualizados no repositório GitHub:
   ```
   git add .
   git commit -m "Implementação do acesso de vendedores"
   git push origin main
   ```

### 2. Deploy no Render

1. Acesse o [Dashboard do Render](https://dashboard.render.com/)
2. Clique em "New" e selecione "Web Service"
3. Conecte ao repositório GitHub do projeto
4. Configure o serviço:
   - **Nome**: newagrobusiness-app
   - **Ambiente**: Python
   - **Build Command**: `pip install -r requirements.txt && python -m flask cli init-db`
   - **Start Command**: `gunicorn run:app`
   - **Plano**: Free (ou outro de sua escolha)

5. Adicione as seguintes variáveis de ambiente:
   - `FLASK_APP`: run.py
   - `FLASK_ENV`: production
   - `SECRET_KEY`: (gere uma chave secreta forte)

6. Clique em "Create Web Service"

### 3. Verificação do Deploy

1. Aguarde o processo de build e deploy ser concluído
2. Acesse a URL fornecida pelo Render para verificar se a aplicação está funcionando corretamente
3. Teste o login com as credenciais:
   - Admin: admin@newagrobusiness.com.br / adminpassword
   - Vendedor: vendedor1@newagrobusiness.com.br / vendedor123

### 4. Solução de Problemas

Se encontrar problemas durante o deploy:

1. Verifique os logs no dashboard do Render
2. Certifique-se de que todas as dependências estão listadas no arquivo `requirements.txt`
3. Verifique se o comando de inicialização do banco de dados está funcionando corretamente

## Manutenção

Para atualizar a aplicação após fazer alterações:

1. Faça commit e push das alterações para o GitHub
2. O Render detectará automaticamente as alterações e iniciará um novo deploy
3. Para forçar a recriação do banco de dados, você pode:
   - Acessar o dashboard do Render
   - Ir para o serviço da aplicação
   - Clicar em "Manual Deploy" e selecionar "Clear build cache & deploy"

## Acesso ao Sistema

### Usuários Padrão

- **Administrador**:
  - Email: admin@newagrobusiness.com.br
  - Senha: adminpassword

- **Vendedor 1**:
  - Email: vendedor1@newagrobusiness.com.br
  - Senha: vendedor123

- **Vendedor 2**:
  - Email: vendedor2@newagrobusiness.com.br
  - Senha: vendedor123

### Funcionalidades por Tipo de Usuário

- **Administrador**:
  - Acesso a todos os dados de todos os vendedores
  - Gerenciamento de usuários (criar, editar, desativar)
  - Gerenciamento de produtos
  - Visualização de todos os pedidos, despesas, visitas e agenda

- **Vendedor**:
  - Acesso apenas aos seus próprios dados
  - Criação e gerenciamento de seus pedidos
  - Registro de despesas
  - Registro de visitas a clientes
  - Gerenciamento de sua agenda

