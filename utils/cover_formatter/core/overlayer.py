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

    def _draw_episode_number(self, img: np.ndarray, episode_number: str) -> None:
        """Draw the episode number in the top-left corner with an outline for readability."""
        if not episode_number:
            return

        h, w = img.shape[:2]
        # Scale font according to image size (tuned for ~3000px covers)
        # Previous sizing was too small and too close to the corner.
        # Increase scale and padding to better match the visual reference.
        base = max(h, w)
        # Raddoppia la grandezza del numero: ~17.0 su 3000px (prima ~8.5)
        font_scale = max(7.0, base / 175.0)
        # Spessore proporzionato alla nuova scala per mantenere l'effetto bold
        thickness = int(max(6, round(font_scale * 3.2)))
        font = cv.FONT_HERSHEY_SIMPLEX

        text = f"{episode_number}"

        # Padding from the top-left corner (spostato un po' più a destra)
        pad_x = int(max(100, base * 0.05))  # ~150px on 3000px
        pad_y = int(max(140, base * 0.065)) # ~195px on 3000px

        # For better alignment, get text size
        (text_w, text_h), baseline = cv.getTextSize(text, font, font_scale, thickness)
        org = (pad_x, pad_y + text_h)

        # Draw outline (black) – leggermente più spesso per mantenere contrasto
        cv.putText(img, text, org, font, font_scale, (0, 0, 0), thickness + 3, cv.LINE_AA)
        # Draw main text (white)
        cv.putText(img, text, org, font, font_scale, (255, 255, 255), thickness, cv.LINE_AA)

    def overlay(self, image_path: str, frame_path: str, output_path: str, episode_number: str | None = None) -> None:
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

        # Optionally draw episode number on top-left corner
        if episode_number:
            try:
                self._draw_episode_number(blended, episode_number)
            except Exception as e:
                logger.warning("Impossibile disegnare il numero episodio '%s': %s", episode_number, e)

        cv.imwrite(output_path, blended)
        logger.info("Image overlayed with frame.")
