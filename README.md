# vidsquid

vidsquid is a Python script that compresses various video file formats to MP4 using `ffmpeg`. It focuses on maintaining
compatibility and reducing file size with three compression levels: Extreme, Medium, and Fast.

## Requirements

- Python 3.6 or higher
- `ffmpeg` and `ffprobe` installed and accessible in the system's PATH
- Required Python packages: `ffmpeg-python`, `tkinter`

### Installation

1. **Install Python packages:**

   Run the following command in your terminal or command prompt to install the required Python packages:

   ```
   pip install ffmpeg-python
   ```

2. **Install ffmpeg and ffprobe:**

   #### macOS:

   Ensure `ffmpeg` and `ffprobe` are installed and accessible in your system's PATH. For macOS, you can use Homebrew:

   ```
   brew install ffmpeg
   ```

   #### Windows:

   Download and install `ffmpeg` from the official website [FFmpeg Download](https://ffmpeg.org/download.html). Extract
   the files and add the `bin` directory to your system's PATH.

## Usage

### Command-Line Mode

Run the following command in your terminal or command prompt:

```
python main.py -i input.mov -o output.mp4 -c extreme
```

- `-i, --input`: Input video file (supports `.mov`, `.mp4`, `.avi`, `.mkv`, `.flv`, `.wmv`, `.webm`)
- `-o, --output`: Output MP4 file
- `-c, --compression`: Compression level (`extreme`, `medium`, `fast`; default: `medium`)

### GUI Mode

To run the script with a graphical user interface:

```
python main.py --gui
```

1. Select the input video file.
2. Choose the output file location and name.
3. Select the desired compression level (`Extreme`, `Medium`, `Fast`).
4. The progress will be displayed in the GUI.