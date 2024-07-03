# Importar flask
from flask import Flask

# Inicializar la app
app = Flask(__name__)

# Declarar la lleva secreta
app.secret_key = "llave secretisima"