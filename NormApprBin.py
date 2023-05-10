from manim import *
import numpy as np

class IncreasingN50(Scene):
    def initialize_p_value(self):
        self.p = 0.5
        self.upTo = 25
        self.play_rate = 0.3

    def construct(self):
        self.initialize_p_value()
        from scipy.stats import binom, norm

        z_drawn = False

        def generateChart(n, p):
            values = [binom.pmf(k, n, p) for k in np.arange(n+1)]
            max_val = round(np.asarray(values).max(), 3)
            new_chart = BarChart(
                bar_names=np.arange(n+1) if n<15 else None,     # Cut off labeling X values after a certain point once there's too many
                values=values,
                y_range=[0, max_val, round(max_val / 5, 4)],
                y_length=5.5,
                x_length=10,
                x_axis_config={"font_size": 36},
                bar_width=1
            )
            return new_chart, max_val

        def genX(n,max_val):
            return Axes(
                (0, n, 1), 
                (0, max_val, 0.2),
                tips=False,
                axis_config={"include_numbers": True},
                y_length=5.5, 
                x_length=10 * (n-1) / n
            )

        def genZ(axes, mu, sigma):
            return axes.plot(
                lambda x: norm.pdf(x, loc=mu, scale=sigma),
                color=YELLOW,
            )

        title = Title(
            # spaces between braces to prevent SyntaxError
            r"Binomial distribution with $p={" + str(self.p) + "}, n=" + str(1) + "$",
            include_underline=False,
            font_size=40,
        )


        new_chart, max_val = generateChart(1, self.p)
        axes = genX(1, max_val)
        z_pdf = genZ(axes, 1*self.p, (self.p*(1-self.p))**0.5)
        self.play(Write(new_chart), Write(title))
        # self.add(title)

        for n in range(2, self.upTo):
            old_chart = new_chart
            old_axes  = axes
            old_pdf   = z_pdf
            old_title = title

            new_chart, max_val = generateChart(n, self.p)
            axes = genX(n, max_val)
            z_pdf = genZ(axes, mu=n*self.p, sigma=(n*self.p*(1-self.p))**0.5)

            title = Title(
                # spaces between braces to prevent SyntaxError
                r"Binomial distribution with $p={" + str(self.p) + "}, n=" + str(n) + "$",
                include_underline=False,
                font_size=24,
            )

            if z_drawn:
                self.play(
                    ReplacementTransform(old_chart, new_chart, run_time=self.play_rate),
                    ReplacementTransform(old_title, title, run_time=self.play_rate),
                    ReplacementTransform(old_pdf, z_pdf, run_time=self.play_rate),
                )
            else:
                self.play(
                    ReplacementTransform(old_chart, new_chart, run_time=self.play_rate),
                    ReplacementTransform(old_title, title, run_time=self.play_rate),
                )
                # Start drawing the Z approximation once it is considered sufficiently accurate
                if n*self.p >= 5 and n*(1-self.p) >= 5:
                    z_drawn = True
                    self.play(
                        Write(z_pdf, run_time=1.5),
                    )

            self.wait(1/n**0.5)
        
class IncreasingN05(IncreasingN50):
    def initialize_p_value(self):
        self.p = 0.05
        self.upTo = 105
        self.play_rate = 0.3

class IncreasingN25(IncreasingN50):
    def initialize_p_value(self):
        self.p = 0.25
        self.upTo = 35
        self.play_rate = 0.3

class IncreasingN75(IncreasingN50):
    def initialize_p_value(self):
        self.p = 0.75
        self.upTo = 35
        self.play_rate = 0.3

class IncreasingN95(IncreasingN50):
    def initialize_p_value(self):
        self.p = 0.95
        self.upTo = 105
        self.play_rate = 0.3

