import pandas as pd

# Datos limpios (Lo que esperas recibir)
datos_buenos = {
    "id_usuario": [101, 102, 103],
    "nombre": ["Ana", "Pedro", "Luis"],
    "edad": [28, 34, 42],
    "email": ["ana@email.com", "pedro@email.com", "luis@email.com"]
}

# Datos sucios (Con errores que GX detectará)
datos_malos = {
    "id_usuario": [104, None, 106],          # Hay un nulo donde no debería
    "nombre": ["Sofía", "Carlos", "Marta"],
    "edad": [19, -5, 150],                    # Edad negativa y una irreal
    "email": ["sofia.com", "carlos@email.com", "marta@email.com"] # Email inválido
}

pd.DataFrame(datos_buenos).to_csv("usuarios_buenos.csv", index=False)
pd.DataFrame(datos_malos).to_csv("usuarios_malos.csv", index=False)
print("Archivos de prueba generados.")