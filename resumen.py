# resumen.py
from significados import SIGNIFICADOS
from engine_utils import calcular_hechos_finales_auto
from troncales import cargar_materias_troncales
from horarios import filtrar_materias_segun_hechos, mostrar_materias_filtradas
from recomendaciones import imprimir_recomendaciones_conversacionales

def generar_resumen_significados(engine, path_reglas="reglas.py"):
    inferidos = []
    finales = []
    troncales = []
    materias_filtradas = []

    finales_ids = set(calcular_hechos_finales_auto(engine, path_reglas))

    for _, hecho in engine.facts.items():
        nombre = hecho.__class__.__name__
        if nombre in SIGNIFICADOS:
            inferidos.append(f"{nombre}: {SIGNIFICADOS[nombre]}")

        if nombre in SIGNIFICADOS and nombre in finales_ids:
            finales.append(f"{nombre}: {SIGNIFICADOS[nombre]}")

            if nombre == "T":
                troncales = cargar_materias_troncales()

            if nombre in ["L", "N", "M", "V"]:
                hechos_finales = calcular_hechos_finales_auto(engine)
                materias_filtradas = filtrar_materias_segun_hechos(hechos_finales)

    return {
        "inferidos": inferidos,
        "finales": finales,
        "finales_ids": finales_ids,
        "troncales": troncales,
        "materias_filtradas": materias_filtradas,
    }

def imprimir_todo_unificado(engine, hechos_usuario, path_reglas="reglas.py"):
    resumen = generar_resumen_significados(engine, path_reglas)

    #inferidos = resumen.get("inferidos", [])
    #finales = resumen.get("finales", [])
    finales_ids = resumen.get("finales_ids", set())
    troncales = resumen.get("troncales", [])
    materias_filtradas = resumen.get("materias_filtradas", [])
    '''
    print("\n===============================")
    print("      RESUMEN COMPLETO")
    print("===============================\n")

    print("=== HECHOS INFERIDOS ===")
    if inferidos:
        for linea in inferidos:
            print(" -", linea)
    else:
        print(" (No se infirió nada nuevo.)")

    print("\n=== HECHOS FINALES ===")
    if finales:
        for linea in finales:
            print(" -", linea)
    else:
        print(" (No se detectaron hechos finales.)")'''

    print("\n=== RECOMENDACIONES ===")
    recs = imprimir_recomendaciones_conversacionales(finales_ids, hechos_usuario, solo_devolver=True)
    if recs:
        for r in recs:
            print(" •", r)
    else:
        print(" (No hubo recomendaciones específicas.)")

    if troncales:
        print("\n--- MATERIAS TRONCALES ---")
        for ruta in troncales:
            print(" •", ruta)

    if materias_filtradas:
        print("\n--- MATERIAS y HORARIOS DISPONIBLES SEGÚN TU PERFIL ---")
        mostrar_materias_filtradas(materias_filtradas)

    ''' print("\n===============================")
    print("  FIN DEL RESUMEN COMPLETO")
    print("===============================\n")'''

    return finales_ids
