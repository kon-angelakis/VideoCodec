import sys, numpy as np


#Prints out in the same line updating it
def print_progress(n, m, action):
    sys.stdout.write(f"\r{ action }: {n + 1}/{m}")
    sys.stdout.flush()
    #Reached end
    if n == m - 1:
        print("")
        
        
#Every iframe_repeat frames its I frame        
def calculate_ip_frames(frames, iframe_repeat = 12):
    print('Calculating I/P-Frames..')
    
    I_frames = []
    P_frames = []

    for f_index, frame in enumerate(frames):
        if f_index % iframe_repeat == 0:
            I_frames.append(frame)
        else:
            P_frames.append(frame)
    return I_frames, P_frames


#Calculate the error/difference between 2 concecutive P frames
def calculate_diff(frames, iframe_repeat = 12):
    
    differences = []
    
    for f_index, frame in enumerate(frames):
        if f_index % iframe_repeat == 0:
            differences.append(frame)
        else:
            differences.append(frame - frames[f_index - 1])
        print_progress(f_index, len(frames), "Differences")

    return differences
  
  
def vectors_exhaustive_motion(frames, iframe_repeat = 12, macroblock_size = 16, search_radius = 8):
    
    motion_vectors = []
    height, width, layers = frames[0].shape
    #Calculate block amount
    vertical_blocks = height // macroblock_size
    horizontal_blocks = width // macroblock_size
    
    for index, frame in enumerate(frames):
        print_progress(index, len(frames), "Calculating Exhaustive Search Vectors")
        if index % iframe_repeat != 0:
           current_frame = frame
           previous_frame = frames[index - 1]
        else:
            continue
        
        #Motion vector is saved like y, x so as to match opencv which also saves frames in this format 
        motion_vector = np.zeros((vertical_blocks, horizontal_blocks, 2))

        for ver in range(vertical_blocks):
            for hor in range(horizontal_blocks):
                #Mean Absolute Difference will be used as a metric
                min_MAD = float('inf')
                best_d_hor, best_d_ver = 0, 0

                block_y_cord = ver * macroblock_size
                block_x_cord = hor * macroblock_size

                for d_ver in range(-search_radius, search_radius + 1):
                    for d_hor in range(-search_radius, search_radius + 1):
                        #Loop through all the block reached by the search radius and find the one with the minimum MAD
                        #The blocks are the previous frame's reference points/blocks that are compared with the current frame's block
                        #When the min_MAD is achieved thats the best vector move
                        refblock_y_cord = block_y_cord + d_ver
                        refblock_x_cord = block_x_cord + d_hor

                        #Make sure everything is in bounds
                        if (0 <= refblock_y_cord < height - macroblock_size) and (0 <= refblock_x_cord < width - macroblock_size):
                            current_block = current_frame[block_y_cord:block_y_cord + macroblock_size, block_x_cord:block_x_cord + macroblock_size]
                            reference_block = previous_frame[refblock_y_cord:refblock_y_cord + macroblock_size, refblock_x_cord:refblock_x_cord + macroblock_size]

                            tmp_MAD = np.sum(np.abs(current_block - reference_block))

                            if tmp_MAD < min_MAD:
                                min_MAD = tmp_MAD
                                best_d_ver, best_d_hor = d_ver, d_hor

                motion_vector[ver, hor] = (best_d_ver, best_d_hor)

        motion_vectors.append(motion_vector)
        
    return motion_vectors

