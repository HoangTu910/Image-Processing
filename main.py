import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Scale, Label
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

# Chuyển ảnh sang xám
def grayscale():
    global processed_image
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)  # Đổi lại BGR để hiển thị
    display_image(processed_image)

# Điều chỉnh độ sáng
def adjust_brightness(value):
    global processed_image
    brightness = int(value) - 50
    processed_image = cv2.convertScaleAbs(image, alpha=1, beta=brightness)
    display_image(processed_image)

# Điều chỉnh kích thước
def resize_image(scale):
    global processed_image
    scale = int(scale) / 100.0
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    processed_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    display_image(processed_image)

# Phát hiện cạnh
def edge_detection():
    global processed_image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    display_image(processed_image)

# Lọc nhiễu Gaussian
def gaussian_filter():
    global processed_image
    processed_image = cv2.GaussianBlur(image, (5, 5), 0)
    display_image(processed_image)

# Lọc nhiễu trung vị
def median_filter():
    global processed_image
    processed_image = cv2.medianBlur(image, 5)
    display_image(processed_image)

# Lưu ảnh
def save_image():
    if processed_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, processed_image)

# Tạo các nút và điều khiển
Button(root, text="Load Image", command=load_image).pack()
Button(root, text="Grayscale", command=grayscale).pack()
Button(root, text="Edge Detection", command=edge_detection).pack()
Button(root, text="Gaussian Filter", command=gaussian_filter).pack()
Button(root, text="Median Filter", command=median_filter).pack()
Button(root, text="Save Image", command=save_image).pack()

Label(root, text="Brightness").pack()
Scale(root, from_=0, to=100, orient="horizontal", command=adjust_brightness).pack()

Label(root, text="Resize").pack()
Scale(root, from_=10, to=200, orient="horizontal", command=resize_image).pack()

# Khung hiển thị ảnh
label_img = Label(root)
label_img.pack()

root.mainloop()
