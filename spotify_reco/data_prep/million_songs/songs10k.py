import os
import sys
from PythonSrc import hdf5_getters
import numpy as np
from collections import defaultdict


def read(hdf5path, start_row=0, end_row=100):
    '''
    inclusive of start_row and end_row
    '''
    songs = defaultdict(list)#defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    # sanity check
    if not os.path.isfile(hdf5path):
        print("ERROR: file", hdf5path, "does not exist.")
        sys.exit(0)
    h5 = hdf5_getters.open_h5_file_read(hdf5path)
    # numSongs = hdf5_getters.get_num_songs(h5)
    # print("number of songs in this file:", numSongs)

    # get all getters
    getters = filter(lambda x: x[:4] == "get_", hdf5_getters.__dict__.keys())
    getters = [
        getter for getter in getters if getter != "get_num_songs" #or getter != "get_artist_mbtags"
    ]  # special case
    getters = np.sort(getters)

    # print them
    for songidx in range(start_row, end_row + 1):
        for getter in getters:
            try:
                res = hdf5_getters.__getattribute__(getter)(h5, songidx)
            except AttributeError as e:
                print(e)

            songs[getter[4:]].append(res)
        # print("Read song", songidx, "from file:", hdf5path)

    h5.close()
    return songs
