# SYSTEM BACKEND

![CI](https://github.com/BrandonLlivisaca/system_backend/actions/workflows/ci.yml/badge.svg)

Backend System development with FastAPI

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy 2.0 (async)
- **Auth:** JWT
- **Container:** Docker

## Instalacion

### Local
```bash
git clone https://github.com/BrandonLlivisaca/system_backend.git
cd system-backend

# Entorno Virtual
python -m venv venv
.\venv\Scripts\Activate

# Dependencias
pip install -r requirements.txt

# Configurar
cp .env.example .env

# Ejecutar
uvicorn app.main:app --reload
```

## API Docs
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Tests
```bash
pytest tests/ -v
```

## Estructura
```

appp/
├── api/v1/          # Endpoints
├── core/            # Seguridad
├── models/          # Entidades
├── repositories/    # Acceso a datos
├── schemas/         # DTOs
└── services/        # Lógica de negocio
```


