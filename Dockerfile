FROM python:3.11-slim

#ENVIRONMENT VARIABLES
ENV PTYHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Working directory within the container
WORKDIR /app

#Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Copiar archivo de dependencias \
COPY requirements.txt .

# Instalar dependencias de PYTHON
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#Copiar el codigo de la aplicacion \
COPY ./app ./app

# Puerto que expone la aplicacion
EXPOSE 8000

# Comando para ejecutar la aplicacion
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


