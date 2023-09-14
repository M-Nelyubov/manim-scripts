from manim import *
import numpy as np


class LineExample(Scene):
    def construct(self):
        d = VGroup()
        for i in range(0,10):
            d.add(Dot())
        d.arrange_in_grid(buff=1)
        self.add(d)
        l= Line(d[0], d[1])
        self.add(l)
        self.wait()
        l.put_start_and_end_on(d[1].get_center(), d[2].get_center())
        self.wait()
        l.put_start_and_end_on(d[4].get_center(), d[7].get_center())
        self.wait()

class JointCDFExample(Scene):
    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-1, 4),
            # y-axis ranges from -2 to 2 with a step size of 0.5
            y_range=(-1, 2, 0.5),
            # The axes will be stretched so as to match the specified
            # height and width
            height=6,
            width=10,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config=dict(
                stroke_color=GREY_A,
                stroke_width=2,
                numbers_to_exclude=[0],
            ),
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            y_axis_config=dict(
                numbers_with_elongated_ticks=[-2, 2],
            )
        )
        # Keyword arguments of add_coordinate_labels can be used to
        # configure the DecimalNumber mobjects which it creates and
        # adds to the axes
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
        self.add(axes)

        shadow_axes = axes.copy()
        shadow_axes.move_to(axes.c2p(-1, -1))
        self.add(shadow_axes)


        # Axes descends from the CoordinateSystem class, meaning
        # you can call call axes.coords_to_point, abbreviated to
        # axes.c2p, to associate a set of coordinates with a point,
        # like so:
        dot = Dot(color=RED)
        dot.move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))

        shadow_dot = Dot()
        shadow_dot.move_to(axes.c2p(-10, 0))
        self.add(shadow_dot)

        # dashed_line = DashedLine(start=axes.c2p(-5, 0.5), end=axes.c2p(1, 0.5))
        # self.add(dashed_line)
        # self.wait()

        def moveDot(x,y):
            dot.move_to(axes.c2p(x, y))
            shadow_dot.move_to(axes.c2p(-10, y))
            
            ctr = dot.get_center()
            ctr_l = shadow_dot.get_center()

            line2 = Line(ctr,ctr_l)
            # line2.put_start_and_end_on(ctr, ctr_l)

        moveDot(2,2)        

        # Draw a rectangle for support bounds
        rectangle = Rectangle()
        rectangle.move_to(axes.c2p(1, 0.5))   # Coordinates based on center of object
        rectangle.set_width(4)
        rectangle.set_height(2)
        rectangle.set_fill(BLUE, opacity=0.2)
        rectangle.set_stroke(BLUE_E, width=4)
        self.play(ShowCreation(rectangle))
        self.wait()



        # Similarly, you can call axes.point_to_coords, or axes.p2c
        # print(axes.p2c(dot.get_center()))
        print(dot.get_bottom())
        h_line = always_redraw(lambda: shadow_axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: shadow_axes.get_v_line(dot.get_bottom()))

        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
        )


        self.play(dot.animate.move_to(axes.c2p(-1, -0.5)))
        print(dot.get_bottom())
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        print(dot.get_bottom())
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(4, 0.5)))
        print(dot.get_bottom())
        self.wait()


        # We can draw lines from the axes to better mark the coordinates
        # of a given point.
        # Here, the always_redraw command means that on each new frame
        # the lines will be redrawn
        self.play(dot.animate.move_to(axes.c2p(3, -0.5)))
        print(dot.get_bottom())
        self.wait()

        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        print(dot.get_bottom())
        self.wait()

        self.play(dot.animate.move_to(axes.c2p(0, 0)))
        print(dot.get_bottom())
        self.wait()

        # If we tie the dot to a particular set of coordinates, notice
        # that as we move the axes around it respects the coordinate
        # system defined by them.
        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        # self.play(
        #     axes.animate.scale(0.75).to_corner(UL),
        #     run_time=2,
        # )
        self.wait()
        # self.play(FadeOut(VGroup(axes, dot, h_line, v_line)))

        # Other coordinate systems you can play around with include
        # ThreeDAxes, NumberPlane, and ComplexPlane.

