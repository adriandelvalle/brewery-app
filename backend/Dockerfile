# Imagen base oficial de Python 3.12 slim
# slim = versión reducida, sin herramientas innecesarias — menos peso, menos superficie de ataque
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
# Todo lo que hagamos a partir de aquí ocurre dentro de /app
WORKDIR /app

# Copiar solo requirements.txt primero — aprovecha la caché de Docker
# Si requirements.txt no cambió, Docker reutiliza esta capa y no reinstala nada
COPY requirements.txt .

# Instalar dependencias de producción
# --no-cache-dir: no guarda caché de pip, reduce el tamaño de la imagen
# --upgrade pip: garantiza que pip está actualizado
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
# Esto ocurre DESPUÉS de instalar dependencias — si solo cambió el código,
# Docker reutiliza la capa de pip install y solo reconstruye esta capa
COPY src/ ./src/

# Exponer el puerto que usa uvicorn
EXPOSE 8000

# Comando de arranque
# --host 0.0.0.0: escucha en todas las interfaces, necesario dentro de Docker
# --workers 1: un worker por ahora, suficiente para desarrollo
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
