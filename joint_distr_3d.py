from manim import *

epsilon = 0.01
ep = epsilon

class SupUpperTriangleY(ThreeDScene):
    def f(self,x,y):
        return 6*x

    def writeFixed(self, mobj, pause_time=0):
        self.add_fixed_in_frame_mobjects(mobj)
        self.play(Write(mobj))
        self.wait(pause_time)

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

        y=0.5   # the value of x at which the support will be cut
        cross_section = Surface(
            lambda u, v: axes.c2p(u, y, v),
            u_range=[x_supp[0]-.5, x_supp[1]+.5],
            v_range=[z_range[0]-1, z_range[1]+2], 
            fill_opacity = 1,
            checkerboard_colors=[YELLOW, YELLOW], resolution=(1, 1)
        )

        self.play(Write(cross_section))

        # The upper and lower halves of the support after it is cut at the cross section
        lower_supp = Polyhedron([
            axes.c2p(0,0,0),  # 0 - origin
            axes.c2p(0,y,0),  # 1 - upper left  corner of the bottom triangle
            axes.c2p(y,y,0),  # 2 - upper right corner of the bottom triangle

            axes.c2p(y,y,self.f(y,y))  # 3 - top of the corner
        ],[
            [0,1,2],  # base triangle
            [0,1,3],  # support top
            [0,3,2],  # lower edge of the support
            [1,2,3]   # upper edge of the support
        ], graph_config={"vertex_config":{'radius': 0.0001}})

        upper_supp =  Polyhedron([
            axes.c2p(0,y,0),  # 0 - lower left  corner of the upper trapezoid
            axes.c2p(y,y,0),  # 1 - lower right corner of the upper trapezoid
            axes.c2p(1,1,0),  # 2 - upper right corner of the upper trapezoid
            axes.c2p(0,1,0),  # 3 - upper left  corner of the upper trapezoid

            axes.c2p(y,y,self.f(y,y)), # 4 - lower left peak point
            axes.c2p(1,1,self.f(1,1))  # 5 - global peak point
        ],[
            [0,1,2,3], # base of the support
            [0,1,4],   # bottom face
            [1,2,5,4], # y=x face
            [2,3,5],   # y=1 face
            [0,3,5,4]  # distribution face
        ], graph_config={"vertex_config":{'radius': 0.0001}})

        # The cross-section is replaced by the support intersect the cross section to get the slice of interest
        slice =  Polyhedron([
            axes.c2p(0,y,0),  # 0 - lower  end at x=0
            axes.c2p(y,y,0),  # 1 - higher end at x=y
            axes.c2p(y,y,self.f(y,y)), # 2 - peak point at x=y
        ],[
            [0,1,2]    # the slice
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
        slice.target.shift(UP*1)

        upper_supp.generate_target()
        upper_supp.target.shift(UP*2)

        self.play(MoveToTarget(upper_supp), MoveToTarget(slice))

        self.wait(2)

        # Move everything that has been done so far to the left half of the screen to work on the right half for the next stages
        model_3d = VGroup(axes, labels, graphs)
        model_3d.generate_target()
        model_3d.target.shift(LEFT * 4)
        self.play(MoveToTarget(model_3d))

        self.wait(1)

        old_slice = slice

        marginal_plot = Axes([x_supp[0], x_supp[1]+2*a, a], z_range, 
                    axis_config={"include_numbers": True},
                ).shift(RIGHT*4).scale(0.5)
        self.writeFixed(marginal_plot)
        # self.add_fixed_in_frame_mobjects(slice)
        # self.play(ReplacementTransform(old_slice, slice))

        def fx(x):
            if y<x or y>1:
                return 0
            return self.f(x,y)

        def fxgy(y,x):
            return self.f(x,y) / (3*y*y)

        color = YELLOW
        x_label = MathTex("x").scale(0.5)
        y1_label = MathTex("f_{XY}(x,y="+str(y)+")").scale(0.5).set_color(color)

        labels_2d = marginal_plot.get_axis_labels(x_label, y1_label)
        self.writeFixed(labels_2d)

        und1 = marginal_plot.plot(lambda t:0, x_range=[-0.1,0], color=color)
        sup1 = marginal_plot.plot(fx, x_range=[0,y], color=color)
        auc1 = marginal_plot.get_area(sup1, x_range=[0,y], color=color) # Area under the curve
        ovr1 = marginal_plot.plot(lambda t: 0, x_range=[y,1.5], color=color)
        marginal1 = VGroup(y1_label, und1, auc1, ovr1)
        # self.add_fixed_in_frame_mobjects(simplified)

        # Draw the three components sequentially
        # self.add_fixed_in_frame_mobjects(new_slice)
        # self.play(TransformFromCopy(old_slice, new_slice))
        self.writeFixed(und1, pause_time=0.5)
        self.writeFixed(auc1, pause_time=0.5)
        self.writeFixed(ovr1, pause_time=0.5)
        
        self.wait(0.5)

        # show the constant on the farthest left
        formular0 = MathTex("y="+str(y)).move_to(LEFT * 4 + UP*3).scale(0.5)
        self.writeFixed(formular0)

        scale = 3 * y * y # the integral of the 

        formular1 = MathTex("f_{Y}("+str(y)+") = \int _{x=-\infty}^{x=\infty} f_{XY}(x, y="+str(y)+") dx = \int _{x=0}^{x="+str(y)+"} 6x dx = \\frac{6}{2}x^2|_{0}^{"+str(y)+"}   =  3("+str(y)+"^2) = "+str(scale))
        formular1.scale(0.5).move_to(RIGHT *2 +  UP * 3)
        self.writeFixed(formular1)

        self.wait(3)

        formular2 = MathTex("f_{Y}("+str(y)+") ="+str(scale))
        formular2.scale(0.5).move_to(LEFT * 2 +  UP * 3)
        self.replaceFixed(formular1, formular2)

        self.wait(3)
 
        formular3 = MathTex("f_{X|y="+str(y)+"}(x)"," = \\frac{f_{XY}(x,"+str(y)+")}{f_Y("+str(y)+")}"," = \\frac{f_{XY}(x,"+str(y)+")}{"+str(scale)+"}")
        formular3.scale(0.5).move_to(RIGHT *3 +  UP * 3)
        self.writeFixed(formular3)

        self.wait(1)

        y2_label = MathTex("f_{X|y="+str(y)+"}(x)").scale(0.5).set_color(RED)
        y2_label.next_to(y1_label,UP)
        self.writeFixed(y2_label)

        self.wait(1)

        # Darken the existing plot before making the new one
        graying_actions = []
        for elem in marginal1:
            # Create the object
            darker_elem = elem.copy()
            darker_elem.color = DARK_GRAY

            # Actions to add it to the frame
            self.add_fixed_in_frame_mobjects(darker_elem)
            darken_element_transform = ReplacementTransform(elem, darker_elem)
            graying_actions.append(darken_element_transform)
        self.play(*graying_actions)

        # Draw the normalized marginal distribution for this value of x
        color = RED
        und2 = marginal_plot.plot(lambda t: 0, x_range=[-0.25,0], color=color)
        sup2 = marginal_plot.plot(lambda x: fxgy(y,x), x_range=[0,y], color=color)
        auc2 = marginal_plot.get_area(sup2, x_range=[0,y], color=color)
        ovr2 = marginal_plot.plot(lambda t: 0, x_range=[y,1.5], color=color)

        self.writeFixed(und2, pause_time=0.5)
        self.writeFixed(auc2, pause_time=0.5)
        self.writeFixed(ovr2, pause_time=0.5)
        
        final_area_label = Text("Area = 1",color=color).next_to(sup1,UP).scale(0.5)  # draw above the higher support to avoid overlap collisions to clarity
        self.writeFixed(final_area_label, pause_time=1.0)

        self.wait(3)