class GraphNormalExample(Scene):
    def construct(self):
        axes = Axes((-10, 10, 2), (-.1, 0.4, 0.1), height=6, width=10)
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )

        self.play(Write(axes, lag_ratio=0.01, run_time=1))


        mu = 4
        sigma = 2
        # Axes.get_graph will return the graph of a function
        n_mu_sig = axes.get_graph(
            lambda x: 1/(sigma * (2*np.pi)**0.5) * np.e ** (-0.5 * ((x-mu)/sigma)**2),
            color=BLUE,
        )

        n_0_sig = axes.get_graph(
            lambda x: 1/(sigma * (2*np.pi)**0.5) * np.e ** (-0.5 * ((x)/sigma)**2),
            color=BLUE,
        )

        n_0_1 = axes.get_graph(
            lambda x: 1/((2*np.pi)**0.5) * np.e ** (-0.5 * (x)**2),
            color=BLUE,
        )

        # Axes.get_graph_label takes in either a string or a mobject.
        # If it's a string, it treats it as a LaTeX expression.  By default
        # it places the label next to the graph near the right side, and
        # has it match the color of the graph
        nms_label = axes.get_graph_label(n_mu_sig, Tex(Rf"X\sim N(\mu={mu}, \sigma={sigma})"))
        nms_label2 = axes.get_graph_label(n_mu_sig, Tex(Rf"X\sim N(\mu={mu}-\mu, \sigma={sigma})"))
        n0s_label = axes.get_graph_label(n_mu_sig, Tex(Rf"X\sim N(\mu={0}, \sigma={sigma})"))
        n0s_label2 = axes.get_graph_label(n_mu_sig, Tex(Rf"X\sim N(\mu={0}, \sigma={sigma}/\sigma)"))
        n01_label = axes.get_graph_label(n_mu_sig, Tex(Rf"X\sim N(\mu={0}, \sigma={1})"))

        self.play(
            ShowCreation(n_mu_sig),
            FadeIn(nms_label, RIGHT),
        )

        self.wait(1)

        self.play(FlashAround(nms_label[f"{mu}"]))
        # self.play(ReplacementTransform(nms_label, nms_label2))
        # self.play(nms_label2[R"-\mu"].animate.set_color(RED))  # Doesn't hit the infinity

        self.wait(0.25)

        self.play(
            ReplacementTransform(n_mu_sig, n_0_sig),
            FadeTransform(nms_label, n0s_label),
        )

        self.wait(2)
        self.play(FlashAround(nms_label[f"{sigma}"]))
        self.wait(0.25)

        self.play(
            ReplacementTransform(n_0_sig, n_0_1),
            FadeTransform(n0s_label, n01_label),
        )

        self.wait(2)

        # parabola = axes.get_graph(lambda x: 0.25 * x**2)
        # parabola.set_stroke(BLUE)
        # self.play(
        #     FadeOut(nms_label),
        #     FadeOut(n_mu_sig),
        #     ShowCreation(parabola)
        # )
        # self.wait()

        # # You can use axes.input_to_graph_point, abbreviated
        # # to axes.i2gp, to find a particular point on a graph
        # dot = Dot(color=RED)
        # dot.move_to(axes.i2gp(2, parabola))
        # self.play(FadeIn(dot, scale=0.5))

        # # A value tracker lets us animate a parameter, usually
        # # with the intent of having other mobjects update based
        # # on the parameter
        # x_tracker = ValueTracker(2)
        # f_always(
        #     dot.move_to,
        #     lambda: axes.i2gp(x_tracker.get_value(), parabola)
        # )

        # self.play(x_tracker.animate.set_value(4), run_time=3)
        # self.play(x_tracker.animate.set_value(-2), run_time=3)
        # self.wait()

