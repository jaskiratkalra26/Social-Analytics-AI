import os
import sys
import shutil

# Ensure we can import from the project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import Config
from pipeline.frame_extractor import extract_frames
# We will mock scene_detector if it fails due to missing dependencies, 
# but let's try to import it first. 
try:
    from pipeline.scene_detector import detect_scenes
except ImportError as e:
    print(f"Warning: Could not import scene_detector ({e}). Using dummy scenes.")
    def detect_scenes(video_path):
        return [(0, 5), (5, 10)]

from features.visual_features import extract_visual_features

def test_pipeline():
    video_path = "c:\\Users\\jaski\\OneDrive\\Desktop\\Social Analytics AI\\sample_video (540p).mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: Video not found at {video_path}")
        return

    # Create a temporary output directory for this test
    test_output_dir = os.path.join("data", "test_frames")
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Monkeypatch Config to point to our test directory
    # (Assuming extract_frames uses Config.FRAMES_OUTPUT_DIR)
    original_output_dir = Config.FRAMES_OUTPUT_DIR
    Config.FRAMES_OUTPUT_DIR = test_output_dir
    
    # 1. Extract Frames
    print("Extracting frames...")
    try:
        frameCount = extract_frames(video_path)
        print(f"Extracted {frameCount} frames.")
    except Exception as e:
        print(f"Frame extraction failed: {e}")
        return

    # 2. Detect Scenes
    print("Detecting scenes...")
    try:
        # Check if scenedetect works, otherwise fallback
        scene_list = detect_scenes(video_path)
        print(f"Detected {len(scene_list)} scenes: {scene_list}")
    except Exception as e:
        print(f"Scene detection failed: {e}. Using dummy scenes.")
        scene_list = [(0.0, 1.0), (1.0, 2.0)] # Dummy list

    # 3. Extract Visual Features
    print("Extracting visual features...")
    
    # Import individual functions for granular testing
    from features.visual_features import (
        scene_features, motion_features, quality_features,
        subject_features, composition_features
    )
    
    try:
        print("Running scene_features...")
        sf = scene_features(scene_list)
        print(f" scene_features: {sf}")
        
        print("Running motion_features...")
        mf = motion_features(test_output_dir)
        print(f" motion_features: {mf}")
        
        print("Running quality_features...")
        qf = quality_features(test_output_dir)
        print(f" quality_features: {qf}")
        
        print("Running subject_features...")
        subf = subject_features(test_output_dir)
        print(f" subject_features: {subf}")
        
        print("Running composition_features...")
        cf = composition_features(test_output_dir)
        print(f" composition_features: {cf}")
        
        print("\n--- Visual Features Result ---")
        features = {**sf, **mf, **qf, **subf, **cf}
        for key, value in features.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Visual feature extraction failed: {e}")
        import traceback
        traceback.print_exc()

    # Cleanup (optional)
    # shutil.rmtree(test_output_dir)

if __name__ == "__main__":
    test_pipeline()
