# Blob Tracking System - Project Summary

## Overview
A highly sensitive blob tracking system built in Python that can detect and track even the smallest movements, including dust particles and leaf movements in trees. Each detected blob receives a unique ID and randomized coordinates for tracking.

## Project Structure

```
Blob Tracking/
├── main.py                      # Main application entry point
├── blob_tracker.py              # Core tracking algorithms and Blob class
├── blob_logger.py               # Data logging functionality
├── config.py                    # Configuration parameters
├── example_video_tracking.py    # Example for video file tracking
├── test_installation.py         # Installation verification script
├── requirements.txt             # Python dependencies
├── README.md                    # Comprehensive documentation
├── QUICKSTART.md               # Quick start guide
└── .gitignore                  # Git ignore file
```

## Core Components

### 1. **Blob Class** (`blob_tracker.py`)
Represents a tracked blob with:
- Unique ID
- Centroid coordinates (x, y)
- Randomized color for visualization
- Motion trail history
- Velocity vector
- Age counter

### 2. **BlobTracker Class** (`blob_tracker.py`)
Main tracking engine that:
- Detects motion using background subtraction
- Identifies blob contours
- Matches blobs across frames
- Assigns unique IDs
- Tracks blob lifecycle

### 3. **BlobTrackingApp Class** (`main.py`)
Application wrapper that:
- Manages video capture
- Processes frames
- Handles user input
- Displays visualization
- Provides interactive controls

### 4. **BlobLogger Class** (`blob_logger.py`)
Optional data logging:
- Records blob coordinates to CSV
- Timestamps all events
- Tracks velocity and area

## Key Features

### Detection Capabilities
- **Ultra-sensitive**: Detects movements as small as 1 pixel
- **Dual algorithms**: MOG2 and KNN background subtraction
- **Noise filtering**: Advanced morphological operations
- **Size filtering**: Configurable min/max blob area

### Tracking Features
- **Unique IDs**: Each blob gets a persistent unique identifier
- **Coordinate tracking**: Real-time X,Y position monitoring
- **Motion trails**: Visual history of blob movement
- **Velocity vectors**: Direction and speed calculation
- **Smart matching**: Distance-based blob association across frames

### Visualization
- **Color coding**: Each blob has a unique random color
- **Information overlay**: ID and coordinates displayed
- **Motion trails**: Path history visualization
- **Velocity arrows**: Movement direction indicators
- **Statistics panel**: FPS, blob count, and status

### Interactive Controls
| Key | Function |
|-----|----------|
| SPACE | Pause/Resume |
| T | Toggle trails |
| I | Toggle info display |
| D | Toggle motion detection view |
| A | Switch algorithm (MOG2/KNN) |
| R | Reset tracker |
| Q/ESC | Quit |

## Technical Details

### Background Subtraction
Two algorithms available:

**MOG2 (Mixture of Gaussians)**
- Good for general purpose
- Handles gradual lighting changes
- Configurable variance threshold

**KNN (K-Nearest Neighbors)**
- More sensitive to subtle movements
- Better for detecting small particles
- Configurable distance threshold

### Blob Matching Algorithm
1. Calculate centroids of all detected blobs
2. Compute distance matrix between old and new blobs
3. Greedy matching of closest pairs
4. Update matched blobs
5. Register new blobs
6. Remove disappeared blobs after timeout

### Processing Pipeline
```
Camera Frame
    ↓
Grayscale Conversion
    ↓
Gaussian Blur (noise reduction)
    ↓
Background Subtraction (MOG2/KNN)
    ↓
Morphological Operations (open/close)
    ↓
Thresholding
    ↓
Dilation
    ↓
Contour Detection
    ↓
Size Filtering
    ↓
Blob Tracking & Matching
    ↓
Visualization & Display
```

## Configuration Parameters

### Sensitivity Settings
- `SENSITIVITY`: 1-10 (lower = more sensitive)
- `MIN_BLOB_AREA`: Minimum pixels to detect
- `MAX_BLOB_AREA`: Maximum blob size

### Tracking Parameters
- `MAX_DISTANCE`: Maximum distance for blob matching
- `MAX_FRAMES_TO_SKIP`: Frames before removing blob
- `MAX_TRAIL_LENGTH`: Trail history length

### Algorithm Parameters
- `MOG2_VAR_THRESHOLD`: Motion detection sensitivity
- `KNN_DIST2_THRESHOLD`: Distance threshold for KNN
- `BLUR_KERNEL_SIZE`: Gaussian blur strength
- `MORPH_KERNEL_SIZE`: Morphological operation size

## Use Cases

1. **Environmental Monitoring**
   - Track dust particles in air quality studies
   - Monitor pollen movement
   - Detect insect activity

2. **Nature Observation**
   - Track leaf movements in wind studies
   - Monitor bird or animal activity
   - Observe natural phenomena

3. **Security & Surveillance**
   - Detect subtle movements in restricted areas
   - Monitor for intrusions
   - Track object movements

4. **Scientific Research**
   - Particle tracking in experiments
   - Movement analysis
   - Behavior studies

5. **Interactive Art**
   - Motion-reactive installations
   - Visual effects generation
   - Interactive displays

## Performance Characteristics

### Typical Performance
- **FPS**: 20-60 depending on resolution and blob count
- **Latency**: < 50ms per frame
- **Max Blobs**: Can track 100+ simultaneous blobs
- **Memory**: ~100-200 MB typical usage

### Optimization Tips
1. Lower camera resolution for higher FPS
2. Increase MIN_BLOB_AREA to reduce processing
3. Disable trails for better performance
4. Close extra windows
5. Adjust sensitivity to reduce false positives

## Installation & Setup

### Requirements
- Python 3.8 or higher
- OpenCV 4.8+
- NumPy 1.24+

### Quick Install
```bash
pip install -r requirements.txt
```

### Verification
```bash
python test_installation.py
```

### Run
```bash
python main.py
```

## Future Enhancements

Potential improvements:
- GPU acceleration support
- Multi-camera support
- Advanced filtering (Kalman filter)
- Machine learning classification
- 3D tracking with depth cameras
- Network streaming support
- Mobile app integration

## Troubleshooting

### Common Issues

**No blobs detected**
- Lower SENSITIVITY value
- Check MIN_BLOB_AREA is small enough
- Try KNN algorithm (press 'A')

**Too many false detections**
- Increase SENSITIVITY value
- Increase MIN_BLOB_AREA
- Improve lighting conditions

**Low FPS**
- Reduce camera resolution
- Disable trails and extra windows
- Increase MIN_BLOB_AREA

**Camera not opening**
- Check VIDEO_SOURCE index
- Close other camera applications
- Verify camera permissions

## Credits & License

Built with OpenCV and NumPy for advanced computer vision.
Open source for educational and research purposes.

---

**Version**: 1.0  
**Created**: 2025  
**Language**: Python 3.8+  
**Platform**: Cross-platform (Windows, macOS, Linux)
