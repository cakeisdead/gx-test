import great_expectations as gx
import pandas as pd


def evaluar_archivo(ruta_archivo):
    print(f"\n--- Analizando: {ruta_archivo} ---")

    # 1. Obtener el contexto efímero
    context = gx.get_context(mode="ephemeral")

    # 2. Conectar los datos
    df = pd.read_csv(ruta_archivo)
    data_source = context.data_sources.add_pandas(name="mi_fuente_pandas")
    data_asset = data_source.add_dataframe_asset(name="usuarios")

    # 3. Crear el lote (Batch)
    batch_definition = data_asset.add_batch_definition_whole_dataframe("todo")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    # 4. Crear la suite de reglas
    suite = context.suites.add(gx.ExpectationSuite(name="suite_usuarios"))

    # --- NUEVA REGLA 1: Validación de Volumen (Row Count) ---
    # Esperamos que el archivo tenga entre 2 y 100 filas.
    # Si llega un archivo vacío (0) o con una explosión de datos inusual, fallará.
    suite.add_expectation(gx.expectations.ExpectTableRowCountToBeBetween(
        min_value=2,
        max_value=100
    ))

    # --- NUEVA REGLA 2: Tasa de Nulos (Null Rate / Completeness) ---
    # Para 'id_usuario' exigimos el 100% de completitud (no definimos mostly, por defecto es 1.0)
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(column="id_usuario"))

    # Para 'email', supongamos que el negocio acepta que falte el correo en máximo 15% de los casos.
    # Usamos mostly=0.85 (Al menos el 85% de las filas DEBEN tener email).
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
        column="email",
        mostly=0.85
    ))

    # --- Reglas previas (Formato y Rangos) ---
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
        column="edad", min_value=18, max_value=120))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
        column="email",
        regex=r"^[^@]+@[^@]+\.[^@]+$"
    ))

    # 5. Ejecutar la validación
    resultado = batch.validate(suite)

    # 6. Mostrar resultado en consola
    if resultado.success:
        print("✅ ¡Éxito! Los datos cumplen con todos los estándares de calidad.")
    else:
        print("❌ ¡Alerta! Se encontraron problemas de calidad de datos.")
        for res in resultado.results:
            if not res.success:
                config = res.expectation_config
                tipo_regla = config.type if config else "Desconocida"
                columna = config.kwargs.get('column') if config and config.kwargs.get(
                    'column') else "Nivel de Tabla (Métrica Global)"

                print(f"  - Falló la regla: {tipo_regla} en '{columna}'")

                # Detalles específicos si es un fallo de registros individuales u omitidos
                if res.result.get('unexpected_count') is not None:
                    print(
                        f"    Detalle: {res.result.get('unexpected_count')} registros inválidos de {res.result.get('element_count')}.")
                elif res.result.get('observed_value') is not None:
                    print(
                        f"    Valor observado: {res.result.get('observed_value')}")


# Ejecutar con tus archivos de prueba
evaluar_archivo("usuarios_buenos.csv")
evaluar_archivo("usuarios_malos.csv")
