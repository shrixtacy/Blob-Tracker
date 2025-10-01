# Visual Guide - Understanding the Blob Tracker Display

## Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│  [Statistics Panel - Top Left]                              │
│  ┌──────────────────────────┐                               │
│  │ FPS: 30.5                │                               │
│  │ Active Blobs: 5          │                               │
│  │ Total Tracked: 23        │                               │
│  │ Algorithm: MOG2          │                               │
│  │ Status: RUNNING          │                               │
│  └──────────────────────────┘                               │
│                                                              │
│                    [Tracked Blobs]                          │
│                                                              │
│         ●────────────●  ID:3 (450,230)                      │
│        ╱              ╲                                      │
│       ●                ●                                     │
│      ╱                  ╲                                    │
│     ●                    ●──→ [Velocity Arrow]              │
│                                                              │
│                  ●  ID:7 (620,180)                          │
│                 ╱│╲                                          │
│                ● │ ●                                         │
│                  │                                           │
│                  ●  [Trail showing movement]                │
│                                                              │
│  [Controls - Bottom Left]                                   │
│  Controls:                                                  │
│  SPACE - Pause/Resume                                       │
│  T - Toggle Trails                                          │
│  I - Toggle Info                                            │
│  D - Toggle Diff View                                       │
│  A - Switch Algorithm                                       │
│  R - Reset Tracker                                          │
│  Q/ESC - Quit                                               │
└─────────────────────────────────────────────────────────────┘
```

## Motion Detection Window

```
┌─────────────────────────────────────────────────────────────┐
│                   Motion Detection View                      │
│                                                              │
│  [Heat Map Visualization]                                   │
│                                                              │
│     🔴 Red = High Motion                                    │
│     🟡 Yellow = Medium Motion                               │
│     🔵 Blue = Low Motion                                    │
│     ⚫ Black = No Motion                                    │
│                                                              │
│  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Blob Visualization Elements

### 1. Blob Contour
```
    ╭─────────╮
   ╱           ╲
  │             │  ← Colored outline (unique per blob)
   ╲           ╱
    ╰─────────╯
```

### 2. Centroid Point
```
    ╭─────────╮
   ╱           ╲
  │      ●      │  ← Center point (4px circle)
   ╲           ╱
    ╰─────────╯
```

### 3. Motion Trail
```
         ●  ← Current position
        ╱
       ●
      ╱
     ●
    ╱
   ●  ← Previous positions
  ╱
 ●  ← Oldest position (fades away)
```

### 4. Velocity Vector
```
         ●────────→  ← Yellow arrow showing direction
                      Length = speed
```

### 5. Information Label
```
    ╭─────────╮
   ╱           ╲
  │      ●      │  ID:42 (325,180)
   ╲           ╱     ↑    ↑
    ╰─────────╯      │    └─ X,Y coordinates
                     └─ Unique blob ID
```

## Color Coding

Each blob gets a **random unique color** when first detected:

```
Blob #1: 🔴 Red
Blob #2: 🟢 Green  
Blob #3: 🔵 Blue
Blob #4: 🟡 Yellow
Blob #5: 🟣 Purple
Blob #6: 🟠 Orange
... and so on
```

The color **stays the same** as long as the blob is tracked!

## What You'll See in Action

### Scenario 1: Dust Particles
```
Small dots moving randomly:
  ●  ●    ●
    ●  ●     ●
  ●    ●  ●
```

### Scenario 2: Leaf Movement
```
Larger blobs swaying:
    ╭──╮
   ╱    ╲
  │  ●   │ ←→ [swaying motion]
   ╲    ╱
    ╰──╯
```

### Scenario 3: Hand Waving
```
Large blob with long trail:
              ╭────╮
             ╱      ╲
            │   ●    │ ←─────────────
             ╲      ╱               ╲
              ╰────╯                 ╲
                                      ╲
                                       ● [trail]
```

## Statistics Panel Explained

```
┌──────────────────────────┐
│ FPS: 30.5                │ ← Frames per second (performance)
│ Active Blobs: 5          │ ← Currently visible blobs
│ Total Tracked: 23        │ ← All blobs since start
│ Algorithm: MOG2          │ ← Detection method
│ Status: RUNNING          │ ← Current state
└──────────────────────────┘
```

### FPS Indicator
- **30+ FPS**: Excellent performance ✓
- **20-30 FPS**: Good performance
- **10-20 FPS**: Acceptable
- **< 10 FPS**: Poor (reduce resolution or blob count)

### Active Blobs
- Number of blobs currently being tracked
- Updates in real-time as blobs appear/disappear

### Total Tracked
- Cumulative count since application start
- Never decreases (only resets with 'R' key)

## Motion Detection Heat Map

The heat map shows **where motion is detected**:

```
Intensity Scale:
████ = Maximum motion (255)
███░ = High motion (200)
██░░ = Medium motion (150)
█░░░ = Low motion (100)
░░░░ = No motion (0)
```

### Reading the Heat Map
- **Bright areas**: Active movement detected
- **Dark areas**: Static/no movement
- **Changing patterns**: Real-time motion updates

## Blob Lifecycle

```
1. BIRTH (New Detection)
   ● New blob appears
   ↓
   Assigned unique ID and color
   
2. TRACKING (Active)
   ●────●────●────● Trail builds up
   ↓
   Position and velocity updated each frame
   
3. DISAPPEARANCE (Temporary)
   ● Blob not detected for a few frames
   ↓
   Kept in memory (up to 10 frames)
   
4. DEATH (Removed)
   ✗ Not seen for 10+ frames
   ↓
   Removed from tracking
```

## Coordinate System

```
(0,0) ─────────────────────→ X
  │
  │    ●(100,50)
  │
  │         ●(300,200)
  │
  │                  ●(500,400)
  │
  ↓
  Y

Origin: Top-left corner
X-axis: Left to right (0 to width)
Y-axis: Top to bottom (0 to height)
```

## Tips for Best Visualization

1. **Good Lighting**: Even, consistent lighting works best
2. **Stable Camera**: Mount camera to avoid false detections
3. **Contrasting Background**: Plain backgrounds work better
4. **Appropriate Distance**: Not too close, not too far
5. **Clean Lens**: Ensure camera lens is clean

## Troubleshooting Visual Issues

### Problem: Can't see blobs
**Solution**: 
- Check if motion is actually happening
- Lower sensitivity (SENSITIVITY = 1)
- Press 'A' to switch algorithm

### Problem: Too many blobs everywhere
**Solution**:
- Increase MIN_BLOB_AREA
- Increase SENSITIVITY value
- Stabilize camera and lighting

### Problem: Trails are messy
**Solution**:
- Press 'T' to toggle trails off
- Reduce MAX_TRAIL_LENGTH in config

### Problem: Info text overlapping
**Solution**:
- Press 'I' to toggle info off
- Increase MIN_BLOB_AREA to reduce blob count

---

**Now you're ready to interpret everything you see! 🎯**
