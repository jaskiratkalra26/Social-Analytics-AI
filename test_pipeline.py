import os
import sys
import importlib.util

# Add the current directory to sys.path so we can import Config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import Config
from pipeline.frame_extractor import extract_frames
from pipeline.audio_extractor import extract_audio
from pipeline.scene_detector import detect_scenes

# Import video.loader dynamically because of the dot in the filename
spec = importlib.util.spec_from_file_location("video_loader", os.path.join(os.path.dirname(__file__), "pipeline", "video.loader.py"))
video_loader = importlib.util.module_from_spec(spec)
sys.modules["video_loader"] = video_loader
spec.loader.exec_module(video_loader)

def test_pipeline():
    video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_video (540p).mp4")
    
    if not os.path.exists(video_path):
        print(f"Error: Sample video not found at {video_path}")
        return

    print(f"Testing pipeline with video: {video_path}")
    print("-" * 50)

    # 1. Test video metadata loading
    print("\n[1/4] Testing Video Metadata Loading...")
    try:
        metadata_json = video_loader.load_video_metadata(video_path)
        print("Success! Metadata:")
        print(metadata_json)
    except Exception as e:
        print(f"Failed to load metadata: {e}")

    # 2. Test frame extraction
    print("\n[2/4] Testing Frame Extraction...")
    try:
        num_frames = extract_frames(video_path)
        print(f"Success! Extracted {num_frames} frames.")
    except Exception as e:
        print(f"Failed to extract frames: {e}")

    # 3. Test audio extraction
    print("\n[3/4] Testing Audio Extraction...")
    try:
        audio_path = extract_audio(video_path)
        if audio_path:
            print(f"Success! Audio extracted to: {audio_path}")
        else:
            print("Failed to extract audio (returned None).")
    except Exception as e:
        print(f"Failed to extract audio: {e}")
        
    # 4. Test scene detection
    print("\n[4/4] Testing Scene Detection...")
    try:
        scenes = detect_scenes(video_path)
        print(f"Success! Detected {len(scenes)} scenes:")
        for i, (start, end) in enumerate(scenes):
            print(f"  Scene {i+1}: {start:.2f}s - {end:.2f}s")
    except Exception as e:
        print(f"Failed to detect scenes: {e}")

    print("\n" + "-" * 50)
    print("Pipeline test completed.")

if __name__ == "__main__":
    test_pipeline()
