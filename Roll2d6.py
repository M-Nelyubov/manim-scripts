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

        label = self.label()
        if '--noColor ' in label:
            substrings_to_isolate=[]    # This particular function doesn't support being colored properly due to being too complex
            label = label.replace('--noColor ', '')
        else:
            substrings_to_isolate=["d_1","d_2"]
        label = MathTex(label,substrings_to_isolate=substrings_to_isolate).move_to(UP*3 + RIGHT*2)

        if len(substrings_to_isolate):
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


class MultipleRulesConstSum(Sum):
    def randomVariable(self, d1, d2):
        if d1 <= 4 and d2 <=4:
            return 3
        else:
            return d1 + d2

    def label(self):
        return r"--noColor X(d_1,d_2) = \begin{cases} 3 & d_1 \leq 4 \cap d_2 \leq 4 \\ d_1 + d_2 & \text{else} \end{cases}"


class ConditionalMapping():
    def __init__(self):
        pass

    def rv(self, d1, d2): 
        # returns a tuple (r_val : float, rule : int)
        # Random variable - a function of ω = (d1, d2) --> R (r_val)
        # rule (which entry in the list or rules this corresponds to)
        pass

    def rules(self):
        return []

class ConstOrSum(ConditionalMapping):
    def rv(self,d1, d2):
        if d1 <= 4 and d2 <=4:
            return 3, 0
        else:
            return d1 + d2, 1
    
    def rules(self):
        return [
            ("3",         r"d_1 \leq 4 \cap d_2 \leq 4"),
            ("d_1 + d_2", "else")
        ]


class RollAdvanced(Scene):
    ### Start with a grid of the sample space of 2d6 (2023F Chapter 3 Example 3.3)
    ### Draw ovals around each element of the sample space, transfer it over to the Reals number line
    # stack them up as a histogram?


    def construct(self):
        X = ConstOrSum()

        opening_scroll = Tex("A Random Variable maps elements \n\n of the sample space (S) to the real axis.\n\nLet's view some examples of this mapping.")
        self.play(Write(opening_scroll))

        self.wait(3)

        self.play(Unwrite(opening_scroll, reverse=False))

        self.wait(1)

        S = VGroup()        # Create the sample space S (storing all events)
        support = set()     # Create a set for the support values in R
        for i in range(1,7):
            for j in range(1,7):
                event = Tex(f"{i},{j}")
                event[0][0].set_color(RED)     # color dice red and green
                event[0][2].set_color(GREEN)
                S.add(event)
                support.add(X.rv(i,j)[0])

        # Generate the sample space grid on the left
        S.arrange_in_grid(buff=0.4).move_to(4 * LEFT)
        
        # Generate a number line on the right
        num_line = NumberLine(
            x_range=[min(support)-1, max(support)+2, 1],
            length=6,
            include_tip=True,
            include_numbers=True,
        ).move_to(RIGHT * 4)

        self.play(Write(S))
        self.play(Write(num_line))

        # Create the LaTeX to describe this random variable
        substrings_to_isolate=["d_1","d_2"]
        condition_matrix = VGroup()
        rules = X.rules()
        for vc in rules:   # VC is a tuple of two elements (value, condition) to iterate over (with 'label')
            for label in vc:
                label = MathTex(label,     substrings_to_isolate=substrings_to_isolate)
                label.set_color_by_tex("d_1", RED)
                label.set_color_by_tex("d_2", GREEN)
                condition_matrix.add(label)
        condition_matrix.arrange_in_grid(cols=2,buff=0.4).move_to(UP*3 + RIGHT*3)

        # Determine whether or not the brace is necessary based on how many rules there are
        text_offset = 1
        elements = [Write(condition_matrix)]
        if len(condition_matrix) > 1:
            brace = Brace(condition_matrix, LEFT)
            elements.append(Write(brace))
            text_offset = 2
        
        x_text = MathTex("X(d_1,d_2) = ", substrings_to_isolate=substrings_to_isolate).next_to(condition_matrix, LEFT * text_offset)
        x_text.set_color_by_tex("d_1", RED)
        x_text.set_color_by_tex("d_2", GREEN)
        elements.append(Write(x_text))

        self.play(*elements)
        
        self.wait(2)


        support = list(support)
        support.sort()
        print(support)

        run_time = 1  # Time in seconds for each animation

        priors = {}
        for i in support:
            priors[i]=0

        def get_mapping(elem):  # s in S
            d_0, d_1 = elem.tex_string.split(",")
            r_v, rule = X.rv(int(d_0), int(d_1))
            frame = SurroundingRectangle(elem, buff=0.1)

            point = num_line.number_to_point(r_v)
            rect = Rectangle(
                height=0.1, 
                width=0.1,
                color=ORANGE,
                fill_color=ORANGE,
            ).move_to(point + UP * 0.1 * priors[r_v])  # Shift up by the amount of prior occurances of X
            
            priors[r_v]+=1  # Increment how many times we've seen this

            frame_anim = Write(frame, run_time=run_time)
            frame_move = ReplacementTransform(frame, rect, run_time=run_time)

            return frame_anim, frame_move

        slow_demo_samples = 3

        i=0
        for elem in S:
            frame_anim, frame_move = get_mapping(elem)
            self.play(frame_anim)
            self.wait(1)
            self.play(frame_move)
            self.wait(1)

            i+=1
            if i >= slow_demo_samples:
                break


        return ""
    
        # for i in support:

        #     elems = []
        #     for elem in S:
        #         d_0, d_1 = elem.tex_string.split(",")
        #         _X = X.rv(int(d_0), int(d_1))
        #         if _X != i: continue
        #         elems.append(elem)
            
        #     anim1 = []
        #     anim2 = []
        #     for s in elems:

        #     self.play(*anim1)
        #     self.play(*anim2)            
        
        # self.wait(3)
