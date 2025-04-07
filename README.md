# 📦 Sistema de Controle de Estoque

Um sistema web simples e eficiente para controle de produtos em estoque, com autenticação de usuários, movimentações (entrada/saída), relatórios e visualização com gráficos.

## 🔧 Tecnologias Utilizadas

- Python 3
- Flask
- SQLite3
- HTML + CSS (interface)
- Jinja2 (templates HTML)
- Chart.js (gráficos dinâmicos)
- bcrypt (hash de senha)

## 🚀 Funcionalidades

### 🧑‍💼 Autenticação
- Login e logout
- Perfis de acesso (Administrador / Comum)
- Sessões de usuário
- Criação de contas (Admin pode cadastrar usuários)

### 📦 Gestão de Produtos
- Cadastro, edição e exclusão de produtos
- Movimentações de entrada e saída
- Histórico completo por produto
- Filtros por quantidade mínima

### 📊 Relatórios & Gráficos
- Listagem com alertas visuais de estoque baixo
- Histórico de movimentações
- Gráficos interativos usando Chart.js
- Agrupamento por data e tipo de movimentação

### 🔐 Segurança
- Hash de senhas com `bcrypt`
- Validações de formulário
- Sessões protegidas




