````markdown
# CI/CD con Flask, Docker y GitHub Actions  
_Ejemplo práctico hasta la construcción del package (imagen Docker)_

Este repositorio muestra un flujo completo de **CI/CD** usando:

- Una aplicación web sencilla en **Flask** (`app.py`).
- **Pruebas unitarias** con `pytest` (`test_app.py`).
- Un **pipeline de GitHub Actions** que:
  - Ejecuta las pruebas.
  - Construye una **imagen Docker**.
  - Publica esa imagen en **GitHub Container Registry (GHCR)**.
- Despliegue con **Docker Swarm** + **Traefik** usando `stack.yml` y un `Makefile`.

Al final, el “package” de este proyecto es la **imagen Docker** publicada en:

```text
ghcr.io/paul1578/paul1578t:1.0.0
````

---

## 1. ¿Qué es CI/CD?

* **CI (Integración Continua)**: cada vez que hago `git push` al repositorio (por ejemplo a la rama `main`), se ejecutan automáticamente:

  * Las pruebas de mi aplicación.
  * La construcción del artefacto (en este caso, imagen Docker), si las pruebas pasan.

* **CD (Entrega/Despliegue Continuo)**: una vez construido y publicado el artefacto (imagen Docker), se puede desplegar de forma automatizada o semi-automatizada en un servidor (en este ejemplo, con Docker Swarm y Traefik).

En resumen:

> **Yo subo código → el pipeline verifica, empaqueta y lo deja listo para producción.**

---

## 2. Estructura del proyecto

Ejemplo de estructura de archivos:

```text
.
├── app.py
├── requirements.txt
├── test_app.py
├── Dockerfile
├── Makefile
├── stack.yml
└── .github/
    └── workflows/
        └── docker-image.yml
```

* `app.py`: aplicación Flask.
* `test_app.py`: pruebas con `pytest`.
* `requirements.txt`: dependencias de Python.
* `Dockerfile`: instrucción para construir la imagen Docker.
* `Makefile`: comandos útiles para build/deploy local o en Swarm.
* `stack.yml`: definición del servicio en Docker Swarm + Traefik.
* `.github/workflows/docker-image.yml`: pipeline de CI/CD con GitHub Actions.

---

## 3. Aplicación Flask (`app.py`)

La app es una página HTML bonita servida desde un único archivo `app.py`:

```python
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Página Bonita con Flask</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Estilos omitidos por brevedad -->
</head>
<body>
    <div class="card">
        <div class="badge">
            <div class="dot"></div>
            Flask App • Puerto 80
        </div>
        <h1>¡Hola desde Flask! 👋</h1>
        <p class="subtitle">
            Esta es una página de ejemplo renderizada desde un solo archivo <strong>app.py</strong>.
        </p>
        <!-- Contenido, stats y botón -->
        <button class="primary-btn" onclick="alert('Flask funcionando bonito 😎')">
            Probar botón
        </button>
        <p class="footer-text">
            Desplegada en <span>http://localhost</span> usando Flask.
        </p>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    # host="0.0.0.0" para aceptar conexiones externas (Docker, LAN, etc.)
    app.run(host="0.0.0.0", port=80)
```

---

## 4. Pruebas con `pytest` 

Las pruebas básicas validan que la ruta principal (`/`) responde OK y contiene ciertos textos esperados.

Archivo: **`test_app.py`**

```python
import pytest
from app import app  # El archivo principal se llama app.py

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    """La ruta / debe responder 200 OK."""
    response = client.get("/")
    assert response.status_code == 200

def test_home_contains_title(client):
    """La página debe contener el título correcto."""
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "<title>Mi Página Bonita con Flask</title>" in html

def test_home_contains_main_heading(client):
    """Debe mostrar el encabezado principal."""
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "¡Hola desde Flask! 👋" in html

def test_home_contains_button_text(client):
    """Debe existir el botón con el texto esperado."""
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "Probar botón" in html
    assert "Flask funcionando bonito 😎" in html
```

### Ejecutar pruebas de forma local

```bash
pip install -r requirements.txt
pytest -q
```

---

## 5. Construcción del package: imagen Docker 

### 5.1. Dockerfile

Archivo: **`Dockerfile`**

```dockerfile
# Imagen base Python 3.12
FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 80

# Ejecutar la app
CMD ["python", "app.py"]
```

### 5.2. Construir la imagen localmente

```bash
docker build -t carrilloimg:latest .
docker run -p 80:80 carrilloimg:latest
```

Con esto, la aplicación estaría disponible en `http://localhost:80`.

---

## 6. Automatización con Makefile

Archivo: **`Makefile`**

