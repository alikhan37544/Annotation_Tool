import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

class AnnotationTool:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Annotation Tool")
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()
        self.image = None
        self.rect = None
        self.class_names = ["Class1", "Class2", "Class3", "Class4"]

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.class_var = tk.StringVar(master)
        self.class_var.set(self.class_names[0])

        self.class_menu = tk.OptionMenu(master, self.class_var, *self.class_names)
        self.class_menu.pack()

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.save_button = tk.Button(master, text="Save Annotation", command=self.save_annotation)
        self.save_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image()

    def display_image(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (800, 600))
        self.photo = cv2.PhotoImage(image=cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def on_button_press(self, event):
        self.rect = (event.x, event.y, event.x, event.y)

    def on_mouse_move(self, event):
        self.canvas.delete("rectangle")
        self.rect = (self.rect[0], self.rect[1], event.x, event.y)
        self.canvas.create_rectangle(*self.rect, outline="red", tag="rectangle")

    def on_button_release(self, event):
        class_name = self.class_var.get()
        annotation = {"class": class_name, "coordinates": self.rect}
        print("Annotation:", annotation)

    def save_annotation(self):
        # Write code to save annotations to a file (e.g., JSON)
        pass

def main():
    root = tk.Tk()
    app = AnnotationTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
