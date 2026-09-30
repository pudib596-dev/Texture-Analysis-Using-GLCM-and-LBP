import numpy as np
from skimage.feature import graycomatrix, graycoprops


DISTANCES = [1]
ANGLES = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]


def calculate_glcm(grayscale_image):
    """Build normalized, symmetric GLCMs for four directions."""
    image = np.asarray(grayscale_image, dtype=np.uint8)
    return graycomatrix(
        image,
        distances=DISTANCES,
        angles=ANGLES,
        levels=256,
        symmetric=True,
        normed=True,
    )


def extract_glcm_features(glcm):
    """Average standard GLCM properties across the four directions."""
    return {
        "Contrast": float(np.mean(graycoprops(glcm, "contrast"))),
        "Energy": float(np.mean(graycoprops(glcm, "energy"))),
        "Homogeneity": float(np.mean(graycoprops(glcm, "homogeneity"))),
        "Correlation": float(np.mean(graycoprops(glcm, "correlation"))),
        "Dissimilarity": float(np.mean(graycoprops(glcm, "dissimilarity"))),
    }