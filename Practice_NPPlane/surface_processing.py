import numpy as np
from stl import mesh as mesh_module  # Rename the module
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def CreateMesh(filepath: str):
    """
    Create a Mesh from an STL file
    Parameters:
    - filepath: filepath relative to current directory, use quotations
    """
    my_mesh = mesh_module.Mesh.from_file(filepath)  # Rename the variable
    return my_mesh

def PlotMesh(my_mesh: np.ndarray):
    """
    Plot the Mesh
    Parameters:
    - my_mesh: STL mesh
    """
    # Create a new plot
    figure = pyplot.figure()
    axes = figure.add_subplot(projection='3d')

    # Load the STL files and add the vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))

    # Auto scale to the mesh size
    scale = my_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()

    return figure

my_mesh = CreateMesh("Practice_NPPlane\surface.stl")  # Use a different variable name

#figure = PlotMesh(my_mesh)




