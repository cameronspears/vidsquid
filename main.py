import argparse
import os
import sys
import threading
import tkinter as tk
from tkinter import Tk, filedialog

import ffmpeg


def find_executable(executable_name):
    """Find the full path of an executable, checking common paths."""
    common_paths = [
        "C:\\ffmpeg\\bin",  # Common Windows path
        "C:\\Program Files\\ffmpeg\\bin",  # Common Windows path
        "C:\\Program Files (x86)\\ffmpeg\\bin",  # Common Windows path
        "/usr/local/bin",  # Homebrew (Intel macOS and Linux)
        "/opt/homebrew/bin",  # Homebrew (Apple Silicon macOS)
        "/usr/bin",  # Common Unix path
        "/bin",  # Common Unix path
        "/usr/sbin",  # Common Unix path
        "/sbin",  # Common Unix path
    ]
    paths = os.environ["PATH"].split(os.pathsep) + common_paths
    for path in paths:
        full_path = os.path.join(path, executable_name)
        if os.path.exists(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None


def compress_video(input_path, output_path, compression_level, ffmpeg_path, ffprobe_path, progress_var):
    try:
        # Define compression settings based on the selected level
        if compression_level == 'extreme':
            crf = 28
            preset = 'slow'
        elif compression_level == 'medium':
            crf = 23
            preset = 'medium'
        elif compression_level == 'fast':
            # Fast mode is just a filetype transformation
            (
                ffmpeg
                .input(input_path)
                .output(output_path, vcodec='copy', acodec='copy')
                .run(cmd=ffmpeg_path)
            )
            progress_var.set("Transformation completed with fast mode.")
            return
        else:
            raise ValueError("Invalid compression level specified.")

        # Use ffmpeg to compress the video with the selected settings
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec='libx264',  # Use H.264 codec for better compatibility
                acodec='aac',  # Use AAC audio codec
                movflags='faststart',
                preset=preset,
                crf=crf,  # Constant Rate Factor for quality control
            )
            .run(cmd=ffmpeg_path)
        )

        progress_var.set(f"Video compressed successfully with {compression_level} compression!")
    except ffmpeg.Error as e:
        progress_var.set(f"An error occurred: {e.stderr.decode('utf8')}")
        sys.exit(1)


def compress_video_thread(input_path, output_path, compression_level, ffmpeg_path, ffprobe_path, progress_var):
    # Run the compression in a separate thread
    thread = threading.Thread(target=compress_video, args=(
        input_path, output_path, compression_level, ffmpeg_path, ffprobe_path, progress_var))
    thread.start()


def gui_mode(ffmpeg_path, ffprobe_path):
    def select_file():
        input_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mov *.mp4 *.avi *.mkv *.flv *.wmv *.webm")])
        if input_path:
            output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
            if output_path:
                select_compression_level(input_path, output_path)

    def select_compression_level(input_path, output_path):
        def set_compression_level(level):
            progress_var.set(f"Compressing with {level} mode, please wait...")
            compression_window.destroy()
            compress_video_thread(input_path, output_path, level, ffmpeg_path, ffprobe_path, progress_var)

        compression_window = tk.Toplevel(root)
        compression_window.title("Select Compression Level")
        tk.Label(compression_window, text="Choose Compression Level:").pack(pady=10)
        tk.Button(compression_window, text="Extreme", command=lambda: set_compression_level('extreme')).pack(fill='x')
        tk.Button(compression_window, text="Medium", command=lambda: set_compression_level('medium')).pack(fill='x')
        tk.Button(compression_window, text="Fast", command=lambda: set_compression_level('fast')).pack(fill='x')

    # Create the main application window
    root = Tk()
    root.title("Video Compressor")

    # Create a button to select the video file
    select_button = tk.Button(root, text="Select Video file", command=select_file)
    select_button.pack(pady=20)

    # Create a label to show progress
    progress_var = tk.StringVar()
    progress_label = tk.Label(root, textvariable=progress_var)
    progress_label.pack(pady=10)

    # Start the Tkinter event loop
    root.mainloop()


def main():
    # Determine paths to ffmpeg and ffprobe
    ffmpeg_path = find_executable("ffmpeg")
    ffprobe_path = find_executable("ffprobe")

    if not ffmpeg_path or not ffprobe_path:
        sys.exit("ffmpeg and/or ffprobe not found in system PATH. Please install them or provide their paths.")

    parser = argparse.ArgumentParser(description="Compress video files to MP4 using ffmpeg.")
    parser.add_argument("-i", "--input", type=str, help="Input video file")
    parser.add_argument("-o", "--output", type=str, help="Output MP4 file")
    parser.add_argument("-c", "--compression", choices=['extreme', 'medium', 'fast'], default='medium',
                        help="Compression level")
    parser.add_argument("--gui", action="store_true", help="Run in GUI mode")

    args = parser.parse_args()

    if args.gui:
        gui_mode(ffmpeg_path, ffprobe_path)
    else:
        if not args.input or not args.output:
            parser.print_help()
            sys.exit(1)
        compress_video(args.input, args.output, args.compression, ffmpeg_path, ffprobe_path)


if __name__ == "__main__":
    main()
