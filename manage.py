#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


def main():
    """Run administrative tasks."""
    #Ahora que cambiamos el archivo de configuración settings.py que trae Django por defecto a múltiples archivos de configuración por cada entorno, tenemos que actualizar los archivos asgi.py, wsgi.py y manage.py.
    #La sigueinte linea quiere decir que ahora Django utilizará el archivo de configuración local.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{config("PROJECT_NAME")}.settings.production')

    try:
        from django.core.management import execute_from_command_line
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
