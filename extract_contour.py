"""This takes a xdmf input file from a proteus computation and turns it into multiple vtk files for visualization."""

import os
import sys

import vtk


def to_vtk_files(filepath):
    reader = vtk.vtkXdmfReader()
    reader.SetFileName(filepath)
    reader.Update()

    info = reader.GetOutputInformation(0)
    timestamps = info.Get(vtk.vtkCompositeDataPipeline.TIME_STEPS())

    grid = reader.GetOutput()

    writer = vtk.vtkXMLUnstructuredGridWriter()

    dir_name = 'proteus_vtu'

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for index, time in enumerate(timestamps):
        reader.UpdateTimeStep(time)

        unstructured_grid = grid.GetBlock(0).GetBlock(0)

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

        ugrid_filter = vtk.vtkAppendFilter()
        ugrid_filter.SetInputData(contour)
        ugrid_filter.Update()
        unstructured_grid = ugrid_filter.GetOutput()

        writer.SetInputData(unstructured_grid)
        writer.SetFileName('{}/proteus_contour_{}.vtu'.format(dir_name, index))

        writer.Write()


if __name__ == "__main__":
    to_vtk_files(sys.argv[1])
