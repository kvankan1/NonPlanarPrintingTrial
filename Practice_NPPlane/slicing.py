import numpy as np
from stl import mesh as mesh_module
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from scipy.interpolate import RBFInterpolator
import matplotlib.pyplot as plt
from surface_processing import CreateMesh, PlotMesh
from mesh_interpolation import rbf_interpolation
import fullcontrol as fc

################################Slicing Angled Planes####################################################

def SliceInterpolatedPlaneAngle(rbf_interpolation: object, x_values: np.array, angle: float, t_step: float):

    """
    Slice an interpolated object rbf_interpolation along the XZ axis at a given y value

    Parameters:
    - rbf_interpolation: interpolated plane with x, y and z values
    - x_values: x values where to the plane at an angle will start
    - spacing: spacing of the planes
    - angle: angle of the planes
    - t_step: x and y are defined by parametric equations, t_step defines how big of a step x and y will take to produce new points
    """
    all_points = np.array([0, 0, 0])

    #plane_equations = PlanesAtAngle(angle, plane_spacing, x_values[0], x_values[-1])

    for i, x0 in enumerate(x_values):
        t_arr = np.arange(0, 1, t_step)

        x_points = x0*np.ones_like(t_arr) - x0*t_arr
        y_points = t_arr*x0/np.tan(angle)
        input_grid = np.column_stack((x_points, y_points))
        z_points = rbf_interpolation.__call__(input_grid)

        formatted_points = np.column_stack((input_grid, z_points))

        all_points = np.vstack((all_points, formatted_points))

    return(all_points)



x_values = np.linspace(-20, 20, 100)
y_values = np.linspace(-20, 20, 100)

points = SliceInterpolatedPlaneAngle(rbf_interpolation, x_values, np.pi/4, 0.1)


steps = []
for i in range((len(points))):
    x = points[i,0]
    y = points[i,1]
    z = points[i,2]

    steps.append(fc.Point(x = x, y = y, z = z))

print(fc.transform(steps, "gcode"))
fc.transform(steps, "plot")



    

##########################################Slicing XZ Planes#########################################################



def SliceInterpolatedPlaneXZ(rbf_interpolation: object, x_values: np.array, y_value: np.array):

    """
    Slice an interpolated object rbf_interpolation along the XZ axis at a given y value

    Parameters:
    - rbf_interpolation: interpolated plane with x, y and z values
    - x_values: x values where to slice the interpolated plane
    - y_value: the y value of the xz plane
    """

    # Create a grid of x values and the constant y value
    x_grid = x_values
    y_grid = np.full_like(x_grid, fill_value=y_value)

    # Stack x and y grids horizontally
    input_grid = np.column_stack((x_grid, y_grid))

    # Use the RBF interpolation to calculate z values
    z_values = rbf_interpolation.__call__(input_grid)

    # Stack x, y, and z values horizontally
    sliced_plane = np.column_stack((x_grid, y_grid, z_values))

    return sliced_plane


def GetSteps(x_values: np.array, y_values: np.array, slicer: object):


    """
    Get the sequential steps to produce a gcode

    Parameters:
    x_values: x values (range) of the gcode points
    y_values: y values (range) of the gcode points
    slicer: what function to use to slice the interpolated plane
    """
    steps = []


    for y in y_values: 
        sliced_plane = SliceInterpolatedPlaneXZ(rbf_interpolation, x_values, y)
        #collect points on this plane
        #should find a way to not use for loops here

        for i,x in enumerate(x_values):
            x = sliced_plane[i,0]
            y = sliced_plane[i,1]
            z = sliced_plane[i,2]

            point = fc.Point(x = x, y = y, z = z)
            steps.append(point)

    return steps

#Uncomment to slice xz planes

#x_values = np.linspace(-20, 20, 100)
#y_values = np.linspace(-20, 20, 100)

#steps = GetSteps(x_values, y_values, SliceInterpolatedPlaneAngle)

#print(fc.transform(steps, "gcode"))
#fc.transform(steps, "plot")







