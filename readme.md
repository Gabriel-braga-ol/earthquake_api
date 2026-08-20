# 🌍 Earthquake API

Backend Django que consome a API pública de terremotos do USGS (United States Geological Survey), persiste os dados de forma idempotente e expõe uma API REST própria, somente leitura, com filtros e paginação. Inclui um frontend simples com mapa interativo (Leaflet.js) para visualização dos terremotos.

## 📌 Sobre o projeto

O projeto consiste em duas etapas principais:

1. **Ingestão de dados**: um management command consome o endpoint `query` da API do USGS, buscando terremotos de magnitude 4.5+ nos últimos 30 dias, e persiste esses dados no banco local usando `update_or_create` — garantindo que rodar o comando múltiplas vezes nunca duplica registros.
2. **Exposição de dados**: uma API REST própria (Django REST Framework), somente leitura, expõe os terremotos salvos com suporte a filtros (magnitude, local, intervalo de data) e paginação customizável.

Um frontend separado, consumindo essa API, plota os terremotos num mapa interativo com popups informativos e filtro de magnitude.

## 🚀 Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- django-filter
- django-cors-headers
- SQLite
- requests
- HTML, CSS e JavaScript (frontend)
- Leaflet.js

## ⚙️ Funcionalidades

- Ingestão automatizada de terremotos via API pública do USGS
- Persistência idempotente (sem duplicação de registros a cada nova busca)
- API REST somente leitura (`GET`), sem endpoints de escrita
- Filtros customizados: magnitude mínima, local (busca parcial) e intervalo de data
- Paginação customizável via query param (`page_size`)
- Frontend com mapa interativo (Leaflet.js), marcadores com popup de detalhes e filtro de magnitude

## 🔗 Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/earthquakes/` | Lista os terremotos (paginado) |
| GET | `/api/earthquakes/<id>/` | Detalhe de um terremoto específico |
| GET | `/api/earthquakes/?min_magnitude=5` | Filtra por magnitude mínima |
| GET | `/api/earthquakes/?place=California` | Filtra por local (busca parcial) |
| GET | `/api/earthquakes/?start_date=...&end_date=...` | Filtra por intervalo de data |
| GET | `/api/earthquakes/?page_size=100` | Customiza o tamanho da página |

## 🖥️ Como rodar o projeto

### Backend

```bash

git clone <url-do-repositorio>
cd earthquake_api


python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# instale as dependências
pip install -r requirements.txt

# aplique as migrations
python manage.py migrate

# busque os terremotos mais recentes
python manage.py fetch_earthquakes

# rode o servidor
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/api/earthquakes/`.

### Frontend

Dentro da pasta `earthquake_map/`, abra o `index.html` com a extensão **Live Server** do VS Code (ou qualquer servidor estático local). Certifique-se de que o backend Django esteja rodando simultaneamente.

## 🔮 Próximos passos / sugestões de melhoria

- [ ] Adicionar filtros de local e data também no frontend (hoje só o filtro de magnitude está implementado na interface)
- [ ] Implementar paginação real no frontend, em vez de buscar todos os registros de uma vez (`page_size=1000`)
- [ ] Adicionar clustering de marcadores (ex: Leaflet.markercluster) para melhorar a performance visual em regiões com alta densidade de terremotos
- [ ] Tornar os parâmetros do `fetch_earthquakes` (intervalo de datas, magnitude mínima) configuráveis via argumentos de linha de comando
- [ ] Agendar a execução periódica do `fetch_earthquakes` (via cron, Celery Beat, etc.), permitindo acumular um histórico maior de dados
- [ ] Adicionar uma segunda fonte de dados geológicos (ex: CPRM/GeoSGB) para enriquecer o contexto regional dos eventos
- [ ] Escrever testes automatizados para o management command e para os endpoints da API
- [ ] Adicionar cache (ex: Redis) para reduzir chamadas repetidas à API do USGS
- [ ] Deploy do backend (Render, Railway) e do frontend (Vercel, Netlify ou GitHub Pages)