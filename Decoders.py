from misc import *


#Get encoded frames and decode using the calculated error each P frame is predicted from the previous frame
def decode_frames(encoded_frames):
    
    decoded = []
    
    for f_index, (ftype, error) in enumerate(encoded_frames):
        if ftype == 'I':
            decoded.append(error)
        else:
            decoded.append(decoded[f_index - 1] + error)
        print_progress(f_index, len(encoded_frames), "Decoding")
            
    return decoded