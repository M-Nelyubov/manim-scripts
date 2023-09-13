from manim import *
import numpy as np

class Sum(Scene):
    ### Start with a grid of the sample space of 2d6 (2023F Chapter 3 Example 3.3)
    ### Draw ovals around each element of the sample space, transfer it over to the Reals number line
    # stack them up as a histogram?

    def randomVariable(self, d1, d2):
        return d1+d2

    def label(self):
        return "X(d_1,d_2) = d_1 + d_2"

    def construct(self):
        S = VGroup()

        support = set()

        for i in range(1,7):
            for j in range(1,7):
                event = Tex(f"{i},{j}")
                event[0][0].set_color(RED)
                event[0][2].set_color(GREEN)
                S.add(event)
                support.add(self.randomVariable(i,j))

        S.arrange_in_grid(buff=0.4).move_to(4 * LEFT)
        
        num_line = NumberLine(
            x_range=[min(support)-1, max(support)+2, 1],
            length=6,
            include_tip=True,
            include_numbers=True,
        ).move_to(RIGHT * 4)

        label = MathTex(self.label(),substrings_to_isolate=["d_1","d_2"]).move_to(UP*3 + RIGHT*2)
        label.set_color_by_tex("d_1", RED)
        label.set_color_by_tex("d_2", GREEN)

        self.add(S, num_line, label)
        
        self.wait()

        run_time = 1  # Time in seconds for each animation

        support = list(support)
        support.sort()
        print(support)

        priors = {}
        for i in support:
            priors[i]=0

            elems = []
            for elem in S:
                d_0, d_1 = elem.tex_string.split(",")
                X = self.randomVariable(int(d_0), int(d_1))
                if X != i: continue
                elems.append(elem)
            
            anim1 = []
            anim2 = []
            for s in elems:
                frame = SurroundingRectangle(s, buff=0.1)

                point = num_line.number_to_point(i)
                rect = Rectangle(
                    height=0.1, 
                    width=0.1,
                    color=ORANGE,
                    fill_color=ORANGE,
                ).move_to(point + UP * 0.1 * priors[i])  # Shift up by the amount of prior occurances of X
                
                priors[i]+=1  # Increment how many times we've seen this

                anim1.append(
                    Write(frame, run_time=run_time)
                )

                anim2.append(
                    ReplacementTransform(frame, rect, run_time=run_time)
                )

            self.play(*anim1)
            self.play(*anim2)            
        
        self.wait(3)

class Difference(Sum):
    def randomVariable(self, d1, d2):
        return d1-d2

    def label(self):
        return "X(d_1,d_2) = d_1 - d_2"

class Eq_2d1_6(Sum):
    def randomVariable(self, d1, d2):
        return 2*d1 + 6

    def label(self):
        return "X(d_1,d_2) = 2d_1 + 6"

class Eq_d1(Sum):
    def randomVariable(self, d1, d2):
        return d1

    def label(self):
        return "X(d_1,d_2) = d_1"

class Min(Sum):
    def randomVariable(self, d1, d2):
        return min(d1,d2)

    def label(self):
        return "X(d_1,d_2) = min(d_1, d_2)"

class Max(Sum):
    def randomVariable(self, d1, d2):
        return max(d1,d2)

    def label(self):
        return "X(d_1,d_2) = max(d_1, d_2)"

class One(Sum):
    def randomVariable(self, d1, d2):
        return 1

    def label(self):
        return "X(d_1,d_2) = 1"



