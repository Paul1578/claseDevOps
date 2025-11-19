import pytest
from app import app  # asegúrate de que el archivo se llama app.py


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
    # Y opcionalmente verificamos el onclick
    assert "Flask funcionando bonito 😎" in html
