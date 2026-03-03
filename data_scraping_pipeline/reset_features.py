import pandas as pd
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Config

def reset_features():
    csv_path = os.path.join(Config.BASE_DIR, "scraped_data.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # Columns to reset
    feature_columns = [
        "motion_intensity_3s", "face_ratio_3s", "cuts_first3s",
        "hook_audio_intensity", "tempo_bpm",
        "hook_text_ratio"
    ]
    
    count = 0
    for col in feature_columns:
        if col in df.columns:
            # Set all values to NaN (None) to force reprocessing
            df[col] = None
            count += 1
            
    if count > 0:
        df.to_csv(csv_path, index=False)
        print(f"Successfully reset features for {len(df)} videos in {csv_path}")
        print("You can now run 'python hook_pipeline/build_hook_dataset.py' to re-process cleanly.")
    else:
        print("No feature columns found to reset.")

if __name__ == "__main__":
    reset_features()
