from .z_logger import logger

import numpy as np
from typing import Optional

import cv2 as cv
try:
    from PIL import Image, ImageDraw, ImageFont
    _PIL_AVAILABLE = True
except Exception:
    # Pillow is optional; we fallback to OpenCV text if unavailable
    _PIL_AVAILABLE = False


class Overlayer:
    def __init__(self, font_path: Optional[str] = None) -> None:
        """Overlayer utility.

        font_path: optional path to a .otf/.ttf font to render the episode number.
                    If not provided or invalid, falls back to OpenCV builtin font.
        """
        self.font_path = font_path if font_path else None

    def _read_image(self, image_path: str) -> Optional[np.ndarray]:
        return cv.imread(image_path, cv.IMREAD_COLOR)

    def _read_frame(self, frame_path: str) -> Optional[np.ndarray]:
        return cv.imread(frame_path, cv.IMREAD_UNCHANGED)

    def _draw_episode_number(self, img: np.ndarray, episode_number: str) -> None:
        """Draw the episode number in the top-left corner (bold white, no outline)."""
        if not episode_number:
            return

        h, w = img.shape[:2]
        # Scale font according to image size (tuned for ~3000px covers)
        # Previous sizing was too small and too close to the corner.
        # Increase scale and padding to better match the visual reference.
        base = max(h, w)
        # Aumenta la grandezza del numero del 50%
        font_scale = 1.5 * max(7.0, base / 175.0)
        # Spessore proporzionato alla nuova scala per mantenere l'effetto bold
        thickness = int(max(6, round(font_scale * 3.2)))
        text = f"{episode_number}"

        # Padding from the top-left corner (move number even higher)
        pad_x = int(max(100, base * 0.05))   # ~150px on 3000px
        pad_y = int(max(90, base * 0.03))    # ~90px on 3000px (was ~135px)

        # If we have a font path and Pillow, use it for custom font rendering
        if self.font_path and _PIL_AVAILABLE:
            try:
                # Heuristic: map previous scale to a pixel font size
                # Increase size by 50% to make the number larger
                font_size = int(max(120, round((base / 6.8) * 1.5)))
                font = ImageFont.truetype(self.font_path, font_size)

                # Convert BGR OpenCV image to RGB PIL image
                pil_img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_img)

                # Measure text to align baseline similarly to OpenCV logic
                bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                org = (pad_x, pad_y)

                # Draw solid bold white text (no outline)
                draw.text(
                    org,
                    text,
                    font=font,
                    fill=(255, 255, 255),
                    stroke_width=0,
                )

                # Convert back to OpenCV BGR
                img[:, :, :] = cv.cvtColor(np.array(pil_img), cv.COLOR_RGB2BGR)
                return
            except Exception as e:
                logger.warning("PIL font rendering failed, fallback to OpenCV: %s", e)

        # Fallback: OpenCV builtin font
        font = cv.FONT_HERSHEY_SIMPLEX
        # For better alignment, get text size
        (text_w, text_h), baseline = cv.getTextSize(text, font, font_scale, thickness)
        org = (pad_x, pad_y + text_h)

        # Draw main text (white only, no black outline)
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
