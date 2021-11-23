from manim import *
import random

def cross_product(a, b):
    return a[0]*b[1] - a[1]*b[0]

def sign(x):
    return (x>0) - (x<0)
    
def sum(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def neg(p):
    return [-p[0], -p[1], -p[2]]

def side(a, b, c):
    p1 = sum(a, neg(c))
    p2 = sum(b, neg(c))
    return sign(cross_product(p1, p2))
    
class ConvexHullAnimation(MovingCameraScene):
	def convexHull(self, dots, group):
		lines = []

		dots.sort(key= lambda d : list(map(round, d.get_arc_center().tolist())))

		con = [dots[0].get_arc_center().tolist()]
		for dot in dots[1:]:
			point = dot.get_arc_center().tolist()

			self.play(Indicate(dot), run_time=0.5)

			d = Dot(con[-1]).set_fill(opacity=0)
			nl = Line(con[-1], point)
			self.play(Create(nl))
			while(len(con) > 1 and side(con[-1], con[-2], point) > 0):
				con.pop()
				l = lines.pop()
				group -= l

				ang = Angle(Line(l.get_end(), l.get_start()), nl).set_stroke(color=RED)
				self.play(Create(ang), run_time=0.5)

				self.play(FadeOut(ang), run_time=0.5)
				self.play(Uncreate(nl), run_time=0.5)
				self.play(Uncreate(l), run_time=0.5)
				nl = Line(con[-1], point)
				self.play(Create(nl))

			if len(con) > 1:
				l = lines[-1]
				ang = Angle(Line(l.get_end(), l.get_start()), nl).set_stroke(color=GREEN)
				self.play(Create(ang), run_time=0.5)
				self.play(FadeOut(ang), run_time=0.5)
			con.append(point)
			lines.append(nl)
			group += nl
	def construct(self):
		self.camera.frame.move_to([5, 5, 0])
		self.camera.frame.set(height=9)
		dots = []
		grid = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1])
		self.add(grid)
		group = VGroup()

		with open("input.txt") as file:
			for line in file:
				if (len(line.split()) > 1):
					x = int(line.split()[0])
					y = int(line.split()[1])
					point = [x, y, 0]
					dot = Dot(point)
					self.add(dot)
					group += dot
					dots.append(dot)

		self.convexHull(dots, group)

		self.play(Rotate(group))

		self.convexHull(dots, group)
		self.wait(1)

		self.play(Rotate(group))
		self.wait(1)
