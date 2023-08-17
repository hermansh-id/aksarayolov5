import streamlit as st
import torch
from PIL import Image
import configparser
import os

st.set_page_config(layout="wide")
# Load configuration from config.ini file
@st.cache_resource  # Cache the configuration to avoid repeated file reading
def load_configuration():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

config = load_configuration()

# Read YOLOv5 section from the configuration
yolov5_config = config["YOLOv5"]
model_path = yolov5_config.get("model_path")
device_str = yolov5_config.get("device")
output = yolov5_config.get("output")

# Load YOLOv5 model from path
@st.cache_resource  # Cache the model loading process
def load_yolov5_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, device=device_str, verbose=False)
    model.eval()  # Set the model to evaluation mode
    return model

model = load_yolov5_model()


# Function to perform object detection
def yolov5_object_detection(input_image):
    img = Image.open(input_image)
    model.conf = confidence_threshold
    results = model(img)  # Perform object detection
    output_name = os.path.join(output, input_image.name)
    results.render()  # Render bounding boxes in the image
    for idx, im in enumerate(results.ims):
        im_base64 = Image.fromarray(im)
        im_base64.save(output_name)
    return output_name

st.sidebar.title("Configuration")

# Add a slider for setting the confidence threshold
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.6, 0.01)

st.title("Aksara Jawa")

# Upload image using file uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.text("Original Image:")
        st.image(uploaded_image, use_column_width=True)

    # Perform object detection and display results
    output_name = yolov5_object_detection(uploaded_image)

    with col2:
        st.text("Image with Bounding Boxes:")

        # Display the processed image with bounding boxes using 100% width
        img_ = Image.open(output_name)
        st.image(img_, caption='Model Prediction(s)', use_column_width='always')
