import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import shutil

class SetupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Setup Folder")
        self.geometry("500x400")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.result = {"source": "", "targets": []}
        self.create_widgets()
        
        # Buat dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Posisikan di tengah parent window
        self.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50))
        
    def create_widgets(self):
        # Frame untuk folder sumber
        source_frame = ttk.LabelFrame(self, text="Folder Sumber (berisi file belum disortir)")
        source_frame.pack(fill="x", padx=10, pady=10)
        
        self.source_entry = ttk.Entry(source_frame, width=50)
        self.source_entry.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)
        
        ttk.Button(source_frame, text="Browse...", command=self.browse_source).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Frame untuk folder tujuan
        target_frame = ttk.LabelFrame(self, text="Folder Tujuan")
        target_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Listbox untuk menampilkan folder tujuan
        self.target_listbox = tk.Listbox(target_frame)
        self.target_listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar untuk listbox
        scrollbar = ttk.Scrollbar(target_frame, orient="vertical", command=self.target_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.target_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame untuk tombol folder tujuan
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Tambah Folder", command=self.add_target_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Hapus Folder", command=self.remove_target_folder).pack(side=tk.LEFT, padx=5)
        
        # Tombol OK dan Cancel
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(bottom_frame, text="OK", command=self.on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(bottom_frame, text="Cancel", command=self.on_close).pack(side=tk.RIGHT, padx=5)
        
    def browse_source(self):
        folder = filedialog.askdirectory(title="Pilih Folder Sumber")
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)
    
    def add_target_folder(self):
        folder_name = simpledialog.askstring("Tambah Folder", "Masukkan nama folder tujuan:")
        if folder_name and folder_name.strip():
            # Periksa apakah folder sudah ada dalam list
            if folder_name not in self.target_listbox.get(0, tk.END):
                self.target_listbox.insert(tk.END, folder_name)
    
    def remove_target_folder(self):
        selected = self.target_listbox.curselection()
        if selected:
            self.target_listbox.delete(selected)
    
    def on_ok(self):
        source = self.source_entry.get().strip()
        targets = list(self.target_listbox.get(0, tk.END))
        
        if not source:
            messagebox.showerror("Error", "Folder sumber harus dipilih!")
            return
        
        if not targets:
            messagebox.showerror("Error", "Minimal satu folder tujuan harus ditambahkan!")
            return
        
        self.result = {
            "source": source,
            "targets": targets
        }
        self.destroy()
    
    def on_close(self):
        self.result = None
        self.destroy()

