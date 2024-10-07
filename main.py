import os
import numpy as np
from VideoIO import *
from Encoders import *
from Decoders import *
from misc import *


I_FRAMES_REPEAT = 12
MACROBLOCK_SIZE = 16
SEARCH_RADIUS = 8


video = 'Raw.mkv'
frames, fps = video2frames(video)

print("---No motion compensation---")

I_frames, P_frames = calculate_ip_frames(frames, I_FRAMES_REPEAT)

error_frames = calculate_diff(frames, I_FRAMES_REPEAT)
encoded_frames = encode_frames(error_frames, I_FRAMES_REPEAT)
decoded_frames = decode_frames(encoded_frames)

frames2video(decoded_frames, 'Edited.mkv', fps)
edited_video = 'Edited.mkv'

print("---Motion compensation---")

vectors = vectors_exhaustive_motion(frames, I_FRAMES_REPEAT, MACROBLOCK_SIZE, SEARCH_RADIUS)

print("---Compression---")

#Compare the original and encoded video file sizes to find out the compression rate
original_size = os.path.getsize(video)
encoded_size = os.path.getsize(edited_video)
compression = original_size / encoded_size

print(f"Compression Ratio: {compression:.3f}")
