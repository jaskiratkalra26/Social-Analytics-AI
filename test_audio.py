import os
import sys

# Ensure the project root is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.audio_extractor import extract_audio
from features.audio_features import extract_audio_features

def main():
    video_path = "sample_video (540p).mp4"
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return

    print(f"Extracting audio from {video_path}...")
    audio_path = extract_audio(video_path)
    
    if audio_path:
        print(f"Audio extracted to: {audio_path}")
        print("Calculating audio features...")
        features = extract_audio_features(audio_path)
        
        print("\n--- Audio Features ---")
        for key, value in features.items():
            print(f"{key}: {value}")
    else:
        print("Failed to extract audio.")

if __name__ == "__main__":
    main()
