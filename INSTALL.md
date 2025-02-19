# Guía de instalación

1. Configuración de variables de entorno

| Variable          | Descripción                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| `DATABASE_URL`    | URL de conexión a la base de datos. Formato: `postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_datos>` |
| `SECRET_KEY`      | Clave secreta para la aplicación (por ejemplo, para sesiones).                             |
| `FLASK_ENV`       | Entorno de Flask, puede ser `development` o `production`.                                  |
| `FLASK_APP`       | Nombre del archivo principal de la aplicación (por ejemplo, `app.py`).                     |
| `PORT`       | Puerto en el que se ejecutará la aplicación. Por defecto es `5000`.

1\. Requisitos Previos
----------------------

Asegúrate de tener **Python 3.8** o superior instalado en tu sistema. Puedes verificar esto ejecutando:

```bash
python --version
```

2\. Crear un Entorno Virtual
----------------------------

Es recomendable utilizar un entorno virtual para gestionar las dependencias del proyecto:

```bash
python -m venv venv
```

3\. Activar el Entorno Virtual
------------------------------

Activa el entorno virtual con el siguiente comando:

```bash
source venv/bin/activate
```

4\. Instalar Flask
------------------

Con el entorno virtual activado, instala Flask utilizando pip:

```bash
pip install Flask
```

5\. Instalar Dependencias Adicionales
-------------------------------------

Con el entorno virtual activado, instala las dependencias especificadas en requirements.txt utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```

6\. Ejecutar la Aplicación
--------------------------

Con el entorno virtual activado y Flask instalado, puedes ejecutar tu aplicación:

```bash
flask run
```
