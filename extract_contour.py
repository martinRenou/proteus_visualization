"""This takes a xdmf input file from a proteus computation and turns it into multiple vtk files for visualization."""

import os
import sys

import vtk


def to_vtk_files():
    writer = vtk.vtkXMLUnstructuredGridWriter()

    reader = vtk.vtkXMLUnstructuredGridReader()

    for i in range(77):
        reader.SetFileName('proteus_vtu/proteus_{}.vtu'.format(i))
        reader.Update()

        unstructured_grid = reader.GetOutput()

        contour_filter = vtk.vtkContourFilter()
        contour_filter.SetInputData(unstructured_grid)

        contour_filter.ComputeNormalsOff()
        contour_filter.ComputeGradientsOff()
        contour_filter.ComputeScalarsOff()
        contour_filter.GenerateTrianglesOn()

        # Disable binary tree search, it might not be useful as
        # we compute only one contour
        contour_filter.UseScalarTreeOff()

        contour_filter.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'phi')

        contour_filter.SetValue(0, 0.)

        contour_filter.Update()

        contour = contour_filter.GetOutput()

        def reverse_normals(grid):
            polydata_filter = vtk.vtkGeometryFilter()
            polydata_filter.SetInputData(grid)
            polydata_filter.Update()
            polydata = polydata_filter.GetOutput()

            reverse = vtk.vtkReverseSense()
            reverse.ReverseCellsOn()
            reverse.SetInputData(polydata)
            reverse.Update()
            return reverse.GetOutput()

        contour = reverse_normals(contour)

        ugrid_filter = vtk.vtkAppendFilter()
        ugrid_filter.SetInputData(contour)
        ugrid_filter.Update()
        unstructured_grid = ugrid_filter.GetOutput()

        writer.SetInputData(unstructured_grid)
        writer.SetFileName('proteus_vtu/proteus_contour_{}.vtu'.format(i))

        writer.Write()


if __name__ == "__main__":
    to_vtk_files()
