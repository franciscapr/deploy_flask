# Proyecto de Gestión de Usuarios y Comentarios

Este es un proyecto simple construido con Flask, MySQL y Python que permite a los usuarios registrarse y comentar en eventos.

## Descripción

Este proyecto es una aplicación web que permite a los usuarios registrarse, iniciar sesión y dejar comentarios en diferentes eventos. Utiliza Flask como framework web, MySQL como base de datos y Bootstrap para el diseño de las plantillas HTML.

## Características

- Registro de usuarios
- Inicio de sesión y cierre de sesión de usuarios
- Creación, visualización y edición de eventos
- Comentarios en eventos (solo permitidos para usuarios que no son los creadores del evento)

## Requisitos

- bcrypt==4.1.3; python_version >= '3.7'
- blinker==1.8.2; python_version >= '3.8'
- click==8.1.7; python_version >= '3.7'
- colorama==0.4.6; platform_system == 'Windows'
- flask==3.0.3; python_version >= '3.8'
- flask-bcrypt==1.0.1
- itsdangerous==2.2.0; python_version >= '3.8'
- jinja2==3.1.4; python_version >= '3.7'
- markupsafe==2.1.5; python_version >= '3.7'
- pymysql==1.1.1; python_version >= '3.7'
- werkzeug==3.0.3; python_version >= '3.8'

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd tu-repositorio
    ```

3. Crea y activa un entorno virtual:
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

