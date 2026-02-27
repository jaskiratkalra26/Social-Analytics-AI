import os
import sys

# Try to import VideoFileClip, handling different MoviePy versions
try:
    from moviepy import VideoFileClip
except ImportError:
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        # For some v2 setups
        from moviepy.video.io.VideoFileClip import VideoFileClip

# Add the project root directory to Python path to import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Config

def extract_audio(video_path):
    """
    Extracts audio from a video file and saves it as a WAV file.
    
    Args:
        video_path (str): The path to the video file.
        
    Returns:
        str: The path to the saved audio file, or None if extraction failed.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None
        
    try:
        # Ensure the output directory exists
        os.makedirs(Config.AUDIO_OUTPUT_DIR, exist_ok=True)
        
        # dynamic audio filename based on video filename
        video_filename = os.path.basename(video_path)
        audio_filename = os.path.splitext(video_filename)[0] + ".wav"
        audio_output_path = os.path.join(Config.AUDIO_OUTPUT_DIR, audio_filename)
        
        # Load the video clip
        video_clip = VideoFileClip(video_path)
        
        # check if video has audio
        if video_clip.audio is None:
            print(f"No audio found in {video_path}")
            video_clip.close()
            return None
            
        # Write the audio to a file
        video_clip.audio.write_audiofile(audio_output_path, codec=Config.AUDIO_CODEC)
        
        # Close the clip to release resources
        video_clip.close()
        
        print(f"Audio extracted to: {audio_output_path}")
        return audio_output_path
        
    except Exception as e:
        print(f"An error occurred during audio extraction: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    # extract_audio("path/to/video.mp4")
    pass
