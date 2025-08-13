
"""
Test script for the retail behavior analysis FastAPI
"""

# ubah ke >curl -X POST "http://70.153.9.9:8000/analyze" -F "video=@test_video.mp4" -F "max_duration=30"

import requests
import json
import base64
from PIL import Image
from io import BytesIO

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get("http://70.153.9.9:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_analyze_with_video(video_path):
    """Test analysis endpoint with video generation"""
    print(f"\nTesting analysis with video generation: {video_path}")
    
    with open(video_path, 'rb') as f:
        files = {'video': (video_path, f, 'video/mp4')}
        data = {
            'max_duration': 30,
            'save_to_blob': True,
            'generate_video': True  # Enable video generation
        }
        
        response = requests.post(
            "http://70.153.9.9:8000/analyze",
            files=files,
            data=data
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Analysis ID: {result.get('metadata', {}).get('analysis_id')}")
        print(f"Unique persons: {result.get('unique_persons')}")
        print(f"Total interactions: {result.get('total_interactions')}")
        print(f"Actions detected: {result.get('action_summary', {})}")
        
        # Check download links including annotated video
        download_links = result.get('download_links', {})
        if download_links:
            print("\n📁 Download Links:")
            for file_type, url in download_links.items():
                print(f"  {file_type}: {url}")
                
            # Check if annotated video was generated
            if 'annotated_video' in download_links:
                print("\n🎥 Annotated video generated successfully!")
            else:
                print("\n⚠️  No annotated video found in response")
        else:
            print("\n❌ No download links found!")
            
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_video_only(video_path):
    """Test video generation only endpoint"""
    print(f"\nTesting video generation only: {video_path}")
    
    with open(video_path, 'rb') as f:
        files = {'video': (video_path, f, 'video/mp4')}
        data = {'max_duration': 30}
        
        response = requests.post(
            "http://70.153.9.9:8000/generate-video",
            files=files,
            data=data
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Video generation ID: {result.get('analysis_id')}")
        print(f"Video URL: {result.get('video_url')}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def main():
    """Main test function"""
    print("=== FastAPI Retail Behavior Analysis Test ===\n")
    
    # Test health endpoint
    if not test_health():
        print("Health check failed. Make sure the server is running.")
        return
    
    # Test with a video file - replace with your test video path
    video_path = "e:/Lomba/DATATHON 2025/video/test_video.mp4"  # Update this path
    
    try:
        print("\n" + "="*50)
        print("Testing Full Analysis with Video Generation")
        print("="*50)
        
        if test_analyze_with_video(video_path):
            print("\n✅ Full analysis with video generation passed!")
        else:
            print("\n❌ Full analysis with video generation failed!")
            
        print("\n" + "="*50)
        print("Testing Video Generation Only")
        print("="*50)
        
        if test_video_only(video_path):
            print("\n✅ Video generation only passed!")
        else:
            print("\n❌ Video generation only failed!")
            
    except FileNotFoundError:
        print(f"\n❌ Video file not found: {video_path}")
        print("Please update the video_path variable with a valid video file.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
