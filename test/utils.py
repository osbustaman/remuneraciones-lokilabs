import random

def obtener_nombre_aleatorio():
    nombres = ["Ana", "Juan", "María", "Pedro", "Luis",
               "Laura", "Carlos", "Sofía", "Diego", "Valentina"]
    # Genera un número aleatorio entre 1 y 10 (ambos inclusive)
    numero_aleatorio = random.randint(0, 9)

    # Restamos 1 al número aleatorio para ajustarlo al índice de la lista
    nombre_aleatorio = nombres[numero_aleatorio - 1]
    return nombre_aleatorio

def obtener_rut_aleatorio():
    ruts = ["12345678-9", "98765432-1", "87654321-0", "76543210-8", "65432109-7", "54321098-6",
            "43210987-5", "32109876-4", "21098765-3", "10987654-2"]
    numero_aleatorio = random.randint(0, 9)  # Genera un número aleatorio entre 0 y 9 (ambos inclusive)
    
    rut_aleatorio = ruts[numero_aleatorio]
    return rut_aleatorio