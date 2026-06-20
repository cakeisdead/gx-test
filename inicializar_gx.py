import great_expectations as gx

# Esto crea la estructura física en disco dentro de una carpeta llamada 'gx/'
# (en lugar de la antigua 'great_expectations/')
context = gx.get_context(mode="file")

print("¡Estructura de GX V1 inicializada correctamente en la carpeta ./gx!")
