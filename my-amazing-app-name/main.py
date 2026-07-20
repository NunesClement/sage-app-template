from pathlib import Path

import cv2
import numpy as np

from waggle.plugin import Plugin


IMAGE_PATH = Path(__file__).with_name("example.jpg")


def compute_mean_color(image):
    return np.mean(image, (0, 1)).astype(float)


def main():
    image_bgr = cv2.imread(str(IMAGE_PATH))
    if image_bgr is None:
        raise FileNotFoundError(f"Could not read image: {IMAGE_PATH}")

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    mean_color = compute_mean_color(image_rgb)

    with Plugin() as plugin:
        plugin.publish("color.mean.r", mean_color[0])
        plugin.publish("color.mean.g", mean_color[1])
        plugin.publish("color.mean.b", mean_color[2])
        plugin.upload_file(str(IMAGE_PATH))


if __name__ == "__main__":
    main()
