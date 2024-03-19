import os
import json
import cv2
import tkinter as tk
from tkinter import filedialog


class AnnotationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Annotation Tool")
        self.root.geometry("800x600")

        self.annotation_data = []
        self.image_files = []
        self.current_image_index = 0

        self.load_button = tk.Button(
            self.root, text="Load Images", command=self.load_images)
        self.load_button.pack()

        self.next_button = tk.Button(
            self.root, text="Next Image", command=self.next_image, state=tk.DISABLED)
        self.next_button.pack()

        self.save_button = tk.Button(
            self.root, text="Save Annotations", command=self.save_annotations)
        self.save_button.pack()

        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.rect = None
        self.start_x = None
        self.start_y = None

    def load_images(self):
        directory = filedialog.askdirectory(title="Select Image Directory")
        if directory:
            self.image_files = [os.path.join(directory, file) for file in os.listdir(
                directory) if file.endswith(('.jpg', '.jpeg', '.png'))]
            if self.image_files:
                self.current_image_index = 0
                self.show_image()

    def show_image(self):
        image_path = self.image_files[self.current_image_index]
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, _ = image.shape
        max_size = min(800, height, width)
        if height > width:
            new_height = max_size
            new_width = int(width * (max_size / height))
        else:
            new_width = max_size
            new_height = int(height * (max_size / width))
        image = cv2.resize(image, (new_width, new_height))
        self.img_label.img = tk.PhotoImage(
            data=cv2.imencode('.png', image)[1].tobytes())
        self.img_label.config(image=self.img_label.img)

    def start_rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def draw_rectangle(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def end_rectangle(self, event):
        cur_x, cur_y = event.x, event.y
        self.annotation_data.append({
            "image_path": self.image_files[self.current_image_index],
            "class": None,
            "coordinates": [self.start_x, self.start_y, cur_x, cur_y]
        })
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.select_class()

    def select_class(self):
        class_window = tk.Toplevel(self.root)
        class_window.title("Select Class")
        class_var = tk.StringVar()
        class_var.set("Class 1")

        class_label = tk.Label(class_window, text="Select Class:")
        class_label.pack()

        class_menu = tk.OptionMenu(
            class_window, class_var, "Class 1", "Class 2", "Class 3", "Class 4")
        class_menu.pack()

        confirm_button = tk.Button(class_window, text="Confirm", command=lambda: self.confirm_class(
            class_window, class_var.get()))
        confirm_button.pack()

    def confirm_class(self, class_window, selected_class):
        class_window.destroy()
        self.annotation_data[-1]["class"] = selected_class
        self.next_image()

    def next_image(self):
        self.current_image_index += 1
        if self.current_image_index < len(self.image_files):
            self.show_image()
            self.canvas.delete("all")
        else:
            self.save_button.config(state=tk.NORMAL)

    def save_annotations(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(self.annotation_data, f, indent=4)
            print("Annotations saved successfully.")

    def annotate_image(self):
        self.canvas.bind("<ButtonPress-1>", self.start_rectangle)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_rectangle)


if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotationTool(root)
    root.mainloop()
