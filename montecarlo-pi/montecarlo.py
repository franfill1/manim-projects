from manim import Scene, Create, always_redraw
from manim import Square, Circle, Dot, Tex
from manim import WHITE, RED, BLUE
from manim import LEFT, RIGHT, UP, DOWN
import random


class montecarlo_pi(Scene):
    def construct(self):
        random.seed(0)
        n = 1000
        scale_factor = 3
        delay = 0.1
        batch_size = 100
        square = Square().scale(scale_factor).set_stroke(color=BLUE)
        circle = Circle().set_stroke(color=RED).scale(scale_factor)
        self.play(Create(circle), Create(square))

        in_count = 0
        dots = []
        to_add = []
        estimate = 0

        count_text = always_redraw(lambda: Tex("Inside: %0.3f" % in_count)
                                   .next_to(square, RIGHT))
        pi_text = always_redraw(lambda: Tex("Estimate: %0.3f" % estimate)
                                .next_to(square, RIGHT)
                                .shift(DOWN*count_text.height*1.5))
        self.add(count_text, pi_text)

        for i in range(n):
            x_coord = random.uniform(-1, 1)*scale_factor
            y_coord = random.uniform(-1, 1)*scale_factor
            if x_coord**2 + y_coord**2 <= scale_factor**2:
                color = RED
                in_count += 1
            else:
                color = BLUE
            dot = Dot([x_coord, y_coord, 0]).set_color(color)\
                .scale(0.5).set_z_index(-1)
            dots.append(dot)
            to_add.append(dot)
            estimate = in_count*4 / (i+1)
            if len(to_add) >= batch_size:
                count_text.update()
                pi_text.update()
                self.add(*to_add)
                self.wait(delay)
                to_add = []
