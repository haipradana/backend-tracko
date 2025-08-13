#!/usr/bin/env python3
"""
Startup script for FastAPI Retail Behavior Analysis
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import torch
        import fastapi
        import ultralytics
        import transformers
        import decord
        import supervision
        import shapely
        print("✅ All required packages are available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_models():
    """Check if required model files exist"""
    models_to_check = [
        "models/yolo11s.pt",
        "models/shelf_model/best.pt",
        "models/action_model"
    ]
    
    for model in models_to_check:
        if not os.path.exists(model):
            print(f"❌ Model not found: {model}")
            if "yolo11s.pt" in model:
                print("This will be downloaded automatically on first run")
            elif "shelf_model" in model:
                print("This will be downloaded from HuggingFace on first run")
            elif "action_model" in model:
                print("This will be downloaded from HuggingFace on first run")
        else:
            print(f"✅ Model found: {model}")
    
    return True

def main():
    """Main startup function"""
    print("=== FastAPI Retail Behavior Analysis Startup ===\n")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check models
    check_models()
    
    print("\n🚀 Starting FastAPI server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Start the server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()
