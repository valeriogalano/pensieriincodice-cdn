import cv2 as cv
from typing import Optional
from .z_logger import logger


class OpenCVConverter:
    def __init__(self) -> None:
        pass

    def _get_media_format(self, media_path: str) -> str:
        return media_path.split(".")[-1]

    def convert_image(self, image_path: str, extension: str) -> bool:
        img = cv.imread(image_path)
        if self._get_media_format(image_path) == extension:
            logger.info("Image already in %s format", extension)
            return False
        output_path = f"{image_path.split('.')[0]}.{extension}"

        img = cv.imread(image_path)
        cv.imwrite(output_path, img)
        return True


class OpenCVScaler:
    def __init__(self) -> None:
        pass

    def _get_image_size(self, image_path: str) -> "Optional[tuple]":
        image = cv.imread(image_path)
        if image is None:
            return None
        height, width, _ = image.shape
        return image, width, height

    def scale_image(self, image_path: str, output_path: str, width: int, height: int) -> bool:
        image, image_width, image_height = self._get_image_size(image_path)
        if (image_width, image_height) == (width, height):
            logger.info("Image size already %s x %s", width, height)
            return False

        resized = cv.resize(image, dsize=(width, height), interpolation=cv.INTER_CUBIC)
        cv.imwrite(output_path, resized)
        logger.info("Image scaled to %s x %s", width, height)
        return True
