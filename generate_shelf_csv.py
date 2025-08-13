"""
Script to generate shelf interaction CSV similar to Gradio pipeline
For debugging and comparison purposes
"""

import pandas as pd
from collections import defaultdict
import numpy as np
import os
from datetime import datetime

def generate_shelf_interaction_csv(tracks, shelf_boxes_per_frame, video_width, video_height, output_dir="shelf_analysis"):
    """
    Generate shelf interaction CSV using the same logic as Gradio pipeline
    
    Args:
        tracks: Dictionary of person tracks
        shelf_boxes_per_frame: Dictionary of shelf boxes per frame
        video_width: Video width in pixels
        video_height: Video height in pixels  
        output_dir: Output directory for CSV files
    
    Returns:
        Dictionary with shelf interaction data
    """
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate Shelf Interactions (same as Gradio)
    shelf_interaksi = defaultdict(int)
    
    print(f"Processing {len(tracks)} person tracks...")
    
    for pid, dets in tracks.items():
        print(f"Processing person {pid} with {len(dets)} detections...")
        
        for d in dets:
            f = d['frame']
            x1, y1, x2, y2 = d['bbox']
            cx, cy = (x1+x2)/2, (y1+y2)/2
            
            # First try to match with detected shelves
            found_shelf = False
            for sid, (sx1, sy1, sx2, sy2) in shelf_boxes_per_frame.get(f, []):
                if sx1 <= cx <= sx2 and sy1 <= cy <= sy2:
                    shelf_interaksi[sid] += 1
                    found_shelf = True
                    break
            
            # If no shelf detected, create spatial grid-based shelf ID (like Gradio fallback)
            if not found_shelf:
                grid_x = int(cx // (video_width // 5))  # Divide width into 5 regions
                grid_y = int(cy // (video_height // 4))  # Divide height into 4 regions
                grid_x = min(max(grid_x, 0), 4)  # Ensure within bounds
                grid_y = min(max(grid_y, 0), 3)  # Ensure within bounds
                shelf_id = f"shelf_{grid_x}_{grid_y}"
                shelf_interaksi[shelf_id] += 1
    
    print(f"Found {len(shelf_interaksi)} unique shelves:")
    for shelf_id, count in sorted(shelf_interaksi.items(), key=lambda x: -x[1]):
        print(f"  {shelf_id}: {count} interactions")
    
    # Save interaction summary (same format as Gradio)
    shelf_df = pd.DataFrame(list(shelf_interaksi.items()),
                           columns=['shelf_id', 'interaksi'])
    
    # Save to CSV
    csv_path = os.path.join(output_dir, 'rak_interaksi.csv')
    shelf_df.to_csv(csv_path, index=False)
    print(f"Saved shelf interactions to: {csv_path}")
    
    # Save sorted by interaction count (like Gradio rekomendasi_layout.csv)
    layout_recommendations = pd.DataFrame(sorted(shelf_interaksi.items(),
                                                 key=lambda x: -x[1]),
                                         columns=['shelf_id', 'interaksi'])
    
    layout_path = os.path.join(output_dir, 'rekomendasi_layout.csv')
    layout_recommendations.to_csv(layout_path, index=False)
    print(f"Saved layout recommendations to: {layout_path}")
    
    # Create summary report
    summary_data = {
        'timestamp': datetime.now().isoformat(),
        'total_shelves': len(shelf_interaksi),
        'total_interactions': sum(shelf_interaksi.values()),
        'video_dimensions': f"{video_width}x{video_height}",
        'top_shelf': max(shelf_interaksi.items(), key=lambda x: x[1]) if shelf_interaksi else None,
        'shelf_distribution': dict(shelf_interaksi)
    }
    
    summary_path = os.path.join(output_dir, 'analysis_summary.txt')
    with open(summary_path, 'w') as f:
        f.write("=== Shelf Interaction Analysis Summary ===\n\n")
        f.write(f"Analysis Time: {summary_data['timestamp']}\n")
        f.write(f"Total Shelves Detected: {summary_data['total_shelves']}\n")
        f.write(f"Total Interactions: {summary_data['total_interactions']}\n")
        f.write(f"Video Dimensions: {summary_data['video_dimensions']}\n\n")
        
        if summary_data['top_shelf']:
            f.write(f"Most Active Shelf: {summary_data['top_shelf'][0]} ({summary_data['top_shelf'][1]} interactions)\n\n")
        
        f.write("Shelf Distribution:\n")
        for shelf_id, count in sorted(shelf_interaksi.items(), key=lambda x: -x[1]):
            percentage = (count / sum(shelf_interaksi.values())) * 100
            f.write(f"  {shelf_id}: {count} interactions ({percentage:.1f}%)\n")
    
    print(f"Saved analysis summary to: {summary_path}")
    
    return {
        'shelf_interactions': dict(shelf_interaksi),
        'csv_path': csv_path,
        'layout_path': layout_path,
        'summary_path': summary_path,
        'summary_data': summary_data
    }

if __name__ == "__main__":
    # Test with dummy data
    print("Testing shelf interaction CSV generation...")
    
    # Dummy tracks data
    tracks = {
        1: [
            {'frame': 0, 'bbox': [100, 100, 200, 300], 'pid': 1},
            {'frame': 1, 'bbox': [110, 105, 210, 305], 'pid': 1},
            {'frame': 2, 'bbox': [120, 110, 220, 310], 'pid': 1},
        ],
        2: [
            {'frame': 0, 'bbox': [500, 200, 600, 400], 'pid': 2},
            {'frame': 1, 'bbox': [510, 205, 610, 405], 'pid': 2},
        ]
    }
    
    # Dummy shelf boxes
    shelf_boxes_per_frame = {
        0: [('shelf_A', (50, 50, 250, 350))],
        1: [('shelf_A', (50, 50, 250, 350))],
        2: [('shelf_A', (50, 50, 250, 350))],
    }
    
    result = generate_shelf_interaction_csv(
        tracks=tracks,
        shelf_boxes_per_frame=shelf_boxes_per_frame,
        video_width=1920,
        video_height=1080,
        output_dir="test_output"
    )
    
    print("\nTest completed successfully!")
    print(f"Generated files in: test_output/")
