#!/usr/bin/env nemesis

# Import the math module for trigonometric functions
from ftplib import parse229
import math

# Import Gmsh Python interface
import gmsh

# Import the gmsh_utils Python module supplied with PyLith.
from pylith.meshio.gmsh_utils import (VertexGroup, MaterialGroup, GenerateMesh)

class App(GenerateMesh):
    """
    Domain is 60 km by 80km.

    -40.0 km <= x <= 40.0 km
    -100.0 km <= y <= 0.0 km I might need to change this one

    We create a reverse fault and a splay fault.
    """
    # Define some constants that determine the geometry of the domain.
    DOMAIN_X = 80.0e+3
    DOMAIN_Y = 60.0e+3
    DX = 1.0e+3
    #FAULT_WIDTH = 10.0e+3
    #FAULT_DIP = 85.0
    #SPLAY_DIP = 45.0
    #SPLAY_OFFSET = 15.0e+3

    def __init__(self):
        """Constructor.
        """
        # Set the cell choices available through command line options
        # with the default cell type `tri` matching the PyLith parameter files.
        self.cell_choices = {
            "default": "tri",
            "choices": ["tri"],
            }
        self.filename = "mesh_tri.msh"

    def create_geometry(self):
        """Create geometry.

        This method is abstract in the base class and must be implemented
        in our local App class.
        """
        # Set local variables for domain size and corner of the domain.
        lx = self.DOMAIN_X
        ly = self.DOMAIN_Y
        x1 = -0.5 * lx
        y1 = -ly

        # Create points for domain perimeter.
        p1 = gmsh.model.geo.add_point(x1, y1, 0.0)
        p2 = gmsh.model.geo.add_point(x1+lx, y1, 0.0)
        p3 = gmsh.model.geo.add_point(x1+lx, y1+ly, 0.0)
        p4 = gmsh.model.geo.add_point(x1, y1+ly, 0.0)

        p5 = gmsh.model.geo.add_point(x1+lx, y1+20.0e+3, 0.0)
        p6 = gmsh.model.geo.add_point(0, y1+20.0e+3, 0.0)
        p7 = gmsh.model.geo.add_point(x1, y1+20.0e+3, 0.0)

        #Squared Intrusion points for sill
        p8 = gmsh.model.geo.add_point(2000, -38000, 0.0)
        p9 = gmsh.model.geo.add_point(0,-38000, 0.0)
        p10 = gmsh.model.geo.add_point(-2000, -38000, 0.0)
        p11 = gmsh.model.geo.add_point(2000, -30000, 0.0)
        p12 = gmsh.model.geo.add_point(-2000, -30000, 0.0)



        #New connecting lines for mantle
        self.c_yneg= gmsh.model.geo.add_line(p1, p2)
        self.c_xpos1 = gmsh.model.geo.add_line(p2, p5)
        self.c_mid1 = gmsh.model.geo.add_line(p5, p6)
        self.c_mid2 = gmsh.model.geo.add_line(p6, p7)
        self.c_xneg2 = gmsh.model.geo.add_line(p7, p1)

        #New connecting lines for crust
        self.c_xpos2 = gmsh.model.geo.add_line(p5, p3)
        self.c_ypos = gmsh.model.geo.add_line(p3, p4)
        self.c_xneg1 = gmsh.model.geo.add_line(p4, p7)

        #New connecting lines for intrusion
        self.c_int_connect = gmsh.model.geo.add_line(p6, p9)
        self.c_int_top_1 = gmsh.model.geo.add_line(p9, p10)
        self.c_int_left = gmsh.model.geo.add_line(p10, p12)
        self.c_int_bottom = gmsh.model.geo.add_line(p12, p11)
        self.c_int_right = gmsh.model.geo.add_line(p11, p8)
        self.c_int_top_2 = gmsh.model.geo.add_line(p8, p9)


        #Loops 2 Mantle, 1 crust.
        #c0 = gmsh.model.geo.add_curve_loop([self.c_yneg1, -self.c_down_mid2, self.c_mid2, self.c_xneg2])
        #self.s_mantle1 = gmsh.model.geo.add_plane_surface([c0])
        #c1 = gmsh.model.geo.add_curve_loop([self.c_yneg2, self.c_xpos1, self.c_mid1, self.c_down_mid2])
        #self.s_mantle2 = gmsh.model.geo.add_plane_surface([c1])

        #c3 = gmsh.model.geo.add_curve_loop([-self.c_mid2, self.c_intrusion_left, -self.c_down_mid1, self.c_ypos2, self.c_xneg1])
        #self.s_crust1 = gmsh.model.geo.add_plane_surface([c3])

        #c4 = gmsh.model.geo.add_curve_loop([-self.c_mid1, self.c_xpos2, self.c_ypos1, self.c_down_mid1, self.c_intrusion_right])
        #self.s_crust2 = gmsh.model.geo.add_plane_surface([c4])

        #I need to see how to make intrusion different material.
        #c5 = gmsh.model.geo.add_curve_loop([-self.c_intrusion_right, -self.c_intrusion_left])
        #self.s_intrusion = gmsh.model.geo.add_plane_surface([c5])

        #Mantle
        c0 = gmsh.model.geo.add_curve_loop([self.c_yneg, self.c_xpos1, 
                                            self.c_mid1, self.c_mid2, 
                                            self.c_xneg2])
        self.s_mantle = gmsh.model.geo.add_plane_surface([c0])

        #Crust
        c1 = gmsh.model.geo.add_curve_loop([-self.c_mid2, self.c_int_connect,
                                             self.c_int_top_1, self.c_int_left, 
                                             self.c_int_bottom, self.c_int_right,
                                             self.c_int_top_2, -self.c_int_connect,
                                             -self.c_mid1, self.c_xpos2,
                                             self.c_ypos, self.c_xneg1])
        self.s_crust = gmsh.model.geo.add_plane_surface([c1])

        #Intrusion
        c2 = gmsh.model.geo.add_curve_loop([-self.c_int_bottom, -self.c_int_left,
                                             -self.c_int_top_1, -self.c_int_top_2,
                                             -self.c_int_right])
        self.s_intrusion = gmsh.model.geo.add_plane_surface([c2])

        gmsh.model.geo.synchronize()

    def mark(self):
        """Mark geometry for materials, boundary conditions, faults, etc.

        This method is abstract in the base class and must be implemented
        in our local App class.
        """
        # Create three materials (slab, plate, and wedge).
        # We use the `MaterialGroup` data class defined in `gmsh_utils.`
        # The tag argument specifies the integer tag for the physical group.
        # The entities argument specifies the array of surfaces for the material.
        materials = (
            MaterialGroup(tag=1, entities=[self.s_mantle]),
            MaterialGroup(tag=2, entities=[self.s_crust]),
            MaterialGroup(tag=3, entities=[self.s_intrusion]),
        )
        for material in materials:
            material.create_physical_group()

        # Create physical groups for the boundaries and the faults.
        # We use the `VertexGroup` data class defined in `gmsh_utils`.
        # The name and tag specify the name and tag assigned to the physical group.
        # The dimension and entities specify the geometric entities to include in the physical
        # group.

        #I erased the boundary_xmid and VertexGroup(name="boundary_ymid", tag=14, dim=1, entities=[self.c_xneg_one, self.c_xneg_two]),
        #VertexGroup(name="intrusion_edge", tag=16, dim=0, entities=[self.p_intrusion_start, self.p_intrusion_end
        vertex_groups = (
            VertexGroup(name="boundary_xneg", tag=10, dim=1, entities=[self.c_xneg1, self.c_xneg2]),
            VertexGroup(name="boundary_xpos", tag=11, dim=1, entities=[self.c_xpos1, self.c_xpos2]),
            VertexGroup(name="boundary_yneg", tag=12, dim=1, entities=[self.c_yneg]),
            VertexGroup(name="boundary_ypos", tag=13, dim=1, entities=[self.c_ypos]),
            VertexGroup(name="intrusion", tag=15, dim=1, entities=[self.c_int_bottom, self.c_int_right, 
                                            self.c_int_top_2, self.c_int_top_1,
                                            self.c_int_left ])
        )
        for group in vertex_groups:
            group.create_physical_group()
    
     
    #This is the original mesh. 

    def generate_mesh(self, cell):
        """Generate the mesh.

        This method is abstract in the base class and must be implemented
        in our local App class.
        """
        # Set discretization size with geometric progression from distance to the fault.

        # We turn off the default sizing methods.
        gmsh.option.set_number("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromCurvature", 0)
        gmsh.option.set_number("Mesh.MeshSizeExtendFromBoundary", 0)

        # First, we setup a field `field_distance` with the distance from the fault.
        field_distance = gmsh.model.mesh.field.add("Distance")
        gmsh.model.mesh.field.setNumbers(field_distance, "CurvesList", [self.c_int_bottom, self.c_int_right, 
                                            self.c_int_top_2, self.c_int_top_1,
                                            self.c_int_left ])
        # Second, we setup a field `field_size`, which is the mathematical expression
        # for the cell size as a function of the cell size on the fault, the distance from
        # the fault (as given by `field_size`, and the bias factor.
        # The `GenerateMesh` class includes a special function `get_math_progression` 
        # for creating the string with the mathematical function. min_dx = 1.05e+3 coarser
        field_size = gmsh.model.mesh.field.add("MathEval")
        math_exp = GenerateMesh.get_math_progression(field_distance, min_dx=0.50e+3, bias=1.05) #change this to 1.15 to see different mesh
        gmsh.model.mesh.field.setString(field_size, "F", math_exp)

        # Finally, we use the field `field_size` for the cell size of the mesh.
        gmsh.model.mesh.field.setAsBackgroundMesh(field_size)

        if cell == "quad":
            # Generate a tri mesh and then recombine cells to form quadrilaterals.
            # We use the Frontal-Delaunay for Quads algorithm.
            gmsh.option.setNumber("Mesh.Algorithm", 8)
            gmsh.model.mesh.recombine()
            gmsh.model.mesh.generate(2)
        else:
            gmsh.model.mesh.generate(2)
        gmsh.model.mesh.optimize("Laplace2D")
    
    #This creates uniform meshing
    #def generate_mesh(self, cell):
    #    """Generate the mesh.

    #    This method is abstract in the base class and must be implemented.
    #    """
    #    # Set the cell size
    #    gmsh.option.setNumber("Mesh.MeshSizeMin", self.DX)
    #    gmsh.option.setNumber("Mesh.MeshSizeMax", self.DX)
    #    if cell == "hex":
            # A transfinite mesh with recombine set to True should result in a hex mesh. 
    #        gmsh.model.mesh.set_transfinite_automatic(recombine=True)
    #    else:
    #        gmsh.option.setNumber("Mesh.Algorithm", 8)

    #Generate the mesh and then improve mesh quality using Laplacian smoothing.
    #    gmsh.model.mesh.generate(3)
    #    gmsh.model.mesh.optimize("Laplace2D")

# If script is called from the command line, run the application.
if __name__ == "__main__":
    App().main()


# End of file