class TDistributions(Scene):
    def construct(self):
        refresh_decay_power = 0.75
        axes = Axes((-5, 5, 1), (-.1, 0.4, 0.1), height=6, width=10)
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        from scipy.stats import t, norm

        z_pdf = axes.get_graph(
            lambda x: norm.pdf(x),
            color=YELLOW,
        )

        # The documentation says that this should be x_val = 1, but manimlib\mobject\coordinate_systems.py has get_graph_label defined with x not x_val
        z_label = axes.get_graph_label(z_pdf, Tex(R"Z"), x=0.5)

        new_pdf = axes.get_graph(
            lambda x: t.pdf(x, 1),   # distribution over R.V. x with 1 degree of freedom
            color=BLUE,
        )

        new_label = axes.get_graph_label(new_pdf, Tex(R"t_{\nu=1}"))

        self.play(
            ShowCreation(z_pdf)
        )
        self.play(
            FadeIn(z_label, DOWN)
        )

        self.wait()

        self.play(
            ShowCreation(new_pdf),
            FadeIn(new_label, RIGHT),
        )

        for df in range(2, 101):
            prior_pdf = new_pdf
            prior_label = new_label

            new_pdf = axes.get_graph(
                lambda x: t.pdf(x, df),   # distribution over R.V. x with 1 degree of freedom
                color=BLUE,
            )
            new_label = axes.get_graph_label(new_pdf, Tex(R"t_{\nu="+ str(df) +R"}"))

            self.play(
                ReplacementTransform(prior_pdf, new_pdf),
                ReplacementTransform(prior_label, new_label),
                run_time = 1/(df**refresh_decay_power)
            )

            self.wait(1/(df**refresh_decay_power))
        
        self.wait(2)

        self.play(
            FadeOut(new_pdf),
            FadeOut(new_label)
        )
        
        self.wait()

        self.play(
            FadeOut(axes),
            FadeOut(z_pdf),
            FadeOut(z_label)
        )

        self.wait()

class ChiSquares(Scene):
    def construct(self):
        refresh_decay_power = 0.05
        axes = Axes(
            (0, 30, 2), 
            (0, 0.4, 0.1), 
            tips=False,
            axis_config={"include_numbers": True},
            # height=6, 
            # width=10
        )
        # axes.add_coordinate_labels(
        #     font_size=20,
        #     num_decimal_places=1,
        # )

        x_min, x_max, x_step = axes.x_range

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        from scipy.stats import chi2

        first_nu = 2
        last_nu = 30

        new_pdf = axes.plot(
            lambda x: chi2.pdf(x, first_nu),   # distribution over R.V. x with 1 degree of freedom
            color=BLUE,
        )

        new_label = axes.get_graph_label(new_pdf, (R"\chi^2_{" + str(first_nu) + "}"), buff = 1)

        all_squares = [new_pdf]   # keep a list of all created squares to destroy them at the end

        self.wait()

        self.play(
            Write(new_pdf),
            Write(new_label)
        )
        self.wait()
            

        def colorGenerator(min, max, x):
            r = 250 * (x%4)//4
            g = 255 * (min + x - 1)//max
            b = 255 * (max - x - 1)//max
            color = "#{:02x}{:02x}{:02x}".format(r,g,b)
            print("[{}<={}<={}]".format(min, x, max), "({},{},{})".format(r, g, b), " -> ", color)
            return color


        for df in [4, 6, 8, 10, 15, 20]: #, 25, 30]:
            self.wait(1/(df**refresh_decay_power))
            prior_pdf = new_pdf
            prior_label = new_label
            # prior_area  = new_area

            new_pdf = axes.plot(
                lambda x: chi2.pdf(x, df),   # distribution over R.V. x with 1 degree of freedom
                color=colorGenerator(first_nu, last_nu + 1, df),
            )
            all_squares.append(new_pdf)
            new_label = axes.get_graph_label(new_pdf, (R"\chi^2_{"+ str(df) +R"}"), buff = 1)

            # new_area = axes.get_area(new_pdf, x_range=np.clip(chi2.interval(.95, df), x_min, x_max))

            self.play(
                Write(new_pdf),
                ReplacementTransform(prior_label, new_label),
                run_time = 1/(df**refresh_decay_power)
            )

        
        self.wait(2)

        for square in all_squares:
            self.play(FadeOut(square), run_time = 0.25/len(all_squares))

        self.play(FadeOut(new_label), run_time = 0.25/len(all_squares))

        self.play(FadeOut(axes))
        
        self.wait()

