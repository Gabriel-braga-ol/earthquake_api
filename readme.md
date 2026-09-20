# 🌍 Earthquake API

Backend em Django que consome a API pública de terremotos do USGS (United States Geological Survey), persiste os dados de forma idempotente em PostgreSQL e expõe uma API REST própria, somente leitura, com filtros e paginação. O projeto inclui um frontend com um globo 3D interativo (Three.js / Globe.gl) para visualização dos terremotos e dos limites das placas tectônicas.

**🔗 Demo ao vivo:**
- Frontend: https://gabriel-braga-ol.github.io/earthquake_api/
- API: https://recent-earthquakes.onrender.com/api/earthquakes/

## 📌 Sobre o projeto

O projeto permite visualizar ocorrências de terremotos recentes (últimos 30 dias) com magnitudes superiores a 4,5 Richter de forma acessível e interativa, combinando:

1. **Ingestão de dados**: um management command consome o endpoint `query` da API do USGS, buscando terremotos de magnitude 4.5+ dos últimos 30 dias, e persiste esses dados usando `update_or_create` (com `external_id` como chave de busca) — garantindo que reexecuções nunca dupliquem registros.
2. **Exposição de dados**: uma API REST (Django REST Framework), somente leitura, expõe os terremotos salvos com filtros e paginação customizável.
3. **Visualização**: um frontend estático, separado do backend, consome essa API e renderiza os terremotos num globo 3D, com altura e cor dos pontos representando a magnitude, tooltips com detalhes, e os limites das placas tectônicas sobrepostos.

## ⚙️ Principais funcionalidades

- Ingestão automatizada e idempotente de terremotos via API pública do USGS
- API REST somente leitura (`GET`) — sem endpoints de escrita, por design (a única fonte legítima de dados é o `fetch_earthquakes`)
- Filtros customizados: magnitude mínima (`min_magnitude`), local (`place`, busca parcial) e intervalo de data (`start_date`/`end_date`)
- Paginação customizável via query param (`page_size`), com classe de paginação própria
- CORS configurado de forma restritiva (lista explícita de origens permitidas)
- Frontend com globo 3D interativo:
  - Altura de cada ponto proporcional à magnitude do terremoto
  - Cor diferenciada por faixa de magnitude (branco para < 5, vermelho para ≥ 5)
  - Tooltip ao passar o mouse, com local, magnitude, profundidade e data formatada
  - Limites das placas tectônicas sobrepostos (dataset público baseado em Peter Bird, 2003)
- Execução periódica automatizada do `fetch_earthquakes` em produção (Cron Job, a cada 6 horas)
- Deploy completo: backend + banco de dados no Render, frontend estático no GitHub Pages via GitHub Actions

## 🚀 Tecnologias utilizadas

**Backend**
- Python / Django
- Django REST Framework
- django-filter (filtros customizados)
- django-cors-headers (CORS)
- psycopg2-binary (driver PostgreSQL)
- dj-database-url (configuração de banco via `DATABASE_URL`)
- python-dotenv (variáveis de ambiente locais)
- whitenoise (arquivos estáticos em produção)
- gunicorn (servidor WSGI de produção)
- requests (consumo da API do USGS)
- PostgreSQL

**Frontend**
- HTML, CSS e JavaScript puro (sem framework, sem build tool/npm)
- Three.js / Globe.gl (globo 3D), carregado via CDN
- `fetch()` assíncrono (`async`/`await`) para consumir a API

**Infraestrutura**
- Render (Web Service + PostgreSQL + Cron Job)
- GitHub Pages + GitHub Actions (deploy do frontend)

## 🏗️ Arquitetura

```
Fonte externa (API do USGS)
        │
        │  fetch_earthquakes (management command, requests + update_or_create)
        ▼
Banco de dados (PostgreSQL)
        │
        │  Django REST Framework (serializer + viewset + filtros + paginação)
        ▼
API REST própria (/api/earthquakes/)
        │
        │  fetch() via JavaScript (CORS)
        ▼
Frontend estático (globo 3D, Globe.gl)
```

Backend e frontend são desacoplados: o frontend não é servido pelo Django (não usa `templates/`/`static/` para a página em si) — é um site estático publicado separadamente, que consome a API como qualquer cliente externo faria.

## 📁 Estrutura das principais pastas e arquivos

