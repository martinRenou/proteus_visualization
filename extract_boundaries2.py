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


def write_unstructured_grid_from_polydata(writer, filename, poly):
    ugrid_filter = vtk.vtkAppendFilter()
    ugrid_filter.SetInputData(poly)
    ugrid_filter.Update()
    grid = ugrid_filter.GetOutput()

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

        # Extract the left boundary
        threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, 'x')
        threshold.ThresholdByLower(0)
        threshold.Update()

        front_boundary = threshold.GetOutput()

        front_boundary.GetPointData().RemoveArray('x')
        front_boundary.GetPointData().RemoveArray('y')
        front_boundary.GetPointData().RemoveArray('z')
        front_boundary.GetPointData().RemoveArray('p')

        front_boundary = reverse_normals(front_boundary)

        write_unstructured_grid_from_polydata(writer, 'proteus_vtu/proteus_front_boundary_{}.vtu'.format(i), front_boundary)


if __name__ == "__main__":
    to_vtk_files()
    print('done')
