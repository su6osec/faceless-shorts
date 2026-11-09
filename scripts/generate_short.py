#!/usr/bin/env python3
"""
Standalone execution helper for generating a single short video.
Usage: python scripts/generate_short.py --topic "Marcus Aurelius Stoic Mindset"
"""

import sys
import os

# Ensure package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from faceless_shorts.cli import main

if __name__ == "__main__":
    main()
