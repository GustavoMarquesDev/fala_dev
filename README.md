# 🚀 Fala Dev!!!

Uma plataforma completa de perguntas e respostas para desenvolvedores, inspirada no Stack Overflow, onde você pode fazer perguntas, responder dúvidas da comunidade e interagir com outros desenvolvedores.

![Django](https://img.shields.io/badge/Django-5.2.5-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Usar](#-como-usar)
- [Funcionalidades Detalhadas](#-funcionalidades-detalhadas)
- [Desenvolvimento](#-desenvolvimento)

---

## 🎯 Sobre o Projeto

**Fala Dev!!!** é uma plataforma colaborativa onde desenvolvedores podem:

- Fazer perguntas técnicas sobre programação
- Responder perguntas da comunidade
- Avaliar respostas com likes/dislikes
- Visualizar perfis de outros desenvolvedores
- Receber notificações sobre interações
- Gerenciar suas próprias perguntas e respostas

O projeto foi desenvolvido com Django 5.2.5, seguindo boas práticas de desenvolvimento web e oferecendo uma experiência de usuário moderna e intuitiva.

---

## ✨ Funcionalidades

### 🔐 Autenticação e Perfil

- ✅ Sistema de cadastro e login
- ✅ Perfil de usuário com foto, nome, email e profissão
- ✅ Edição de perfil e atualização de senha
- ✅ Visualização de perfis de outros usuários
- ✅ Estatísticas de perguntas e respostas por usuário

### 💬 Sistema de Perguntas e Respostas

- ✅ Criação de perguntas com título, descrição e categoria
- ✅ Upload de múltiplas imagens por pergunta
- ✅ Sistema de respostas com suporte a imagens
- ✅ Respostas aninhadas (respostas de respostas)
- ✅ Edição e exclusão de perguntas e respostas
- ✅ Visualização detalhada de perguntas e todas as respostas

### 👍 Sistema de Avaliação

- ✅ Likes e dislikes em respostas
- ✅ Contagem de avaliações em tempo real
- ✅ Score total (likes - dislikes)
- ✅ Prevenção de auto-avaliação

### 🔔 Notificações

- ✅ Notificações quando alguém responde sua pergunta
- ✅ Notificações quando alguém responde sua resposta
- ✅ Sistema de marcação de notificações como lidas
- ✅ Contador de notificações não lidas na navbar

### 🔍 Busca e Filtros

- ✅ Busca por título, descrição ou categoria
- ✅ Filtro por categoria (mais de 50 categorias disponíveis)
- ✅ Paginação de resultados
- ✅ Ordenação por data de criação

### 📱 Interface

- ✅ Design responsivo com Bootstrap 5
- ✅ Interface moderna e intuitiva
- ✅ Font Awesome para ícones
- ✅ Mensagens de feedback para o usuário
- ✅ Navegação intuitiva

---

## 🛠 Tecnologias Utilizadas

### Backend

- **Django 5.2.5** - Framework web Python
- **Python 3.11+** - Linguagem de programação
- **SQLite** - Banco de dados (desenvolvimento)
- **Pillow** - Processamento de imagens

### Frontend

- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Biblioteca de ícones
- **JavaScript** - Interatividade
- **HTML5/CSS3** - Estrutura e estilização

### Ferramentas

- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **django-browser-reload** - Recarregamento automático no desenvolvimento
- **crispy-forms** - Formulários estilizados

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11 ou superior**
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar o repositório)

---

## 🚀 Instalação

### 1. Clone o repositório (ou baixe o projeto)

```bash
git clone https://github.com/seu-usuario/fala_dev.git
cd fala_dev
```

### 2. Crie um ambiente virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. Crie um superusuário (opcional, para acessar o admin)

```bash
python manage.py createsuperuser
```

### 6. Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

O projeto estará disponível em: **http://127.0.0.1:8000/**

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**⚠️ Importante:** Em produção, defina `DEBUG=False` e use uma `SECRET_KEY` segura.

### Exemplo de arquivo `.env`:

```env
# Desenvolvimento
SECRET_KEY=django-insecure-sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=

# Produção (exemplo)
# SECRET_KEY=sua-chave-super-secreta-aqui
# DEBUG=False
# ALLOWED_HOSTS=seudominio.com,www.seudominio.com
```

---

## 📁 Estrutura do Projeto

```
fala_dev/
│
├── core/                          # Arquivos globais
│   ├── global_templates/          # Templates base
│   │   ├── base.html
│   │   └── parciais/              # Componentes reutilizáveis
│   └── static/                    # Arquivos estáticos
│       └── assets/
│           ├── bootstrap/         # Bootstrap CSS/JS
│           ├── custom/            # CSS/JS personalizados
│           └── font-awesome/      # Ícones
│
├── lista/                         # App principal (perguntas/respostas)
│   ├── migrations/               # Migrações do banco
│   ├── templates/               # Templates do app
│   ├── forms.py                 # Formulários
│   ├── models.py                # Modelos (importados de perfil)
│   ├── urls.py                  # URLs do app
│   └── views.py                 # Views do app
│
├── perfil/                       # App de autenticação e perfil
│   ├── migrations/              # Migrações do banco
│   ├── templates/              # Templates do app
│   ├── forms.py                # Formulários
│   ├── models.py               # Modelos (Perfil, Perguntas, Respostas, etc.)
│   ├── urls.py                 # URLs do app
│   ├── views.py                # Views do app
│   └── context_processors.py   # Processadores de contexto
│
├── project/                      # Configurações do Django
│   ├── settings.py             # Configurações
│   ├── urls.py                 # URLs principais
│   ├── wsgi.py                 # WSGI
│   └── asgi.py                 # ASGI
│
├── utils/                        # Utilitários
│   └── redimensiona_imagem.py  # Redimensionamento de imagens
│
├── media/                        # Arquivos de mídia (uploads)
│   ├── erros/                   # Fotos de erros
│   ├── perfil/                  # Fotos de perfil
│   └── respostas/               # Fotos de respostas
│
├── db.sqlite3                    # Banco de dados SQLite
├── manage.py                     # Script de gerenciamento Django
├── requirements.txt              # Dependências do projeto
└── README.md                     # Este arquivo
```

---

## 🎮 Como Usar

### Para Usuários

1. **Criar uma conta:**

   - Acesse `/perfil/criar/`
   - Preencha os dados e crie sua conta

2. **Fazer login:**

   - Acesse `/perfil/login`
   - Entre com seu username e senha

3. **Fazer uma pergunta:**

   - Clique em "Perguntar" na navbar
   - Preencha título, descrição, categoria e adicione imagens (opcional)
   - Publique sua pergunta

4. **Responder perguntas:**

   - Visualize uma pergunta clicando nela
   - Clique em "Responder" e escreva sua resposta
   - Adicione imagens se necessário

5. **Avaliar respostas:**

   - Use os botões de like/dislike nas respostas
   - Veja a contagem de avaliações em tempo real

6. **Ver notificações:**

   - Acesse o menu de notificações na navbar
   - Veja todas as interações com suas perguntas/respostas

7. **Visualizar perfis:**
   - Clique no nome de qualquer usuário
   - Veja informações e estatísticas do perfil

### Para Desenvolvedores

#### Executar testes (quando implementados):

```bash
python manage.py test
```

#### Criar migrações após alterar modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Acessar o admin do Django:

```bash
# Após criar superusuário
# Acesse: http://127.0.0.1:8000/admin/
```

#### Coletar arquivos estáticos (produção):

```bash
python manage.py collectstatic
```

---

## 🔧 Funcionalidades Detalhadas

### Sistema de Categorias

O sistema suporta mais de 50 categorias, incluindo:

- Linguagens: Python, JavaScript, Java, C#, PHP, etc.
- Frameworks: React, Angular, Vue, Node.js, Express, etc.
- Bancos de dados: MySQL, PostgreSQL, MongoDB, Firebase, etc.
- Cloud: AWS, Azure, Docker, Kubernetes, etc.
- Mobile: Flutter, iOS, Android, etc.
- E muitas outras...

### Sistema de Respostas Aninhadas

- Respostas podem ter respostas (respostas de respostas)
- Suporte a múltiplos níveis de aninhamento
- Notificações para todos os envolvidos na conversa

### Sistema de Notificações

- Notificações automáticas quando:
  - Alguém responde sua pergunta
  - Alguém responde sua resposta
  - Alguém responde uma resposta que você respondeu
- Contador visual de notificações não lidas
- Marcação individual ou em massa como lidas

### Upload de Imagens

- Redimensionamento automático de imagens
- Suporte a múltiplas imagens por pergunta
- Imagens em respostas
- Fotos de perfil
- Otimização de qualidade e tamanho

### Sistema de Busca

- Busca por:
  - Título da pergunta
  - Descrição da pergunta
  - Categoria
- Resultados paginados
- Ordenação por data (mais recentes primeiro)

---

## 🛠 Desenvolvimento

### Adicionar Nova Funcionalidade

1. Crie uma nova branch:

```bash
git checkout -b feature/nova-funcionalidade
```

2. Faça suas alterações

3. Crie migrações se necessário:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Teste localmente

5. Commit e push:

```bash
git add .
git commit -m "Adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade
```

### Estrutura de Modelos Principais

- **Perfil**: Informações do usuário
- **PerguntasDoUsuario**: Perguntas da plataforma
- **RespostasDoUsuario**: Respostas às perguntas
- **RespostaDaResposta**: Respostas aninhadas
- **AvaliacaoResposta**: Likes/dislikes em respostas
- **AvaliacaoRespostaDaResposta**: Likes/dislikes em respostas aninhadas
- **Notificacao**: Sistema de notificações
- **FotoErro**: Fotos anexadas às perguntas

### Padrões de Código

- Views baseadas em classes (Class-Based Views)
- Templates organizados por app
- Formulários usando Django Forms
- Nomes de URLs descritivos
- Mensagens de feedback para o usuário
- Tratamento de erros adequado

---

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

## 👥 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

---

## 📧 Contato

Para dúvidas, sugestões ou problemas, abra uma issue no repositório.

---

## 🙏 Agradecimentos

- Django Community
- Bootstrap Team
- Font Awesome
- Todos os desenvolvedores que contribuem para o ecossistema Python/Django

---

**Desenvolvido com ❤️ usando Django**
