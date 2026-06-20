import great_expectations as gx

# 1. Conectamos al contexto de archivos local (busca o crea la carpeta ./gx)
context = gx.get_context(mode="file")

# 2. Creamos o recuperamos la suite para usuarios
suite_name = "suite_usuarios"
try:
    suite_usuarios = context.suites.get(name=suite_name)
    print(
        f"La suite '{suite_name}' ya existía, procedemos a actualizar sus reglas.")
except Exception:
    suite_usuarios = context.suites.add(gx.ExpectationSuite(name=suite_name))
    print(f"Nueva suite '{suite_name}' creada exitosamente.")

# ==============================================================================
# 3. REGISTRO DE TODAS LAS EXPECTATIONS (REGLAS DE CALIDAD)
# ==============================================================================

# --- REGLA 1: Validación de Volumen (Row Count) ---
# Esperamos que el archivo tenga entre 2 y 100 filas.
suite_usuarios.add_expectation(gx.expectations.ExpectTableRowCountToBeBetween(
    min_value=2,
    max_value=100
))

# --- REGLA 2: Completitud estricta en Llave Primaria ---
# El 'id_usuario' es obligatorio, por lo que exigimos 100% libre de nulos.
suite_usuarios.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
    column="id_usuario"
))

# --- REGLA 3: Tasa de Nulos Permitida (Null Rate / Completeness) ---
# El negocio acepta que falte el correo en máximo un 15% de los registros (mostly=0.85)
suite_usuarios.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
    column="email",
    mostly=0.85
))

# --- REGLA 4: Rango de Valores Lógicos (Value Range) ---
# Validar que las edades ingresadas estén en un rango biológico y legal coherente.
suite_usuarios.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="edad",
    min_value=18,
    max_value=120
))

# --- REGLA 5: Validación de Formato y Sintaxis (Regex Match) ---
# Verificar que los strings en la columna email cumplan con la estructura básica de correo.
suite_usuarios.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
    column="email",
    regex=r"^[^@]+@[^@]+\.[^@]+$"
))

print(
    f"\n✅ ¡Todas las reglas ({len(suite_usuarios.expectations)}) han sido guardadas físicamente!")
print(f"📁 Revisa el archivo generado en: ./gx/expectations/{suite_name}.json")
