import logging
import uuid
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from glcm_analysis import calculate_glcm, extract_glcm_features
from lbp_analysis import calculate_lbp, save_lbp_histogram


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
RESULTS_FOLDER = BASE_DIR / "results"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}
MAX_UPLOAD_BYTES = 16 * 1024 * 1024

UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULTS_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
logging.basicConfig(level=logging.INFO)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    uploaded_file = request.files.get("image")
    if uploaded_file is None or uploaded_file.filename == "":
        return render_template("index.html", error="Please select an image."), 400

    safe_filename = secure_filename(uploaded_file.filename)
    if not safe_filename or not allowed_file(safe_filename):
        return render_template(
            "index.html", error="Please upload a valid image file."
        ), 400

    image_id = uuid.uuid4().hex
    upload_path = UPLOAD_FOLDER / f"{image_id}_{safe_filename}"
    uploaded_file.save(upload_path)

    try:
        image_bytes = np.fromfile(upload_path, dtype=np.uint8)
        original_image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        if original_image is None:
            return render_template(
                "index.html", error="Please upload a valid image file."
            ), 400

        height, width = original_image.shape[:2]
        if width < 2 or height < 2:
            return render_template(
                "index.html", error="The image must be at least 2 pixels wide and high."
            ), 400

        grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        glcm = calculate_glcm(grayscale_image)
        glcm_features = extract_glcm_features(glcm)
        lbp_image, lbp_histogram, lbp_mean, lbp_variance = calculate_lbp(
            grayscale_image
        )

        output_names = {
            "original": f"{image_id}_original.png",
            "grayscale": f"{image_id}_grayscale.png",
            "lbp": f"{image_id}_lbp.png",
            "histogram": f"{image_id}_lbp_histogram.png",
        }
        output_images = (
            (original_image, output_names["original"]),
            (grayscale_image, output_names["grayscale"]),
            (lbp_image, output_names["lbp"]),
        )
        for image, filename in output_images:
            if not cv2.imwrite(str(RESULTS_FOLDER / filename), image):
                raise OSError("Could not save a generated image.")

        save_lbp_histogram(lbp_histogram, RESULTS_FOLDER / output_names["histogram"])
        return render_template(
            "results.html",
            filename=safe_filename,
            images=output_names,
            glcm_features=glcm_features,
            lbp_mean=lbp_mean,
            lbp_variance=lbp_variance,
        )
    except Exception:
        logging.exception("Image analysis failed")
        return render_template(
            "index.html", error="The image could not be processed. Please try another image."
        ), 400
    finally:
        upload_path.unlink(missing_ok=True)


@app.get("/results/<path:filename>")
def result_file(filename):
    return send_from_directory(RESULTS_FOLDER, filename)


@app.errorhandler(413)
def file_too_large(_error):
    return render_template(
        "index.html", error="The image is too large. Maximum upload size is 16 MB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)