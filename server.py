# Importación de flask_app
from flask_app import app

# Importación controladores
from flask_app.controllers import users_controller
from flask_app.controllers import events_controller
from flask_app.controllers import comments_controller


# Ejecución de la app

if __name__ == "__main__":
    app.run(debug=True)