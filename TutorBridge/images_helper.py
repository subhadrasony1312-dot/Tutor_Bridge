import os
import urllib.request
import threading
from tkinter import *

# URLs for background images
WELCOME_BG_URL = "TutorBridge/images/tutor1pic.jpeg"
REG_BG_URL = "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=1200&h=700&fit=crop&fm=png"
LOGO_URL = "https://img.icons8.com/color/96/graduation-cap.png"

# Setup local paths
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, "images")

# Ensure the images directory exists
os.makedirs(images_dir, exist_ok=True)

HAS_PIL = False
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    pass

def download_image_async(url, dest_name, callback=None):
    dest_path = os.path.join(images_dir, dest_name)
    
    # If file already exists, don't download it again
    if os.path.exists(dest_path):
        if callback:
            callback(dest_path)
        return

    def target():
        try:
            urllib.request.urlretrieve(url, dest_path)
            if callback:
                callback(dest_path)
        except Exception as e:
            print(f"Failed to download online image {dest_name}: {e}")
            # Clean up partial/corrupted files
            if os.path.exists(dest_path):
                try:
                    os.remove(dest_path)
                except Exception:
                    pass
            # Run callback with None to trigger fallback
            if callback:
                callback(None)

    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

def load_and_resize(dest_name, width, height):
    filepath = os.path.join(images_dir, dest_name)
    if not os.path.exists(filepath):
        return None
        
    try:
        if HAS_PIL:
            img = Image.open(filepath)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            # Default Tkinter PhotoImage (only works natively with PNG/GIF/etc. - JPG will fail)
            return PhotoImage(file=filepath)
    except Exception as e:
        print(f"Error loading image {dest_name}: {e}")
        return None

def setup_canvas_bg(canvas, dest_name, fallback_color1="#755e52", fallback_color2="#3d200f", width=1200, height=700):
    """
    Sets up a background on a canvas. If the image is locally cached, it displays it.
    Otherwise, it draws a gradient fallback and starts an asynchronous download.
    """
    filepath = os.path.join(images_dir, dest_name)
    
    # Try loading cached image first
    img_ref = load_and_resize(dest_name, width, height)
    if img_ref:
        canvas.create_image(0, 0, image=img_ref, anchor="nw", tags="bg_image")
        # Keep a reference to prevent garbage collection
        canvas.image_ref = img_ref
        return
        
    # Draw gradient fallback
    draw_gradient(canvas, fallback_color1, fallback_color2, width, height)
    
    # Select appropriate URL
    url = WELCOME_BG_URL if dest_name == "background.png" else REG_BG_URL
    if dest_name == "logo.png":
        url = LOGO_URL
        
    # Download asynchronously
    def on_download_complete(downloaded_path):
        if downloaded_path:
            # Load and display newly downloaded image on the main thread loop safely
            canvas.after(100, lambda: apply_new_bg(canvas, dest_name, width, height))
            
    download_image_async(url, dest_name, on_download_complete)

def apply_new_bg(canvas, dest_name, width, height):
    img_ref = load_and_resize(dest_name, width, height)
    if img_ref:
        # Delete old background line objects/shapes and image
        canvas.delete("bg_gradient")
        canvas.delete("bg_image")
        canvas.create_image(0, 0, image=img_ref, anchor="nw", tags="bg_image")
        # Send to back so other widgets stay on top
        canvas.tag_lower("bg_image")
        canvas.image_ref = img_ref

def draw_gradient(canvas, color1, color2, width, height):
    # Parse RGB components
    c1 = canvas.winfo_rgb(color1)
    c2 = canvas.winfo_rgb(color2)
    
    r1, g1, b1 = c1[0] // 256, c1[1] // 256, c1[2] // 256
    r2, g2, b2 = c2[0] // 256, c2[1] // 256, c2[2] // 256
    
    for i in range(height):
        # Linearly interpolate color
        r = int(r1 + (r2 - r1) * (i / height))
        g = int(g1 + (g2 - g1) * (i / height))
        b = int(b1 + (b2 - b1) * (i / height))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color, tags="bg_gradient")
