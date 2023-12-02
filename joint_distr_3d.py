from manim import *

epsilon = 0.01
ep = epsilon

class triangle(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-1,1,0.25], 
            y_range=[-1,1,0.25],
            z_range=[0,1,0.2]
        )

        base_layer = Surface(
            lambda u, v: np.array([
                u,
                0,
                u*v
                # (v*u) / (u+v+ep)
            ]), v_range=[0, 1], u_range=[0, 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        self.add(axes, base_layer)
        self.set_camera_orientation(phi=75*DEGREES, theta=-60*DEGREES, gamma=None)

class Sup3d(ThreeDScene):
    def f(self,x,y):
        if x > 2 or x < 0:
            return 0
        if y > 2 or y < 0:
            return 0
        return x + y
    
    def triangle(self,ranging,limit):
        return ranging if ranging < limit else (limit+ep)/(ranging+ep)

    def construct(self):
        axes = ThreeDAxes(
            x_range=[-1,1,0.25], 
            y_range=[-1,1,0.25],
            z_range=[0,1,0.2]
        )
        labels = axes.get_axis_labels(
            Tex("x").scale(0.7), Tex("y").scale(0.45), MathTex("f_{X,Y}(x,y)").scale(0.45)
        )

        distribution_layer = Surface(
            lambda u, v: np.array([
                u,
                v,
                self.f(u,v)
            ]), v_range=[0, 2], u_range=[0, 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        base_layer = Surface(
            lambda u, v: np.array([
                u,
                v,
                0
            ]), v_range=[0, 2], u_range=[0, 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        x0_layer = Surface(
            lambda u, v: np.array([
                u,
                0,
                u*v
            ]), v_range=[0, 1], u_range=[0, 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        
        y0_layer = Surface(
            lambda u, v: np.array([
                0,
                u,
                u*v
            ]), v_range=[0, 1], u_range=[0, 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(1, 1)
        )
        
        x_min_layer = Polyhedron([
            [0,0,0],     # 0 - origin (0,0) lower and upper bound

            [0,2,0],     # 1 - (0,y) lower bound
            [0,2,2-ep],  # 2 - (0,y) upper bound

            [2,0,0],     # 3 - (x,0) lower bound
            [2,0,2-ep],  # 4 - (x,0) upper bound

            [2,2,0],     # 5 - (x,y) lower bound
            [2,2,4-ep],  # 6 - (x,y) upper bound
        ],[
            [0,3,4],   # y=0 surface
            [0,1,2],   # x=0 surface
            [1,2,6,5], # y=y surface
            [3,4,6,5]  # x=x surface
        ], graph_config={"vertex_config":{'radius': 0.0001}})

        # x_min_layer.graph

        geometry = VGroup()
        geometry.add(distribution_layer, base_layer, x0_layer, y0_layer)
        # self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Write(axes), Write(labels))
        
        self.play(Write(base_layer))

        self.move_camera(phi=75*DEGREES, theta=-60*DEGREES, gamma=None)

        self.wait()
        self.play(ReplacementTransform(base_layer, geometry))
        # self.play(Write(x_min_layer, run_time = 1.35))

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(3)




class poly(ThreeDScene):
    def f(self,x,y):
        if x > 2 or x < 0:
            return 0
        if y > 2 or y < 0:
            return 0
        return x + y

    def construct(self):
        axes = ThreeDAxes(
            x_range=[-1,1,0.25], 
            y_range=[-1,1,0.25],
            z_range=[0,1,0.2]
        )
        labels = axes.get_axis_labels(
            Tex("x").scale(0.7), Tex("y").scale(0.45), MathTex("f_{X,Y}(x,y)").scale(0.45)
        )


        vertex_coords = [
            [1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [-1, 1, 0],
            [0, 0, 2]
        ]
        faces_list = [
            [0,1,2]
        ]

        distribution = Polyhedron(vertex_coords, faces_list)

        geometry = VGroup()
        # self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Write(axes), Write(labels))
        
        self.play(Write(distribution))

        self.move_camera(phi=75*DEGREES, theta=-60*DEGREES, gamma=None)

        self.wait()
        # self.play(ReplacementTransform(base_layer, geometry))

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.wait(3)
