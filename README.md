# Habilita+

Projeto desenvolvido para a matéria de Back-End da 5ª fase de Sistemas de Informação na UDESC.

A ideia é ser um sistema simples de autoescola digital feito em Django. Ele tem cadastro e login de aluno, dashboard com progresso da CNH, agendamento de aulas e exames, histórico, pagamentos, certificados e avaliações dos instrutores.

## Como o projeto está separado

- `apps/`: parte do back-end em Python.
- `templates/`: páginas HTML que aparecem para o usuário.
- `static/`: CSS, JavaScript e imagens.
- `habilita_mais/`: configurações principais do Django.

Dentro de `apps/` cada funcionalidade ficou em um app separado:

- `accounts`: login, cadastro e perfil.
- `agendamentos`: aulas e exames.
- `progresso`: dashboard, histórico e certificados.
- `pagamentos`: boletos e comprovantes.
- `avaliacoes`: notas e feedback dos instrutores.
- `core`: página inicial e suporte.

## Como rodar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Depois é só abrir:

```text
http://127.0.0.1:8000/
```

## Admin

Para criar um usuário administrador:

```bash
python manage.py createsuperuser
```

No meu ambiente local usei:

```text
Login: admin
Senha: admin123
Email: admin@habilita.com
```

## Observações

O arquivo `.env` e o banco `db.sqlite3` ficam só na máquina local e não vão para o GitHub. No repositório fica apenas o `.env.example`.
