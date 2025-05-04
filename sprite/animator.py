import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SpriteAnimator:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprite Animator")

        self.canvas = tk.Canvas(root, width=256, height=256, bg='gray')
        self.canvas.pack(pady=10)

        # Controls
        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Button(control_frame, text="Load Sprite Sheets", command=self.load_files).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(control_frame, text="Columns:").grid(row=1, column=0, sticky="e")
        self.cols_entry = tk.Entry(control_frame, width=5)
        self.cols_entry.insert(0, "3")
        self.cols_entry.grid(row=1, column=1)

        tk.Label(control_frame, text="Rows:").grid(row=2, column=0, sticky="e")
        self.rows_entry = tk.Entry(control_frame, width=5)
        self.rows_entry.insert(0, "3")
        self.rows_entry.grid(row=2, column=1)

        tk.Label(control_frame, text="Frame Width:").grid(row=3, column=0, sticky="e")
        self.frame_w_entry = tk.Entry(control_frame, width=5)
        self.frame_w_entry.insert(0, "256")
        self.frame_w_entry.grid(row=3, column=1)

        tk.Label(control_frame, text="Frame Height:").grid(row=4, column=0, sticky="e")
        self.frame_h_entry = tk.Entry(control_frame, width=5)
        self.frame_h_entry.insert(0, "256")
        self.frame_h_entry.grid(row=4, column=1)

        tk.Label(control_frame, text="Speed (ms):").grid(row=5, column=0, sticky="e")
        self.speed_entry = tk.Entry(control_frame, width=5)
        self.speed_entry.insert(0, "100")
        self.speed_entry.grid(row=5, column=1)

        tk.Button(control_frame, text="Start", command=self.start).grid(row=6, column=0, pady=10)
        tk.Button(control_frame, text="Stop", command=self.stop).grid(row=6, column=1, pady=10)

        # Variables
        self.sheets = []
        self.frames = []
        self.current_frame = 0
        self.interval = None
        self.tkimage = None

    def load_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PNG files", "*.png")])
        if not files:
            return
        self.sheets = [Image.open(f).convert("RGBA") for f in files]
        self.extract_frames()
        self.current_frame = 0
        self.show_frame(0)

    def extract_frames(self):
        self.frames = []
        try:
            cols = int(self.cols_entry.get())
            rows = int(self.rows_entry.get())
            fw = int(self.frame_w_entry.get())
            fh = int(self.frame_h_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        for sheet in self.sheets:
            for row in range(rows):
                for col in range(cols):
                    left = col * fw
                    upper = row * fh
                    box = (left, upper, left + fw, upper + fh)
                    frame = sheet.crop(box)
                    self.frames.append(frame)

    def show_frame(self, index):
        if not self.frames:
            return
        frame = self.frames[index]
        self.tkimage = ImageTk.PhotoImage(frame)
        self.canvas.config(width=frame.width, height=frame.height)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.tkimage)

    def update_frame(self):
        self.show_frame(self.current_frame)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.interval = self.root.after(int(self.speed_entry.get()), self.update_frame)

    def start(self):
        self.stop()
        self.update_frame()

    def stop(self):
        if self.interval:
            self.root.after_cancel(self.interval)
            self.interval = None

if __name__ == "__main__":
    root = tk.Tk()
    app = SpriteAnimator(root)
    root.mainloop()