class TRevisited(Scene):
    def construct(self):
        refresh_decay_power = 0.75
        axes = Axes(
            (-5, 5, 1), 
            (-.1, 0.4, 0.1), 
            tips=False,
            axis_config={"include_numbers": True},
            # height=6, 
            # width=10
        )
        # axes.add_coordinate_labels(
        #     font_size=20,
        #     num_decimal_places=1,
        # )

        x_min, x_max, x_step = axes.x_range

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        from scipy.stats import t, norm


        z_pdf = axes.plot(
            lambda x: norm.pdf(x),
            color=YELLOW,
        )

        z_label = axes.get_graph_label(z_pdf, Tex(R"Z"), x_val=0.5)

        self.play(Write(z_pdf), Write(z_label))

        first_nu = 1
        last_nu = 100

        new_pdf = axes.plot(
            lambda x: t.pdf(x, first_nu),   # distribution over R.V. x with 1 degree of freedom
            color=BLUE,
        )

        new_label = axes.get_graph_label(new_pdf, (R"t_{" + str(first_nu) + "}"), x_val=3.0, direction=UR)

        new_area = axes.get_area(new_pdf, x_range=t.interval(.95, first_nu))

        self.wait()

        self.play(
            Write(new_pdf),
            Write(new_label),
            Write(new_area)
        )
            
        # self.add()
        self.wait()


        for df in range(first_nu + 1, last_nu + 1):
            self.wait(1/(df**refresh_decay_power))
            prior_pdf = new_pdf
            prior_label = new_label
            prior_area  = new_area

            new_pdf = axes.plot(
                lambda x: t.pdf(x, df),   # distribution over R.V. x with 1 degree of freedom
                color=BLUE,
            )
            new_label = axes.get_graph_label(new_pdf, (R"t_{"+ str(df) +R"}"), x_val=3.0, direction=UR)

            new_area = axes.get_area(new_pdf, x_range=np.clip(t.interval(.95, df), x_min, x_max))

            self.play(
                ReplacementTransform(prior_pdf, new_pdf),
                ReplacementTransform(prior_label, new_label),
                ReplacementTransform(prior_area, new_area),
                run_time = 1/(df**refresh_decay_power)
            )

        
        self.wait(2)
        self.play(
            FadeOut(new_pdf),
            FadeOut(new_area),
            FadeOut(new_label)
        )

        self.play(
            FadeOut(axes),
            FadeOut(z_pdf),
            FadeOut(z_label)
        )
        
        self.wait()

class CollapseZ2(ThreeDScene):
    def construct(self):
        matrix_write_time = 0.3   # Seconds to draw a matrix

        matrix1_data = [
            [.01, .02, .03, .04],
            [.02, .03, .04, .05],
            [.01, .01, .02, .02],
            [.03, .02, .01, .01]
        ]
        
        matrix2_data = [
            [.03, .05, .04, .01],
            [.02, .04, .06, .08],
            [.03, .07, .02, .08],
            [.01, .02, .03, .04]
        ]

        # Calculate sum of matrixes
        def getSum(matrix1_data, matrix2_data):
            matrix_sum = []
            for i in range(len(matrix1_data)):
                matrix_sum.append([])
                for j in range(len(matrix1_data[i])):
                    matrix_sum[i].append(matrix1_data[i][j] + matrix2_data[i][j])
            return matrix_sum

        matrix_sum = getSum(matrix1_data, matrix2_data)

        matrix1 = Matrix(matrix1_data).move_to([-3,0,0])
        matrix2 = Matrix(matrix2_data).move_to([ 3,0,0])
        matrixS = Matrix(matrix_sum).move_to([0, 0, 0])
        

        self.play(
            Write(matrix1),
            Write(matrix2)
        )
        self.wait()

        self.move_camera(phi=70 * DEGREES)

        self.play(
            matrix1.animate.move_to([0,0, 1.5]),
            matrix2.animate.move_to([0,0, -1.5])
        )
        self.wait()

        addition_matrix = Tex("+").move_to([0, 0, 0])
        
        self.play(
            Write(addition_matrix, run_time = matrix_write_time)
        )
        self.wait(2)

        self.play(
            Uncreate(addition_matrix),
            ReplacementTransform(matrix1, matrixS),
            ReplacementTransform(matrix2, matrixS)
        )
        self.wait(1)

        self.move_camera(phi   = 0 * DEGREES)
        self.wait(3)

