# troncales.py
import json
from collections import defaultdict

def cargar_materias_troncales(path="materias_troncales.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    correlativas_dict = defaultdict(list)

    for fila in data["materias_troncales"]:
        materia = fila["nombre"]
        correlativa = fila["correlativa"]
        anio = fila["año"].capitalize()
        cuatri = fila["cuatrimestre"]

        if correlativa.lower() == "no tiene":
            continue

        requisitos = [c.strip() for c in correlativa.split("y")]

        for req in requisitos:
            correlativas_dict[req].append(
                f"{materia} (de {anio} año, {cuatri} cuatrimestre)"
            )

    mensajes = []
    for req, destinos in correlativas_dict.items():
        destinos_str = ", ".join(destinos)
        mensajes.append(
            f" {req} para avanzar a: {destinos_str}."
        )

    return mensajes
