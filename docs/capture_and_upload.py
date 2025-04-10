import os
from datetime import datetime
import git
from PIL import ImageGrab
import pygetwindow as gw
import atexit
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

# Clean exit
atexit.register(lambda: print("Clean exit without subprocess warnings."))

# Configuration
REPO_PATH = r"C:\Users\jmyro\Downloads\roblox-live-view"
GITHUB_REPO_URL = "https://github.com/thefiringflame32/roblox-live-view.git"
SCREENSHOT_DIR = os.path.join(REPO_PATH, "docs/images")

def capture_roblox_windows():
    roblox_windows = gw.getWindowsWithTitle("Roblox")  # Adjust title if needed
    screenshots = []
    
    for i, window in enumerate(roblox_windows):
        if window.isActive:
            try:
                # Capture the window
                screenshot = ImageGrab.grab(bbox=(
                    window.left,
                    window.top,
                    window.right,
                    window.bottom
                ))
                screenshot_path = os.path.join(SCREENSHOT_DIR, f"tab_{i}.png")
                screenshot.save(screenshot_path)
                screenshots.append(screenshot_path)
            except Exception as e:
                print(f"Error capturing window {i}: {e}")
    
    return screenshots

def commit_and_push():
    try:
        with git.Repo(REPO_PATH) as repo:
            repo.git.add(all=True)
            repo.index.commit(f"Update screenshots {datetime.now()}")
            origin = repo.remote(name="origin")
            origin.push()
    except Exception as e:
        print(f"Git error: {e}")

if __name__ == "__main__":
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    
    # Capture screenshots and push to GitHub
    capture_roblox_windows()
    commit_and_push()
    print("Screenshots updated!")
