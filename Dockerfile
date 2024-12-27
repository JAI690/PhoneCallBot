FROM public.ecr.aws/lambda/python:3.12

# Actualiza los paquetes y instala las dependencias del sistema necesarias
RUN yum update && yum install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    && yum clean \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de tu aplicación
COPY . ${LAMBDA_TASK_ROOT}

# Instala las dependencias
RUN pip install --upgrade pip \
    &&pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Configura el handler para Lambda
CMD ["app.lambda_handler"]