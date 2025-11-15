import os
import shutil
import subprocess
from pathlib import Path

import requests

from core.opencv_handler import OpenCVScaler, OpenCVConverter
from core.overlayer import Overlayer
from core.z_logger import logger

import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument(
    "--images_dir", type=str, help="Path to the images directory"
)

covers_dir = argparser.parse_args().images_dir

opencv_scaler = OpenCVScaler()
opencv_converter = OpenCVConverter()
overlayer = Overlayer()


def _dest_filename(cover_name: str) -> str:
    """Return destination filename without extension, ensuring single PIC prefix.

    Examples:
    - cover_name="PIC144" -> "PIC144"
    - cover_name="144" -> "PIC144"
    - cover_name="PIC144-ce" -> "PIC144-ce"
    - cover_name="144-ce" -> "PIC144-ce"
    """
    if cover_name.upper().startswith("PIC"):
        return cover_name
    return f"PIC{cover_name}"


def _dest_path_for_cover(cover_name: str) -> str:
    return f"../../public/covers/{_dest_filename(cover_name)}.png"


def is_already_processed(cover_name: str):
    """Check if the final destination file for this cover already exists."""
    return os.path.exists(_dest_path_for_cover(cover_name))


def download_frame(episode_tag: str):
    tag = ""
    if episode_tag != "untagged":
        tag = f"-{episode_tag}"
    frame_name = f"frame{tag}.png"

    url = f"https://raw.githubusercontent.com/valeriogalano/pensieriincodice-assets/main/covers/{frame_name}"
    frame_path = f"tmp/{frame_name}"
    r = requests.get(url)
    open(frame_path, 'wb').write(r.content)

    return frame_path


def main():
    os.makedirs("tmp", exist_ok=True)
    frame_path = {}

    try:
        extensions = ('*.png', '*.jpg')
        covers = []
        for ext in extensions:
            covers.extend(Path(covers_dir).glob(ext))

        for cover in covers:
            cover_name = str(cover).split("/")[-1].split(".")[0]

            # Compute destination path and skip if it already exists
            overlayed_cover_path = _dest_path_for_cover(cover_name)
            if os.path.exists(overlayed_cover_path):
                logger.info("Cover %s already processed (destination exists)", cover_name)
                continue

            cover_extension = str(cover).split(".")[-1]
            cover_path = f"{covers_dir}/{cover_name}.{cover_extension}"
            scaled_cover_path = (
                f"tmp/{cover_name}_scaled.{cover_extension}"
            )
            converted_cover_path = (
                f"tmp/{cover_name}_converted.png"
            )
            # Destination path (ensures no double PIC prefix)
            overlayed_cover_path = _dest_path_for_cover(cover_name)

            episode_tag = "untagged"
            if "-" in cover_name:
                episode_tag = cover_name.split("-")[1]

            if episode_tag not in frame_path.keys():
                frame_path[episode_tag] = download_frame(episode_tag)

            image_to_overlay = cover_path
            is_scaled = opencv_scaler.scale_image(cover_path, scaled_cover_path, 3000, 3000)
            if is_scaled:
                image_to_overlay = scaled_cover_path
                logger.info("Cover %s scaled", cover_name)
            else:
                logger.info("Cover %s no scaling needed", cover_name)

            is_converted = opencv_converter.convert_image(scaled_cover_path, "png")
            if is_converted:
                image_to_overlay = converted_cover_path
                logger.info("Cover %s converted", cover_name)
            else:
                logger.info("Cover %s no conversion needed", cover_name)

            overlayer.overlay(
                image_to_overlay,
                frame_path[episode_tag],
                overlayed_cover_path
            )
            logger.info("Cover %s formatted", cover_name)

            # Optimize resulting PNG with pngquant, if available
            try:
                def _pngquant_exists() -> bool:
                    # Prefer shutil.which but keep fallback to PATH execution
                    from shutil import which
                    return which("pngquant") is not None

                def _optimize_png(png_path: str) -> None:
                    if not _pngquant_exists():
                        logger.warning("pngquant non trovato: salto l'ottimizzazione della cover %s", cover_name)
                        return

                    optimized_tmp = f"tmp/{Path(png_path).stem}_optimized.png"
                    # Build pngquant command
                    cmd = [
                        "pngquant",
                        "--quality=60-80",
                        "--speed", "1",
                        "--strip",
                        "--skip-if-larger",
                        "--output", optimized_tmp,
                        "--",
                        png_path,
                    ]

                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    if result.returncode == 0 and os.path.exists(optimized_tmp):
                        try:
                            orig_size = os.path.getsize(png_path)
                            opt_size = os.path.getsize(optimized_tmp)
                            os.replace(optimized_tmp, png_path)  # atomic replace
                            saved_pct = (1 - (opt_size / orig_size)) * 100 if orig_size else 0
                            logger.info(
                                "Cover %s ottimizzata con pngquant: %.1f%% in meno (%d -> %d bytes)",
                                cover_name, saved_pct, orig_size, opt_size
                            )
                        except Exception as e:
                            logger.warning("Impossibile sostituire il PNG ottimizzato per %s: %s", cover_name, e)
                    else:
                        # pngquant return code 99 typically means file would be larger; keep original
                        if result.returncode not in (0, 99):
                            logger.warning(
                                "pngquant ha restituito codice %s per %s: %s",
                                result.returncode, cover_name, result.stderr.decode(errors="ignore")
                            )
                        # Clean up tmp file if it exists but wasn't used
                        if os.path.exists(optimized_tmp):
                            try:
                                os.remove(optimized_tmp)
                            except Exception:
                                pass

                _optimize_png(overlayed_cover_path)
            except Exception as e:
                # Never fail the whole pipeline for optimization
                logger.warning("Errore durante l'ottimizzazione della cover %s: %s", cover_name, e)
    finally:
        shutil.rmtree('tmp')


if __name__ == "__main__":
    main()
