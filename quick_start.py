"""
QUICK START GUIDE
Simple steps to get the project running
"""

import os
import sys
import subprocess

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def install_dependencies():
    """Install required packages"""
    print_header("Step 1: Installing Dependencies")
    print("This will install all required Python packages...")
    print("(This may take 2-3 minutes)\n")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ Dependencies installed successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Error installing dependencies: {e}")
        return False

def check_camera():
    """Check if camera is available"""
    print_header("Step 2: Checking Camera")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera detected and working!")
            cap.release()
            return True
        else:
            print("✗ Camera not found or not accessible")
            print("Make sure your webcam is connected and enabled")
            return False
    except Exception as e:
        print(f"✗ Error checking camera: {e}")
        return False

def show_next_steps():
    """Show next steps for user"""
    print_header("Next Steps")
    
    print("1️⃣  COLLECT TRAINING DATA:")
    print("   python collect_data.py")
    print("   - You'll collect 50 samples per gesture (5 gestures total)")
    print("   - Total time: ~5-10 minutes\n")
    
    print("2️⃣  TRAIN THE MODEL:")
    print("   python train_model.py")
    print("   - Trains on collected data")
    print("   - Takes ~30 seconds\n")
    
    print("3️⃣  RUN GESTURE CONTROL:")
    print("   python main_pipeline.py")
    print("   - Start controlling volume and media!")
    print("   - Press 'Q' to quit\n")

def main():
    print_header("🎯 GESTURE CONTROL - QUICK START")
    
    print("This script will help you set up the project.\n")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt not found!")
        print("Make sure you're in the project directory.")
        return
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\n⚠️  Installation failed. Please install manually:")
        print("   pip install -r requirements.txt")
        return
    
    # Step 2: Check camera
    if not check_camera():
        print("\n⚠️  Camera check failed. Please connect your webcam.")
        return
    
    # Show next steps
    show_next_steps()
    
    print("="*60)
    print("Setup complete! Follow the steps above to proceed.")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
