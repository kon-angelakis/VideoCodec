import cv2


#Also return fps value for the later video reconstruction
def video2frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        #If end of capture reached break
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames, fps


def frames2video(frames, output_path, fps=30):
    print("Saving video..")
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), fps, size)
    for frame in frames:
        out.write(frame)
    out.release()
    print(f"Video saved as: {output_path}")