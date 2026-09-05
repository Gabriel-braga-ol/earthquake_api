# 🌍 Earthquake API

Backend Django que consome a API pública de terremotos do USGS (United States Geological Survey), persiste os dados de forma idempotente e expõe uma API REST própria, somente leitura, com filtros e paginação. Inclui um frontend com um globo 3D interativo (Globe.gl / Three.js) para visualização dos terremotos e dos limites das placas tectônicas.

## 📌 Sobre o projeto

O projeto consiste em duas etapas principais:

1. **Ingestão de dados**: um management command consome o endpoint `query` da API do USGS, buscando terremotos de magnitude 4.5+ nos últimos 30 dias, e persiste esses dados no banco local usando `update_or_create` — garantindo que rodar o comando múltiplas vezes nunca duplica registros.
2. **Exposição de dados**: uma API REST própria (Django REST Framework), somente leitura, expõe os terremotos salvos com suporte a filtros (magnitude, local, intervalo de data) e paginação customizável.

Um frontend separado, consumindo essa API, renderiza os terremotos num **globo 3D interativo**, com a altura e a cor de cada ponto representando a magnitude do evento, além de tooltips com detalhes e os limites das placas tectônicas sobrepostos.

## 🚀 Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- django-filter
- django-cors-headers
- SQLite
- requests
- HTML, CSS e JavaScript (frontend)
- Three.js / Globe.gl

## ⚙️ Funcionalidades

- Ingestão automatizada de terremotos via API pública do USGS
- Persistência idempotente (sem duplicação de registros a cada nova busca)
- API REST somente leitura (`GET`), sem endpoints de escrita
- Filtros customizados: magnitude mínima, local (busca parcial) e intervalo de data
- Paginação customizável via query param (`page_size`)
- Frontend com globo 3D interativo (Globe.gl):
  - Terremotos representados como pontos cuja **altura** é proporcional à magnitude
  - Cor diferenciada por faixa de magnitude (branco para magnitude < 5, vermelho translúcido para >= 5)
  - Tooltip ao passar o mouse, com local, magnitude, profundidade e data formatada
  - Limites das placas tectônicas sobrepostos ao globo (dataset público baseado em Peter Bird, 2003)

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
# clone o repositório
git clone https://github.com/Gabriel-braga-ol/earthquake_api.git
cd earthquake_api

# crie e ative o ambiente virtual
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