class CollapseZ3(ThreeDScene):
    def construct(self):
        matrix_write_time = 0.3   # Seconds to draw a matrix

        matrix1_data = [
            [.001, .002, .003],
            [.006, .005, .004],
            [.007, .008, .009]
        ]
        
        matrix2_data = [
            [.07, .06, .01],
            [.08, .05, .02],
            [.09, .04, .03]
        ]

        matrix3_data = [
            [.03, .01,  .05],
            [.02, .145, .04],
            [.07, .06,  .08]
        ]

        # Calculate sum of matrixes
        def getSum(matrix1_data, matrix2_data):
            matrix_sum = []
            for i in range(len(matrix1_data)):
                matrix_sum.append([])
                for j in range(len(matrix1_data[i])):
                    matrix_sum[i].append(round(matrix1_data[i][j] + matrix2_data[i][j], 5))   # rounded to 5 decimal places to mitigate floating point errors
            return matrix_sum

        partial_matrix_sum = getSum(matrix1_data, matrix2_data)
        matrix_sum = getSum(partial_matrix_sum, matrix3_data)

        matrix1 = Matrix(matrix1_data).scale(0.9).move_to([4.2, 0, 0])#2])
        matrix2 = Matrix(matrix2_data).scale(0.9).move_to([0, 0, 0])
        matrix3 = Matrix(matrix3_data).scale(0.9).move_to([-4.2, 0, 0]) # -2])

        matrixS = Matrix(matrix_sum).move_to([0, 0, 0])
        

        # must add the matrix
        self.add(matrix1)

        self.play(
            Write(matrix2, run_time = matrix_write_time),
            Write(matrix3, run_time = matrix_write_time)
        )
        self.wait()

        self.move_camera(phi   = 70 * DEGREES)
        self.wait()

        self.play(
            matrix1.animate.move_to([0,0, 2]),
            matrix3.animate.move_to([0,0,-2])
        )
        self.wait()

        addition_matrix1 = Tex("+").move_to([0, 0,  1])
        addition_matrix2 = Tex("+").move_to([0, 0, -1])

        self.play(
            Write(addition_matrix1, run_time = matrix_write_time),
            Write(addition_matrix2, run_time = matrix_write_time)
        )
        
        self.wait(2)

        self.play(
            FadeOut(addition_matrix1),
            FadeOut(addition_matrix2),
            ReplacementTransform(matrix1, matrixS),
            ReplacementTransform(matrix2, matrixS),
            ReplacementTransform(matrix3, matrixS)
        )

        self.wait(1)

        self.move_camera(
            phi   = 0 * DEGREES, 
            # gamma = 10 * DEGREES,
        )

        self.wait(3)

# The scene Roll2d6 has been moved to a separate file (Roll2d6.py)

class Combinations(Scene):
    def construct(self):
        slots = VGroup()
        chips = VGroup()

        contents = [
            {
                "letter": "r",
                "color": RED,
                "count": 3
            },
            {
                "letter": "b",
                "color": BLUE,
                "count": 2
            },
            {
                "letter": "g",
                "color": GREEN,
                "count": 1
            }
        ]   

        for chip_type in contents:
            for i in range(chip_type['count']):
                slots.add(Text("_").scale(1.2))
                chips.add(MathTex(f"{chip_type['letter']}_{i}", color=chip_type['color']))

        slots.arrange_in_grid(rows=1)  

        for chip,slot in zip(chips,slots):
            chip.next_to(slot, direction=UP*0.5)

        self.add(slots)
        self.play(
            Write(chips)
        )
        self.wait(3)
