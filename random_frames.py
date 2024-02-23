import numpy as np
import random


def select_random_frame(frames, position):
    # Set the random seed
    random.seed(random.randint(0,100))

    # Shuffling the frames using Fischer Yates Shuffling
    shuffled_frames = frames.copy()
    random.shuffle(shuffled_frames)

    # Select a particular frame according to 'position' parameter
    selected_frame = shuffled_frames[position]

    # Index of frame in original array of frames
    for idx in range(len(frames)):
        if(np.array_equal(selected_frame, frames[idx])):
            break

    return idx

