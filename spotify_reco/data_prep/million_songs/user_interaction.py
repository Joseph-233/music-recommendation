import itertools


def read(path, start_row=0, end_row=1000):
    '''
    inclusive of start_row and end_row
    Has 48,373,586 rows totally
    '''
    interactions = {"user_id": [], "song_id": [], "play_count": []}
    with open(path, "r") as f:
        for line in itertools.islice(f, start_row, end_row + 1):
            interactions["user_id"].append(line.split()[0])
            interactions["song_id"].append(line.split()[1])
            interactions["play_count"].append(line.split()[2])
    return interactions