class HalfUnitCorrection(Scene):
    def initialize_p_value(self):
        self.p = 0.5
        self.n = 100
        self.play_rate = 0

    def construct(self):
        self.initialize_p_value()
        from scipy.stats import binom, norm

        z_drawn = False

        def generateChart(n, p, min=None, max=None):
            if max == None:
                max = n
            if min == None:
                min = 0

            values = [binom.pmf(k, n, p) for k in np.arange(min, max+1)]
            max_val = round(np.asarray(values).max(), 3)
            new_chart = BarChart(
                bar_names=np.arange(min, max+1) if len(values)<=25 else None,     # Cut off labeling X values after a certain point once there's too many
                values=values,
                y_range=[0, max_val, round(max_val / 5, 4)],
                y_length=5.5,
                x_length=10,
                x_axis_config={"font_size": 24},
                bar_width=1
            )
            return new_chart, max_val

        def genX(n, min_x, max_x, max_val):
            return Axes(
                (min_x - 0.5, max_x + 0.5, 1),
                (0, max_val, 0.2),
                tips=False,
                axis_config={"include_numbers": True},
                y_length=5.5, 
                x_length=10 * (n-1) / n
            )

        def genZ(axes, mu, sigma):
            return axes.plot(
                lambda x: norm.pdf(x, loc=mu, scale=sigma),
                color=YELLOW,
            )

        title = Title(
            # spaces between braces to prevent SyntaxError
            r"Binomial distribution with $p={" + str(self.p) + "}, n=" + str(self.n) + "$",
            include_underline=False,
            font_size=40,
        )



        min_x = 40
        max_x = 60
        new_chart, max_val = generateChart(self.n, self.p, min_x, max_x)
        axes = genX(self.n, min_x, max_x, max_val)

        r_s = 45 # Real start
        r_e = 55 # Real end
        a_s = 45 # Approximation start
        a_e = 55 # Approximation end

        mean = self.n*self.p
        variance = self.n * self.p * (1-self.p)
        std = variance**0.5

        z_pdf = genZ(axes, mean, std)
        z_area = axes.get_area(z_pdf, x_range=(r_s, r_e), color=YELLOW, opacity = 0.7)

        # value_text = Tex("X ~ Bin(100, 0.5) \n Y ~ N($\\mu, \\sigma$)").to_edge(RIGHT)
        value_text = Tex("$$\int_{" + str(a_s) + "}^{" + str(a_e) + "}f_Y(x)\,dx = " + str(round(norm.cdf(a_e, mean, std) - norm.cdf(a_s, mean, std), 4)) + "$$\n" + 
                        "$$F_{B}(" + str(a_e) + ") - F_{B}(" + str(a_s - 1) + ") = " + str(round(binom.cdf(a_e, self.n, self.p) - binom.cdf(a_s-1, self.n, self.p), 4) ) + " $$", font_size = 36).to_edge(RIGHT).shift([0,2,0])  # To the right and then up one

        self.play(
            Write(new_chart), 
            Write(title), 
            Write(z_pdf)
        )

        self.wait()

        self.play(
            Write(z_area),
            Write(value_text)
        )

        self.wait(5)

        # Now make the half-unit correction

        new_value_text = Tex("$$\int_{" + str(a_s-0.5) + "}^{" + str(a_e+0.5) + "}f_Y(x)\,dx = " + str(round(norm.cdf(a_e+0.5, mean, std) - norm.cdf(a_s-0.5, mean, std), 4)) + "$$\n" + 
                             "$$F_{B}(" + str(a_e) + ") - F_{B}(" + str(a_s - 1) + ") = " + str(round(binom.cdf(a_e, self.n, self.p) - binom.cdf(a_s-1, self.n, self.p), 4) ) + " $$", font_size = 36).to_edge(RIGHT).shift([0,2,0])  # To the right and then up one
        new_z_area = axes.get_area(z_pdf, x_range=(r_s-0.5, r_e+0.5), color=YELLOW, opacity = 0.7)

        self.play(
            ReplacementTransform(z_area, new_z_area)
        )
        self.play(
            ReplacementTransform(value_text, new_value_text, run_time=0.2)
        )

        self.wait(5)

