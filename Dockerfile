FROM public.ecr.aws/lambda/python:3.9

# Actualiza los paquetes y prepara el entorno
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define el directorio de trabajo
WORKDIR /var/task

# Copia los archivos de la aplicación
COPY . /var/task

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /var/task/requirements.txt

# Configura el handler para Lambda
CMD ["app.lambda_handler"]
