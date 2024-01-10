from manim import *

epsilon = 0.01
ep = epsilon

class SupUpperTriangle(ThreeDScene):
    def f(self,x,y):
        return 6*x

    def writeFixed(self, mobj):
        self.add_fixed_in_frame_mobjects(mobj)
        self.play(Write(mobj))

    def replaceFixed(self, old_mobj, new_mobj):
        self.add_fixed_in_frame_mobjects(new_mobj)
        self.play(ReplacementTransform(old_mobj, new_mobj))

    def construct(self):
        x_supp = [0,1]
        y_supp = [0,1]
        z_range = [
            self.f(x_supp[0], y_supp[0]),
            self.f(x_supp[1], y_supp[1])    
        ]
        z_midpoint = (z_range[1] - z_range[0]) / 2

        xy_step = 0.20
        a = xy_step
        axes = ThreeDAxes(
            x_range=[-a, 1+a, a], 
            y_range=[-a, 1+a, a],
            z_range=[0,z_range[1]+1,1],
            x_length=3,
            y_length=3,
            z_length=4
        )

        x_label = Tex('x').scale(0.5)
        y_label = Tex('y').scale(0.5)# .move_to(axes.c2p(0,1.2,0))
        z_label = MathTex('f_{XY}(x,y)').scale(0.5)# .move_to(axes.c2p(0,0,7.0))

        # tracker = ValueTracker(0)
        x_label.add_updater(lambda m: m.move_to(axes.c2p(1+2*a, 0, 0)))
        y_label.add_updater(lambda m: m.move_to(axes.c2p(0, 1+2*a, 0)))
        z_label.add_updater(lambda m: m.move_to(axes.c2p(0,  0,  7.0)))
        labels = VGroup(x_label, y_label, z_label)

        # labels = axes.get_axis_labels(
        #     Tex("x").scale(0.7), 
        #     Tex("y").scale(0.7), 
        #     MathTex("f_{X,Y}(x,y)").scale(0.7)
        # )


        distribution_layer = Surface(
            lambda u, v: axes.coords_to_point(
                u*v,
                v,
                v*self.f(u,v)
            ), v_range=y_supp, u_range=x_supp,
            fill_opacity = 0.5,
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        base_layer = Surface(
            lambda u, v: axes.c2p(
                u*v,
                v,
                0
            ), v_range=y_supp, u_range=x_supp,
            fill_opacity = 0.5,
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        y1_border = Surface(
            lambda u, v: axes.c2p(
                u,
                1,
                v * self.f(u,v)
            ), v_range=y_supp, u_range=x_supp,
            fill_opacity = 0.5,
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        diag_border = Surface(
            lambda u, v: axes.c2p(
                u,
                u,
                v * self.f(u,v)
            ), v_range=y_supp, u_range=x_supp,
            fill_opacity = 0.5,
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )

        geometry = VGroup()
        geometry.add(
            distribution_layer, 
            base_layer, 
            y1_border, 
            diag_border
        )

        # self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        # self.add_fixed_orientation_mobjects(labels)
        self.play(Write(axes), Write(labels))
        
        self.play(Write(base_layer))

        self.move_camera(
            phi   =  75 * DEGREES, 
            theta = -90 * DEGREES, 
            gamma = None,
            frame_center=axes
        )

        self.wait()
        self.play(ReplacementTransform(base_layer, geometry))
        self.wait()

        # self.play(Write(x_min_layer, run_time = 1.35))

        # Do one full rotation around the object
        play_time = 6
        r = 2 * PI / play_time
        self.begin_ambient_camera_rotation(rate=r)
        self.wait(play_time)
        self.stop_ambient_camera_rotation()

        self.move_camera(
            phi   =  90 * DEGREES, 
            theta = (360-90) * DEGREES, 
            gamma = None,
            frame_center=axes
        )

        t = 360

        # Show just the four corners
        self.wait()
        self.move_camera(theta = (t+0) * DEGREES)
        # self.wait()
        # self.move_camera(theta = (t+90) * DEGREES)
        self.wait(2)

        self.move_camera(
            phi   =  30 * DEGREES, 
            theta = (360-90-5) * DEGREES, 
            gamma = None,
            frame_center=axes
        )

        self.wait(2)

        x=0.6   # the value of x at which the support will be cut
        cross_section = Surface(
            lambda u, v: axes.c2p(x, u, v),
            u_range=[y_supp[0]-.5, y_supp[1]+.5],
            v_range=[z_range[0]-1, z_range[1]+2], 
            fill_opacity = 1,
            checkerboard_colors=[YELLOW, YELLOW], resolution=(1, 1)
        )

        self.play(Write(cross_section))
       
        # The upper and lower halves of the support after it is cut at the cross section
        lower_supp = Polyhedron([
            axes.c2p(0,0,0),  # 0 - origin
            axes.c2p(0,1,0),  # 1 - upper left  corner of the left trapezoid
            axes.c2p(x,1,0),  # 2 - upper right corner of the left trapezoid
            axes.c2p(x,x,0),  # 3 - lower right corner of the left trapezoid

            axes.c2p(x,x,self.f(x,x)), # 4 - lower right peak point
            axes.c2p(x,1,self.f(x,1))  # 5 - upper right peak point
        ],[
            [0,1,2,3],  # lower left support area
            [0,3,4],    # front face
            [1,2,5],    # rear face
            [0,1,5,4]   # top
        ], graph_config={"vertex_config":{'radius': 0.0001}})

        upper_supp =  Polyhedron([
            axes.c2p(x,1,0),  # 0 - upper left  corner of the right triangle
            axes.c2p(x,x,0),  # 1 - lower left  corner of the right triangle
            axes.c2p(1,1,0),  # 2 - upper right corner of the right triangle

            axes.c2p(x,x,self.f(x,x)), # 3 - lower left peak point
            axes.c2p(x,1,self.f(x,1)), # 4 - upper left peak point
            axes.c2p(1,1,self.f(1,1))  # 5 - global peak point
        ],[
            [0,1,2],    # upper right support area
            [1,3,5,2],  # front face
            [0,4,5,2],  # rear face
            [3,4,5]     # top
        ], graph_config={"vertex_config":{'radius': 0.0001}})

        # The cross-section is replaced by the support intersect the cross section to get the slice of interest
        slice =  Polyhedron([
            axes.c2p(x,1,0),  # 0 - higher base
            axes.c2p(x,x,0),  # 1 - lower base
            axes.c2p(x,x,self.f(x,x)), # 2 - lower peak point
            axes.c2p(x,1,self.f(x,1)) # 3 - upper peak point
        ],[
            [0,1,2,3]    # the slice
        ], graph_config={"vertex_config":{'radius': 0.0001}}).set_color(YELLOW)

        # Since all of these are by default polygons with non-zero node sizes, 
        # they need to have node thickness be invisible to still look like the support
        graphs = VGroup(lower_supp, slice, upper_supp)
        for graph in graphs:
            graph.set_stroke(width=1)

        # Replace the functionally defined shape with the slices
        self.play(
            Unwrite(cross_section),
            Unwrite(geometry),
            Write(lower_supp),
            Write(upper_supp),
            Write(slice)
        )

        self.wait(1)

        # Move the components of the split shape apart
        slice.generate_target()
        slice.target.shift(RIGHT*1)

        upper_supp.generate_target()
        upper_supp.target.shift(RIGHT*2)

        self.play(MoveToTarget(upper_supp), MoveToTarget(slice))

        self.wait(2)

        # Move everything that has been done so far to the left half of the screen to work on the right half for the next stages
        model_3d = VGroup(axes, labels, graphs)
        model_3d.generate_target()
        model_3d.target.shift(LEFT * 4)
        self.play(MoveToTarget(model_3d))

        self.wait(1)

        old_slice = slice

        slice = Axes([y_supp[0], y_supp[1]+2*a, a], z_range, 
                    axis_config={"include_numbers": True},
                ).shift(RIGHT*4).scale(0.5)
        self.writeFixed(slice)
        # self.add_fixed_in_frame_mobjects(slice)
        # self.play(ReplacementTransform(old_slice, slice))

        x_label = MathTex("y").scale(0.5)
        y_label = MathTex("f_{XY}(x="+str(x)+",y)").scale(0.5).set_color(YELLOW)
        labels_2d = slice.get_axis_labels(x_label, y_label)
        self.writeFixed(labels_2d)

        def fy(y):
            if y<x or y>1:
                return 0
            return self.f(x,y)

        def fygx(y,x):
            return self.f(x,y) / (6*x * (1-x))

        color = YELLOW
        under = slice.plot(lambda t: 0, x_range=[0,x], color=color)
        supported = slice.plot(fy, x_range=[x,1], color=color)
        over = slice.plot(lambda t: 0, x_range=[1,1.5], color=color)
        new_slice = VGroup(under, supported, over)
        # self.add_fixed_in_frame_mobjects(simplified)

        # Draw the three components sequentially
        # self.add_fixed_in_frame_mobjects(new_slice)
        # self.play(TransformFromCopy(old_slice, new_slice))
        self.writeFixed(under)
        self.wait(0.5)
        self.writeFixed(supported)
        self.wait(0.5)
        self.writeFixed(over)

        self.wait(1)

        formular0 = MathTex("x="+str(x)).move_to(LEFT * 4 + UP*3).scale(0.5)
        self.writeFixed(formular0)

        scale = 6 * x * (1-x)

        formular1 = MathTex("f_{X}("+str(x)+") = \int _{y=-\infty}^{y=\infty} f_{XY}(x="+str(x)+", y) dy = \int _{y="+str(x)+"}^{y=1} 6x dy = 6xy|_{"+str(x)+"}^{1}   =  6("+str(x)+") (1-("+str(x)+")) = "+str(scale))
        formular1.scale(0.5).move_to(RIGHT *2 +  UP * 3)
        self.writeFixed(formular1)

        self.wait(3)

        formular2 = MathTex("f_{X}("+str(x)+") ="+str(6 * x * (1-x)))
        formular2.scale(0.5).move_to(LEFT * 2 +  UP * 3)
        self.replaceFixed(formular1, formular2)

        self.wait(3)
 
        formular3 = MathTex("f_{Y|x="+str(x)+"}(y) = \\frac{f_{XY}("+str(x)+",y)}{f_X("+str(x)+")} = \\frac{f_{XY}("+str(x)+",y)}{"+str(scale)+"}")
        formular3.scale(0.5).move_to(RIGHT *3 +  UP * 3)
        self.writeFixed(formular3)

        self.wait(1)

        # y_label = slice.get_y_axis_label()
        y2_label = MathTex("f_{Y|x="+str(x)+"}(y)").scale(0.5).set_color(RED)
        y2_label.next_to(y_label,UP)
        self.writeFixed(y2_label)

        self.wait(1)

        under2 = slice.plot(lambda t: 0, x_range=[0,x], color=RED)
        supported2 = slice.plot(lambda y: fygx(y,x), x_range=[x,1], color=RED)
        over2 = slice.plot(lambda t: 0, x_range=[1,1.5], color=RED)

        self.writeFixed(under2)
        self.wait(0.5)
        self.writeFixed(supported2)
        self.wait(0.5)
        self.writeFixed(over2)

        self.wait(3)
