# Usa una imagen base compatible con AWS Lambda y Python
FROM public.ecr.aws/lambda/python:3.9

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
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Configura el handler para Lambda
CMD ["app.lambda_handler"]