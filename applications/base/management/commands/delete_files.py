import os
import shutil

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):

        list_directories = [
            'applications/account/migrations/',
            'applications/reinventor/migrations/'
        ]

        for dir in list_directories:
            for root, dirs, files in os.walk(dir):

                for file in files:
                    if file != '__init__.py':
                        archivo_path = os.path.join(dir, file)
                        # Verificar si es un archivo y no un directorio
                        if os.path.isfile(archivo_path):
                            os.remove(archivo_path)
                            print(f"Eliminado: {archivo_path}")

                for carpeta in dirs:
                    if carpeta == "__pycache__":
                        carpeta_path = os.path.join(root, carpeta)
                        shutil.rmtree(carpeta_path)
                        print(f"Eliminado: {carpeta_path}")
                

        self.stdout.write('¡La migracion fue realizada con exito!')