class ImageSorterApp:
    def __init__(self, root, source_folder, target_folders):
        self.root = root
        self.root.title("Sortir Gambar")
        self.root.geometry("800x600")
        
        self.source_folder = source_folder
        self.target_folders = target_folders
        
        # Dapatkan daftar file gambar dari folder sumber
        self.image_files = self._get_image_files()
        self.current_index = 0
        
        self._create_ui()
        
        # Tampilkan gambar pertama jika ada
        if self.image_files:
            self.show_current_image()
        else:
            messagebox.showinfo("Info", f"Tidak ada file gambar di folder sumber: {self.source_folder}")
    
    def _create_ui(self):
        # Frame utama
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Area untuk menampilkan gambar
        self.image_frame = ttk.Frame(main_frame)
        self.image_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Label informasi file
        self.file_info = ttk.Label(main_frame, text="", font=("Helvetica", 10))
        self.file_info.pack(pady=5)
        
        # Frame untuk tombol
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Buat tombol untuk setiap folder target
        for folder_name, folder_path in self.target_folders.items():
            btn = ttk.Button(
                button_frame, 
                text=folder_name,
                command=lambda path=folder_path: self.move_to_folder(path)
            )
            btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Tombol lewati
        ttk.Button(
            main_frame, 
            text="Lewati",
            command=self.skip_image
        ).pack(fill=tk.X, pady=5)
    
    def _get_image_files(self):
        """Dapatkan semua file gambar dari folder sumber"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.psd']
        files = []
        
        if os.path.exists(self.source_folder):
            for file in os.listdir(self.source_folder):
                file_path = os.path.join(self.source_folder, file)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in image_extensions:
                        files.append(file_path)
        
        return files
    
    def show_current_image(self):
        """Tampilkan gambar saat ini"""
        if self.current_index < len(self.image_files):
            image_path = self.image_files[self.current_index]
            
            try:
                # Buka gambar dengan PIL
                image = Image.open(image_path)
                
                # Dapatkan ukuran frame
                frame_width = self.image_frame.winfo_width() or 600
                frame_height = self.image_frame.winfo_height() or 400
                
                # Resize gambar agar sesuai dengan frame
                image.thumbnail((frame_width, frame_height), Image.LANCZOS)
                
                # Konversi ke format yang dapat ditampilkan oleh tkinter
                tk_image = ImageTk.PhotoImage(image)
                
                # Tampilkan gambar
                self.image_label.config(image=tk_image)
                self.image_label.image = tk_image  # Simpan referensi
                
                # Tampilkan info file
                file_name = os.path.basename(image_path)
                self.file_info.config(text=f"File: {file_name} ({self.current_index + 1}/{len(self.image_files)})")
            
            except Exception as e:
                self.image_label.config(image=None)
                self.file_info.config(text=f"Error: {str(e)}")
                messagebox.showerror("Error", f"Tidak dapat membuka gambar: {str(e)}")
        else:
            self.image_label.config(image=None)
            self.file_info.config(text="Semua gambar telah disortir!")
            messagebox.showinfo("Selesai", "Semua gambar telah disortir!")
    
    def move_to_folder(self, target_folder):
        """Pindahkan file ke folder target dan lanjut ke gambar berikutnya"""
        if self.current_index < len(self.image_files):
            current_file = self.image_files[self.current_index]
            file_name = os.path.basename(current_file)
            target_path = os.path.join(target_folder, file_name)
            
            # Periksa jika file sudah ada di folder tujuan
            if os.path.exists(target_path):
                base_name, extension = os.path.splitext(file_name)
                i = 1
                while os.path.exists(os.path.join(target_folder, f"{base_name}_{i}{extension}")):
                    i += 1
                target_path = os.path.join(target_folder, f"{base_name}_{i}{extension}")
            
            try:
                # Pindahkan file
                shutil.move(current_file, target_path)
                print(f"Memindahkan {file_name} ke {target_folder}")
                
                # Hapus file dari daftar
                self.image_files.pop(self.current_index)
                
                # Tampilkan gambar berikutnya atau pesan selesai
                if self.image_files:
                    self.show_current_image()
                else:
                    self.image_label.config(image=None)
                    self.file_info.config(text="Semua gambar telah disortir!")
                    messagebox.showinfo("Selesai", "Semua gambar telah disortir!")
            
            except Exception as e:
                self.file_info.config(text=f"Error: {str(e)}")
                messagebox.showerror("Error", f"Tidak dapat memindahkan file: {str(e)}")
    
    def skip_image(self):
        """Lewati gambar saat ini dan lanjut ke berikutnya"""
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_current_image()

def main():
    root = tk.Tk()
    
    # Tampilkan dialog setup
    setup = SetupWindow(root)
    root.wait_window(setup)
    
    if setup.result is None:
        root.destroy()
        return
    
    source_folder = setup.result["source"]
    target_names = setup.result["targets"]
    
    # Buat folder target jika belum ada
    target_folders = {}
    parent_dir = os.path.dirname(source_folder)
    
    for name in target_names:
        path = os.path.join(parent_dir, name)
        # Buat folder jika belum ada
        os.makedirs(path, exist_ok=True)
        target_folders[name] = path
    
    # Tampilkan window utama
    root.deiconify()
    app = ImageSorterApp(root, source_folder, target_folders)
    root.mainloop()

if __name__ == "__main__":
    main()