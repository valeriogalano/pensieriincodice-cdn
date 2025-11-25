## How it works
The Cover Formatter Tool consists of three main classes:

**FFmpegConverter**: to convert images to a specific format (we use png, but sometimes, during the cob=ver creation, I leave the default format, which is png).
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

## O1verlayer
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
