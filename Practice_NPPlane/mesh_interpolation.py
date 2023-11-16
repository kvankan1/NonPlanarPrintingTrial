import numpy as np
from stl import mesh as mesh_module
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from scipy.interpolate import RBFInterpolator
import matplotlib.pyplot as plt
from surface_processing import CreateMesh, PlotMesh

def InterpolateRBF(mesh: np.ndarray, res: int):
    """
    Create an RBF interpolation of the mesh
    Parameters:
    - mesh: STL mesh
    - res: Every res points will be taken in order to not have to interpolate too many points
    """
    mesh_points = mesh.points.reshape([-1,3])
    x_points = mesh_points[:,0].reshape(-1,1).astype(float)
    x_points = x_points[::res]
    y_points = mesh_points[:,1].reshape(-1,1).astype(float)
    y_points = y_points[::res]
    z_points = mesh_points[:,2].reshape(-1,1).astype(float)
    z_points = z_points[::res]

    print("points =", mesh_points)

    print("X_points =", x_points)

    input_grid = np.hstack((x_points, y_points))
      
    print("Input Grid =", input_grid)

    rbf_interpolation = RBFInterpolator(input_grid, z_points, neighbors = 2, kernel = "linear")

    return rbf_interpolation


def PlotInterpolant(rbf_interpolator: object, x_range: range , y_range: range):
    """
    Plot the interpolant using RBFInterpolator.__call__(x).

    Parameters:
    - rbf_interpolator: RBFInterpolator instance
    - x_range: 1D NumPy array representing the x-axis values
    - y_range: 1D NumPy array representing the y-axis values
    """
    # Create a mesh grid from x_range and y_range
    x_mesh, y_mesh = np.meshgrid(x_range, y_range)
    
    # Flatten the mesh grid to obtain (x, y) pairs
    xy_pairs = np.column_stack((x_mesh.flatten(), y_mesh.flatten()))

    # Compute the interpolated values using RBFInterpolator.__call__(x)
    z_interp = rbf_interpolator.__call__(xy_pairs)

    # Reshape the interpolated values to the shape of the mesh grid
    z_interp = z_interp.reshape(x_mesh.shape)

    # Plot the interpolant
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x_mesh, y_mesh, z_interp, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Interpolated Z')
    plt.show()



def PlotMeshAndInterpolant(original_mesh: np.ndarray, rbf_interpolator: object, x_range: range, y_range: range):
    """
    Plot the original mesh and the interpolant on the same axes.

    Parameters:
    - original_mesh: STL mesh instance
    - rbf_interpolator: RBFInterpolator instance
    - x_range: 1D NumPy array representing the x-axis values
    - y_range: 1D NumPy array representing the y-axis values
    """
    # Plot the original mesh
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(original_mesh.x, original_mesh.y, original_mesh.z, cmap='viridis', alpha=0.5)

    # Create a mesh grid from x_range and y_range
    x_mesh, y_mesh = np.meshgrid(x_range, y_range)

    # Flatten the mesh grid to obtain (x, y) pairs
    xy_pairs = np.column_stack((x_mesh.flatten(), y_mesh.flatten()))

    # Compute the interpolated values using RBFInterpolator.__call__(x)
    z_interp = rbf_interpolator(xy_pairs)

    # Reshape the interpolated values to the shape of the mesh grid
    z_interp = z_interp.reshape(x_mesh.shape)

    # Plot the interpolant on the same axes
    ax.plot_surface(x_mesh, y_mesh, z_interp, cmap='viridis', alpha=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

my_mesh = CreateMesh("Practice_NPPlane\surface.stl")
original_mesh = my_mesh

# Example x and y ranges for plotting
x_range = np.linspace(-20, 20, 100)
y_range = np.linspace(-20, 20, 100)

rbf_interpolation = InterpolateRBF(my_mesh, res = 100)

#PlotInterpolant(rbf_interpolation, [-20,20], [-20,20])

PlotMeshAndInterpolant(my_mesh, rbf_interpolation, x_range, y_range)
