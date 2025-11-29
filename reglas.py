# reglas.py
from experta import *
from hechos import *

# ======== TRAZAS PARA EXPLICABILIDAD ========
EXPLICACION = []
def registrar(regla, antecedentes, consecuentes):
    EXPLICACION.append({
        "regla": regla,
        "antecedentes": antecedentes,
        "consecuentes": consecuentes
    })

class SistemaEducativo(KnowledgeEngine):

    # 1
    @Rule(Perfil(AB=True), Perfil(AG=True))
    def r1(self):
        registrar("R1", ["AB=True", "AG=True"], ["A"])
        self.declare(A())
    
    # 2
    @Rule(Perfil(AB=True))
    def r2(self):
        registrar("R2", ["AB=True"], ["FF"])
        self.declare(FF())

    # 3
    @Rule(FF())
    def r3(self):
        registrar("R3", ["FF"], ["E", "V"])
        self.declare(E(), V())

    # 4
    @Rule(Perfil(AG=True))
    def r4(self):
        registrar("R4", ["AG=True"], ["A","C","D","AA"])
        self.declare(B(), C(), D(), AA())


    # 5
    @Rule(Perfil(AH=True))
    def r5(self):
        registrar("R5", ["AH=True"], ["I","K"])
        self.declare(I(), K())

    # 6
    @Rule(K())
    def r6(self):
        registrar("R6", ["K"], ["X"])
        self.declare(X())

    # 7
    @Rule(Perfil(AF=True))
    def r7(self):
        registrar("R7", ["AF=True"], ["F","T","U","LL"])
        self.declare(F(), T(), U(), LL())

    # 8
    @Rule(Perfil(AD=True))
    def r8(self):
        registrar("R8", ["Ad=True"], ["L", "M"])
        self.declare(L(), M())

    # 9
    @Rule(Perfil(AC=True))
    def r9(self):
        registrar("R9", ["AC=True"], ["M", "N"])
        self.declare(M(), N())


    # 10
    @Rule(O())
    def r10(self):
        registrar("R10", ["O"], ["S","R"])
        self.declare(S(), R())


    # 11
    @Rule(Perfil(AI=True))
    def r11(self):
        registrar("R11", ["AI=True"], ["AA","DD"])
        self.declare(AA(), DD())

    # 12
    @Rule(Perfil(AI=True), Perfil(AG=True))
    def r12(self):
        registrar("R12", ["AI=True", "AG=True"], ["GG"])
        self.declare(GG())

    # 13
    @Rule(DD())
    def r13(self):
        registrar("R13", ["DD"], ["EE"])
        self.declare(EE())


    # 14
    @Rule(Perfil(AB=True), Perfil(AF=True), Perfil(AI=True))
    def r14(self):
        registrar("R14", ["AB=True", "AG=True", "AI=True"], ["BB"])
        self.declare(BB())

    # 15
    @Rule(BB())
    def r15(self):
        registrar("R15", ["BB"], ["CC"])
        self.declare(CC())


    # 16
    @Rule(Perfil(AE=True), Perfil(AG=True))
    def r16(self):
        registrar("R16", ["AB=True", "AG=True"], ["KK","GG"])
        self.declare(KK(), GG())

    # 17
    @Rule(GG())
    def r17(self):
        registrar("R17", ["GG"], ["HH","K","II"])
        self.declare(HH(), K(), II())

    # 18
    @Rule(HH())
    def r18(self):
        registrar("R18", ["HH"], ["JJ","M","N"])
        self.declare(JJ(), M(), N())


    # 19
    @Rule(Perfil(AI=True), Perfil(AH=True))
    def r19(self):
        registrar("R19", ["AI=True", "AH=True"], ["LL","MM"])
        self.declare(LL(), MM())

    # 20
    @Rule(Perfil(AI=True), GG())
    def r20(self):
        registrar("R20", ["AI=True", "GG"], ["NN"])
        self.declare(NN())

    # 21
    @Rule(LL())
    def r21(self):
        registrar("R21", ["LL"], ["OO"])
        self.declare(OO())

    # 22
    @Rule(MM())
    def r22(self):
        registrar("R22", ["MM"], ["A"])
        self.declare(A())


    # 23
    @Rule(Perfil(AE=True), Perfil(AF=True))
    def r23(self):
        registrar("R23", ["AE=True", "AF=True"], ["BB"])
        self.declare(BB())

    # 24
    @Rule(BB())
    def r24(self):
        registrar("R24", ["BB"], ["HH","RR"])
        self.declare(HH(), RR())

    # 25
    @Rule(HH())
    def r25(self):
        registrar("R25", ["HH"], ["N","M"])
        self.declare(N(), M())


    # 26
    @Rule(Perfil(AF=True), Perfil(AC=True), Perfil(AD=True))
    def r26(self):
        registrar("R26", ["AF=True", "AC=True", "AD=True"], ["QQ"])
        self.declare(QQ())

    # 27
    @Rule(QQ())
    def r27(self):
        registrar("R27", ["QQ"], ["G"])
        self.declare(G())

    # 28
    @Rule(Perfil(AC=True), Perfil(AE=True))
    def r28(self):
        registrar("R28", ["AC=True", "AE=True"], ["QQ"])
        self.declare(QQ())
    
    #29
    @Rule(UU())
    def dificultad_teorica(self):
        registrar("R29", ["UU"], ["U1","U2","U3"])
        self.declare(U1())
        self.declare(U2())
        self.declare(U3())
    #30
    @Rule(VV())
    def dificultad_practica(self):
        registrar("R30", ["VV"], ["V1", "W"])
        self.declare(V1())
        self.declare(W())
   #31
    @Rule(UU(), W())
    def regla_mixta(self):
        registrar("R231", ["UU", "W"], ["U1","U2","U3","V1", "W"])
        self.declare(U1())
        self.declare(U2())
        self.declare(U3())
        self.declare(V1())
        self.declare(W())


    