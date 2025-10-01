# Quick Start Guide

## Installation

1. **Install Python** (3.8 or higher)
   - Download from [python.org](https://www.python.org/downloads/)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Webcam Tracking (Default)
```bash
python main.py
```

### Option 2: Video File Tracking
Edit `main.py` line 233:
```python
VIDEO_SOURCE = "your_video.mp4"
```
Then run:
```bash
python main.py
```

## First Time Setup

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Wait for camera initialization** (a few seconds)

3. **You should see two windows**:
   - **Blob Tracking**: Main window with colored blobs
   - **Motion Detection**: Heat map of detected motion

4. **Move something in front of the camera** to see blobs appear!

## Understanding the Display

### What You'll See:
- **Colored outlines**: Each blob has a unique color
- **Dots**: Center point of each blob
- **Lines**: Motion trails showing where blobs moved
- **Yellow arrows**: Direction and speed of movement
- **Text labels**: "ID:X (x,y)" showing blob ID and coordinates

### Info Panel (Top-Left):
- **FPS**: Frames per second
- **Active Blobs**: Currently tracked blobs
- **Total Tracked**: All blobs detected since start
- **Algorithm**: MOG2 or KNN
- **Status**: Running or Paused

## Quick Controls

| Key | What It Does |
|-----|--------------|
| **SPACE** | Pause/Resume |
| **Q** | Quit |
| **T** | Show/hide trails |
| **D** | Show/hide motion detection window |
| **A** | Switch detection algorithm |

## Adjusting Sensitivity

### For Dust Particles / Very Small Movements:
Edit `main.py` lines 235-237:
```python
SENSITIVITY = 1      # Ultra sensitive
MIN_BLOB_AREA = 1    # Detect 1-pixel movements
MAX_BLOB_AREA = 500  # Only small objects
```

### For Leaf Movements / Medium Objects:
```python
SENSITIVITY = 3      # Medium sensitivity
MIN_BLOB_AREA = 5    # Ignore very tiny noise
MAX_BLOB_AREA = 2000 # Medium-sized objects
```

### For Large Objects Only:
```python
SENSITIVITY = 7      # Less sensitive
MIN_BLOB_AREA = 50   # Larger minimum size
MAX_BLOB_AREA = 10000 # Large objects
```

## Common Issues

### "Camera not opening"
- Make sure no other app is using the camera
- Try changing `VIDEO_SOURCE = 1` or `VIDEO_SOURCE = 2`

### "Too many false detections"
- Increase `SENSITIVITY` (e.g., from 3 to 5)
- Increase `MIN_BLOB_AREA` (e.g., from 1 to 10)
- Ensure stable lighting and camera position

### "Not detecting small movements"
- Decrease `SENSITIVITY` (e.g., from 3 to 1)
- Set `MIN_BLOB_AREA = 1`
- Press 'A' to switch to KNN algorithm (more sensitive)

### "Low FPS / Laggy"
- Close the Motion Detection window (press 'D')
- Turn off trails (press 'T')
- Reduce camera resolution in `main.py` line 56-57

## Testing the System

### Test 1: Hand Movement
- Wave your hand in front of the camera
- You should see blobs tracking your hand with trails

### Test 2: Small Objects
- Drop small pieces of paper or dust
- Blobs should track even tiny particles

### Test 3: Multiple Objects
- Move multiple objects simultaneously
- Each should get a unique ID and color

## Next Steps

1. **Experiment with controls** - Try all the keyboard shortcuts
2. **Adjust sensitivity** - Find the right settings for your use case
3. **Try video files** - Track movements in recorded videos
4. **Read README.md** - Learn about advanced features

## Need Help?

Check the full **README.md** for:
- Detailed parameter explanations
- Advanced configuration
- Troubleshooting guide
- Technical details

---

**Enjoy tracking! 🎯**
