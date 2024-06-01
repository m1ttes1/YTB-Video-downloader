import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
from PIL import Image, ImageTk
from io import BytesIO
from pydub import AudioSegment
import configparser
import requests
import threading
import webbrowser

class DownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        self.default_folder = os.path.join(os.path.dirname(__file__), "Downloads", "YTB Downloads")
        self.folder_path = self.default_folder

        self.create_widgets()

    def create_widgets(self):
        self.load_settings()

        self.folder_label = tk.Label(self.master, text="Pasta atual: " + self.folder_path)
        self.folder_label.pack()

        self.url_label = tk.Label(self.master, text="URL do vídeo:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.master)
        self.url_entry.pack()

        self.format_label = tk.Label(self.master, text="Formato:")
        self.format_label.pack()

        self.format_var = tk.StringVar()
        self.format_var.set("video")
        self.format_radio_video = tk.Radiobutton(self.master, text="Vídeo (.mp4)", variable=self.format_var, value="video")
        self.format_radio_video.pack()
        self.format_radio_audio = tk.Radiobutton(self.master, text="Áudio (.mp3)", variable=self.format_var, value="audio")
        self.format_radio_audio.pack()

        self.quality_label = tk.Label(self.master, text="Qualidade:")
        self.quality_label.pack()

        self.quality_var = tk.StringVar()
        self.quality_var.set("Melhor disponível") # 'Melhor disponivel' como default
        self.quality_menu = tk.OptionMenu(self.master, self.quality_var, "Melhor disponível", "360p", "480p", "720p", "1080p")
        self.quality_menu.pack()

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack()

        self.folder_button = tk.Button(self.buttons_frame, text="Escolher pasta de destino", command=self.choose_folder)
        self.folder_button.pack(side=tk.LEFT, padx=5)

        self.default_folder_button = tk.Button(self.buttons_frame, text="Abrir pasta downloads", command=self.open_default_folder)
        self.default_folder_button.pack(side=tk.LEFT, padx=5)

        self.download_button = tk.Button(self.master, text="Baixar", command=self.start_download_thread)
        self.download_button.pack(pady=10)

        self.progress_label = tk.Label(self.master, text="")
        self.progress_label.pack()

        self.progress_bar = tk.Label(self.master, text="", bg="green", width=0)
        self.progress_bar.pack()

        self.downloads_label = tk.Label(self.master, text="Últimos Downloads:")
        self.downloads_label.pack()

        self.downloads_frame = tk.Frame(self.master)
        self.downloads_frame.pack()

    def load_settings(self):
        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")
        if "Settings" in self.config:
            self.folder_path = self.config["Settings"].get("last_folder", self.default_folder)
        else:
            self.folder_path = self.default_folder

    def save_settings(self):
        if not self.config.has_section("Settings"):
            self.config.add_section("Settings")
        self.config["Settings"]["last_folder"] = self.folder_path
        with open("settings.ini", "w") as configfile:
            self.config.write(configfile)

    def choose_folder(self):
        selected_folder = filedialog.askdirectory(initialdir=self.folder_path)
        if selected_folder:
            self.folder_path = os.path.join(selected_folder, "YTB Downloads")
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            self.folder_label.config(text="Pasta atual: " + self.folder_path)
            self.save_settings()

    def open_default_folder(self):
        if not os.path.exists(self.default_folder):
            os.makedirs(self.default_folder)
        webbrowser.open(self.default_folder)

    def get_unique_filename(self, filepath):
        base, ext = os.path.splitext(filepath)
        counter = 1
        new_filepath = filepath

        while os.path.exists(new_filepath):
            new_filepath = f"{base}({counter}){ext}"
            counter += 1

        return new_filepath

    def start_download_thread(self):
        thread = threading.Thread(target=self.download)
        thread.start()

    def download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erro", "A URL não pode estar vazia.")
            return

        download_format = self.format_var.get()
        quality = self.quality_var.get()

        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)

            if quality == "Melhor disponível":
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            else:
                stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=quality).first() if download_format == "video" else yt.streams.filter(only_audio=True).first()

            if not stream:
                messagebox.showerror("Erro", "Stream não encontrada.")
                return

            filename = stream.default_filename
            filepath = os.path.join(self.folder_path, filename)
            filepath = self.get_unique_filename(filepath)

            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))

            stream.download(output_path=self.folder_path, filename=os.path.basename(filepath))

            if download_format == "audio":
                base, ext = os.path.splitext(filepath)
                new_file = base + '.mp3'
                audio = AudioSegment.from_file(filepath)
                audio.export(new_file, format="mp3")
                os.remove(filepath)
                filepath = new_file
                filename = os.path.basename(filepath)

            self.update_downloads(filename, yt.thumbnail_url)
            self.progress_label.config(text="Download completo!")
            self.progress_bar.config(bg="green")

        except Exception as e:
            self.log_error(str(e))
            self.progress_label.config(text="Erro durante o download: " + str(e))
            self.progress_bar.config(bg="red")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_bar.config(width=int(percentage))
        self.progress_label.config(text=f"{int(percentage)}% concluído")

    def update_downloads(self, filename, thumbnail_url):
        response = requests.get(thumbnail_url)
        thumbnail_bytes = BytesIO(response.content)

        img = Image.open(thumbnail_bytes)
        img.thumbnail((50, 50))
        img = ImageTk.PhotoImage(img)

        download_frame = tk.Frame(self.downloads_frame)
        download_frame.pack(side=tk.TOP, padx=5, pady=5)

        thumbnail_label = tk.Label(download_frame, image=img)
        thumbnail_label.image = img
        thumbnail_label.pack(side=tk.LEFT)

        filename_label = tk.Label(download_frame, text=filename, anchor="w")
        filename_label.pack(side=tk.LEFT, padx=5)

    def log_error(self, message):
        with open("error_log.txt", "a") as log_file:
            log_file.write(message + "\n")

def main():
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
