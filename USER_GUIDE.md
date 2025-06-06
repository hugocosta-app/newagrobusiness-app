# Guia do Usuário - Sistema New Agrobusiness

Bem-vindo ao Sistema de Gestão da New Agrobusiness! Este guia ajudará você a utilizar as funcionalidades disponíveis de acordo com o seu perfil (Administrador ou Vendedor).

## 1. Acesso ao Sistema

*   Acesse o sistema pelo endereço fornecido (ex: `http://newagrobusiness.com.br` ou o endereço local `http://127.0.0.1:5000` durante testes).
*   Utilize seu email e senha cadastrados para fazer login.
*   **Primeiro Acesso (Admin):** Use `admin@newagrobusiness.com.br` e a senha `adminpassword`. **É crucial alterar esta senha padrão o mais rápido possível.**
*   Caso esqueça sua senha, entre em contato com o administrador do sistema.

## 2. Visão Geral do Dashboard

Após o login, você será direcionado ao Dashboard. Esta é sua página inicial e oferece acesso rápido às principais funcionalidades do seu perfil.

*   **Administrador:** Verá links para Gerenciar Produtos, Ver Relatórios Gerais (Pedidos, Despesas, Visitas) e Visualizar Agenda da Equipe.
*   **Vendedor:** Verá links para Novo Pedido, Registrar Despesa, Registrar Visita e Minha Agenda.

## 3. Funcionalidades do Administrador

### 3.1. Gerenciar Produtos

*   Acesse pelo link no Dashboard ou menu de navegação.
*   **Listar Produtos:** Visualize todos os produtos cadastrados com ID, Nome e Preço.
*   **Adicionar Produto:**
    *   Clique em "Adicionar Novo Produto".
    *   Preencha Nome, Descrição (opcional) e Preço (use vírgula como separador decimal, ex: `150,99`).
    *   Clique em "Adicionar Produto".
*   **Editar Produto:**
    *   Na lista de produtos, clique em "Editar" ao lado do produto desejado.
    *   Modifique os campos necessários.
    *   Clique em "Atualizar Produto".
*   **Excluir Produto:**
    *   Na lista de produtos, clique em "Excluir" ao lado do produto desejado.
    *   Confirme a exclusão. (Atenção: Produtos associados a pedidos existentes podem não ser excluíveis).

### 3.2. Visualizar Todos os Pedidos

*   Acesse pelo menu "Pedidos" ou link no Dashboard.
*   Visualize a lista de todos os pedidos realizados por todos os vendedores.
*   A lista inclui ID, Data, Cliente, CNPJ, Valor Total, Status e Vendedor.
*   Clique em "Ver Detalhes" para visualizar um pedido específico.
*   Clique em "Baixar TXT" para gerar o relatório de um pedido individual.

### 3.3. Visualizar Todas as Despesas (Relatório)

*   Acesse pelo menu "Despesas" ou link no Dashboard.
*   Visualize a lista de todas as despesas registradas por todos os vendedores.
*   **Filtros:** Utilize os campos no topo da página para filtrar despesas por:
    *   Período (Data De/Até)
    *   Tipo de Despesa
    *   Vendedor
    *   Clique em "Filtrar" para aplicar.
*   **Relatório TXT:** Clique em "Gerar Relatório TXT" para baixar um arquivo de texto contendo as despesas que correspondem aos filtros aplicados.
*   Clique em "Ver Detalhes" para visualizar uma despesa específica, incluindo o anexo (nota fiscal).

### 3.4. Visualizar Todos os Relatórios de Visita

*   Acesse pelo menu "Visitas".
*   Visualize a lista de todos os relatórios de visita registrados pelos vendedores.
*   A lista inclui ID, Data, Cliente, Cidade/UF, Vendedor e quantidade de fotos.
*   Clique em "Ver Detalhes" para visualizar um relatório completo, incluindo resumo, destaques, observações e fotos anexadas.

### 3.5. Visualizar Agenda da Equipe

*   Acesse pelo menu "Agenda".
*   Por padrão, exibe a agenda do dia atual para todos os vendedores.
*   Utilize o seletor de data e clique em "Ver Agenda" para visualizar os compromissos de um dia específico.
*   A tabela mostra Vendedor, Localização, Descrição e data/hora do registro.

## 4. Funcionalidades do Vendedor

### 4.1. Criar Novo Pedido

