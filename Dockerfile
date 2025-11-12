# Imagen base Python 3.12
FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
# (primero requirements.txt para aprovechar la cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código (incluyendo app.py)
COPY . .

# Exponer el puerto
EXPOSE 80

# Ejecutar la app
CMD ["python", "app.py"]
