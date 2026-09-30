const imageInput = document.getElementById("imageInput");
const fileName = document.getElementById("fileName");
const uploadForm = document.getElementById("uploadForm");
const clientError = document.getElementById("clientError");
const supportedExtensions = new Set(["jpg", "jpeg", "png", "bmp"]);

imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];
    clientError.hidden = true;
    clientError.textContent = "";
    fileName.textContent = file ? file.name : "No file selected";

    if (file) {
        const extension = file.name.split(".").pop().toLowerCase();
        if (!supportedExtensions.has(extension)) {
            clientError.textContent = "Please upload a valid image file.";
            clientError.hidden = false;
            imageInput.value = "";
            fileName.textContent = "No file selected";
        }
    }
});

uploadForm.addEventListener("submit", (event) => {
    if (!imageInput.files.length) {
        event.preventDefault();
        clientError.textContent = "Please select an image.";
        clientError.hidden = false;
    }
});