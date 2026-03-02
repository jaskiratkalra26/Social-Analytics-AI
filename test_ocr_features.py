import cv2
import os
import shutil
import sys
# Add features to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'features'))

from features.text_features import extract_text_features

def test_ocr_on_video(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join("data", "frames", video_name)
    
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Extracting frames from {video_path} to {output_folder}...")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Extract every frame for the test, let text_features handle the sampling (it samples every 3rd)
        # But to be safe and efficient for a test, we can just dump all frames.
        frame_filename = f"frame_{frame_count:04d}.jpg"
        cv2.imwrite(os.path.join(output_folder, frame_filename), frame)
        saved_count += 1
        frame_count += 1
        
    cap.release()
    print(f"Extracted {saved_count} frames.")
    
    print("Running Text Features Extraction...")
    try:
        features = extract_text_features(output_folder, verbose=True)
        print("\n--- OCR Features ---")
        for key, value in features.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    # Adjust path if needed
    video_path = "Video_for_OCR_Model_Testing.mp4"
    if not os.path.exists(video_path):
        # try full path
        video_path = os.path.join(os.getcwd(), "Video_for_OCR_Model_Testing.mp4")
        
    if os.path.exists(video_path):
        test_ocr_on_video(video_path)
    else:
        print(f"Video file not found: {video_path}")
