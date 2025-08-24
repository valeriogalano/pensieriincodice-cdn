from utils.cover_formatter.core.ffmpeg_handler import (
    FFmpegConverter,
    FFmpegScaler,
)
from utils.cover_formatter.core.overlayer import Overlayer
from utils.cover_formatter.core.z_logger import logger

import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument(
    "--images_dir", type=str, help="Path to the images directory"
)
argparser.add_argument("--frame_path", type=str, help="Path to the frame file")

covers_dir = argparser.parse_args().images_dir
frame_path = argparser.parse_args().frame_path

ffmpeg_scaler = FFmpegScaler()
ffmpeg_converter = FFmpegConverter()
overlayer = Overlayer()


def main():
    for cover in covers_dir:
        cover_name = cover.split("/")[-1].split(".")[0]
        cover_extension = cover.split(".")[-1]
        cover_path = f"{covers_dir}/{cover_name}.{cover_extension}"
        scaled_cover_path = (
            f"{covers_dir}/{cover_name}_scaled.{cover_extension}"
        )
        converted_cover_path = (
            f"{covers_dir}/{cover_name}_converted.{cover_extension}"
        )
        overlayed_cover_path = f"{covers_dir}/{cover_name}{cover_extension}"
        ffmpeg_scaler.scale_image(cover_path, 3000, 3000)
        logger.info("Cover %s scaled", cover_name)
        ffmpeg_converter.convert_image(scaled_cover_path, "png")
        logger.info("Cover %s converted", cover_name)
        overlayer.overlay(
            converted_cover_path, frame_path, overlayed_cover_path
        )
        logger.info("Cover %s formatted", cover_name)


if __name__ == "__main__":
    main()
