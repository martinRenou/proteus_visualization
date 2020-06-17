"""This takes the marin vtu files from the proteus computation and extracts the boundaries."""

import vtk


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


def to_ugrid(grid):
    ugrid_filter = vtk.vtkAppendFilter()
    ugrid_filter.SetInputData(grid)
    ugrid_filter.Update()
    return ugrid_filter.GetOutput()


def write_unstructured_grid_from_polydata(writer, filename, poly):
    grid = to_ugrid(poly)

    writer.SetInputData(grid)
    writer.SetFileName(filename)

    writer.Write()


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
        boundaries_filter.Update()
        boundaries = boundaries_filter.GetOutput()

        # Add the position data arrays
        array_x = vtk.vtkFloatArray()
        array_x.SetNumberOfComponents(1)
        array_x.SetName("x")

        array_y = vtk.vtkFloatArray()
        array_y.SetNumberOfComponents(1)
        array_y.SetName("y")

        array_z = vtk.vtkFloatArray()
        array_z.SetNumberOfComponents(1)
        array_z.SetName("z")

        ncells = boundaries.GetNumberOfCells()
        for idx in range(ncells):
            p = boundaries.GetPoint(idx)

            array_x.InsertNextValue(p[0])
            array_y.InsertNextValue(p[1])
            array_z.InsertNextValue(p[2])

        boundaries.GetPointData().AddArray(array_x)
        boundaries.GetPointData().AddArray(array_y)
        boundaries.GetPointData().AddArray(array_z)

        # Extract boundaries one by one using the Threshold filter
        threshold = vtk.vtkThreshold()
        threshold.SetInputData(boundaries)

        # # Extract the whole boundary
        threshold.AllScalarsOff()
        threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'z')
        threshold.ThresholdByLower(0.999)
        threshold.Update()

        boundaries = threshold.GetOutput()

        boundaries.GetPointData().RemoveArray('x')
        boundaries.GetPointData().RemoveArray('y')
        boundaries.GetPointData().RemoveArray('z')
        boundaries.GetPointData().RemoveArray('p')

        boundaries = reverse_normals(boundaries)

        write_unstructured_grid_from_polydata(writer, 'proteus_vtu/proteus_boundaries_{}.vtu'.format(i), boundaries)

        # # Extract the left boundary
        # threshold.AllScalarsOn()
        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'x')
        # threshold.ThresholdByLower(0)
        # threshold.Update()

        # left_boundary = threshold.GetOutput()

        # left_boundary.GetPointData().RemoveArray('x')
        # left_boundary.GetPointData().RemoveArray('y')
        # left_boundary.GetPointData().RemoveArray('z')
        # left_boundary.GetPointData().RemoveArray('p')

        # left_boundary = reverse_normals(left_boundary)

        # write_unstructured_grid_from_polydata(writer, 'proteus_vtu/proteus_left_boundary_{}.vtu'.format(i), left_boundary)

        # # Extract the right boundary
        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'x')
        # threshold.ThresholdByUpper(3.22)
        # threshold.Update()

        # right_boundary = threshold.GetOutput()

        # right_boundary.GetPointData().RemoveArray('x')
        # right_boundary.GetPointData().RemoveArray('y')
        # right_boundary.GetPointData().RemoveArray('z')
        # right_boundary.GetPointData().RemoveArray('p')

        # right_boundary = reverse_normals(right_boundary)

        # write_unstructured_grid_from_polydata(writer, 'proteus_vtu/proteus_right_boundary_{}.vtu'.format(i), right_boundary)

        # # Extract the front boundary
        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'y')
        # threshold.ThresholdByLower(0)
        # threshold.Update()

        # front_boundary = threshold.GetOutput()

        # front_boundary.GetPointData().RemoveArray('x')
        # front_boundary.GetPointData().RemoveArray('y')
        # front_boundary.GetPointData().RemoveArray('z')
        # front_boundary.GetPointData().RemoveArray('p')

        # front_boundary = reverse_normals(front_boundary)

        # write_unstructured_grid_from_polydata(writer, 'proteus_vtu/proteus_front_boundary_{}.vtu'.format(i), front_boundary)

        # # Extract the back boundary
        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'y')
        # threshold.ThresholdByUpper(1)
        # threshold.Update()

        # back_boundary = threshold.GetOutput()

        # back_boundary.GetPointData().RemoveArray('x')
        # back_boundary.GetPointData().RemoveArray('y')
        # back_boundary.GetPointData().RemoveArray('z')
        # back_boundary.GetPointData().RemoveArray('p')

        # back_boundary = reverse_normals(back_boundary)

        # write_unstructured_grid_from_polydata(writer, 'proteus_vtu/proteus_back_boundary_{}.vtu'.format(i), back_boundary)

        # # Extract the ground
        # threshold.AllScalarsOff()  # All points should verify the condition on a cell from now on

        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'y')
        # threshold.ThresholdByLower(0.9999)
        # threshold.Update()

        # inter = threshold.GetOutput()
        # threshold.SetInputData(to_ugrid(inter))

        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'y')
        # threshold.ThresholdByUpper(0.0001)
        # threshold.Update()

        # inter = threshold.GetOutput()
        # threshold.SetInputData(to_ugrid(inter))

        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'x')
        # threshold.ThresholdByLower(3.2199)
        # threshold.Update()

        # inter = threshold.GetOutput()
        # threshold.SetInputData(to_ugrid(inter))

        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'x')
        # threshold.ThresholdByUpper(0.0001)
        # threshold.Update()

        # inter = threshold.GetOutput()
        # threshold.SetInputData(to_ugrid(inter))

        # threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'z')
        # threshold.ThresholdByLower(0.9999)
        # threshold.Update()

        # bottom_boundary = threshold.GetOutput()

        # bottom_boundary.GetPointData().RemoveArray('x')
        # bottom_boundary.GetPointData().RemoveArray('y')
        # bottom_boundary.GetPointData().RemoveArray('z')
        # bottom_boundary.GetPointData().RemoveArray('p')

        # bottom_boundary = reverse_normals(bottom_boundary)

        # write_unstructured_grid_from_polydata(writer, 'proteus_vtu/proteus_bottom_boundary_{}.vtu'.format(i), bottom_boundary)



if __name__ == "__main__":
    to_vtk_files()
    print('done')
