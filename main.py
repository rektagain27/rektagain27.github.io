import os
import threading
from tkinter import Tk, Label, Button, Checkbutton, filedialog, BooleanVar, messagebox
from PIL import Image, ImageTk

class CR2toJPGConverter:
    def __init__(self, master):
        self.master = master
        master.title("CR2 to JPG Converter")

        self.input_label = Label(master, text="Select Input Folder:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        self.input_button = Button(master, text="Browse", command=self.browse_input)
        self.input_button.grid(row=0, column=1, padx=10, pady=10)

        self.output_label = Label(master, text="Select Output Folder:")
        self.output_label.grid(row=1, column=0, padx=10, pady=10)

        self.output_button = Button(master, text="Browse", command=self.browse_output)
        self.output_button.grid(row=1, column=1, padx=10, pady=10)

        self.replace_var = BooleanVar()
        self.replace_checkbutton = Checkbutton(master, text="Replace Original CR2 Files", variable=self.replace_var, command=self.update_output_state)
        self.replace_checkbutton.grid(row=2, column=0, columnspan=2, pady=10)

        self.thumbnail_label = Label(master)
        self.thumbnail_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.start_button = Button(master, text="Start Conversion", command=self.start_conversion)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.current_file_label = Label(master, text="")
        self.current_file_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.progress_label = Label(master, text="")
        self.progress_label.grid(row=6, column=0, columnspan=2, pady=10)

        self.stop_button = Button(master, text="Stop Conversion", command=self.stop_conversion, state="disabled")
        self.stop_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.conversion_stopped = False
        self.lock = threading.Lock()

    def browse_input(self):
        global input_folder
        input_folder = filedialog.askdirectory()
        if input_folder:
            self.input_label.config(text=f"Input Folder: {input_folder}")
            self.input_folder = input_folder
            self.update_output_state()
            

    def browse_output(self):
        output_folder = filedialog.askdirectory()
        if output_folder:
            self.output_label.config(text=f"Output Folder: {output_folder}")
            self.output_folder = output_folder

    def update_output_state(self):
        if self.replace_var.get():
            self.output_label.config(state="disabled")
            self.output_folder = input_folder
            messagebox.showwarning("Warning", "Replacing CR2 files with JPEG is irreversible. Original CR2 files will be permanently deleted.")
        else:
            self.output_label.config(state="normal")

    def show_thumbnail(self, input_path):
        try:
            with Image.open(input_path) as img:
                img.thumbnail((200, 200))
                thumbnail = ImageTk.PhotoImage(img)
                self.thumbnail_label.config(image=thumbnail)
                self.thumbnail_label.image = thumbnail
        except Exception as e:
            messagebox.showerror("Error", f"Error creating thumbnail for {input_path}: {e}")

    def convert_cr2_to_jpg(self, input_path, output_path, file_count, total_files):
        self.show_thumbnail(input_path)
        self.current_file_label.config(text=f"Converting: {os.path.basename(input_path)}")
        self.progress_label.config(text=f"Progress: {file_count}/{total_files}")

        try:
            with Image.open(input_path) as img:
                img.convert("RGB").save(output_path, "JPEG")

            if self.replace_var.get():
                os.remove(input_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error converting {input_path}: {e}")

        with self.lock:
            if self.conversion_stopped:
                self.current_file_label.config(text="Conversion stopped.")
                self.progress_label.config(text="")
                self.thumbnail_label.config(image="")
                self.stop_button.config(state="disabled")
                self.start_button.config(state="normal")
                return

    def convert_images_in_thread(self):
        if not self.output_folder and not self.replace_var.get():
            messagebox.showwarning("Warning", "Please select an output folder.")
            return

        cr2_files = [filename for filename in os.listdir(self.input_folder) if filename.lower().endswith(".cr2")]
        total_files = len(cr2_files)

        with self.lock:
            self.conversion_stopped = False

        for file_count, filename in enumerate(cr2_files, start=1):
            input_path = os.path.join(self.input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".jpg"
            output_path = os.path.join(self.output_folder, output_filename)

            self.convert_cr2_to_jpg(input_path, output_path, file_count, total_files)

            with self.lock:
                if self.conversion_stopped:
                    break

        with self.lock:
            if not self.conversion_stopped:
                messagebox.showinfo("Info", "Conversion complete.")

        self.current_file_label.config(text="")
        self.progress_label.config(text="")
        self.thumbnail_label.config(image="")
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")

    def start_conversion(self):
        if hasattr(self, 'input_folder') and (hasattr(self, 'output_folder') or self.replace_var.get()):
            self.stop_button.config(state="normal")
            self.start_button.config(state="disabled")
            threading.Thread(target=self.convert_images_in_thread).start()
        else:
            messagebox.showwarning("Warning", "Please select input and output folders.")

    def stop_conversion(self):
        with self.lock:
            self.conversion_stopped = True

if __name__ == "__main__":
    root = Tk()
    app = CR2toJPGConverter(root)
    root.mainloop()
