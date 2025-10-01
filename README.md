# Advanced Blob Tracking System

A highly sensitive blob tracking system in Python that can detect and track even the smallest movements, including dust particles and leaf movements in trees.

## Features

- **Ultra-Sensitive Detection**: Detects movements as small as 1 pixel
- **Unique ID Assignment**: Each blob gets a unique ID and randomized color
- **Real-time Coordinate Tracking**: Tracks X,Y coordinates for every blob
- **Motion Trails**: Visual trails showing blob movement history
- **Velocity Vectors**: Shows direction and speed of movement
- **Dual Algorithm Support**: Switch between MOG2 and KNN background subtraction
- **Interactive Controls**: Real-time parameter adjustment

## How It Works

### Blob Detection
1. **Background Subtraction**: Uses advanced algorithms (MOG2/KNN) to separate moving objects from static background
2. **Noise Reduction**: Applies Gaussian blur and morphological operations to filter out camera noise
3. **Contour Detection**: Identifies distinct blobs in the motion mask
4. **Size Filtering**: Filters blobs by area (1-5000 pixels by default)

### Blob Tracking
1. **Centroid Calculation**: Computes the center point of each blob
2. **Distance Matching**: Matches blobs across frames using Euclidean distance
3. **ID Assignment**: Assigns unique IDs to new blobs and maintains them across frames
4. **Coordinate Tracking**: Records and displays X,Y coordinates for each blob
5. **Trail Recording**: Maintains a history of positions for visualization

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python main.py
```

### Using a Video File
Edit `main.py` and change:
```python
VIDEO_SOURCE = "path/to/your/video.mp4"
```

### Adjusting Sensitivity
Edit the configuration in `main.py`:
```python
SENSITIVITY = 3      # Lower = more sensitive (1-10)
MIN_BLOB_AREA = 1    # Minimum pixels to detect
MAX_BLOB_AREA = 5000 # Maximum blob size
```

## Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume tracking |
| **T** | Toggle motion trails |
| **I** | Toggle blob information display |
| **D** | Toggle motion detection view |
| **A** | Switch between MOG2 and KNN algorithms |
| **R** | Reset tracker (clear all blobs) |
| **Q/ESC** | Quit application |

## Display Information

### Main Window
- **Colored Contours**: Each blob has a unique color
- **Centroid Dots**: Center point of each blob
- **Motion Trails**: Path history of blob movement
- **ID & Coordinates**: Shows "ID:X (x,y)" for each blob
- **Velocity Vectors**: Yellow arrows showing movement direction

### Statistics Panel
- **FPS**: Current frames per second
- **Active Blobs**: Number of currently tracked blobs
- **Total Tracked**: Total number of blobs detected since start
- **Algorithm**: Current background subtraction method
- **Status**: Running or paused

### Motion Detection Window
- Heat map visualization of detected motion
- Red areas indicate high motion
- Blue areas indicate low motion

## Configuration Parameters

### BlobTracker Parameters
- `sensitivity`: Motion detection threshold (1-10, lower = more sensitive)
- `min_blob_area`: Minimum blob size in pixels (default: 1)
- `max_blob_area`: Maximum blob size in pixels (default: 5000)
- `max_distance`: Maximum distance to match blobs across frames (default: 50)
- `max_frames_to_skip`: Frames before removing disappeared blob (default: 10)

### Background Subtractor Parameters
- **MOG2**: Good for general purpose, handles gradual lighting changes
  - `history`: Number of frames for background model (500)
  - `varThreshold`: Threshold for pixel-model match (8 for high sensitivity)
  
- **KNN**: More sensitive, better for subtle movements
  - `history`: Number of frames for background model (500)
  - `dist2Threshold`: Threshold for pixel-model match (200.0)

## Use Cases

1. **Environmental Monitoring**: Track dust particles, pollen, or insects
2. **Nature Observation**: Monitor leaf movements, bird activity
3. **Security**: Detect subtle movements in surveillance footage
4. **Scientific Research**: Track particle movements in experiments
5. **Art Installations**: Create interactive visual experiences

## Technical Details

### Blob Class
Each blob contains:
- `id`: Unique identifier
- `centroid`: (x, y) coordinates
- `contour`: OpenCV contour data
- `color`: Randomized RGB color
- `trail`: List of previous positions
- `velocity`: (vx, vy) velocity vector
- `age`: Number of frames tracked

### Tracking Algorithm
Uses a simplified Hungarian algorithm approach:
1. Calculate distance matrix between existing and new blobs
2. Greedily match closest pairs within max_distance threshold
3. Update matched blobs with new positions
4. Register unmatched detections as new blobs
5. Remove blobs that haven't been seen for max_frames_to_skip

## Performance Tips

1. **Reduce Resolution**: Lower camera resolution for better FPS
2. **Adjust Sensitivity**: Higher sensitivity = more processing
3. **Limit Blob Count**: Adjust min/max area to filter unwanted detections
4. **Disable Trails**: Turn off trails for better performance
5. **Close Extra Windows**: Only show main window if FPS is low

## Troubleshooting

### No Blobs Detected
- Increase sensitivity (lower the SENSITIVITY value)
- Check MIN_BLOB_AREA is small enough
- Try switching algorithms (press 'A')
- Ensure there's actual movement in the scene

### Too Many False Detections
- Decrease sensitivity (higher SENSITIVITY value)
- Increase MIN_BLOB_AREA
- Reduce camera noise (better lighting, stable camera)

### Low FPS
- Reduce camera resolution
- Disable trails and extra windows
- Increase MIN_BLOB_AREA to reduce blob count

### Camera Not Opening
- Check VIDEO_SOURCE is correct (0 for default webcam)
- Ensure no other application is using the camera
- Try different camera indices (0, 1, 2, etc.)

## License

This project is open source and available for educational and research purposes.

## Credits

Built with OpenCV and NumPy for advanced computer vision and blob tracking.
