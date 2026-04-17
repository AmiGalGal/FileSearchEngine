import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

import OneAboveAll as Backend


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Search Engine")

        self.widgets = []

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Query:").pack()
        self.query_entry = tk.Entry(self.root, width=50)
        self.query_entry.pack()

        tk.Label(self.root, text="Type:").pack()
        self.type_var = tk.StringVar(value="Images")
        tk.OptionMenu(self.root, self.type_var, "Docs", "Images", "Videos").pack()

        tk.Label(self.root, text="Top results:").pack()
        self.top_entry = tk.Entry(self.root)
        self.top_entry.insert(0, "3")
        self.top_entry.pack()

        tk.Button(self.root, text="Search", command=self.do_search).pack()
        tk.Button(self.root, text="Create DB", command=self.create_db).pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

    def create_db(self):
        folder = filedialog.askdirectory()
        if folder:
            Backend.Create(folder)
            messagebox.showinfo("Done", "All DBs created!")

    def do_search(self):
        query = self.query_entry.get()

        try:
            top_k = int(self.top_entry.get())
        except:
            messagebox.showerror("Error", "Top must be a number")
            return

        type_map = {
            "Docs": 0,
            "Images": 1,
            "Videos": 2
        }

        search_type = type_map[self.type_var.get()]

        results = Backend.search(query, search_type, top_k)

        self.clear()

        if search_type == 0:
            self.show_docs(results)
        elif search_type == 1:
            self.show_images(results)
        elif search_type == 2:
            self.show_videos(results)

    def show_docs(self, results):
        if not results or len(results) != 2:
            return

        paths = results[0]
        texts = results[1]

        for path, text in zip(paths, texts):
            container = tk.Frame(self.frame, bd=2, relief="groove", padx=8, pady=8)
            container.pack(fill="x", pady=5, padx=5)

            tk.Label(container, text=path, wraplength=700, justify="left").pack(anchor="w")
            tk.Label(container, text=text, wraplength=700, justify="left").pack(anchor="w")

            self.widgets.append(container)

    def show_images(self, results):
        for path in results:
            container = tk.Frame(self.frame)
            container.pack(side="left", padx=10)

            tk.Label(container, text=path, wraplength=150).pack()

            try:
                img = Image.open(path)
                img.thumbnail((200, 200))
                tk_img = ImageTk.PhotoImage(img)

                lbl = tk.Label(container, image=tk_img)
                lbl.image = tk_img
                lbl.pack()

                self.widgets.append(container)
            except:
                tk.Label(container, text="Failed to load image").pack()

    def show_videos(self, results):
        for path in results:
            container = tk.Frame(self.frame)
            container.pack(side="left", padx=10)

            tk.Label(container, text=path, wraplength=150).pack()

            label = tk.Label(container)
            label.pack()

            cap = cv2.VideoCapture(path)

            widget = {
                "frame": container,
                "label": label,
                "cap": cap
            }

            self.widgets.append(container)
            self.play_video(widget)

    def play_video(self, widget):
        cap = widget["cap"]
        label = widget["label"]

        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((200, 150))

            tk_img = ImageTk.PhotoImage(img)

            label.config(image=tk_img)
            label.image = tk_img

        self.root.after(30, lambda: self.play_video(widget))

    def clear(self):
        for w in self.widgets:
            w.destroy()
        self.widgets.clear()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()