# engine_utils.py
import os
import re
from reglas import EXPLICACION
from significados import SIGNIFICADOS

def detectar_hechos_antecedentes(path_reglas):
    if not os.path.isfile(path_reglas):
        print(f"⚠️ No encontré {path_reglas}. Usando lista vacía.")
        return set()
    antecedentes = set()
    with open(path_reglas, 'r', encoding='utf-8') as f:
        contenido = f.read()
    for match in re.finditer(r'@Rule\s*\((.*?)\)\s*def', contenido, re.DOTALL):
        dentro = match.group(1)
        for name in re.findall(r'\b([A-Z][A-Za-z0-9_]*)\s*\(', dentro):
            antecedentes.add(name)
    return antecedentes

def calcular_hechos_finales_auto(engine, path_reglas="reglas.py"):
    hechos_inferidos = []
    for fid, hecho in engine.facts.items():
        hechos_inferidos.append(hecho.__class__.__name__)
    hechos_inferidos = list(dict.fromkeys(hechos_inferidos))

    antecedentes = detectar_hechos_antecedentes(path_reglas)

    return [h for h in hechos_inferidos if h not in antecedentes]

def preparar_engine(respuestas, SistemaEducativo, Perfil):
    engine = SistemaEducativo()
    engine.reset()

    hechos_usuario = set()

    # === TRABAJA ===
    if respuestas.get("trabaja") is True:
        turno = respuestas.get("turno_trabajo")
        if turno:
            engine.declare(Perfil(**{turno: True}))
            hechos_usuario.add(turno)
    else:
        engine.declare(Perfil(AB=True))  # se mantiene tu lógica
        # NO agregar AB a hechos_usuario

    # === CURSA TODAS ===
    if respuestas.get("cursa_todas") is True:
        engine.declare(Perfil(AG=True))
        hechos_usuario.add("AG")
    else:
        engine.declare(Perfil(AF=True))  # se mantiene tu lógica
        # NO agregar AF a hechos_usuario

    # === RETOMA ===
    if respuestas.get("retoma_estudios") is True:
        engine.declare(Perfil(AH=True))
        hechos_usuario.add("AH")

    # === DOBLE CARRERA ===
    if respuestas.get("doble_carrera") is True:
        engine.declare(Perfil(AI=True))
        hechos_usuario.add("AI")

    engine.run()
    return engine, hechos_usuario


def imprimir_trazabilidad():
    print("\n====================================")
    print("     EXPLICACIÓN DEL RAZONAMIENTO")
    print("====================================\n")

    # Convierte una clave/etiqueta de hecho a su significado si existe en SIGNIFICADOS.
    def significado(hecho_raw):
        # hecho_raw puede venir en formatos como: "AB", "AB=True", "Perfil(AB=True)" o "A"
        if not isinstance(hecho_raw, str):
            return str(hecho_raw)

        hecho = hecho_raw

        # Si viene "X=Y" o "X=True" tomamos la parte izquierda
        if "=" in hecho:
            hecho = hecho.split("=", 1)[0]

        # Si viene algo como Perfil(AB=True) tomamos antes del paréntesis
        if "(" in hecho:
            inside = re.search(r'\((.*?)\)', hecho)
            if inside:
                contenido = inside.group(1)
                # contenido puede ser "AB=True" -> tomamos antes del '='
                hecho = contenido.split("=", 1)[0]

        hecho = hecho.strip()
        return SIGNIFICADOS.get(hecho, hecho_raw)  # si no está, devolvemos el raw original

    # Imprimimos la traza utilizando SIGNIFICADOS
    if not EXPLICACION:
        print("(No hay registro de explicaciones. Asegurate de haber registrado con 'registrar(...)' en reglas.py.)")
    else:
        for paso in EXPLICACION:
            regla = paso.get("regla", "sin_nombre")
            antecedentes = paso.get("antecedentes", []) or paso.get("antecedent", [])
            consecuentes = (
                paso.get("consecuentes", [])
                or paso.get("consecuente", [])
                or paso.get("inferred", [])
                or paso.get("consequences", [])
            )

            print(f"\n• Se activó {regla}:")

            # Antecedentes (mostrados con significado)
            if antecedentes:
                print("   - Porque se cumplieron:")
                for ant in antecedentes:
                    print(f"       • {significado(ant)}")
            else:
                print("   - Porque se cumplieron: (no hay antecedentes registrados)")

            # Consecuentes / inferidos (mostrados con significado)
            if consecuentes:
                print("   - Entonces el sistema infirió:")
                for c in consecuentes:
                    print(f"       • {significado(c)}")
            else:
                print("   - Entonces el sistema infirió: (no hay consecuentes registrados)")
