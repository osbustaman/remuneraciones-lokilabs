# Configuración app01

## Configuración entorno

Estos son los pasos para instalar la aplicación den algun entorno.

> Instalar Apache

+ sudo apt-get update
+ sudo apt-get install apache2

> Instalar PIP

+ sudo apt install python3-pip

> Instalar virtualenv

+ sudo apt install python3-virtualenv

> Instalar Python (version 3.10 como mínimo.)

+ sudo apt update
+ Instalar Python 3.10 como mínimo.
+ python3 --version

> Instalar mod_wsgi, esto es para la interacción de apacho con python

+ sudo apt-get install libapache2-mod-wsgi-py3

## Configuración de la base de datos

> Actualizar la lista de paquetes de Ubuntu e instalar los paquetes necesarios:
    
    sudo apt-get update
    sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
    
> Cambiar clave usuario postgres

    sudo -u postgres psql postgres
    \password postgres
    Enter new password:
    Enter it again:
    \q
  
> para poder configurar el acceso desde un computador local se debe solicitar las intrucciones
    

## Configuración del proyecto despés de la configuración del entorno

> Descargar el proyecto desde el repositorio

+ para desacargar el proyecto se deben solicitar las credenciales al administrador de git
+ la descarga debe ser en la ruta /var/www/html
+ se debe dar permisos sudo chmod -R (consultar que permiso) horusforce/
+ crear la carpeta de entorno virtual dentro de la ruta del proyecto /var/www/html/horusforce/app01 (seguir los siguientes pasos)

        virtualenv env
        source env/bin/activate
        
+ despues de activar el entorno virtual se van a instalar las librerias que se usarán para que se pueda levantar la aplicación, para eso se debe ejecutar el siguiente comando

        pip install -r requirements.txt
        
Ya con esto se tiene configurado el proyecto

# app
Configuración

Requisitos

> Instalar Python 3.10 como mínimo.

    sudo apt update
    sudo apt install python3.11
    python3 --version

> Descargar el proyecto.

> Con pip se debe ejecutar el siguiente comando
(en el caso de no tener pip ver el siguiente link https://pip.pypa.io/en/stable/installation/)

> Con este comando se instalaran las librerías que usa la aplicación. 

    pip install -r requirements.txt
    
> instalar postgresql

# Instalación de Git

    sudo apt update
    sudo apt install git
    git --version

# Instalación de Samba  (paso opcional)

    sudo apt-get install samba
    sudo systemctl status nmbd

> Configuración del servidor de samba

    sudo mkdir /samba
    sudo nano /etc/samba/smb.conf

> Compartir carpeta

    [html]
    comment = Carpeta apache
    path = /var/www/html
    guest ok = yes
    writable = yes
    browsable = yes
    create mask = 0666
    directory mask = 0777
    public = yes

# Instalar y configurar virtualenv (opcional)

> Se debe instalar, para eso ir al siguiente link: https://pypi.org/project/virtualenv/
> Se debe copiar
    pip install virtualenv
    
  Luego pegarlo en el terminal, de esa forma se instala la libreria de virtualenv (entorno virtual)

> Ir a la raiz del proyecto desde la terminal y escribir lo siguiente:

    virtualenv venv
    
  Esto creara una carpeta con un entorno virtual el cual se debe activar de la siguiente manera:
    
    cd /path/raiz/proyecto/venv/bin/
    source activate
  
  (buscar comandos para windows)
  
# Instalar y configurar django, PostgreSQL en servidor Ubuntu Server
        
> Actualizar la lista de paquetes de Ubuntu e instalar los paquetes necesarios:
    
    sudo apt-get update
    sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
        
> Crea un entorno virtual utilizando venv:
    
    sudo apt-get install python3-venv
    python3 -m venv myenv
    source myenv/bin/activate
    
> Instala Django dentro del entorno virtual:

    pip install django
    
> Instala Django dentro del entorno virtual:

    sudo -u postgres psql
    CREATE DATABASE myproject;
    CREATE USER myuser WITH PASSWORD 'mypassword';
    ALTER ROLE myuser SET client_encoding TO 'utf8';
    ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE myproject TO myuser;

> Instala Django dentro del entorno virtual:

    django-admin startproject myproject

> Instala Django dentro del entorno virtual:

    python manage.py runserver 127.0.0.1:8000
    
Ahora se deberías poder acceder al proyecto Django desde cualquier navegador visitando http://127.0.0.1:8000


# Elementos para generar PDF

## Instala pandas y la librería que permite crear un PDF con pandas:

> Para generar un PDF con pandas en Django y luego devolverlo como una cadena codificada en base64, puedes seguir estos pasos:

    python manage.py runserver 127.0.0.1:8000
    pip install pandas
    pip install pdfkit
    
> Asegúrate de tener wkhtmltopdf instalado en tu sistema. Si no lo tienes, puedes descargarlo desde https://wkhtmltopdf.org/downloads.html.


# Instalar Swagger

## Swaggeres la libreria que nos permite documentar las apis creadas, para instalarlo se deben seguir lo siguiente:

> Ejecutar lo siguiente:

    pip install drf-yasg
    
> Agrega drf_yasg a la lista INSTALLED_APPS en el archivo settings.py de tu proyecto Django:

    INSTALLED_APPS = [
        # ...
        'rest_framework',
        'drf_yasg',
        # ...
    ]

> Agrega la URL de Swagger a tus urls.py:

    from django.urls import path, include
    from rest_framework import routers
    from rest_framework.documentation import include_docs_urls
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="API Documentation",
            default_version='v1',
            description="API documentation",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@yourcompany.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[],
    )

    urlpatterns = [
        # ...
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        # ...
    ]

> Luego se debe agregar esta estructura a ca archivo de API:

    from drf_yasg import openapi

    # Define el objeto Parameter para el encabezado Authorization
    header_param = openapi.Parameter(
        name="Authorization",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        description="Token Bearer",
    )

    # Agrega el parámetro a tu schema view
    class MySchemaView(SchemaView):
        authentication_classes = [TokenAuthentication] # opcional
        permission_classes = [IsAuthenticated] # opcional
        # Agrega el parámetro de encabezado en el método get
        @swagger_auto_schema(
            manual_parameters=[header_param],
            operation_id="My Operation ID",
            operation_description="My Operation Description",
            security=[{"Bearer": []}],
        )
        def get(self, request):
            # Código de la vista

