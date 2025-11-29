## How it works
The Cover Formatter Tool consists of three main classes:

**FFmpegConverter**: to convert images to a specific format (we use png, but sometimes, during the cover creation, I leave the default format, which is png).
By the way, this should not impact so much on the performance of the scripts, as it performs a check before converting: if same extension, it continues the flow.
**FFmpegScaler**: to scale images to a specific size using FFmpeg.
**Overlayer**: to overlay our frame on top of an image using OpenCV.
The main.py script uses these classes to format the images in the specified directory and, from now on, it also writes the episode number on the top-left corner of the final cover.

## FFmpegConverter
The FFmpegConverter class has two methods:

_get_media_format: Returns the format of a media file.
convert_image: Converts an image to a specific format using FFmpeg.
FFmpegScaler
The FFmpegScaler class has two methods:

_get_image_size: Returns the size of an image.
scale_image: Scales an image to a specific size using FFmpeg.

## Overlayer
The Overlayer class has two methods:

_read_image: Reads an image using OpenCV.
_read_frame: Reads a frame image using OpenCV.
overlay: Overlays a frame on top of an image using OpenCV.
The overlay method uses alpha compositing to blend the frame with the image.

## Episode number rendering

The tool automatically extracts the episode number from the input filename and renders it in the top-left corner with a readable outlined font. Examples of accepted filenames and the detected number:

- `PIC144.png`  -> `144`
- `144.jpg`     -> `144`
- `PIC144-ce.png` -> `144`
- `144-something.png` -> `144`

If no digits are present in the filename, no number will be drawn.

## Usage

Run the script using python main.py and pass the required arguments:
--images_dir: Path to the directory containing the images to format.
--frame_path: Path to the frame image to overlay on top of the formatted images.
Example:

```bash
python main.py --images_dir /path/to/images
```

Notes:
- Frame images are downloaded automatically from the repository of assets based on the detected tag in the filename (e.g., `PIC144-ce.png` uses frame `frame-ce.png`).
- The output covers are written to `public/covers/PIC{EPISODE}.png`.

## Custom font for the episode number (Pillow)

You can render the episode number using a custom `.otf`/`.ttf` font via Pillow. If a custom font is not provided or Pillow fails, the tool falls back to OpenCV's built‑in font.

CLI options:

- `--font_url`: HTTP(S) URL to a font file. The font will be downloaded to a temporary file and used.
- `--font_path`: Local path to a font file. If both `--font_url` and `--font_path` are provided, `--font_path` wins.

Examples (run from `utils/cover_formatter`):

```bash
# Install requirements (includes Pillow)
pip install -r requirements.txt

# Use the Courier 10 Pitch Regular from the assets repository (RAW URL)
python main.py --images_dir "../../raw/covers" \
  --font_url "https://raw.githubusercontent.com/valeriogalano/pensieriincodice-assets/refs/heads/main/fonts/Courier%2010%20Pitch%20Regular.otf"

# Alternatively, use a local font file
python main.py --images_dir "../../raw/covers" \
  --font_path "/path/to/Courier 10 Pitch Regular.otf"
```

Notes:
- Size and padding are scaled according to the cover dimensions (~3000px) and include a black outline for readability.
- If PIL/Pillow is unavailable or the font cannot be loaded, rendering automatically falls back to the OpenCV font without failing the pipeline.
