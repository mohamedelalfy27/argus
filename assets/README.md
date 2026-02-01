# Assets

This folder contains images and media for the README and documentation.

## Files

- `dashboard-preview.png` - Main dashboard screenshot (TODO: add this)
- `demo.gif` - Demo showing Argus in action (TODO: add this)

## How to Create

### Dashboard Screenshot

```bash
# Run the helper script
python scripts/screenshot_helper.py

# Or manually:
# 1. Load demo data: python scripts/load_demo_data.py
# 2. Start dashboard: argus dashboard
# 3. Take screenshot (Cmd+Shift+4 on macOS)
# 4. Save as: assets/dashboard-preview.png
```

### Demo GIF

**Option 1: QuickTime + ezgif.com**
1. Open QuickTime Player
2. File → New Screen Recording
3. Record 15-30 seconds showing:
   - Code with `@watch.agent` decorator
   - Running the script
   - Dashboard updating
4. Export as .mov
5. Convert to GIF: https://ezgif.com/video-to-gif
6. Save as: assets/demo.gif

**Option 2: Kap (recommended)**
```bash
brew install --cask kap
# Then record and export as GIF
```

## Guidelines

- **Screenshot size:** 800x400 to 1200x600 pixels
- **GIF size:** Max 5MB, 10-30 seconds
- **Format:** PNG for screenshots, GIF for demos
- **Theme:** Dark mode preferred
- **Quality:** High resolution (2x for Retina displays)
