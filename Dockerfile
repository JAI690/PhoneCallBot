FROM public.ecr.aws/lambda/python:3.9

# Actualiza los paquetes y instala las dependencias del sistema necesarias
RUN yum update -y && \
    yum install -y \
    gcc \
    gcc-c++ \
    libffi-devel \
    openssl-devel \
    curl && \
    yum clean all && \
    rm -rf /var/cache/yum


# Define el directorio de trabajo
WORKDIR /var/task

# Copia los archivos de tu aplicación
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip \
    &&pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Configura el handler para Lambda
CMD ["app.lambda_handler"]