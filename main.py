# main.py

import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping

from experta import *
from reglas import SistemaEducativo
from hechos import Perfil

# importación de módulos modularizados
from ui import imprimir_info_inicial, solicitar_nombre_usuario, imprimir_despedida, preguntar_si_no, preguntar_turno_trabajo
from engine_utils import preparar_engine
from resumen import imprimir_todo_unificado

# preguntas (pueden permanecer en main o pasarlas a ui.py; acá las mantengo simples)
PREGUNTAS_PERFILES = {
    "AB": "¿Solo estudias? (si/no): ",
    "AC": "¿Trabajás por la mañana? (si/no): ",
    "AD": "¿Trabajás por la tarde? (si/no): ",
    "AE": "¿Trabajás por la noche? (si/no): ",
    "AF": "¿Vas a cursar solo algunas materias? (si/no): ",
    "AG": "¿Vas a cursar todas las materias? (si/no): ",
    "AH": "¿Estás retomando los estudios después de un tiempo? (si/no): ",
    "AI": "¿Estás estudiando dos carreras a la vez? (si/no): ",
}

def run_engine():
    imprimir_info_inicial()
    nombre_usuario = solicitar_nombre_usuario()
    print("Respondé las siguientes preguntas con SI/NO:\n")
    respuestas = {}

    trabaja = preguntar_si_no("¿Trabajás actualmente? (si/no): ")
    if trabaja:
        respuestas["trabaja"] = True
        respuestas["turno_trabajo"] = preguntar_turno_trabajo()
    else:
        respuestas["trabaja"] = False

    respuestas["cursa_todas"] = preguntar_si_no(PREGUNTAS_PERFILES["AG"])
    respuestas["retoma_estudios"] = preguntar_si_no(PREGUNTAS_PERFILES["AH"])
    respuestas["doble_carrera"] = preguntar_si_no(PREGUNTAS_PERFILES["AI"])
    print("\nDIFICULTADES ACADÉMICAS ")
    resp_teorica = preguntar_si_no("¿Tenés dificultad en la parte teórica? (si/no): ")
    resp_practica = preguntar_si_no("¿Tenés dificultad en la parte práctica? (si/no): ")
    #print("\n>>> Ejecutando inferencia...\n")
    engine, hechos_usuario = preparar_engine(respuestas, SistemaEducativo, Perfil)
    # Ahora agregamos las dificultades
    from hechos import UU, VV

    if resp_teorica:
      engine.declare(UU())

    if resp_practica:
     engine.declare(VV())

    # Ejecutar inferencia secundaria
    engine.run()

    finales_ids = imprimir_todo_unificado(engine, hechos_usuario, "reglas.py")
    # Aqui explicaion de TRazabilidad
    from engine_utils import imprimir_trazabilidad
    imprimir_trazabilidad()

    imprimir_despedida(nombre_usuario)

if __name__ == "__main__":
    run_engine()



