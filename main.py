from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import cohere as ch
import cv2
import pytesseract
from PIL import Image
import io
import os
from query import answer_query
import time
from key import key as api_key

co = ch.ClientV2(api_key=api_key)
article_website = Flask(__name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in article_website.config["ALLOWED_EXTENSIONS"]
    )


@article_website.route("/")
def home():
    return render_template("index.html")


@article_website.route("/generate", methods=["POST"])
def answer_prompt():
    user_input = request.form.get("user_input")
    generated_text = answer_query(user_input)
    return render_template(
        "index.html", generated_text=generated_text, user_input=user_input
    )


@article_website.route("/upload", methods=["POST"])
def upload_image():
    # Check if an image file was uploaded in the request
    if "image" not in request.files:
        return render_template("index.html", image_text="No image provided.")

    # Get the image file from the request
    image_file = request.files["image"]
    image = Image.open(image_file)

    try:
        image_text = convert_image(image)
        if not image_text:
            raise ValueError("No text deteced in image.")
    except ValueError as e:
        # Pass the error message to the template
        return render_template("index.html", image_text=str(e))

    return render_template("index.html", image_text=image_text)


def convert_image(image):

    # Load the image
    user_image = np.array(image)

    # Convert to grayscale
    gray_image = cv2.cvtColor(user_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, threshold_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

    # Resize the image (optional, may improve accuracy)
    width = int(threshold_image.shape[1] * 1.5)
    height = int(threshold_image.shape[0] * 1.5)
    dim = (width, height)
    resized_image = cv2.resize(threshold_image, dim, interpolation=cv2.INTER_LINEAR)

    text = pytesseract.image_to_string(resized_image)

    response = answer_query(text)

    return response


if __name__ == "__main__":
    article_website.run(debug=True)