```makefile
build: 
	docker build -t carrilloimg:latest .

deploy:
	docker stack deploy --with-registry-auth -c stack.yml quinto

rm: 
	docker stack rm quinto
```

* `make build`: construye la imagen local.
* `make deploy`: despliega el stack en Docker Swarm.
* `make rm`: elimina el stack.

---

## 7. Despliegue con Docker Swarm + Traefik

Archivo: **`stack.yml`**

```yaml
version: "3.8"

services:
  webcarrillo:
    image: ghcr.io/paul1578/paul1578t:1.0.0
    deploy:
      replicas: 1
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.webcarrillo.entrypoints=http"
        - "traefik.http.routers.webcarrillo.rule=Host(`webcarrillo.byronrm.com`)"
        - "traefik.http.middlewares.webcarrillo-https-redirect.redirectscheme.scheme=https"
        - "traefik.http.routers.webcarrillo.middlewares=webcarrillo-https-redirect"
        - "traefik.http.routers.webcarrillo-secure.entrypoints=https"
        - "traefik.http.routers.webcarrillo-secure.rule=Host(`webcarrillo.byronrm.com`)"
        - "traefik.http.routers.webcarrillo-secure.tls=true"
        - "traefik.http.routers.webcarrillo-secure.tls.certresolver=http"
        - "traefik.http.routers.webcarrillo-secure.service=webcarrillo"
        - "traefik.http.services.webcarrillo.loadbalancer.server.port=80"
        - "traefik.docker.network=traefik-public"
    networks:
      - traefik-public

networks:
  traefik-public:
    external: true
```

Se asume que:

* Ya tienes un **cluster Docker Swarm** inicializado.
* Ya existe una red externa `traefik-public` creada por el stack de Traefik.
* Traefik está configurado para manejar HTTP/HTTPS y los certificados.

Comando de despliegue:

```bash
docker stack deploy --with-registry-auth -c stack.yml quinto
```

---

## 8. Pipeline CI/CD con GitHub Actions (criterios 2, 3 y 4)

Archivo: **`.github/workflows/docker-image.yml`**

Este workflow se ejecuta en cada `push` a `main` y también se puede correr manualmente.
Hace lo siguiente:

1. Descarga el código del repositorio.
2. Instala Python y dependencias.
3. Ejecuta las pruebas con `pytest`.
4. Inicia sesión en GitHub Container Registry.
5. Construye y publica la imagen Docker `ghcr.io/paul1578/paul1578t:1.0.0`.

```yaml
name: Build and Publish Docker image

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write 

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies and run tests
        run: |
          pip install --no-cache-dir -r requirements.txt
          pip install pytest
          pytest -q

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ghcr.io/paul1578/paul1578t:1.0.0
```

### Flujo completo del CI/CD en este proyecto

1. **Desarrollo local**

   * Modifico `app.py` o las pruebas.
   * Ejecuto `pytest` localmente.
   * Opcionalmente `docker build -t carrilloimg:latest .` para probar la imagen local.

2. **Commit y push**

   * `git add .`
   * `git commit -m "Añadir tests y CI/CD"`
   * `git push origin main`

3. **CI en GitHub Actions**

   * El workflow se dispara automáticamente.
   * Se instalan dependencias y se ejecutan pruebas `pytest`.
   * Si las pruebas pasan, se construye la imagen Docker y se publica en GHCR.

4. **Package listo (Docker image)**

   * La imagen `ghcr.io/paul1578/paul1578t:1.0.0` queda disponible como **package** en el registro.

5. **CD / Despliegue**

   * En el servidor con Docker Swarm, ejecuto:

     ```bash
     docker stack deploy --with-registry-auth -c stack.yml quinto
     ```
   * Traefik enruta el dominio `https://webcarrillo.byronrm.com` hacia el servicio `webcarrillo`.

---

## 9. Cómo reproducir el ejemplo

1. **Clonar el repositorio**

```bash
git clone <URL_DE_TU_REPO_PUBLICO>
cd <nombre-del-repo>
```

2. **Instalar dependencias y correr pruebas**

```bash
pip install -r requirements.txt
pytest -q
```

3. **Construir imagen local y probar**

```bash
docker build -t carrilloimg:latest .
docker run -p 80:80 carrilloimg:latest
# Abrir http://localhost
```

4. **Hacer push a main para disparar el CI/CD**

```bash
git add .
git commit -m "Configurar CI/CD con tests y Docker"
git push origin main
```

5. **Verificar el package en GitHub**

* Ir a la sección **Packages** del usuario/organización.
* Confirmar que la imagen `ghcr.io/paul1578/paul1578t:1.0.0` fue publicada.

---

```
```
