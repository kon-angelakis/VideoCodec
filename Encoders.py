from misc import *


#Encodes the frames in the following tuple form (Frame(I/P), difference)
def encode_frames(error_frames, iframe_repeat = 12):
    
    encoded = []
    n = 0
    
    for f_index, difference in enumerate(error_frames):
        if f_index % iframe_repeat == 0:
            encoded.append(('I', difference))
        else:
            encoded.append(('P', difference))
        
        print_progress(n, len(error_frames), "Encoding")
        n += 1
        
    return encoded