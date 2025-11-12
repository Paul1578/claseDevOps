from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Página Bonita con Flask</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1d3557, #457b9d, #a8dadc);
            color: #1d3557;
        }

        .card {
            background: #f1faee;
            border-radius: 24px;
            padding: 32px 28px;
            max-width: 480px;
            width: 90%;
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.25);
            text-align: center;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(69, 123, 157, 0.1);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            margin-bottom: 18px;
        }

        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #06d6a0;
        }

        h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 14px;
            color: #457b9d;
            margin-bottom: 24px;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 24px;
            text-align: left;
        }

        .stat {
            flex: 1;
            padding: 14px;
            border-radius: 16px;
            background: rgba(168, 218, 220, 0.5);
        }

        .stat-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #457b9d;
            margin-bottom: 6px;
        }

        .stat-value {
            font-size: 16px;
            font-weight: 600;
        }

        .primary-btn {
            border: none;
            outline: none;
            background: #e63946;
            color: #f1faee;
            font-size: 14px;
            font-weight: 600;
            padding: 10px 18px;
            border-radius: 999px;
            cursor: pointer;
            transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.15s ease;
            box-shadow: 0 10px 20px rgba(230, 57, 70, 0.45);
        }

        .primary-btn:hover {
            background: #d62839;
            transform: translateY(-1px);
            box-shadow: 0 14px 26px rgba(230, 57, 70, 0.55);
        }

        .primary-btn:active {
            transform: translateY(0);
            box-shadow: 0 8px 16px rgba(230, 57, 70, 0.4);
        }

        .footer-text {
            margin-top: 18px;
            font-size: 12px;
            color: #457b9d;
        }

        .footer-text span {
            font-weight: 600;
            color: #1d3557;
        }
    </style>
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

        <div class="stats">
            <div class="stat">
                <div class="stat-label">Estado</div>
                <div class="stat-value">Online ✅</div>
            </div>
            <div class="stat">
                <div class="stat-label">Framework</div>
                <div class="stat-value">Flask</div>
            </div>
            <div class="stat">
                <div class="stat-label">Versión</div>
                <div class="stat-value">Demo 1.0</div>
            </div>
        </div>

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
    # puerto 80 como pediste
    app.run(host="0.0.0.0", port=80)
