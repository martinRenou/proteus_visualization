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

        # Clean useless data for visualization
        cell_data = unstructured_grid.GetCellData()

        cell_data.RemoveArray('CellMapL2G')
        cell_data.RemoveArray('elementMaterialTypes')

        point_data = unstructured_grid.GetPointData()

        point_data.RemoveArray('pInit')
        point_data.RemoveArray('phi_sp0')
        point_data.RemoveArray('pInc')
        point_data.RemoveArray('quantDOFs_for_clsvof0')
        point_data.RemoveArray('vof0')
        point_data.RemoveArray('nodeMaterialTypes')
        point_data.RemoveArray('NodeMapL2G')

        writer.SetInputData(unstructured_grid)
        writer.SetFileName('{}/proteus_{}.vtu'.format(dir_name, index))

        writer.Write()


if __name__ == "__main__":
    to_vtk_files(sys.argv[1])
