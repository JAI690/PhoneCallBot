FROM 637423663433.dkr.ecr.us-east-1.amazonaws.com/python:3.9-slim
# Actualiza los paquetes y instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de tu aplicación
COPY . ${LAMBDA_TASK_ROOT}

# Instala las dependencias
RUN pip install --upgrade pip \
    &&pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Configura el handler para Lambda
CMD ["app.lambda_handler"]