#!/usr/bin/env python
"""
NexusAI Server Launcher

Run from project root:
    python run.py
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Change to project root directory
import os
os.chdir(Path(__file__).parent)

# Now import and run the server
from main import main

if __name__ == "__main__":
    main()
