from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import local_binary_pattern


RADIUS = 1
POINTS = 8


def calculate_lbp(grayscale_image):
    """Return the LBP image, code histogram, mean, and variance."""
    image = np.asarray(grayscale_image, dtype=np.uint8)
    lbp_image = local_binary_pattern(image, POINTS, RADIUS, method="default")
    histogram, _ = np.histogram(lbp_image, bins=256, range=(0, 256))
    return (
        np.clip(lbp_image, 0, 255).astype(np.uint8),
        histogram,
        float(np.mean(lbp_image)),
        float(np.var(lbp_image)),
    )


def save_lbp_histogram(histogram, output_path):
    """Save the LBP code-frequency plot as a PNG image."""
    output_path = Path(output_path)
    figure, axis = plt.subplots(figsize=(9, 3.5), constrained_layout=True)
    axis.bar(np.arange(256), histogram, width=1.0, color="#24786f")
    axis.set(xlabel="LBP code", ylabel="Frequency", xlim=(0, 255))
    axis.set_xticks(np.arange(0, 256, 32))
    axis.grid(axis="y", alpha=0.2)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)