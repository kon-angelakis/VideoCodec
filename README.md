# VideoCodec
Custom video encoding/decoding with (and without) motion compensation using python's opencv library

### Without Motion Compensation

Initially, using the OpenCV library, the video `"Raw.mkv"` is read, and its fps is saved for later use. The frames are placed in the `frames` list. Then, the I-frames (every `I_FRAMES_REPEAT = 12` frames) and the P-frames are calculated and placed in their respective lists. Afterward, the difference frames are calculated: if it’s an I-frame, its difference is the frame itself, whereas if it’s a P-frame, the difference is the current frame minus the previous frame. Now follows the encode/decode phase.

**Encode**:  
During encoding, each frame is encoded as a tuple `(Frame_Type, Error)`. These tuples are placed in the `encoded_frames` list.

**Decode**:  
The decoder works in reverse, processing the `encoded_frames`. If the frame is an I-frame, the decoded frame remains as is, while for a P-frame, the decoded frame is computed as the previous decoded frame plus the `error` difference. These frames are placed in the `decoded_frames` list.

Finally, using OpenCV again, the video is saved to disk under the name `"Edited.mkv"` with the appropriate fps to match the original video.

---

### Motion Compensation

The macroblock size is stored in the `MACROBLOCK_SIZE` variable, and the radius size is stored in `SEARCH_RADIUS`. The comparison technique used is **Mean Absolute Difference (MAD)**. The function `vectors_exhaustive_motion(frames, iframe_repeat=12, block_size=16, search_radius=8)` computes and returns the motion vectors in the `vectors` list. Here's how it works:

1. The frame is split into a grid of macroblocks with `cell_size = (x=width//macroblock_size, y=height//macroblock_size)`.
2. For each frame in the `frames` list, if it’s a P-frame, the reference frame is the one preceding it.
3. The `motion_vector` matrix is initialized with zeros (using Numpy), and its size is `N x M`, where `N = vertical_blocks` and `M = horizontal_blocks`. This is because OpenCV stores frames in (y,x) format instead of (x,y).
4. The traversal of macroblocks begins from right to left. For each block, its coordinates `(block_y_cord, block_x_cord)` are calculated, and the `MAD` is initialized to infinity.
5. Using the `search_radius`, reference blocks and their coordinates `(refblock_y_cord, refblock_x_cord)` are identified around the current block. If the reference block is within the frame's boundaries, the `MAD` is calculated between the `current_block` of the current frame and the `reference_block` of the previous frame.
6. If the calculated `MAD` is smaller than the stored `MAD`, it is updated along with the reference block coordinates.
7. Once the search for reference blocks is complete, the `motion_vector` at `(y, x)` is set to the coordinates of the reference block with the smallest MAD.

This process continues until the `motion_vectors` matrix is fully populated and then returned.

---

### Additional Processes

Using the os library the compression rate of the video is calculated using the formula `Original_File_Size / Final_File_Size`
