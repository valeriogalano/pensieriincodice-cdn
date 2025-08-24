## How it works
The Cover Formatter Tool consists of three main classes:

**FFmpegConverter**: to convert images to a specific format (we use png, but sometimes, during the cob=ver creation, I leave the default format, which is png).
By the way, this should not impact so much on the performance of the scripts, as it performs a check before converting: if same extension, it continues the flow.
**FFmpegScaler**: to scale images to a specific size using FFmpeg.
**Overlayer**: to overlay our frame on top of an image using OpenCV.
The main.py script uses these classes to format the images in the specified directory.

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

## Usage

Run the script using python main.py and pass the required arguments:
--images_dir: Path to the directory containing the images to format.
--frame_path: Path to the frame image to overlay on top of the formatted images.
Example:

```bash
python main.py --images_dir /path/to/images --frame_path /path/to/frame.png
```
