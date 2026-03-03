import pandas as pd
import os
import sys
import shutil
import subprocess
import glob

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Config
from pipeline.frame_extractor import extract_frames
from pipeline.audio_extractor import extract_audio
from pipeline.scene_detector import detect_scenes
from features.visual_features import extract_visual_features, get_sorted_frame_paths
from features.audio_features import extract_audio_features
from features.text_features import extract_text_features

import imageio_ffmpeg

def download_video(video_id, output_dir="data/videos"):
    """
    Downloads a YouTube video using yt-dlp.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    video_path = os.path.join(output_dir, f"{video_id}.mp4")
    
    # Return existing if already downloaded (though we usually delete it)
    if os.path.exists(video_path):
        return video_path

    url = f"https://youtube.com/watch?v={video_id}"
    
    # get ffmpeg path from imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    # yt-dlp command
    # -f mp4: Format
    # -o ...: Output template
    # --download-sections "*0-3": Download only the first 3 seconds
    # --force-keyframes-at-cuts: Re-encode to ensure we get exactly 0-3s (optional, but good for short clips)
    # --ffmpeg-location: Use the ffmpeg binary from imageio-ffmpeg
    command = [
        "yt-dlp",
        "-f", "mp4",
        "--download-sections", "*0-3",
        "--force-keyframes-at-cuts",
        "--ffmpeg-location", ffmpeg_path,
        "-o", os.path.join(output_dir, "%(id)s.mp4"),
        url
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(video_path):
            return video_path
        else:
            print(f"Failed to download video {video_id}: File not found after download.")
            return None
    except subprocess.CalledProcessError:
        print(f"Failed to download video {video_id}: yt-dlp error.")
        return None
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install it with 'pip install yt-dlp'.")
        return None

def main():
    csv_path = os.path.join(Config.BASE_DIR, "combined_final_data.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # Create columns if they don't exist
    new_columns = [
        "motion_intensity_3s", "face_ratio_3s", "cuts_first3s",
        "hook_audio_intensity", "tempo_bpm",
        "hook_text_ratio"
    ]
    
    for col in new_columns:
        if col not in df.columns:
            df[col] = None

    print(f"Starting hook extraction pipeline for {len(df)} videos...")

    processed_count = 0
    
    for i, row in df.iterrows():
        video_id = row["video_id"]
        
        # STEP 2 — SKIP PROCESSED ROWS
        if "motion_intensity_3s" in df.columns and pd.notna(df.loc[i, "motion_intensity_3s"]):
            # print(f"Skipping {video_id} (already processed)")
            continue
            
        print(f"Processing {video_id} ({processed_count + 1})...")
        
        # STEP 3 — DOWNLOAD VIDEO
        video_path = download_video(video_id)
        if not video_path:
            continue
            
        frames_folder = None
        audio_path = None
        
        try:
            # STEP 4 — EXTRACT FIRST 3 SECONDS FRAMES
            # Note: extract_frames now returns the folder path and accepts duration
            frames_folder = extract_frames(
                video_path,
                fps_sampling=1,
                duration=3
            )
            
            # STEP 5 — EXTRACT FIRST 3 SECONDS AUDIO
            # Note: extract_audio now accepts duration
            audio_path = extract_audio(
                video_path,
                duration=3
            )
            
            # Additional step: Detect scenes for the first 3 seconds
            all_scenes = detect_scenes(video_path)
            # Filter scenes that start within first 3 seconds
            scenes_3s = [s for s in all_scenes if s[0] < 3.0]
            # Clamp end time to 3.0
            scenes_3s = [(s[0], min(s[1], 3.0)) for s in scenes_3s]
            
            # STEP 6 — EXTRACT VISUAL FEATURES
            visual_features = extract_visual_features(
                frames_folder,
                scene_list=scenes_3s
            )
            
            motion_intensity_3s = visual_features.get("motion_intensity", 0.0)
            face_ratio_3s = visual_features.get("face_ratio", 0.0)
            cuts_first3s = visual_features.get("cut_frequency", 0.0)

            # STEP 7 — EXTRACT AUDIO FEATURES
            if audio_path:
                audio_features = extract_audio_features(audio_path)
            else:
                audio_features = {}
            
            hook_audio_intensity = audio_features.get("hook_audio_intensity", 0.0)
            tempo_bpm = audio_features.get("tempo_bpm", 0.0)

            # STEP 8 — EXTRACT TEXT FEATURES
            text_features = extract_text_features(frames_folder)
            
            hook_text_ratio = text_features.get("hook_text_ratio", 0.0)

            # STEP 9 — SAVE FEATURES INTO DATASET
            df.loc[i, "motion_intensity_3s"] = motion_intensity_3s
            df.loc[i, "face_ratio_3s"] = face_ratio_3s
            df.loc[i, "cuts_first3s"] = cuts_first3s
            df.loc[i, "hook_audio_intensity"] = hook_audio_intensity
            df.loc[i, "tempo_bpm"] = tempo_bpm
            df.loc[i, "hook_text_ratio"] = hook_text_ratio
            
            # Save CSV after each video
            df.to_csv(csv_path, index=False)
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {video_id}: {e}")
            continue
            
        finally:
            # STEP 10 — DELETE FILES
            # Delete video file
            if video_path and os.path.exists(video_path):
                try:
                    os.remove(video_path)
                except OSError as e:
                    print(f"Error removing video file {video_path}: {e}")
            
            # Delete frames folder
            if frames_folder and os.path.exists(frames_folder):
                try:
                    shutil.rmtree(frames_folder)
                except OSError as e:
                    print(f"Error removing frames folder {frames_folder}: {e}")
            
            # Delete audio file
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except OSError as e:
                    print(f"Error removing audio file {audio_path}: {e}")

    print("Pipeline complete.")

if __name__ == "__main__":
    main()
