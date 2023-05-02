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


# class BinomialApproximation500(Scene):
#     def construct(self):
#         refresh_decay_power = 0.75
#         axes = Axes(
#             (0, 5, 1), 
#             (0, 1, 0.2),
#             tips=False,
#             axis_config={"include_numbers": True},
#             # height=6, 
#             # width=10
#         )
#         # axes.add_coordinate_labels(
#         #     font_size=20,
#         #     num_decimal_places=1,
#         # )

#         x_min, x_max, x_step = axes.x_range

#         self.play(Write(axes, lag_ratio=0.01, run_time=1))

#         from scipy.stats import binom, norm


#         # z_pdf = axes.plot(
#         #     lambda x: norm.pdf(x),
#         #     color=YELLOW,
#         # )

#         # z_label = axes.get_graph_label(z_pdf, Tex(R"Z"), x_val=0.5)

#         # self.play(Write(z_pdf), Write(z_label))

#         first_n = 1
#         last_n = 100

#         new_pmf = 

#         new_pdf = axes.plot(
#             lambda x: binom.pmf(x, first_nu),   # distribution over R.V. x with 1 degree of freedom
#             color=BLUE,
#         )

#         new_label = axes.get_graph_label(new_pdf, (R"t_{" + str(first_nu) + "}"), x_val=3.0, direction=UR)

#         new_area = axes.get_area(new_pdf, x_range=t.interval(.95, first_nu))

#         self.wait()

#         self.play(
#             Write(new_pdf),
#             Write(new_label),
#             Write(new_area)
#         )
            
#         # self.add()
#         self.wait()


#         for df in range(first_nu + 1, last_nu + 1):
#             self.wait(1/(df**refresh_decay_power))
#             prior_pdf = new_pdf
#             prior_label = new_label
#             prior_area  = new_area

#             new_pdf = axes.plot(
#                 lambda x: t.pdf(x, df),   # distribution over R.V. x with 1 degree of freedom
#                 color=BLUE,
#             )
#             new_label = axes.get_graph_label(new_pdf, (R"t_{"+ str(df) +R"}"), x_val=3.0, direction=UR)

#             new_area = axes.get_area(new_pdf, x_range=np.clip(t.interval(.95, df), x_min, x_max))

#             self.play(
#                 ReplacementTransform(prior_pdf, new_pdf),
#                 ReplacementTransform(prior_label, new_label),
#                 ReplacementTransform(prior_area, new_area),
#                 run_time = 1/(df**refresh_decay_power)
#             )

        
#         self.wait(2)
#         self.play(
#             FadeOut(new_pdf),
#             FadeOut(new_area),
#             FadeOut(new_label)
#         )

#         self.play(
#             FadeOut(axes),
#             FadeOut(z_pdf),
#             FadeOut(z_label)
#         )
        
#         self.wait()

class BarChartExample(Scene):
    def construct(self):
        p = 0.5
        from scipy.stats import binom, norm

        def generateChart(n, p):
            values = [binom.pmf(k, n, p) for k in np.arange(n+1)]
            max_val = round(np.asarray(values).max(), 3)
            new_chart = BarChart(
                bar_names=np.arange(n+1),
                values=values,
                y_range=[0, max_val, round(max_val / 5, 4)],
                y_length=6,
                x_length=10,
                x_axis_config={"font_size": 36},
            )
            return new_chart, max_val

        def genX(n,max_val):
            return Axes(
                (0, n, 1), 
                (0, max_val, 0.2),
                tips=False,
                axis_config={"include_numbers": True},
                # height=6, 
                x_length=10 * (n-1) / n
            )

        def genZ(axes, mu, sigma):
            return axes.plot(
                lambda x: norm.pdf(x, loc=mu, scale=sigma),
                color=YELLOW,
            )

        new_chart, max_val = generateChart(1, p)
        axes = genX(1, max_val)
        z_pdf = genZ(axes, 1*p, (p*(1-p))**0.5)
        self.play(Write(new_chart))
        self.add(axes, z_pdf)

        for n in range(2, 21):
            old_chart = new_chart
            old_axes  = axes
            old_pdf   = z_pdf

            new_chart, max_val = generateChart(n, p)
            axes = genX(n, max_val)
            z_pdf = genZ(axes, mu=n*p, sigma=(n*p*(1-p))**0.5)


            self.play(
                ReplacementTransform(old_chart, new_chart),
                ReplacementTransform(old_pdf, z_pdf),
                ReplacementTransform(old_axes, axes)
            )
            self.wait(1/n)
        
