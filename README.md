# Habilita+

Sistema web de gestão de habilitação digital desenvolvido em Django.

## Funcionalidades

- Landing page pública.
- Login, cadastro e perfil de aluno.
- Dashboard com progresso da CNH.
- Agendamento de aulas práticas e exames.
- Listagem e cancelamento lógico de agendamentos.
- Histórico de aulas.
- Gestão de pagamentos, boletos e comprovantes.
- Certificados digitais.
- Avaliações de instrutores e simulados.
- Administração dos dados pelo Django Admin.

## Estrutura

```text
habilita_mais/
|-- habilita_mais/          # Configuração principal do Django
|-- apps/                   # Apps separados por domínio
|   |-- core/               # Landing page e suporte
|   |-- accounts/           # Autenticação, cadastro e perfil
|   |-- agendamentos/       # Aulas e exames
|   |-- progresso/          # Dashboard, histórico e certificados
|   |-- pagamentos/         # Pagamentos e comprovantes
|   `-- avaliacoes/         # Avaliações e resultados
|-- templates/              # Templates HTML globais
|-- static/                 # CSS, JavaScript e imagens
|-- manage.py
|-- requirements.txt
|-- .env.example
`-- superuser.txt
```

## Arquitetura

- Cada app possui seu próprio `urls.py`.
- Views organizadas dentro de pastas `views/`, separadas por responsabilidade.
- Rotas internas protegidas com `@login_required(login_url="/login/")`.
- Persistência feita com ORM do Django.
- Models principais possuem campo `ativo` para deleção lógica.
- Configurações sensíveis são lidas de variáveis de ambiente.
- Models registrados no Django Admin com `list_display`, `list_filter` e `search_fields`.

## Como rodar localmente

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Admin

Crie um superusuário com:

```bash
python manage.py createsuperuser
```

Credenciais de referência usadas no ambiente local:

```text
Usuário: admin
Senha: admin123
Email: admin@habilita.com
```
