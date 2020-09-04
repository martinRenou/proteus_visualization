# Load hdf5 file using memory mapping

import h5py

import mmap

import numpy as np


def metadata_to_array(metadata, mapping):
    """Turn array metadata into a NumPy array."""
    shape = metadata['shape']
    dtype = metadata['dtype']
    offset = metadata['offset']
    length = np.prod(shape)

    return np.frombuffer(mapping, dtype=dtype, count=length, offset=offset).reshape(shape)

def extract_arrays_metadata(hdf5_path, print_metadata=False):
    """Extract arrays metadata from an HDF5 file."""
    arrays_metadata = {}

    with h5py.File(hdf5_path, 'r') as fobj:
        def dump(name, item):
            if isinstance(item, h5py.Dataset):
                if print_metadata:
                    print(name, item.shape, item.dtype)

                arrays_metadata[name] = dict(
                    offset=item.id.get_offset(),
                    shape=item.shape,
                    dtype=item.dtype,
                    filename=hdf5_path
                )

        fobj.visititems(dump)

    return arrays_metadata

def extract_array(arrays_metadata, array_name):
    """Extract NumPy array from an HDF5 file, given the arrays metadata and the array name you want to extract."""
    metadata = arrays_metadata[array_name]

    with open(metadata['filename'], 'rb') as fobj:
        mapping = mmap.mmap(fobj.fileno(), 0, access=mmap.ACCESS_READ)

        return metadata_to_array(metadata, mapping)