*   Acesse pelo link no Dashboard ou menu "Pedidos" > "Novo Pedido".
*   **Dados do Cliente:** Preencha Nome, CNPJ e Endereço de Entrega.
*   **Adicionar Produtos:**
    *   No campo "Buscar Produto", comece a digitar o nome do produto.
    *   Uma lista de sugestões aparecerá. Clique no produto desejado.
    *   O produto será adicionado à tabela de itens.
*   **Ajustar Itens:**
    *   **Quantidade:** Altere a quantidade conforme necessário (mínimo 1).
    *   **Desconto (%):** Insira o percentual de desconto para aquele item (0 a 100, use ponto ou vírgula para decimais, ex: `10.5` ou `10,5`).
    *   **Remover:** Clique no botão "Remover" para tirar um item do pedido.
*   **Total do Pedido:** O valor total é calculado automaticamente.
*   **Finalizar:** Clique em "Criar Pedido".

### 4.2. Visualizar Meus Pedidos

*   Acesse pelo menu "Pedidos".
*   Visualize a lista dos seus pedidos realizados.
*   Clique em "Ver Detalhes" para visualizar um pedido específico.
*   Clique em "Baixar TXT" para gerar o relatório do pedido individual.

### 4.3. Registrar Despesa

*   Acesse pelo link no Dashboard ou menu "Despesas" > "Registrar Despesa".
*   Preencha os campos:
    *   **Data da Despesa:** Data em que ocorreu o gasto.
    *   **Tipo de Despesa:** Selecione na lista (Combustível, Pedágio, etc.).
    *   **Valor (R$):** Valor total da despesa (use vírgula, ex: `55,30`).
    *   **Nota Fiscal (Opcional):** Clique em "Escolher arquivo" para anexar a foto ou PDF da nota.
    *   **Cidade/Estado:** Local onde a despesa ocorreu.
    *   **KM Inicial/Final (Opcional):** Informe a quilometragem no início e fim do dia/trajeto para cálculo automático do KM total.
    *   **Descrição (Opcional):** Detalhes adicionais sobre a despesa.
*   Clique em "Registrar Despesa".

### 4.4. Visualizar Minhas Despesas

*   Acesse pelo menu "Despesas".
*   Visualize a lista das suas despesas registradas.
*   Clique em "Ver Detalhes" para visualizar uma despesa específica e seu anexo.
*   Clique em "Gerar Relatório TXT" para baixar um arquivo com suas despesas listadas.

### 4.5. Registrar Visita

*   Acesse pelo link no Dashboard ou menu "Visitas" > "Registrar Visita".
*   Preencha os campos:
    *   **Cliente Visitado:** Nome do cliente.
    *   **Data da Visita:** Data em que ocorreu a visita.
    *   **Cidade/Estado:** Local da visita.
    *   **Produtos Discutidos (Opcional):** Liste os produtos abordados.
    *   **Resumo da Visita:** Descrição concisa do que aconteceu.
    *   **Destaques (Opcional):** Pontos importantes da visita.
    *   **Observações (Opcional):** Informações adicionais.
    *   **Anexar Fotos (Opcional):** Clique em "Escolher arquivos" para selecionar uma ou mais fotos da visita (formatos de imagem permitidos).
*   Clique em "Registrar Visita".

### 4.6. Visualizar Meus Relatórios de Visita

*   Acesse pelo menu "Visitas".
*   Visualize a lista dos seus relatórios de visita.
*   Clique em "Ver Detalhes" para ver o relatório completo e as fotos anexadas.

### 4.7. Gerenciar Minha Agenda Semanal

*   Acesse pelo link no Dashboard ou menu "Agenda".
*   **Visualização:** Veja seus compromissos organizados por dia da semana atual.
*   **Navegação:** Use os botões "Semana Anterior" e "Próxima Semana" para navegar.
*   **Adicionar Compromisso:**
    *   Clique no botão "+ Adicionar" no dia desejado ou vá pelo menu "Agenda" > "Adicionar Compromisso".
    *   Preencha a Data, Localização e Descrição (opcional).
    *   Clique em "Adicionar Compromisso".
*   **Editar Compromisso:**
    *   Na visualização semanal, clique em "Editar" no compromisso desejado.
    *   Modifique os campos.
    *   Clique em "Atualizar Compromisso".
*   **Excluir Compromisso:**
    *   Na visualização semanal, clique em "Excluir" no compromisso desejado.
    *   Confirme a exclusão.

## 5. Dicas Gerais

*   Mantenha seus dados atualizados.
*   Em caso de dúvidas ou problemas, contate o administrador do sistema.
*   Utilize senhas seguras e não as compartilhe.

