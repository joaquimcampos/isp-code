#!/usr/bin/python3

import os
import cv2
import math
import subprocess
from typing import Final

import click
from PIL import Image

FPS: Final[int] = 50


def write_video(img_paths: list[str], video_path: str):
    """
    Writes frames to an mp4 video file
    :param file_path: Path to output video, must end with .mp4
    :param frames: List of PIL.Image objects
    :param fps: Desired frame rate
    """
    first_frame = Image.open(img_paths[0])
    w, h = first_frame.size

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(video_path, fourcc, FPS, (w, h))

    for img_path in img_paths:
        writer.write(cv2.imread(img_path))

    writer.release()

    print(f'Video written to {video_path}')


def main(filename: str, outdir: str, zoom_factor: int, duration: float) -> None:
    if not (filename.endswith('.png') or filename.endswith('.jpg')):
        raise ValueError('Only .png and .jpg images accepted.')

    if not os.path.isdir(outdir):
        os.umask(0)
        os.makedirs(outdir, mode=0o777, exist_ok=True)

    frames_total: int = int(FPS * duration)
    base_filename = filename.split('/')[-1].split('.')[0]

    im = Image.open(filename)
    img_paths: list[str] = []

    for i in range(frames_total):
        sub_size = [
            math.ceil(
                size *
                (1./zoom_factor * (frames_total - i)/frames_total +
                 1. * i/frames_total)
            )
            for size in im.size
        ]
        img_path = os.path.join(outdir, f"{base_filename}{i}.png")
        subprocess.run([
            "convert", filename,
            "-colorspace", "RGB",
            "-gravity", "Center",
            "-crop", f"{sub_size[0]}x{sub_size[1]}+0+0",
            "-resize", f"{im.size[0]}x{im.size[1]}!",  # noqa: W605
            img_path
        ])
        print(f'Saved image in {img_path}.')
        img_paths.append(img_path)

        # if i == 0:
        #     im_tmp = Image.open(img_path)
        #     im_tmp.show()

    print(f'images saved in {outdir}.')

    video_path = os.path.join(outdir, f"{base_filename}.mp4")
    write_video(img_paths, video_path)


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--outdir', type=str, default="./output", show_default=True)
@click.option('--zoom-factor', type=int, default=18, show_default=True)
@click.option('--duration', type=float, default=10, show_default=True,
              help="Duration of zoom out video in seconds")
def cli(filename: str, outdir: str, zoom_factor: int, duration: float):
    """Make zoom out video based on image."""
    main(filename, outdir, zoom_factor, duration)


if __name__ == "__main__":
    cli()
