from manim import *

epsilon = 0.01
ep = epsilon

class SupUpperTriangle(ThreeDScene):
    def f(self,x,y):
        return 6*x

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
        self.wait(3)

        self.move_camera(
            phi   =  30 * DEGREES, 
            theta = (360-90-5) * DEGREES, 
            gamma = None,
            frame_center=axes
        )

        self.wait(3)

        x=0.8
        cross_section = Surface(
            lambda u, v: axes.c2p(x, u, v),
            u_range=[y_supp[0]-.5, y_supp[1]+.5],
            v_range=[z_range[0]-1, z_range[1]+2], 
            fill_opacity = 1,
            checkerboard_colors=[YELLOW, YELLOW], resolution=(1, 1)
        )

        self.play(Write(cross_section))

        self.wait(1)

        model_3d = VGroup(cross_section, axes, labels, geometry)

        model_3d.generate_target()
        model_3d.target.shift(LEFT * 4)
        self.play(MoveToTarget(model_3d))

        self.wait(1)

        slice = Axes([y_supp[0], y_supp[1]+2*a, a], z_range).shift(RIGHT*4).scale(0.5)
        self.add_fixed_in_frame_mobjects(slice)
        self.play(Write(slice))

        labels_2d = slice.get_axis_labels(
            MathTex("y").scale(0.5), 
            MathTex("f_{XY}(x="+str(x)+",y)").scale(0.5)
        )
        self.add_fixed_in_frame_mobjects(labels_2d)
        self.play(Write(labels_2d))

        def fy(y):
            if y<x or y>1:
                return 0
            return self.f(x,y)
        
        simplified = slice.plot(fy)
        self.add_fixed_in_frame_mobjects(simplified)
        self.play(Write(simplified))

        self.wait(5)
