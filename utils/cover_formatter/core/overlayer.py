from typing import TYPE_CHECKING
from utils.cover_formatter.core.z_logger import logger


if TYPE_CHECKING:
    import numpy as np
    from typing import Optional

import cv2 as cv


class Overlayer:
    def __init__(self) -> None:
        pass

    def _read_image(self, image_path: str) -> "Optional[np.ndarray]":
        return cv.imread(image_path, cv.IMREAD_COLOR)

    def _read_frame(self, frame_path: str) -> "Optional[np.ndarray]":
        return cv.imread(frame_path, cv.IMREAD_UNCHANGED)

    def overlay(
        self, image_path: str, frame_path: str, output_path: str
    ) -> None:
        image = self._read_image(image_path)
        frame = self._read_frame(frame_path)
        b, g, r, a = cv.split(frame)
        # convert a (alpha channel) to float in [0.0, 1.0]
        alpha_mask = a / 255.0
        # Inverse of the alpha: where frame is opaque (1.0), this becomes 0.0
        # where frame is transparent (0.0), this becomes 1.0
        alpha_inv = 1.0 - alpha_mask
        # Rebuild a 3-channel BGR image from the split channels (drop alpha)
        frame_bgr = cv.merge((b, g, r))
        # For each B, G, R channel: blend using alpha compositing
        # result = (1 - alpha) * image + alpha * frame
        for c in range(3):
            image[:, :, c] = (
                alpha_inv * image[:, :, c] + alpha_mask * frame_bgr[:, :, c]
            )
        logger.info("Image overlayed with frawe.")
        cv.imwrite(output_path, image)
        cv.imwrite(output_path, image)
