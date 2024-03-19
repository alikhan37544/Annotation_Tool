import os
import json
import tkinter as tk
from tkinter import filedialog
from annotation_tool import AnnotationTool


class CustomAnnotationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Annotation Tool")
        self.root.geometry("800x600")

        self.annotation_data = []
        self.image_files = []
        self.current_image_index = 0

        self.load_button = tk.Button(
            self.root, text="Load Images", command=self.load_images)
        self.load_button.pack()

        self.save_button = tk.Button(
            self.root, text="Save Annotations", command=self.save_annotations, state=tk.DISABLED)
        self.save_button.pack()

        self.annotation_tool = None

    def load_images(self):
        directory = filedialog.askdirectory(title="Select Image Directory")
        if directory:
            self.image_files = [os.path.join(directory, file) for file in os.listdir(
                directory) if file.endswith('.png')]
            if self.image_files:
                self.current_image_index = 0
                self.show_image()

    def show_image(self):
        if self.current_image_index < len(self.image_files):
            image_path = self.image_files[self.current_image_index]
            self.annotation_tool = AnnotationTool(
                [image_path], layers=['foreground', 'background'])
            self.annotation_tool.mainloop()
            self.annotation_data.append(self.annotation_tool.get_annotations())
            self.next_image()
        else:
            self.save_button.config(state=tk.NORMAL)

    def next_image(self):
        self.current_image_index += 1
        self.show_image()

    def save_annotations(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(self.annotation_data, f, indent=4)
            print("Annotations saved successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomAnnotationTool(root)
    root.mainloop()
