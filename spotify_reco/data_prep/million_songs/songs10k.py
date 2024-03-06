import os
import sys
from PythonSrc import hdf5_getters
import numpy as np


def read(hdf5path, numSongs=10000):
    songs = {}
    # sanity check
    if not os.path.isfile(hdf5path):
        print("ERROR: file", hdf5path, "does not exist.")
        sys.exit(0)
    h5 = hdf5_getters.open_h5_file_read(hdf5path)
    #numSongs = hdf5_getters.get_num_songs(h5)
    print("number of songs in this file:", numSongs)

    # get all getters
    getters = filter(lambda x: x[:4] == "get_", hdf5_getters.__dict__.keys())
    getters = [
        getter for getter in getters if getter != "get_num_songs"
    ]  # special case
    getters = np.sort(getters)

    # print them
    for songidx in range(numSongs):
        for getter in getters:
            try:
                res = hdf5_getters.__getattribute__(getter)(h5, songidx)
            except AttributeError as e:
                print(e)

            if songidx == 0:
                songs[getter[4:]] = [res]
            else:
                songs[getter[4:]].append(res)
        print("Read song", songidx, "/", numSongs - 1, "from file:", hdf5path)
    
    h5.close()
    return songs