```
earthquake_api/
├── main/                       # projeto Django (configuração)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── earthquakes/                 # app Django (domínio único: terremotos)
│   ├── models.py                # model Earthquake
│   ├── serializers.py           # EarthquakeSerializer
│   ├── views.py                 # EarthquakeViewSet
│   ├── urls.py                  # roteamento via DefaultRouter
│   ├── filters.py                # EarthquakeFilter (django-filter)
│   ├── pagination.py             # EarthquakePagination (page_size customizável)
│   └── management/
│       └── commands/
│           └── fetch_earthquakes.py   # ingestão idempotente da API do USGS
├── earthquake_map/               # frontend (HTML/CSS/JS puro, globo 3D)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions: publica earthquake_map/ no GitHub Pages
├── manage.py
├── requirements.txt
└── .env                          # variáveis de ambiente locais (não versionado)
```

## ✅ Pré-requisitos

- Python 3.x instalado
- PostgreSQL instalado e rodando localmente (ou acesso a uma instância remota)
- pip / venv
- Um servidor estático simples para o frontend (ex: extensão **Live Server** do VS Code) — o frontend não depende do Django para rodar

## 🔧 Instalação

```bash
# clone o repositório
git clone <url-do-repositorio>
cd earthquake_api

# crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# instale as dependências
pip install -r requirements.txt
```

## 🔑 Configuração de variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (mesmo nível de `manage.py`), com as seguintes variáveis:

| Variável | Descrição | Exemplo / observação |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django | gerada pelo Django ao criar o projeto |
| `DEBUG` | Ativa/desativa modo debug | `True` localmente, `False` em produção — a comparação no código é sensível a maiúsculas (`os.getenv('DEBUG') == 'True'`) |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula | opcional localmente (tem valor padrão `localhost,127.0.0.1`); obrigatório em produção |
| `DATABASE_URL` | URL de conexão do PostgreSQL, formato `postgresql://usuario:senha@host:porta/nome_do_banco` | valores com caracteres especiais (ex: `#`) na senha podem quebrar o parsing da URL — evite ou faça URL encoding |


## ▶️ Como rodar o projeto localmente

### Backend

```bash
# aplique as migrations
python manage.py migrate

# popule o banco com os terremotos mais recentes
python manage.py fetch_earthquakes

# rode o servidor de desenvolvimento
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/api/earthquakes/`.

### Frontend

Dentro da pasta `earthquake_map/`, abra o `index.html` com a extensão **Live Server** do VS Code (ou outro servidor estático local). Certifique-se de que:
- o backend Django esteja rodando simultaneamente, e
- a URL da API dentro de `earthquake_map/script.js` aponte para o backend correto (local ou produção, dependendo do que você quer testar).


## 🏭 Desenvolvimento vs. Produção

| Aspecto | Desenvolvimento | Produção |
|---|---|---|
| Servidor | `python manage.py runserver` | `gunicorn main.wsgi` |
| Banco de dados | PostgreSQL local | PostgreSQL gerenciado (Render) |
| `DEBUG` | `True` | `False` |
| Arquivos estáticos | servidos automaticamente pelo `runserver` | servidos via `whitenoise`, após `collectstatic` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` (padrão) | domínio real do serviço (ex: `recent-earthquakes.onrender.com`) |
| Ingestão de dados | manual (`python manage.py fetch_earthquakes`) | automatizada via Cron Job do Render, a cada 6 horas |

## 🗄️ Banco de dados e migrations

O projeto usa **PostgreSQL** (migrado de SQLite durante o desenvolvimento, por SQLite não ser confiável em ambientes de deploy com sistema de arquivos efêmero).

```bash
# gerar uma nova migration após alterar models.py
python manage.py makemigrations

# aplicar migrations pendentes
python manage.py migrate
```

Não há fixtures/seeds formais no projeto — a "população" do banco é feita pelo comando `fetch_earthquakes`, que busca dados reais da API do USGS (não dados fictícios).

## 📡 Comando de ingestão de dados

```bash
python manage.py fetch_earthquakes
```

O que esse comando faz:
- Consulta o endpoint `query` da API do USGS (`https://earthquake.usgs.gov/fdsnws/event/1/query`)
- Parâmetros fixos no código: `format=geojson`, últimos 30 dias, `minmagnitude=4.5`
- Para cada terremoto retornado, usa `update_or_create` com `external_id` (o ID do evento no USGS) como critério de busca — evitando duplicação em execuções repetidas
- Converte o timestamp (epoch em milissegundos) para `datetime` timezone-aware (UTC)

> ⚠️ **A conferir:** os parâmetros de busca (intervalo de datas, magnitude mínima) estão fixos no código-fonte do comando, não configuráveis via linha de comando no momento.


## 🔗 Documentação da API

