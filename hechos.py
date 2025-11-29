# hechos.py
from experta import Fact

# -------------------------------
# HECHOS DE PERFILES
# -------------------------------

class Perfil(Fact):
    """Hechos de perfiles del estudiante"""
    pass
# AB SOLO ESTUDIA
# AC TRABAJA MAÑANA
# AD TRABAJA TARDE
# AE TRABAJA NOCHE
# AF CURSAR ALGUNAS MATERIAS
# AG CURSAR TODAS LAS MATERIAS
# AH RETOMA ESTUDIO
# AI ESTUDIA DOS CARRERAS


# -------------------------------
# HECHOS RESTANTES
# -------------------------------
class A(Fact): pass   # dedicar una hora por turno
class B(Fact): pass   # seguir ritmo
class C(Fact): pass   # rendir finales apenas termina
class D(Fact): pass   # promocionar materias
class E(Fact): pass   # asistir y tomar apuntes
class F(Fact): pass  # (F) tiempo fijo a cada materia
class G(Fact): pass   # organizar tiempos por doble turno
class H(Fact): pass  # priorizar materias
class I(Fact): pass   # motivar
class J(Fact): pass   # no tiene método
class K(Fact): pass   # recomendar técnica
class L(Fact): pass   # horario mañana
class M(Fact): pass   # clases virtuales
class N(Fact): pass   # horario tarde
class O(Fact): pass   # dificulta retomar ritmo
class P(Fact): pass   # método de estudio
class Q(Fact): pass   # dificultad para entender materia
class R(Fact): pass   # cursos nivelatorios
class S(Fact): pass   # tutores académicos
class T(Fact): pass   # materias troncales
class U(Fact): pass   # aprovechar tiempo libre
class V(Fact): pass   # clases presenciales
class W(Fact): pass   # clases de consulta
class X(Fact): pass   # mapa conceptual
class Y(Fact): pass   # consultar compañero
class Z(Fact): pass   # buscar en internet
class AA(Fact): pass  # evitar superposición
class BB(Fact): pass  # riesgo estrés
class CC(Fact): pass  # actividades recreativas
class DD(Fact): pass  # equivalencias
class EE(Fact): pass  # priorizar materias comunes
class FF(Fact): pass  # tiene disponibilidad
class GG(Fact): pass  # sobrecarga académica
class HH(Fact): pass  # horarios flexibles
class II(Fact): pass  # manejo de estrés
class JJ(Fact): pass  # cursar descansado
class KK(Fact): pass  # buena organización
class LL(Fact): pass  # plan de horarios
class MM(Fact): pass  # plan estudio diario
class NN(Fact): pass  # priorizar carrera principal
class OO(Fact): pass  # usar google calendar
class PP(Fact): pass  # llegar descansado
class QQ(Fact): pass  # dificultad asistir clases
class RR(Fact): pass  # plan de descanso
class SS(Fact): pass  # apoyarse en materiales virtuales
class TT(Fact): pass  # cronograma de clases
# ---------------------------------------------------
# Hechos sobre dificultades (simples)
# ---------------------------------------------------

class UU(Fact):
    """Tiene dificultad en la parte teórica"""
    pass

class U1(Fact):
    """Hacer resúmenes entendiendo el tema"""
    pass

class U2(Fact):
    """Subrayar conceptos claves"""
    pass

class U3(Fact):
    """Hacer diagramas"""
    pass


class VV(Fact):
    """Tiene dificultad en la parte práctica"""
    pass

class V1(Fact):
    """Intentar resolver ejercicios"""
    pass

class W(Fact):
    """Ir a clases de consulta"""
    pass
