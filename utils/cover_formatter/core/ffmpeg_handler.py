from typing import TYPE_CHECKING

import cv2 as cv
import os


if TYPE_CHECKING:
    from typing import Optional

from utils.cover_formatter.core.z_logger import logger


def check_ffmpeg_is_installed() -> bool:
    os.system("ffmpeg -version")
    if os.system("ffmpeg -version") == 0:
        return True
    else:
        logger.error("FFmpeg is not installed.")
        return False


class FFmpegConverter:
    def __init__(self) -> None:
        pass

    def _get_media_format(self, media_path: str) -> str:
        return media_path.split(".")[-1]

    def convert_image(self, image_path: str, extension: str) -> bool:
        if self._get_media_format(image_path) == extension:
            logger.info("Image already in %s format", extension)
            return False
        output_path = f"{image_path.split('.')[0]}.{extension}"
        os.system(f"ffmpeg -i {image_path} -f {extension} {output_path}")
        return True


class FFmpegScaler:
    def __init__(self) -> None:
        pass

    def _get_image_size(self, image_path: str) -> "Optional[tuple]":
        image = cv.imread(image_path)
        if image is None:
            return None
        height, width, _ = image.shape
        return width, height

    def scale_image(self, image_path: str, width: int, height: int) -> bool:
        if self._get_image_size(image_path) == (width, height):
            logger.info("Image size already %s x %s", width, height)
            return False
        os.system(
            f"ffmpeg -i {image_path} -vf scale={width}:{height} {image_path}"
        )
        logger.info("Image scaled to %s x %s", width, height)
        return True
