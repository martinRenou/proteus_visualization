"""This takes a xdmf input file from a proteus computation and turns it into multiple vtk files for visualization."""

import os
import sys

import vtk


def to_vtk_files():
    reader = vtk.vtkXMLUnstructuredGridReader()
    writer = vtk.vtkXMLUnstructuredGridWriter()

    for i in range(77):
        reader.SetFileName('proteus_vtu/proteus_{}.vtu'.format(i))
        reader.Update()

        grid = reader.GetOutput()

        # Extract boundaries
        boundaries_filter = vtk.vtkGeometryFilter()
        boundaries_filter.SetInputData(grid)
        # boundaries_filter.ComputeNormalsOff()
        # boundaries_filter.ComputeGradientsOff()
        # boundaries_filter.ComputeScalarsOff()
        # boundaries_filter.GenerateTrianglesOn()
        boundaries_filter.Update()
        boundaries = boundaries_filter.GetOutput()

        # Reverse cells indexing (for reversing the normals)
        reverse_normals = vtk.vtkReverseSense()
        reverse_normals.ReverseCellsOn()
        reverse_normals.ReverseNormalsOn()
        reverse_normals.SetInputData(boundaries)
        reverse_normals.Update()
        reversed_normals = reverse_normals.GetOutput()

        # Compute the cell normals (this is needed otherwise ReverseSense seems
        # to compute point normals)
        # compute_cell_normals = vtk.vtkPolyDataNormals()
        # compute_cell_normals.ComputePointNormalsOff()  # Flat shading in shaders
        # compute_cell_normals.ComputeCellNormalsOn()
        # compute_cell_normals.SetInputData(reversed_normals)
        # computed_cell_normals = compute_cell_normals.GetOutput()

        # Extract the unstructured grid
        ugrid_filter = vtk.vtkAppendFilter()
        ugrid_filter.SetInputData(reversed_normals)
        ugrid_filter.Update()
        unstructured_grid = ugrid_filter.GetOutput()

        writer.SetInputData(unstructured_grid)
        writer.SetFileName('proteus_vtu/proteus_boundaries_{}.vtu'.format(i))

        writer.Write()


if __name__ == "__main__":
    to_vtk_files()
    print('done')
