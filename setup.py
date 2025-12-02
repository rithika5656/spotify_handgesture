"""
SETUP AND INSTALLATION GUIDE
"""

# INSTALLATION STEPS:
# 1. Create a virtual environment:
#    python -m venv venv
#
# 2. Activate virtual environment:
#    Windows: venv\Scripts\activate
#    Linux/Mac: source venv/bin/activate
#
# 3. Install dependencies:
#    pip install -r requirements.txt
#
# 4. Collect training data:
#    python collect_data.py
#
# 5. Train the model:
#    python train_model.py
#
# 6. Run the real-time gesture control:
#    python main_pipeline.py

import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Requirements installed successfully!")

if __name__ == "__main__":
    import os
    os.system("pip install -r requirements.txt")
