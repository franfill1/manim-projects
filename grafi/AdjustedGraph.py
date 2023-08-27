from manim import Graph, Line, Arc
from manim import WHITE
from manim import Create, rush_into, rush_from
from manim import override_animate, AnimationGroup, Succession
import numpy as np
import math


def unit_vector(vector):
    """ Returns the unit vector of the vector. """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2' """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


class DirectedGraph(Graph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_updaters()
        self.add_updater(lambda g: g.update_edges())
        self.update()

    def update_edges(self):
        for (u, v), e in self.edges.items():
            self.position_edge(e, u, v)

    def create_edge(self, edge, edge_type=Line, edge_config=None):
        u, v = edge
        if edge_config is None:
            edge_config = {}
        center_u = self[u].get_center()
        center_v = self[v].get_center()
        d = unit_vector(center_u - center_v)
        start = center_u - d * self[u].radius
        end = center_v + d * self[u].radius
        edge = edge_type(start, end, **edge_config)
        return edge

    def position_edge(self, edge, u, v):
        center_u = self[u].get_center()
        center_v = self[v].get_center()
        d = unit_vector(center_u - center_v)
        start = center_u - d * self[u].radius
        end = center_v + d * self[v].radius
        edge.put_start_and_end_on(start, end)

    def travel(self,
               u, v,
               edge_color=None,
               vertex_color=WHITE,
               edge_type=Line,
               edge_config=None):
        pass

    @override_animate(travel)
    def animate_travel(self,
                       u, v,
                       edge_color=None,
                       vertex_color=None,
                       edge_type=Line,
                       edge_config=None,
                       anim_args=None):
        print(edge_color)
        if edge_config is None:
            edge_config = {}
        if edge_color is not None:
            edge_config["stroke_color"] = edge_color
        animation = anim_args.pop("animation", Create)

        edge = self.create_edge((u, v), edge_config=edge_config)

        if vertex_color:
            direction = edge.get_end() - self[v].get_center()
            angle = angle_between(direction, np.array([1, 0, 0]))

            if (direction[1] < 0):
                angle = 2*math.pi - angle
            arc1 = Arc(radius=self[v].radius,
                       arc_center=self[v].get_center(),
                       start_angle=angle,
                       angle=math.pi,
                       stroke_color=vertex_color,
                       stroke_width=self[v].stroke_width)  # .set_z_index(1)
            arc2 = Arc(radius=self[v].radius,
                       arc_center=self[v].get_center(),
                       start_angle=angle,
                       angle=-math.pi,
                       stroke_color=vertex_color,
                       stroke_width=self[v].stroke_width)  # .set_z_index(1)

            def on_finish(scene):
                if (u, v) in self.edges:
                    self.remove(self.edges[(u, v)])
                scene.remove(edge)
                self.add(edge)
                self.edges[(u, v)] = edge
                scene.remove(arc1, arc2)
                self[v].set_stroke(color=vertex_color)

            return Succession(animation(edge,
                                        rate_func=rush_into,
                                        **anim_args),
                              AnimationGroup(animation(arc1, **anim_args),
                                             animation(arc2, **anim_args),
                                             group=self,
                                             rate_func=rush_from),
                              _on_finish=on_finish,
                              group=self)
        else:
            def on_finish(scene):
                if (u, v) in self.edges:
                    self.remove(self.edges[(u, v)])
                scene.remove(edge)
                self.add(edge)
                self.edges[(u, v)] = edge
            return animation(edge, **anim_args, _on_finish=on_finish,
                             group=self)
