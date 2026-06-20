import great_expectations as gx
import pandas as pd


def evaluar_archivo(ruta_archivo, nombre_suite):
    print(f"\n--- 🔍 Iniciando Control de Calidad para: {ruta_archivo} ---")

    # 1. Cargar el contexto físico (GX detecta automáticamente la carpeta ./gx)
    context = gx.get_context(mode="file")

    # 2. Leer los datos del pipeline (el CSV)
    df = pd.read_csv(ruta_archivo)

    # 3. Conectar el DataFrame dinámicamente al contexto
    # Usamos nombres únicos por archivo para evitar colisiones en memoria
    nombre_asset = ruta_archivo.replace(".", "_").replace("/", "_")
    data_source = context.data_sources.add_pandas(
        name=f"source_{nombre_asset}")
    data_asset = data_source.add_dataframe_asset(name=nombre_asset)

    batch_definition = data_asset.add_batch_definition_whole_dataframe("todo")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    # 4. RECUPERAR LAS REGLAS DEL DISCO (La suite JSON)
    try:
        suite = context.suites.get(name=nombre_suite)
        print(
            f"📖 Suite '{nombre_suite}' cargada exitosamente desde el catálogo.")
    except Exception as e:
        print(
            f"❌ Error: No se encontró la suite '{nombre_suite}' en ./gx/expectations/")
        return

    # 5. EJECUTAR VALIDACIÓN
    resultado = batch.validate(suite)

    # 6. Procesar Resultados (Lógica Fail-Fast para tus Pipelines)
    if resultado.success:
        print("✅ ¡Éxito! Los datos cumplen con todos los estándares de calidad.")
    else:
        print("❌ ¡Alerta! Se encontraron problemas de calidad de datos.")

        # Iterar sobre las reglas que fallaron para dar un reporte detallado
        for res in resultado.results:
            if not res.success:
                config = res.expectation_config
                tipo_regla = config.type if config else "Desconocida"
                columna = config.kwargs.get('column') if config and config.kwargs.get(
                    'column') else "Métrica Global"

                print(f"  - Falló: {tipo_regla} en '{columna}'")
                if res.result.get('unexpected_count') is not None:
                    print(
                        f"    Detalle: {res.result.get('unexpected_count')} registros inválidos de {res.result.get('element_count')}.")
                elif res.result.get('observed_value') is not None:
                    print(
                        f"    Valor observado: {res.result.get('observed_value')}")


# ==============================================================================
# EJECUCIÓN DEL PIPELINE
# ==============================================================================
if __name__ == "__main__":
    # Ejecutamos la misma suite de producción contra ambos archivos
    evaluar_archivo("usuarios_buenos.csv", nombre_suite="suite_usuarios")
    evaluar_archivo("usuarios_malos.csv", nombre_suite="suite_usuarios")
