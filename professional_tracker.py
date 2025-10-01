"""
Professional Motion Detection and Tracking System
- Color-coded motion intensity (green to yellow to red)
- Accurate blob tracking with filtering
- Clean, professional visualization
"""
import cv2
import numpy as np
import time
from collections import deque


class ProfessionalMotionTracker:
    """Professional motion detection with accurate blob tracking"""
    
    def __init__(self, source=0):
        self.source = source
        self.cap = None
        
        # Background subtractor with optimized settings
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=300,
            varThreshold=30,  # Balanced sensitivity - good detection
            detectShadows=False
        )
        
        # Tracking parameters - optimized for accuracy
        self.min_contour_area = 800  # Balanced minimum - catches medium to large movements
        self.max_contour_area = 50000  # Maximum area
        self.min_movement = 5  # Minimum movement to track
        
        # Tracked objects
        self.tracked_objects = {}
        self.next_id = 0
        self.max_disappeared = 8  # Balanced - keeps objects briefly when motion pauses
        self.max_tracked_objects = 10  # Allow more objects for better tracking
        
        # Motion history for visualization
        self.motion_history = deque(maxlen=10)
        
        # Display settings
        self.show_motion_map = False  # Disabled by default - no yellow heatmap
        self.show_trails = True
        
        # Feature settings
        self.show_terrain_tracking = True
        self.show_datetime = True
        self.show_heat_box = True
        
        # Performance
        self.fps = 0
        self.prev_time = time.time()
        
    def initialize(self):
        """Initialize camera"""
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
        
        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Camera initialized")
        print(f"Resolution: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    
    def create_motion_heatmap(self, motion_mask):
        """Create professional color-coded motion heatmap"""
        # Apply Gaussian blur for smooth visualization
        blurred = cv2.GaussianBlur(motion_mask, (15, 15), 0)
        
        # Create color map: Green (low) -> Yellow (medium) -> Red (high)
        # Convert to 3-channel
        heatmap = cv2.applyColorMap(blurred, cv2.COLORMAP_JET)
        
        # Custom color mapping for professional look
        # Green to Yellow gradient
        colored = np.zeros_like(heatmap)
        
        # Normalize motion mask
        normalized = blurred.astype(float) / 255.0
        
        # Create gradient: Green -> Yellow -> Orange -> Red
        colored[:, :, 0] = (normalized * 0).astype(np.uint8)  # Blue channel (low)
        colored[:, :, 1] = (normalized * 255).astype(np.uint8)  # Green channel (high)
        colored[:, :, 2] = (normalized * 255).astype(np.uint8)  # Red channel (increases with intensity)
        
        return colored
    
    def detect_and_track_blobs(self, frame, motion_mask):
        """Detect and track blobs ONLY when there's active movement"""
        # Morphological operations to clean up mask - improved accuracy
        kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        
        # Remove noise with opening
        cleaned = cv2.morphologyEx(motion_mask, cv2.MORPH_OPEN, kernel_small, iterations=2)
        # Fill gaps with closing
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel_large, iterations=2)
        # Dilate slightly to ensure we capture the full object
        cleaned = cv2.dilate(cleaned, kernel_small, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter and process contours - ONLY ACTIVE MOTION
        valid_blobs = []
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if self.min_contour_area <= area <= self.max_contour_area:
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate centroid
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Check if this region has actual motion (not just static detection)
                    roi = motion_mask[y:y+h, x:x+w]
                    motion_density = np.sum(roi) / (w * h * 255)  # Percentage of motion pixels
                    
                    # Only track if there's decent motion (>25% of the region) - balanced
                    if motion_density > 0.25:
                        valid_blobs.append({
                            'centroid': (cx, cy),
                            'bbox': (x, y, w, h),
                            'area': area,
                            'contour': contour,
                            'motion_density': motion_density
                        })
        
        # Update tracking
        self.update_tracking(valid_blobs)
        
        return valid_blobs
    
    def update_tracking(self, current_blobs):
        """Update object tracking with ID assignment"""
        if len(current_blobs) == 0:
            # Increment disappeared counter for all tracked objects
            for obj_id in list(self.tracked_objects.keys()):
                self.tracked_objects[obj_id]['disappeared'] += 1
                if self.tracked_objects[obj_id]['disappeared'] > self.max_disappeared:
                    del self.tracked_objects[obj_id]
            return
        
        if len(self.tracked_objects) == 0:
            # Register all as new objects
            for blob in current_blobs:
                self.register_object(blob)
            return
        
        # Match current blobs with tracked objects
        tracked_ids = list(self.tracked_objects.keys())
        tracked_centroids = [self.tracked_objects[tid]['centroid'] for tid in tracked_ids]
        current_centroids = [blob['centroid'] for blob in current_blobs]
        
        # Calculate distance matrix
        distances = np.zeros((len(tracked_centroids), len(current_centroids)))
        for i, tc in enumerate(tracked_centroids):
            for j, cc in enumerate(current_centroids):
                distances[i, j] = np.sqrt((tc[0] - cc[0])**2 + (tc[1] - cc[1])**2)
        
        # Match using minimum distance
        matched_tracked = set()
        matched_current = set()
        
        # Sort by distance and match
        for _ in range(min(len(tracked_ids), len(current_blobs))):
            min_dist = float('inf')
            min_i, min_j = -1, -1
            
            for i in range(len(tracked_ids)):
                if i in matched_tracked:
                    continue
                for j in range(len(current_blobs)):
                    if j in matched_current:
                        continue
                    if distances[i, j] < min_dist:
                        min_dist = distances[i, j]
                        min_i, min_j = i, j
            
            # Match if distance is reasonable (within 100 pixels)
            if min_dist < 100:
                obj_id = tracked_ids[min_i]
                self.update_object(obj_id, current_blobs[min_j])
                matched_tracked.add(min_i)
                matched_current.add(min_j)
            else:
                break
        
        # Register unmatched current blobs as new
        for j in range(len(current_blobs)):
            if j not in matched_current:
                self.register_object(current_blobs[j])
        
        # Mark unmatched tracked objects as disappeared
        for i in range(len(tracked_ids)):
            if i not in matched_tracked:
                obj_id = tracked_ids[i]
                self.tracked_objects[obj_id]['disappeared'] += 1
                if self.tracked_objects[obj_id]['disappeared'] > self.max_disappeared:
                    del self.tracked_objects[obj_id]
    
    def register_object(self, blob):
        """Register new tracked object"""
        # Don't register if we've reached max tracked objects
        if len(self.tracked_objects) >= self.max_tracked_objects:
            return
        
        self.tracked_objects[self.next_id] = {
            'centroid': blob['centroid'],
            'bbox': blob['bbox'],
            'area': blob['area'],
            'trail': deque([blob['centroid']], maxlen=20),
            'disappeared': 0,
            'age': 0
        }
        self.next_id += 1
    
    def update_object(self, obj_id, blob):
        """Update existing tracked object"""
        obj = self.tracked_objects[obj_id]
        obj['centroid'] = blob['centroid']
        obj['bbox'] = blob['bbox']
        obj['area'] = blob['area']
        obj['trail'].append(blob['centroid'])
        obj['disappeared'] = 0
        obj['age'] += 1
    
    def draw_professional_overlay(self, frame, motion_heatmap):
        """Draw professional overlay with tracked objects"""
        # Blend motion heatmap with frame
        if self.show_motion_map:
            # Create semi-transparent overlay
            overlay = cv2.addWeighted(frame, 0.7, motion_heatmap, 0.3, 0)
        else:
            overlay = frame.copy()
        
        # Draw tracked objects
        for obj_id, obj in self.tracked_objects.items():
            cx, cy = obj['centroid']
            x, y, w, h = obj['bbox']
            
            # Choose color based on object age (newer = brighter)
            color_intensity = min(255, 150 + obj['age'] * 5)
            color = (255, 255, 255)  # White for all objects
            
            # Draw bounding box
            cv2.rectangle(overlay, (x, y), (x + w, y + h), color, 2)
            
            # Draw centroid
            cv2.circle(overlay, (cx, cy), 6, color, -1)
            cv2.circle(overlay, (cx, cy), 7, (0, 0, 0), 1)
            
            # Draw trail
            if self.show_trails and len(obj['trail']) > 1:
                points = list(obj['trail'])
                for i in range(1, len(points)):
                    # Fade trail
                    alpha = i / len(points)
                    thickness = max(1, int(2 * alpha))
                    cv2.line(overlay, points[i-1], points[i], color, thickness)
            
            # Draw ID and coordinates
            label = f"ID:{obj_id} ({cx},{cy})"
            cv2.putText(overlay, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return overlay
    
    def draw_datetime_box(self, frame):
        """Draw time and date in top-left corner"""
        if not self.show_datetime:
            return
            
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        cv2.rectangle(frame, (10, 10), (250, 60), (0, 0, 0), -1)
        cv2.addWeighted(frame, 0.7, frame, 0.3, 0, frame)
        
        # Current time and date
        from datetime import datetime
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        
        # Draw time and date
        cv2.putText(frame, f"Time: {time_str}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)  # Yellow
        cv2.putText(frame, f"Date: {date_str}", (20, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # White
    
    def draw_terrain_box(self, frame):
        """Draw terrain tracking info in top-right corner"""
        if not self.show_terrain_tracking:
            return
            
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        cv2.rectangle(frame, (w-260, 10), (w-10, 120), (0, 0, 0), -1)
        cv2.addWeighted(frame, 0.7, frame, 0.3, 0, frame)
        
        # Terrain analysis (simplified)
        terrain_info = [
            "Terrain Analysis",
            f"Motion Areas: {len(self.tracked_objects)}",
            f"Avg Movement: {self.calculate_avg_movement():.1f}px",
            f"Activity Level: {self.get_activity_level()}"
        ]
        
        for i, text in enumerate(terrain_info):
            color = (0, 255, 0) if i == 0 else (255, 255, 255)  # Green title, white text
            cv2.putText(frame, text, (w-250, 35 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    def draw_heat_box(self, frame, motion_mask):
        """Draw heat tracking box in bottom-left corner"""
        if not self.show_heat_box:
            return
            
        h, w = frame.shape[:2]
        
        # Create heat visualization
        heat_size = 150
        heat_x, heat_y = 10, h - heat_size - 10
        
        # Semi-transparent background
        cv2.rectangle(frame, (heat_x, heat_y), (heat_x + heat_size, heat_y + heat_size), (0, 0, 0), -1)
        cv2.addWeighted(frame, 0.7, frame, 0.3, 0, frame)
        
        # Create mini heat map
        if motion_mask is not None:
            # Resize motion mask to fit the box
            mini_heat = cv2.resize(motion_mask, (heat_size-20, heat_size-20))
            
            # Apply color map (Blue -> Green -> Red)
            colored_heat = cv2.applyColorMap(mini_heat, cv2.COLORMAP_JET)
            
            # Place in the box
            frame[heat_y+10:heat_y+heat_size-10, heat_x+10:heat_x+heat_size-10] = colored_heat
        
        # Heat box title and info
        cv2.putText(frame, "Heat Tracking", (heat_x + 10, heat_y + 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Blue:Low | Green:Med | Red:High", (heat_x + 10, heat_y + heat_size - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def calculate_avg_movement(self):
        """Calculate average movement of tracked objects"""
        if not self.tracked_objects:
            return 0.0
        
        movements = []
        for obj in self.tracked_objects.values():
            if len(obj['trail']) > 1:
                # Calculate movement distance
                trail = list(obj['trail'])
                movement = np.sqrt((trail[-1][0] - trail[0][0])**2 + (trail[-1][1] - trail[0][1])**2)
                movements.append(movement)
        
        return np.mean(movements) if movements else 0.0
    
    def get_activity_level(self):
        """Get activity level description"""
        avg_movement = self.calculate_avg_movement()
        if avg_movement < 5:
            return "Low"
        elif avg_movement < 15:
            return "Medium"
        else:
            return "High"
    
    def draw_info_panel(self, frame):
        """Draw information panel in bottom-right corner"""
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        cv2.rectangle(frame, (w-200, h-100), (w-10, h-10), (0, 0, 0), -1)
        cv2.addWeighted(frame, 0.7, frame, 0.3, 0, frame)
        
        # Info text
        info = [
            f"FPS: {self.fps:.1f}",
            f"Active Objects: {len(self.tracked_objects)}",
            f"Total Tracked: {self.next_id}",
            f"Motion Map: {'ON' if self.show_motion_map else 'OFF'}",
        ]
        
        for i, text in enumerate(info):
            cv2.putText(frame, text, (w-190, h-70 + i * 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    def run(self):
        """Main loop"""
        self.initialize()
        
        print("\nProfessional Motion Tracker")
        print("Controls:")
        print("  M - Toggle motion heatmap")
        print("  T - Toggle trails")
        print("  R - Reset tracking")
        print("  Q - Quit")
        print("  D - Toggle date/time display")
        print("  E - Toggle terrain tracking")
        print("  H - Toggle heat tracking box")
        print()
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Calculate FPS
            current_time = time.time()
            self.fps = 1 / (current_time - self.prev_time)
            self.prev_time = current_time
            
            # Process frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Get motion mask
            motion_mask = self.bg_subtractor.apply(blurred)
            
            # Threshold
            _, motion_mask = cv2.threshold(motion_mask, 25, 255, cv2.THRESH_BINARY)
            
            # Create professional heatmap
            motion_heatmap = self.create_motion_heatmap(motion_mask)
            
            # Detect and track blobs
            blobs = self.detect_and_track_blobs(frame, motion_mask)
            
            # Draw professional overlay
            output = self.draw_professional_overlay(frame, motion_heatmap)
            
            # Draw feature boxes
            self.draw_datetime_box(output)
            self.draw_terrain_box(output)
            self.draw_heat_box(output, motion_mask)
            
            # Draw info panel
            self.draw_info_panel(output)
            
            # Display
            cv2.imshow('Professional Motion Tracker', output)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                self.show_motion_map = not self.show_motion_map
                print(f"Motion map: {'ON' if self.show_motion_map else 'OFF'}")
            elif key == ord('t'):
                self.show_trails = not self.show_trails
                print(f"Trails: {'ON' if self.show_trails else 'OFF'}")
            elif key == ord('r'):
                self.tracked_objects.clear()
                self.next_id = 0
                print("Tracking reset")
            elif key == ord('d'):
                self.show_datetime = not self.show_datetime
                print(f"Date/Time: {'ON' if self.show_datetime else 'OFF'}")
            elif key == ord('e'):
                self.show_terrain_tracking = not self.show_terrain_tracking
                print(f"Terrain tracking: {'ON' if self.show_terrain_tracking else 'OFF'}")
            elif key == ord('h'):
                self.show_heat_box = not self.show_heat_box
                print(f"Heat box: {'ON' if self.show_heat_box else 'OFF'}")
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = ProfessionalMotionTracker(source=0)
    tracker.run()
