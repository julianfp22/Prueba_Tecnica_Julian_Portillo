"""Datos de prueba de la API de usuarios."""

# Cuerpo exacto que pide el enunciado
USUARIO = {"name": "Test User", "job": "Automation Engineer"}

USUARIO_ACTUALIZADO = {"name": "Test User", "job": "QA Lead"}

USUARIO_EXISTENTE_ID = 2
USUARIO_INEXISTENTE_ID = 23

TIEMPO_MAXIMO_S = 5

# (name, job) para comprobar que la API refleja los datos sin alterarlos
DATOS_VARIADOS = [
    ("José Ñandú Pérez", "Ingeniero de Automatización"),
    ("O'Brien & Sons <QA>", 'Tester "Senior" / Lead'),
    ("A" * 200, "B" * 200),
]
IDS_DATOS_VARIADOS = ["acentos_y_enie", "caracteres_especiales", "texto_largo"]
