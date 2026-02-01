#!/usr/bin/env python3
"""
Helper script to prepare dashboard for screenshot
Loads demo data and starts dashboard
"""

import sys
import os
import subprocess
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("=" * 60)
    print("📸 Argus Screenshot Helper")
    print("=" * 60)
    print()
    
    # Step 1: Load demo data
    print("Step 1/3: Loading demo data...")
    print("-" * 60)
    
    try:
        from scripts.load_demo_data import load_demo_data
        load_demo_data()
    except Exception as e:
        print(f"❌ Error loading demo data: {e}")
        print("Continuing anyway...")
    
    print()
    print("=" * 60)
    print("Step 2/3: Starting dashboard...")
    print("=" * 60)
    print()
    print("🌐 Dashboard will open at: http://localhost:3001")
    print()
    print("=" * 60)
    print("Step 3/3: Take Screenshot")
    print("=" * 60)
    print()
    print("📸 Instructions:")
    print("1. Open http://localhost:3001 in your browser")
    print("2. Wait for data to load (5 seconds)")
    print("3. Take screenshot:")
    print("   macOS: Cmd+Shift+4, then Space, click browser window")
    print("4. Save as: argus/assets/dashboard-preview.png")
    print()
    print("💡 Tips:")
    print("- Use dark mode for better contrast")
    print("- Capture full browser window (not just content)")
    print("- Make sure all data is visible")
    print()
    print("Press Ctrl+C to stop dashboard when done")
    print("=" * 60)
    print()
    
    # Step 2: Start dashboard
    try:
        from argus.cli import main as cli_main
        sys.argv = ["argus", "dashboard"]
        cli_main()
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped. Screenshot saved?")
        print()
        print("Next steps:")
        print("1. Create assets folder: mkdir -p assets")
        print("2. Move screenshot: mv ~/Desktop/screenshot.png assets/dashboard-preview.png")
        print("3. Update README.md (replace placeholder image)")
        print("4. Commit: git add assets/ README.md && git commit -m 'docs: add dashboard screenshot'")
        print("5. Push: git push origin main")
        print()

if __name__ == "__main__":
    main()
