# Texture Analysis Using GLCM and LBP

## Introduction
This web application analyzes image texture using the Gray-Level Co-occurrence Matrix (GLCM) and Local Binary Pattern (LBP). HTML and CSS provide the pages, while Flask connects the upload form to Python image-processing code.

## Objective
Upload a JPG, JPEG, PNG, or BMP image and display its original and grayscale versions, calculated GLCM features, an LBP image, an LBP histogram, and LBP statistics. All image processing and feature calculations run in Python.

## Features
- Accepts JPG, JPEG, PNG, and BMP images up to 16 MB
- Converts the uploaded image to grayscale with OpenCV
- Calculates five GLCM features and LBP statistics in Python
- Generates grayscale, LBP, and LBP histogram images
- Removes uploaded source files after processing

## Technologies Used
- HTML and CSS for the website
- Small JavaScript interactions for file selection and form validation
- Flask for the web server
- OpenCV and NumPy for image reading, grayscale conversion, and arrays
- scikit-image for GLCM and LBP
- Matplotlib for the LBP histogram
- Pillow for image-format support

## Project Structure
```text
Texture-Analysis-GLCM-LBP/
├── app.py
├── glcm_analysis.py
├── lbp_analysis.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── results.html
├── .gitignore
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── uploads/
│   └── .gitkeep
└── results/
	└── .gitkeep
```

Generated result images and uploaded source files are ignored by Git. The `.gitkeep` files preserve the empty folders in the repository.

## How the Project Works
1. The user selects an image in the HTML form.
2. Flask validates the file type and reads the image with OpenCV.
3. OpenCV converts the image to grayscale.
4. Python calculates GLCM and LBP features and saves the result images.
5. Flask sends the calculated values and image paths to the results template.

## GLCM
The Gray-Level Co-occurrence Matrix records how often pairs of gray levels occur at a chosen distance and direction. This project uses distance 1 and angles 0, 45, 90, and 135 degrees. scikit-image calculates the features for each direction, and the displayed values are averaged across all four.

## Contrast
Contrast measures the squared intensity difference between neighboring pixel pairs. Larger differences contribute more to the value.

## Energy
Energy is the square root of the angular second moment. It describes how concentrated the gray-level pair distribution is.

## Homogeneity
Homogeneity measures how close gray-level pairs are to the diagonal of the GLCM. Similar neighboring values contribute more.

## Correlation
Correlation describes the relationship between the gray levels in neighboring pixel pairs.

## Dissimilarity
Dissimilarity measures the absolute intensity difference between neighboring pixels.

## LBP
Local Binary Pattern compares each pixel with eight neighbors at radius one. It produces an LBP image and a histogram of the 256 possible codes. The application reports the mean and variance of the LBP image. Matplotlib saves the histogram as an image.

## Installation
Use Python 3.10 or newer. From the project directory, create and activate a virtual environment if desired, then install the dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the Project
From the project directory, start the Flask server:

```bash
python app.py
```

Open `http://127.0.0.1:5000`, choose an image, and select **Analyze Image**. This built-in Flask server is intended for local development.

## Expected Output
The results page shows the uploaded image, its grayscale conversion, a GLCM table with five calculated features, an LBP image, an LBP histogram, and the LBP mean and variance. It does not classify or interpret the texture.

## Applications
Texture features can support experiments in medical imaging, fingerprint analysis, remote sensing, and surface inspection. This project demonstrates the calculations and does not provide a diagnostic or classification system.

## Limitations
GLCM values can change with image brightness, noise, and orientation. The fixed LBP radius captures local patterns and may not represent larger textures. Very large uploads are limited to control server memory use.

## Future Improvements
- Add controls for GLCM directions, distance, and LBP radius
- Add automated tests for more image sizes and edge cases
- Improve handling of very large images

## Conclusion
The project combines a simple Flask website with Python-based GLCM and LBP analysis. It keeps the image-processing logic out of JavaScript and displays only calculated results and generated images.
