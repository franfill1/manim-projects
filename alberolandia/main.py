from manim import *
from manim import OpenGLVMobject
from math import *
import random

class Node(OpenGLVMobject):
	def __init__(self, label):
		super().__init__()
		self.body = Circle().set_stroke(color=WHITE).set_fill(color=BLACK, opacity=0.8)
		self.text = Text(label)
		self.add(self.body)
		self.add(self.text)
	
	def get_point_toward(self, obj):
		"""
		calcola il punto sul quale deve trovarsi l'estremo di un arco che collega il nodo all'oggetto
		"""
		dx = obj.get_x() - self.get_x()
		dy = obj.get_y() - self.get_y()

		if (dy == 0.0):
			y = 0
			x = 1
		else:
			r = abs(dx/dy)
			"""
			x = r*y
			x*x + y*y = 1
			-> y*y*(r*r+1) = 1
			"""
			y = sqrt(1/(r*r+1))
			x = r*y 
			
		if (dx < 0):
			x = -x
		if (dy < 0):
			y = -y

		x *= self.body.width/2
		y *= self.body.width/2
		return [self.get_x() + x, self.get_y() + y, 0]

class Edge(OpenGLVMobject):
	def __init__(self, A, B):
		super().__init__()
		self.nodeA = A
		self.nodeB = B
		self.body = Line()

		self.add_updater(Edge.updater)
		self.add(self.body)
		self.update()

	def calcLength(self):
		"""
		calcola la lunghezza dell'arco, basandosi sulla posizione e sulla dimensione dei nodi
		"""
		x0 = self.nodeA.get_x()
		x1 = self.nodeB.get_x()
		dx = x1-x0

		y0 = self.nodeA.get_y()
		y1 = self.nodeB.get_y()
		dy = y1-y0

		r0 = self.nodeA.body.width / 2
		r1 = self.nodeB.body.width / 2

		d = sqrt(dx*dx + dy*dy)
		return d - (r0 + r1);
	
	def updater(self):
		"""
		posiziona l'arco
		"""
		if (self.calcLength() > 0):
			pa = self.nodeA.get_point_toward(self.nodeB)
			pb = self.nodeB.get_point_toward(self.nodeA)
			self.body.become(Line(pa, pb, color=self.color).add_tip(tip_length=0.2))
		else:
			self.body.become(Line([0, 0, 0], [0, 0, 0]))
	
def makeTree(n, x0=-4, x1=4, y=3, parent=None, step=1):
	global nodes, full 
	x = (x0+x1)/2
	animations = [nodes[n].animate.move_to([x, y, 0])]
	count = len(full[n])
	if parent!=None:
		count -= 1
	
	if (count != 0):
		size = (x1-x0)/count

		ind = 0
		for	ne in full[n]: 
			if (ne != parent):
				animations += makeTree(ne, x0 + ind*size, x0+(ind+1)*size, y-step, n, step)
				ind+=1
	return animations

def getToRevert(n, par=None):
	global graph, full, ref
	ans = []
	for i, ne in enumerate(full[n]):
		if ne != par:
			if not(ne in graph[n]):
				ans.append(ref[n][i])
			ans += getToRevert(ne, n)
	return ans

class myScene(Scene):
	def construct(self):
		global nodes, edges, graph, full, ref, cnt
		nodes = []
		edges = []
		graph = []
		full = []
		ref = []
		cnt = 0

		text = Text("")
		text.add_updater(lambda x : x.become(Text("Archi da invertire: " + str(cnt)).shift([3, 3, 0]).scale(0.5)))
		self.add(text)

		with open("input.txt", "r") as file:
			nm = file.readline()
			n = int(nm.split()[0])

			for i in range(n):
				x = random.randrange(-4, 4)
				y = random.randrange(-4, 4)
				nodes.append(Node(str(i+1)).shift([x, y, -1]).scale(0.4))
				graph.append([])
				full.append([])
				ref.append([])

			for i in range(n-1):
				l = file.readline()
				a = int(l.split()[0]) - 1
				b = int(l.split()[1]) - 1
				edge = Edge(nodes[a], nodes[b]);
				edges.append(edge)
				self.add(edge)

				graph[a].append(b)

				full[a].append(b)
				ref[a].append(edge)

				full[b].append(a)
				ref[b].append(edge)
			
			for node in nodes:
				self.add(node)

		self.play(*makeTree(0, step=2))

		for edge in edges:
			edge.remove_updater(Edge.updater)

		rect = SurroundingRectangle(nodes[0], buff = 0.1, color = GREEN)
		self.play(Create(rect))

		toRevert = getToRevert(0)
		
		for ed in toRevert:
			cnt += 1
			self.play(Indicate(ed.set_color(RED)))
			self.wait(0.5)

		self.explore(0, rect)
		self.wait(2)

	def explore(self, n, rect, par=None):
		global nodes, edges, graph, full, ref, cnt
		self.wait(0.5)
		for i, ne in enumerate(full[n]):
			if ne != par:
				an = rect.animate.move_to(nodes[ne])

				if not(ne in graph[n]):
					cnt-=1
					self.play(an, ref[n][i].animate.set_color(WHITE))
					ref[n][i].set_color(WHITE)
				else:
					cnt+=1
					self.play(an, ref[n][i].animate.set_color(RED))
					ref[n][i].set_color(RED)
	
				self.explore(ne, rect, n)
				self.wait(0.5)

				an = rect.animate.move_to(nodes[n])

				if not(ne in graph[n]):
					cnt+=1
					self.play(an, ref[n][i].animate.set_color(RED))
					ref[n][i].set_color(RED)
				else:
					cnt-=1
					self.play(an, ref[n][i].animate.set_color(WHITE))
					ref[n][i].set_color(WHITE)
