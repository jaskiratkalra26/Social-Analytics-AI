import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# Frames output directory
FRAMES_OUTPUT_DIR = os.path.join(DATA_DIR, "frames")

# Audio output directory
AUDIO_OUTPUT_DIR = os.path.join(DATA_DIR, "audio")

# Audio extraction settings
AUDIO_CODEC = 'pcm_s16le'

# Metadata output directory
METADATA_OUTPUT_DIR = os.path.join(DATA_DIR, "json")

# Scene detection settings
SCENE_THRESHOLD = 30.0
SCENE_DOWNSCALE_FACTOR = 1
SCENE_SHOW_PROGRESS = False

# Target FPS for extraction
TARGET_FPS = 1

# Tesseract OCR path configuration
# Use environment variable TESSERACT_CMD if set, otherwise default to standard installation path
# or leave as None if in PATH
TESSERACT_CMD = os.environ.get('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')

# OCR Analysis Settings
OCR_SAMPLE_RATE = 3         # Process every Nth frame
OCR_HOOK_FRAMES_LIMIT = 5   # Number of initial frames to check for 'Hook' text
OCR_MIN_WORD_LENGTH = 3     # Minimum length for a word to be considered valid
