from manim import Scene, Circle, FadeToColor, VGroup
from manim import YELLOW, WHITE, GREEN
from AdjustedGraph import DirectedGraph


class Node(VGroup):
    def __init__(self, label, radius, **kwargs):
        super().__init__(**kwargs)
        self.body = Circle(radius, **kwargs)
        self.radius = radius
        self.label = label
        self.add(self.body, self.label)


class ProvaScena(Scene):
    def construct(self):
        N = 30
        edges = [(0, 1), (1, 2), (4, 5),
                 (1, 7), (3, 9), (5, 11),
                 (6, 7), (8, 9), (9, 10), (10, 11),
                 (6, 12), (11, 17),
                 (14, 15),
                 (12, 18), (13, 19), (14, 20), (15, 21), (16, 22), (17, 23),
                 (18, 19), (21, 22), (22, 23),
                 (18, 24), (19, 25), (21, 27), (22, 28),
                 (25, 26), (26, 27), (28, 29)]
        layout = {}
        for i in range(N):
            layout[i] = (i % 6, -(i // 6), 0)

        g = DirectedGraph(vertices=list(range(N)),
                          edges=edges,
                          label_fill_color=WHITE,
                          layout=layout,
                          vertex_config={
                                         "stroke_color": WHITE,
                                         "stroke_width": 15},
                          ).move_to((0, 0, 0))
        #for x in g.vertices.values():
        #    x.set_z_index(1)
        self.add(g)
        self.wait()

        vis = [False] * N
        done = [False] * N
        queue = []

        r = 21
        vis[r] = True
        self.play(FadeToColor(g[r], YELLOW), run_time=0.2)
        queue.append(r)
        while len(queue):
            x = queue.pop(0)
            for y in g._graph.neighbors(x):
                if vis[y] and not done[y]:
                    self.play(g.animate.travel(x, y, edge_color=YELLOW),
                              run_time=0.5)
                if not vis[y]:
                    self.play(g.animate.travel(x, y,
                                               edge_color=YELLOW,
                                               vertex_color=YELLOW),
                              run_time=0.5)
                    queue.append(y)
                    vis[y] = True
            vertex = g[x]
            done[x] = True
            self.play(FadeToColor(vertex, GREEN), run_time=0.2)

        self.play(g.animate.change_layout("tree", root_vertex=r))
        self.play(g.animate.change_layout("circular"))
        self.wait(5)
