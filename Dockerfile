FROM python:3.9-slim

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar los archivos de la aplicación
COPY app/ /var/task/

# Especificar el comando Lambda
CMD ["app.lambda_handler"]