Base URL (produção): `https://recent-earthquakes.onrender.com/api/`
Base URL (local): `http://127.0.0.1:8000/api/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/earthquakes/` | Lista os terremotos (paginado) |
| GET | `/earthquakes/<id>/` | Detalhe de um terremoto específico |
| GET | `/earthquakes/?min_magnitude=5` | Filtra por magnitude mínima (lookup `gte`) |
| GET | `/earthquakes/?place=California` | Filtra por local (busca parcial, `icontains`) |
| GET | `/earthquakes/?start_date=2026-01-01T00:00:00Z&end_date=2026-01-31T23:59:59Z` | Filtra por intervalo de data (campo `time`) |
| GET | `/earthquakes/?page_size=100` | Customiza o tamanho da página (padrão 10, máximo 1000) |

Campos retornados por terremoto: `id`, `external_id`, `magnitude`, `place`, `latitude`, `longitude`, `depth`, `time`, `sig`, `fetched_at`.

A API é **somente leitura** — não há endpoints de criação, atualização ou remoção via HTTP.

### Exemplo de uso

```bash
curl "https://recent-earthquakes.onrender.com/api/earthquakes/?min_magnitude=6&page_size=20"
```

## 🚢 Build e Deploy

### Backend (Render — Web Service)

- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command:** `gunicorn main.wsgi`
- **Banco de dados:** PostgreSQL gerenciado pelo Render (plano Free — atenção: pode expirar após um período, conforme política do Render no momento da criação)
- **Variáveis de ambiente configuradas na plataforma:** `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`

### Ingestão automatizada (Render — Cron Job)

- **Comando:** `python manage.py fetch_earthquakes`
- **Schedule:** `0 */6 * * *` (a cada 6 horas)
- Mesmas variáveis de ambiente do Web Service (exceto `ALLOWED_HOSTS`)

### Frontend (GitHub Pages via GitHub Actions)

O workflow em `.github/workflows/deploy.yml` publica automaticamente o conteúdo da pasta `earthquake_map/` no GitHub Pages a cada push na branch `main`:
- Fonte do GitHub Pages configurada como **"GitHub Actions"** (não "Deploy from a branch")
- Etapas do workflow: checkout → configure-pages → upload do artefato (`path: earthquake_map`) → deploy

## 🌱 Convenções do projeto

- **Commits:** seguem parcialmente o padrão Conventional Commits (`feat:`, `fix:`, `docs:`, `ci:`), com mensagens descritivas do que foi entregue, não dos arquivos alterados.
- **Branches:** mudanças grandes/arriscadas (ex: a migração do frontend para o globo 3D) são feitas em branches próprias (ex: `feature/globo-3d`) e mescladas na `main` somente após validação.
- **Migrations:** sempre commitadas junto com a alteração de model correspondente (nunca separadamente, nem ignoradas via `.gitignore`).
- **Arquivos derivados** (`staticfiles/`, `__pycache__/`, `venv/`, `.env`) não são versionados.

## 🛠️ Troubleshooting

Problemas reais encontrados durante o desenvolvimento deste projeto, e como foram resolvidos:

- **`ModuleNotFoundError` ao rodar `runserver`/comandos:** geralmente causado por erro de digitação no nome do app em `INSTALLED_APPS`. Confira a grafia exata.
- **Erro de CORS no console do navegador (`blocked by CORS policy`):** a origem do frontend (protocolo + domínio, sem o caminho) precisa estar exatamente listada em `CORS_ALLOWED_ORIGINS` no `settings.py` do backend. Após alterar, é necessário commitar e reimplantar o backend para a mudança ter efeito em produção.
- **`page_size` na URL sendo ignorado pela paginação:** a classe padrão `PageNumberPagination` do DRF não aceita esse parâmetro sem configuração explícita. É necessário definir `page_size_query_param` numa classe de paginação customizada (ver `earthquakes/pagination.py`).
- **`CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False`:** normalmente indica que `load_dotenv()` está sendo chamado **depois** de alguma configuração que já lê variáveis de ambiente no `settings.py`. `load_dotenv()` deve ser a primeira coisa executada no arquivo.
- **Erro ao converter o campo `time` da API do USGS:** o timestamp vem em epoch **milissegundos**, não segundos — é necessário dividir por 1000 antes de usar `datetime.fromtimestamp()`.
- **`DATABASE_URL` com senha contendo `#`:** o caractere `#` tem significado especial tanto em arquivos `.env` (comentário) quanto em URLs (fragmento). Evite caracteres especiais na senha do banco, ou trate-os adequadamente (aspas no `.env`, URL encoding na `DATABASE_URL`).
- **Shell não disponível no Render (plano Free):** para rodar comandos pontuais em produção sem acesso a shell, usar um Cron Job (ele executa o comando e também serve como agendamento recorrente).

