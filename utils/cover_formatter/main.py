import os
import shutil
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


def clean_up(paths: list[str]):
    for a_path in paths:
        try:
            os.remove(a_path)
        except FileNotFoundError:
            pass


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
            cover_extension = str(cover).split(".")[-1]
            cover_path = f"{covers_dir}/{cover_name}.{cover_extension}"
            scaled_cover_path = (
                f"{covers_dir}/{cover_name}_scaled.{cover_extension}"
            )
            converted_cover_path = (
                f"{covers_dir}/{cover_name}_converted.{cover_extension}"
            )
            overlayed_cover_path = f"{covers_dir}/{cover_name}_final.{cover_extension}"

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
            clean_up([converted_cover_path, scaled_cover_path])
    finally:
        shutil.rmtree('tmp')


if __name__ == "__main__":
    main()
