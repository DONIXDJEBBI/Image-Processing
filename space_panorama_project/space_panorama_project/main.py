import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button
from PIL import Image, ImageTk
import os

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

def select_images():
    filez = filedialog.askopenfilenames(
        title='Select Space Images',
        filetypes=[('Image files', '*.jpg *.jpeg *.png *.bmp')]
    )
    if len(filez) < 2:
        messagebox.showerror("Error", "Select at least two images.")
        return

    # Add a temporary status label
    status_label = Label(root, text="Please wait, stitching images...", fg="blue", font=("Arial", 12))
    status_label.pack()
    root.update()  # Force update to display the label immediately

    # Run the stitching process
    result = stitch_images(filez)

    # Remove status label after processing
    status_label.destroy()

    if result is not None:
        result_path = "panorama_result.jpg"
        cv2.imwrite(result_path, result)
        show_result(result_path)
    else:
        messagebox.showerror("Error", "Failed to stitch images.")


def show_result(img_path):
    top = tk.Toplevel()
    top.title("Panorama Result")

    img = Image.open(img_path)
    img.thumbnail((800, 400))
    imgtk = ImageTk.PhotoImage(img)

    lbl = Label(top, image=imgtk)
    lbl.image = imgtk
    lbl.pack()

# GUI Setup
root = tk.Tk()
root.title("Space Panorama Builder")
root.geometry("500x300")  # Increased size for logo

# Add top spacing
tk.Label(root, text="", height=1).pack()

# Load and display university logo
logo_image = Image.open("university_logo.png")
logo_image = logo_image.resize((120, 120), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(root, image=logo_photo)
logo_label.image = logo_photo  # Keep a reference
logo_label.pack()

Label(root, text="Panorama Builder for Space Image Dataset", font=("Arial", 14), pady=10).pack()

# Add spacing
tk.Label(root, text="", height=5).pack()

Button(root, text="Select Space Images", command=select_images, width=30, height=2).pack()

# Add spacing
tk.Label(root, text="", height=15).pack()

Label(root, text="Project Developed by Beykoz University Students", font=("Arial", 14), pady=10).pack()


root.mainloop()
