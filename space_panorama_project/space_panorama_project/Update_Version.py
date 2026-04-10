import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button
from PIL import Image, ImageTk
import os

# Theme colors
BG_COLOR = "#1e1e2f"           # Dark background
BTN_COLOR = "#4caf50"          # Green button
BTN_TEXT_COLOR = "#ffffff"     # White button text
TEXT_COLOR = "#e0e0e0"         # Light gray text

# Image stitching function
def stitch_images(image_paths):
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            continue
        images.append(img)

    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        return stitched
    else:
        return None

# Select and process images
def select_images():
    filez = filedialog.askopenfilenames(
        title='Select Space Images',
        filetypes=[('Image files', '*.jpg *.jpeg *.png *.bmp')]
    )

    if len(filez) < 6:
        messagebox.showerror("Error", "Select at least six images.")
        return

    # Show status
    status_label.config(text="Please wait, stitching images...")
    root.update()

    result = stitch_images(filez)

    # Hide status
    status_label.config(text="")

    if result is not None:
        result_path = "panorama_result.jpg"
        cv2.imwrite(result_path, result)
        show_result(result_path)
    else:
        messagebox.showerror(
            "Error",
            "Failed to stitch images. The algorithm may need more images with better overlap or quality."
        )

# Show stitched image
def show_result(img_path):
    top = tk.Toplevel(bg=BG_COLOR)
    top.title("Panorama Result")

    img = Image.open(img_path)
    img.thumbnail((1000, 600))
    imgtk = ImageTk.PhotoImage(img)

    lbl = Label(top, image=imgtk, bg=BG_COLOR)
    lbl.image = imgtk
    lbl.pack(padx=10, pady=10)

# --- GUI Setup ---
root = tk.Tk()
root.title("Space Panorama Builder")
root.geometry("520x500")
root.configure(bg=BG_COLOR)

# Top spacing
tk.Label(root, text="", bg=BG_COLOR).pack()

# Load and display university logo
try:
    logo_image = Image.open("university_logo.png")
    logo_image = logo_image.resize((120, 120), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = Label(root, image=logo_photo, bg=BG_COLOR)
    logo_label.image = logo_photo
    logo_label.pack()
except Exception as e:
    print("Logo could not be loaded:", e)

# Main title
Label(
    root,
    text="Panorama Builder for Space Image Dataset",
    font=("Arial", 14),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(pady=(80, 20))

# Select button
Button(
    root,
    text="Select Space Images",
    command=select_images,
    width=30,
    height=2,
    bg=BTN_COLOR,
    fg=BTN_TEXT_COLOR,
    activebackground="#45a049",
    font=("Arial", 12)
).pack(pady=(10, 5))

# Status label shown after button
status_label = Label(root, text="", font=("Arial", 12), fg="yellow", bg=BG_COLOR)
status_label.pack(pady=(0, 10))

# Footer
Label(
    root,
    text="Project Developed by Beykoz University Students",
    font=("Arial", 12),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(pady=(200, 10))

root.mainloop()
