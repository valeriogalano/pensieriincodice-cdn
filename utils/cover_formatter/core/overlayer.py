from .z_logger import logger

import numpy as np
from typing import Optional

import cv2 as cv


class Overlayer:
    def __init__(self) -> None:
        pass

    def _read_image(self, image_path: str) -> Optional[np.ndarray]:
        return cv.imread(image_path, cv.IMREAD_COLOR)

    def _read_frame(self, frame_path: str) -> Optional[np.ndarray]:
        return cv.imread(frame_path, cv.IMREAD_UNCHANGED)

    def overlay(self, image_path: str, frame_path: str, output_path: str) -> None:
        image = self._read_image(image_path)
        frame = self._read_frame(frame_path)

        if image is None or frame is None:
            logger.error("Could not read image or frame")
            return

        b, g, r, a = cv.split(frame)
        frame_bgr = cv.merge((b, g, r))

        alpha_mask = (a / 255.0)[:, :, None]
        alpha_inv = 1.0 - alpha_mask

        blended = (alpha_inv * image + alpha_mask * frame_bgr).astype(np.uint8)

        cv.imwrite(output_path, blended)
        logger.info("Image overlayed with frame.")
