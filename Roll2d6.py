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
        return r"--noColor X(d_1,d_2) = \begin{cases} 3 & (d_1 \leq 4) \cap (d_2 \leq 4) \\ d_1 + d_2 & \text{else} \end{cases}"


class ConditionalMapping():
    def __init__(self):
        self.elems_of_interest = []

    def rv(self, d1, d2): 
        # returns a tuple (r_val : float, rule : int)
        # Random variable - a function of ω = (d1, d2) --> R (r_val)
        # rule (index - which entry in the list or rules this corresponds to)
        pass

    def rules(self):
        return []

class ConstOrSum(ConditionalMapping):
    def __init__(self):
        self.elems_of_interest = ["1,1", "4,4", "6,6", "1,5"]

    def rv(self,d1, d2):
        if d1 <= 4 and d2 <=4:
            return 3, 0
        else:
            return d1 + d2, 1
    
    def rules(self):
        return [
            ("3",         r"(d_1 \leq 4) \cap (d_2 \leq 4)"),
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
        wait_time = 0.25

        priors = {}
        for i in support:
            priors[i]=0

        # Keep a data structure at the outer level to track the pointers for all the blocks that go onto the number line
        block_pointers = {}
        for s in support:
            block_pointers[s] = []

        # Create all of the relevant animations
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
            
            # move_elem_to_below_rv 
            temp_tex = MathTex(elem.tex_string).next_to(condition_matrix, DOWN * text_offset)
            temp_tex[0][0].set_color(RED)     # color dice red and green
            temp_tex[0][2].set_color(GREEN)
            move_elem_to_below_rv = ReplacementTransform(frame, temp_tex, run_time=run_time)
            darker_elem = elem.copy()
            darker_elem.color = DARK_GRAY
            darken_element_transform = ReplacementTransform(elem, darker_elem, run_time=run_time)

            # rule_highlight
            # first highlight the rule then highlight the output
            print(f"Accessing rule {rule} of condition matrix of length {len(condition_matrix)}")
            rule_rect = SurroundingRectangle(condition_matrix[2*rule + 1])
            rule_highlight = Write(rule_rect, run_time=run_time)
            outcome_rect = SurroundingRectangle(condition_matrix[2*rule + 0])
            outcome_highlight = ReplacementTransform(rule_rect, outcome_rect, run_time=run_time)

            # transform the highlighted random variable formula into the desired number
            outcome_text = Tex(r_v).next_to(temp_tex, DOWN * 0)
            outcome_overwrite_elem = ReplacementTransform(outcome_rect, outcome_text, run_time=run_time)
            remove_elem = Unwrite(temp_tex, run_time=run_time)

            # Final state transitions.  Either the outcome number or the frame around the initial number go onto the number line as a rectangle.
            frame_move = ReplacementTransform(outcome_text, rect, run_time=run_time)
            elem_to_rv = ReplacementTransform(frame, rect, run_time=run_time)

            block_pointers[r_v].append(rect)    # The pointer to the rectangle is kept for future use

            return r_v, frame_anim, move_elem_to_below_rv, rule_highlight, outcome_highlight, outcome_overwrite_elem, remove_elem, frame_move, elem_to_rv, darken_element_transform

        fast_anims = [ ]
        
        
        backlog = []  # Elements of the support that we are saving for later to play multiple at a time
        # Play the extended animations for all of the high priority elements of interest
        for elem in S:
            if elem.tex_string in X.elems_of_interest:
                r_v, frame_anim, move_elem_to_below_rv, rule_highlight, outcome_highlight, outcome_overwrite_elem, remove_elem, frame_move, elem_to_rv, darken_element_transform = get_mapping(elem)
                self.play(frame_anim)
                self.wait(wait_time)
                self.play(move_elem_to_below_rv, darken_element_transform)
                self.wait(wait_time)
                self.play(rule_highlight)
                self.wait(wait_time)
                self.play(outcome_highlight)
                self.wait(wait_time)
                self.play(outcome_overwrite_elem, remove_elem)
                self.wait(wait_time)
                self.play(frame_move)
                self.wait(wait_time)
            else:
                backlog.append(elem)
        # Play faster animations that are grouped by outcome number afterwards to show the full distribution
        for elem in backlog:
                r_v, frame_anim, move_elem_to_below_rv, rule_highlight, outcome_highlight, outcome_overwrite_elem, remove_elem, frame_move, elem_to_rv, darken_element_transform = get_mapping(elem)
                fast_anims.append((r_v, frame_anim, elem_to_rv, darken_element_transform))

        # evaluate all remaining r_v outcomes in the fast_anims buffer, sorted for the sake of looking nice since sets aren't ordered
        remaining_support = list(set([r_v for r_v,fa,etr,dark in fast_anims]))
        remaining_support.sort()

        # Play the two stages of each of the remaining elements at the same time
        for x in remaining_support:
            frame_anim = [fa   for rv,fa,etr,dark in fast_anims if rv == x]
            elem_to_RV = [etr  for rv,fa,etr,dark in fast_anims if rv == x]
            darkenElem = [dark for rv,fa,etr,dark in fast_anims if rv == x]

            self.play(*frame_anim)
            self.play(*elem_to_RV, *darkenElem)
        
        self.wait(1)

        # Drop down all of the pmf cells into a pmf table

        # Draw the pmf table
        t1 = MathTable(
            [[str(s) for s in support], [("\\frac{?}{?}") for _ in support]],
            row_labels=[MathTex("x"), MathTex("f_X(x)")],
            include_outer_lines=True).scale(1.4/3.0).move_to(DOWN*2 + RIGHT*3)

        self.play(Write(t1, run_time=run_time))

        # Go over each RV support value,
            # Dropping it into the table
        distribution = t1.get_rows()[1]
        for i in range(len(support)):
            x = support[i]
            blank = distribution[1+i]  # 1 offset for column name
            ctr = blank.get_center()
            print(f"Blank {i} center coordinates: {ctr}")
            fx = MathTex("\\frac{" + str(len(block_pointers[x])) + "}{36}").move_to(ctr).scale(1.3/3)
            animations = [
                # ReplacementTransform(blank, fx)
                Unwrite(blank, run_time=run_time/2)
            ]
            for bp in block_pointers[x]:
                darker_elem = bp.copy()
                darker_elem.color = DARK_BROWN

                animations.append(ReplacementTransform(bp, fx, run_time=run_time))
                animations.append(Write(darker_elem, run_time=run_time))

            self.play(*animations)
            self.wait(1/4)

        self.wait(3)
