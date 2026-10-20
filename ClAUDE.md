# Earthquake API

Backend Django/DRF que consome a API do USGS, salva em PostgreSQL e expõe uma API REST somente leitura. Frontend estático (globo 3D com Globe.gl) em `earthquake_map/`.

## Estrutura
- `main/` — configuração do Django (settings, urls, wsgi)
- `earthquakes/` — único app: models, serializers, views, filters, pagination
- `earthquakes/management/commands/fetch_earthquakes.py` — ingestão idempotente (`update_or_create` por `external_id`)
- `earthquake_map/` — frontend HTML/CSS/JS puro, sem build tool/npm
- `.github/workflows/deploy.yml` — publica `earthquake_map/` no GitHub Pages a cada push na `main`

## Comandos
- Rodar servidor: `python manage.py runserver`
- Migrations: `python manage.py makemigrations` e `python manage.py migrate` (só `makemigrations` quando alterar `models.py`)
- Ingestão manual: `python manage.py fetch_earthquakes`
- Estáticos (produção): `python manage.py collectstatic --noinput`
- Frontend local: abrir `earthquake_map/index.html` com Live Server

## Regras importantes
- `load_dotenv()` deve ser a **primeira** coisa em `main/settings.py`, antes de qualquer `os.getenv`.
- `DEBUG = os.getenv('DEBUG') == 'True'` (sensível a maiúsculas).
- Nunca commitar `.env`, `staticfiles/`, `venv/` nem `__pycache__/`.
- Sempre commitar a migration junto com a alteração do model.
- Senha do banco local sem caracteres especiais (`#`, `@`, `:` quebram a `DATABASE_URL`).
- A API é somente leitura: não adicionar endpoints de escrita.
- O timestamp do USGS vem em **milissegundos** (dividir por 1000). Coordenadas GeoJSON: `[lon, lat, depth]`.
- CORS: `CORS_ALLOWED_ORIGINS` aceita só origem (protocolo + domínio), sem caminho e sem barra final.
- Frontend: não carregar `three.min.js` separado, o Globe.gl já inclui Three.js (duplicar causa esfera preta).

## Deploy (Render + GitHub Pages)
- Web Service `recent-earthquakes`. Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`. Start: `gunicorn main.wsgi`.
- Cron Job `fetch-earthquakes-job`: `python manage.py fetch_earthquakes`, schedule `0 */6 * * *`.
- Plano Free não tem Shell: usar Cron Job para comandos pontuais.
- **Postgres Free do Render expira em ~30 dias.** Para recriar: novo Postgres → trocar `DATABASE_URL` no Web Service primeiro (o `migrate` recria as tabelas) → aguardar o deploy → trocar no Cron Job → disparar execução manual. Usar a Internal Database URL, nunca a local.
- Um 502 do USGS faz o Cron Job falhar, mas é transitório: a próxima execução corrige.
- Frontend: https://gabriel-braga-ol.github.io/earthquake_api/ (Source do Pages = "GitHub Actions"). A URL da API está fixa em `earthquake_map/script.js`.

## Convenções
- Commits no estilo Conventional Commits (`feat:`, `fix:`, `docs:`, `ci:`), no imperativo e descrevendo o que foi entregue.
- Mudanças grandes ou arriscadas vão em branch própria (ex.: `feature/...`) e só entram na `main` depois de validadas.
- Nunca usar `--amend` em commit já enviado (push).

## Pendências conhecidas
- Retry/backoff no `fetch_earthquakes`.
- Reintroduzir filtros (magnitude, local, data) na interface do globo.
- Migrar o Postgres para um provedor sem expiração.
- Testes automatizados, lint e Swagger (drf-spectacular).