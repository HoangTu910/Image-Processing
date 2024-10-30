import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Scale, Label, Frame
from PIL import Image, ImageTk

# Tạo giao diện ứng dụng
root = Tk()
root.title("Simple Photoshop App")

# Biến toàn cục
image = None  # Ảnh gốc
processed_image = None  # Ảnh đã qua xử lý

# Hàm load ảnh
def load_image():
    global image, processed_image
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        processed_image = image.copy()
        display_image(processed_image)

# Hàm hiển thị ảnh
def display_image(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Chuyển sang RGB để hiển thị
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    label_img.config(image=img_tk)
    label_img.image = img_tk

# Các hàm xử lý ảnh (grayscale, brightness, resize, edge detection, etc.)
def grayscale():
    global processed_image
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
    display_image(processed_image)

def adjust_brightness(value):
    global processed_image
    brightness = int(value) - 50
    processed_image = cv2.convertScaleAbs(image, alpha=1, beta=brightness)
    display_image(processed_image)

def resize_image(scale):
    global processed_image
    scale = int(scale) / 100.0
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    processed_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    display_image(processed_image)

def edge_detection():
    global processed_image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    display_image(processed_image)

def gaussian_filter():
    global processed_image
    processed_image = cv2.GaussianBlur(image, (5, 5), 0)
    display_image(processed_image)

def median_filter():
    global processed_image
    processed_image = cv2.medianBlur(image, 5)
    display_image(processed_image)

def save_image():
    if processed_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, processed_image)

def rotate_image(angle):
    global processed_image
    (h, w) = processed_image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, int(angle), 1.0)
    rotated = cv2.warpAffine(processed_image, M, (w, h))
    processed_image = rotated
    display_image(processed_image)

def flip_image(direction):
    global processed_image
    if direction == "horizontal":
        processed_image = cv2.flip(processed_image, 1)
    elif direction == "vertical":
        processed_image = cv2.flip(processed_image, 0)
    display_image(processed_image)

def adjust_contrast(value):
    global processed_image
    contrast = float(value) / 50
    processed_image = cv2.convertScaleAbs(image, alpha=contrast, beta=0)
    display_image(processed_image)

def apply_sepia():
    global processed_image
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    processed_image = cv2.transform(image, sepia_filter)
    processed_image = np.clip(processed_image, 0, 255).astype(np.uint8)
    display_image(processed_image)

def adjust_saturation(value):
    global processed_image
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image = np.array(hsv_image, dtype=np.float64)
    hsv_image[:, :, 1] = hsv_image[:, :, 1] * (int(value) / 50)
    hsv_image[:, :, 1][hsv_image[:, :, 1] > 255] = 255
    hsv_image = np.array(hsv_image, dtype=np.uint8)
    processed_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    display_image(processed_image)

# Tạo khung trái, phải và khung hiển thị ảnh ở giữa
left_frame = Frame(root)
left_frame.pack(side="left", padx=10, pady=10)

right_frame = Frame(root)
right_frame.pack(side="right", padx=10, pady=10)

center_frame = Frame(root)
center_frame.pack(pady=10)

# Nút và điều khiển ở khung bên trái
Button(left_frame, text="Load Image", command=load_image).pack(pady=5)
Button(left_frame, text="Save Image", command=save_image).pack(pady=5)
Button(left_frame, text="Grayscale", command=grayscale).pack(pady=5)
Button(left_frame, text="Edge Detection", command=edge_detection).pack(pady=5)
Button(left_frame, text="Gaussian Filter", command=gaussian_filter).pack(pady=5)
Button(left_frame, text="Median Filter", command=median_filter).pack(pady=5)
Button(left_frame, text="Sepia Filter", command=apply_sepia).pack(pady=5)

# Điều chỉnh độ sáng và độ tương phản ở khung bên phải
Label(right_frame, text="Brightness").pack()
Scale(right_frame, from_=0, to=100, orient="horizontal", command=adjust_brightness).pack(pady=5)
Label(right_frame, text="Contrast").pack()
Scale(right_frame, from_=10, to=100, orient="horizontal", command=adjust_contrast).pack(pady=5)

# Điều chỉnh độ bão hòa và kích thước ở khung bên phải
Label(right_frame, text="Saturation").pack()
Scale(right_frame, from_=0, to=100, orient="horizontal", command=adjust_saturation).pack(pady=5)
Label(right_frame, text="Resize").pack()
Scale(right_frame, from_=10, to=200, orient="horizontal", command=resize_image).pack(pady=5)
Label(right_frame, text="Rotate").pack()
Scale(right_frame, from_=0, to=360, orient="horizontal", command=rotate_image).pack(pady=5)

# Nút lật ảnh trong khung bên phải
Button(right_frame, text="Flip Horizontal", command=lambda: flip_image("horizontal")).pack(pady=5)
Button(right_frame, text="Flip Vertical", command=lambda: flip_image("vertical")).pack(pady=5)

# Khung hiển thị ảnh ở giữa
label_img = Label(center_frame)
label_img.pack()

root.mainloop()
