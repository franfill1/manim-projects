from manim import *
from manim_editor import PresentationSectionType
from math import *
import numpy as np
def get_angle(A, B, C):
    A1 = A-B
    C1 = C-B
    A1 = A1 / np.linalg.norm(A1)
    C1 = C1 / np.linalg.norm(C1)
    return acos(np.dot(A1, C1))

def get_dist(A, B):
    dx = A[0]-B[0]
    dy = A[1]-B[1]
    return sqrt(dx**2 + dy**2)

def get_intersection(p0, p1, q0, q1):
    a = np.transpose(np.array([p0-p1, q1-q0, [1, 1, 1]]))
    b = q1-p1
    i = np.linalg.solve(a, b)
    s = i[1]
    return p0*s + p1*(1-s)
    
    
class sensore(Scene):
    def construct(self):
        
        textScale = 0.8
        baseRuntime = 0.5
        labelRuntime = 0.3
        interval = 0.5
        
        A = np.array([-3, -2.75, 0])
        B = np.array([4, -2.75, 0])
        C = np.array([-2, 3.25, 0])
        X = ((B-C)*get_dist(A,C)/get_dist(B,C) + C)
        Y = ((C-B)*get_dist(A,B)/get_dist(B,C) + B)
        M = (A+X)/2
        N = (A+Y)/2
        V = get_intersection(B, N, C, M)

        ####Triangolo####
        self.next_section("Disegno", type=PresentationSectionType.NORMAL)
        #Vertici
        pA = Dot().move_to(A)
        lA = MathTex("A").scale(textScale).next_to(A, DOWN+LEFT)
        pB = Dot().move_to(B)
        lB = MathTex("B").scale(textScale).next_to(B, DOWN+RIGHT)
        pC = Dot().move_to(C)
        lC = MathTex("C").scale(textScale).next_to(C, UP+LEFT)
      
        #Lati
        AB = Line(pA, pB).set_stroke(color=BLUE)
        BC = Line(pB, pC).set_stroke(color=BLUE)
        CA = Line(pC, pA).set_stroke(color=BLUE)
        
        #Angoli
        alpha = Angle(AB,Line(A, C))
        gamma = Angle(CA,Line(C, B))
        beta = Angle(BC,Line(B, A))
        
        sides = VGroup(AB, BC, CA)
        vertices = VGroup(pA, pB, pC)
        vlabels = VGroup(lA, lB, lC)

        self.play(Create(vertices), run_time=baseRuntime)
        self.play(Write(vlabels), run_time=labelRuntime)
        self.play(Create(sides), run_time=baseRuntime)
        
        #### X e Y ####
        pX = Dot().move_to(X)
        lX = MathTex("X").scale(textScale).next_to(X, UP+RIGHT)
        pY = Dot().move_to(Y)
        lY = MathTex("Y").scale(textScale).next_to(Y, UP+RIGHT)
        
        self.wait(interval)
        self.next_section("X", type=PresentationSectionType.NORMAL)
        temp = VGroup(CA.copy(), pA.copy())
        self.play(Rotate(temp, gamma.get_value(), about_point=C), run_time=baseRuntime)
        self.remove(temp)
        self.add(pX)
        self.play(Write(lX), run_time=labelRuntime)
        
        self.wait(interval)
        self.next_section("Y", type=PresentationSectionType.NORMAL)
        temp = VGroup(AB.copy().set_z_index(-1), pA.copy())
        self.play(Rotate(temp, -beta.get_value(), about_point=B), run_time=baseRuntime)
        self.remove(temp)
        self.add(pY)
        self.play(Write(lY), run_time=labelRuntime)
                
        #### AX e AY ####
        self.wait(interval)
        self.next_section("AX e AY", type=PresentationSectionType.NORMAL)
        AX = Line(A, X)
        AY = Line(A, Y)
        self.play(Create(AX), Create(AY), run_time=baseRuntime)
        
        #### BN e CM ####
        self.wait(interval)
        self.next_section("BN e CM", type=PresentationSectionType.NORMAL)
        pM = Dot().move_to(M)
        lM = MathTex("M").scale(textScale).next_to(M, DOWN+RIGHT)
        pN = Dot().move_to(N)
        lN = MathTex("N").scale(textScale).next_to(N, UP+LEFT)
        
        BN = Line(B, N)
        CM = Line(C, M)
        
        self.play(Create(pN), Create(pM), run_time=baseRuntime)
        self.play(Write(lM), Write(lN), run_time=labelRuntime)
        self.play(Create(BN), Create(CM), run_time=baseRuntime)
        
        #### V e AVM ####
        self.wait(interval)
        self.next_section("V e AVM", type=PresentationSectionType.NORMAL)
        pV = Dot().move_to(V)
        lV = MathTex("V").scale(textScale).next_to(pV, UP+RIGHT, buff=0.1)
        AV = Line(A, V).set_stroke(color=RED).set_z_index(-1)
        AVM = Angle(Line(V, A), Line(V, M)).set_stroke(color=ORANGE)
        
        texAVM = MathTex(r"\angle ", "A", "V", "M", r" =", "\ ?").set_color(ORANGE).shift(RIGHT*5)
        self.play(Create(pV), run_time=baseRuntime)
        self.play(Write(lV), run_time=labelRuntime)
        self.play(Create(AV), run_time=baseRuntime)
        self.play(Create(AVM), run_time=baseRuntime) 
        
        self.wait(interval)
        self.next_section("Angolo AVM", type=PresentationSectionType.NORMAL)
        lAC = lA.copy()
        lVC = lV.copy()
        lMC = lM.copy()
        self.play(lAC.animate.become(texAVM[1]), lVC.animate.become(texAVM[2]), lMC.animate.become(texAVM[3]), run_time=baseRuntime)
        self.play(Write(texAVM[0]), *[Write(tex) for tex in texAVM[4:]], run_time=baseRuntime)
        self.remove(lAC, lVC, lMC)
        self.add(texAVM)
        
        #### ABC ####
        self.wait(interval)
        self.next_section("angolo ABC", type=PresentationSectionType.NORMAL)
        ABC = Angle(Line(B,C), Line(B,A), radius=0.6).set_stroke(color=GREEN)
        
        texABC = MathTex(r"\angle ", "A", "B", "C", r" =\ 62^\circ").set_color(GREEN).shift(RIGHT*5+UP*3)
        
        self.play(Create(ABC), run_time=baseRuntime)
        self.play(lA.copy().animate.become(texABC[1]), lB.copy().animate.become(texABC[2]), lC.copy().animate.become(texABC[3]), run_time=baseRuntime)
        self.play(Write(texABC[0]), *[Write(tex) for tex in texABC[4:]], run_time=baseRuntime)
        
        #### ANGOLI RETTI ####
        self.wait(interval)
        self.next_section("Angoli retti", type=PresentationSectionType.NORMAL)
        BNY = RightAngle(Line(N, B), Line(N, Y), length=0.25)
        CMX = RightAngle(Line(M, C), Line(M, X), length=0.25)
        
        self.play(Create(BNY), run_time=baseRuntime)
        self.play(Create(CMX), run_time=baseRuntime)
        
        #### BAY e AYB ####
        self.wait(interval)
        self.next_section("BAY e AYB", type=PresentationSectionType.NORMAL)
        BAY = Angle(Line(A, B), Line(A, Y)).set_stroke(color=PURPLE).set_z_index(-1)
        AYB = Angle(Line(Y, A), Line(Y, B)).set_stroke(color=PURPLE).set_z_index(-1)
        self.play(Create(BAY), Create(AYB), run_time=baseRuntime)
        
        self.wait(interval)
        self.next_section("Calcoli", type=PresentationSectionType.NORMAL)
        texAYB = MathTex(r"\angle", "A", "Y", "B", r"=", r"{ 180^\circ -", r"\angle ABC", r"\over 2}").set_color(PURPLE).shift(RIGHT*4, UP*2)
        lAC = lA.copy()
        lYC = lY.copy()
        lBC = lB.copy()
        self.play(lAC.animate.become(texAYB[1]), lYC.animate.become(texAYB[2]), lBC.animate.become(texAYB[3]), run_time=baseRuntime)
        self.play(Write(texAYB[0]), *[Write(tex) for tex in texAYB[4:]], run_time=baseRuntime)
        self.remove(lAC, lYC, lBC)
        self.add(texAYB)
        self.next_section("Calcoli", type=PresentationSectionType.NORMAL)
        self.play(texAYB.animate.become(MathTex(r"\angle", "A", "Y", "B", r"=", r"{ 180^\circ -", r"62^\circ", r"\over 2}").set_color(PURPLE).shift(RIGHT*4, UP*2)), run_time=baseRuntime*2)
        self.play(texAYB[5:8].animate.become(MathTex(r"\ {118^\circ", "\over 2}").set_color(PURPLE).shift(RIGHT*4.3, UP*2)), run_time=baseRuntime*2)
        self.play(texAYB[5:8].animate.become(MathTex(r"\ {59^\circ}").set_color(PURPLE).shift(RIGHT*4.3, UP*2)), run_time=baseRuntime*2)
        self.play(texAYB.animate.next_to(texABC, DOWN*2), run_time=baseRuntime)
        
        #### circle ####
        self.wait(interval)
        self.next_section("Cerchio", type=PresentationSectionType.NORMAL)
        circle = Circle(get_dist(V, A)).rotate(-get_angle(X, V, V + [1,0,0])).move_to(V).set_z_index(-1)
        self.play(Create(circle), run_time=baseRuntime)    
              
        #### XV  e AVX ####
        self.wait(interval)
        self.next_section("XV e AVX", type=PresentationSectionType.NORMAL)
        XV = Line(X, V).set_stroke(color=RED).set_z_index(-1)
        AVX = Angle(Line(V, A), Line(V, X), radius=0.5).set_stroke(color=ORANGE)
        self.play(Create(XV), run_time=baseRuntime)
        self.play(Create(AVX), run_time=baseRuntime)

        self.wait(interval)
        self.next_section("Arco", type=PresentationSectionType.NORMAL)
        arcAX = Angle(Line(V, A), Line(V, X), radius=get_dist(V, A)).set_color(RED).set_z_index(-1)
        self.play(arcAX.animate.set_color(YELLOW), run_time=baseRuntime/2)
        
        self.wait(interval)
        self.next_section("Calcoli", type=PresentationSectionType.NORMAL)
        self.play(arcAX.animate.set_color(RED), run_time=baseRuntime/2)
        texAVX = MathTex(r"\angle", "A", "V", "X", "=", r"{\angle AYB", r"\times 2}").set_color(ORANGE).shift(RIGHT*4.5, UP*1)
        lAC = lA.copy()
        lVC = lV.copy()
        lXC = lX.copy()
        self.play(lAC.animate.become(texAVX[1]), lVC.animate.become(texAVX[2]), lXC.animate.become(texAVX[3]), run_time=baseRuntime)
        self.play(Write(texAVX[0]), *[Write(tex) for tex in texAVX[4:]], run_time=baseRuntime)
        self.add(texAVX)
        self.next_section("Calcoli", type=PresentationSectionType.NORMAL)
        self.remove(lAC, lVC, lXC)
        self.play(texAVX.animate.become(MathTex(r"\angle", "A", "V", "X", "=", r"{59^\circ", r"\times 2}").set_color(ORANGE).shift(RIGHT*5, UP*1)), run_time=baseRuntime*2)
        self.play(texAVX[-2:].animate.become(MathTex("118^\circ").set_color(ORANGE).shift(RIGHT*5.9, UP*1)), run_time=baseRuntime*2)
        
        #### finale ####
        self.wait(interval)
        self.next_section("Risultato", type=PresentationSectionType.NORMAL)
        
        self.play(texAVM.animate.become(MathTex(r"\angle ", "A", "V", "M", r" =", r"{\angle AVX \over 2}").set_color(ORANGE).shift(RIGHT*5)), run_time=baseRuntime*2)
        self.next_section("Calcoli", type=PresentationSectionType.NORMAL)
        self.play(texAVM.animate.become(MathTex(r"\angle ", "A", "V", "M", r" =", r"{118 ^\circ \over 2}").set_color(ORANGE).shift(RIGHT*5)), run_time=baseRuntime*2)
        self.play(texAVM.animate.become(MathTex(r"\angle ", "A", "V", "M", r" =", r"{59 ^\circ}").set_color(ORANGE).shift(RIGHT*5)), run_time=baseRuntime*2)
        self.wait()
