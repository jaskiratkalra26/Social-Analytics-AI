import cv2
import os
import sys

# Add the project root directory to Python path to import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Config

def extract_frames(video_path):
    """
    Extracts frames from a video at a specified frame rate (FPS).
    Saves the frames to the directory specified in Config.py.

    Args:
        video_path (str): Path to the input video file.

    Returns:
        int: Number of frames extracted.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Ensure output directory exists
    os.makedirs(Config.FRAMES_OUTPUT_DIR, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return 0

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate interval to skip frames based on target FPS
    # If target FPS is 1 and video FPS is 30, we save every 30th frame
    if Config.TARGET_FPS > 0:
        frame_interval = int(video_fps / Config.TARGET_FPS)
    else:
        # Default to saving all frames if target fps is invalid
        frame_interval = 1
    
    # Ensure interval is at least 1
    frame_interval = max(1, frame_interval)

    frame_count = 0
    saved_count = 0
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Check if this frame should be saved
        if frame_count % frame_interval == 0:
            frame_filename = f"{video_name}_frame_{saved_count:04d}.jpg"
            frame_path = os.path.join(Config.FRAMES_OUTPUT_DIR, frame_filename)
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted {saved_count} frames from {video_path}")
    return saved_count

if __name__ == "__main__":
    # Example usage
    # extract_frames("path/to/video.mp4")
    pass
