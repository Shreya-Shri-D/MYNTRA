import numpy as np
import cv2
import streamlit as st
from PIL import Image

# Function to resize image to match frame dimensions
def resize_image(image, frame):
    return cv2.resize(image, (frame.shape[1], frame.shape[0]))

# Function to apply mask and overlay design on the original image
def apply_mask(original_image, design_image):
    # Convert original image to BGR format (if not already)
    main_frame = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)

    # Convert design image to BGR format (if not already)
    design = cv2.cvtColor(design_image, cv2.COLOR_RGB2BGR)

    # Convert main frame to HSV
    hsv = cv2.cvtColor(main_frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for blue color (adjust as needed)
    lower_blue = np.array([80, 50, 50])
    upper_blue = np.array([150, 255, 255])

    # Create masks for white and black areas based on HSV range
    mask_white = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_black = cv2.bitwise_not(mask_white)

    # Resize masks to match main_frame dimensions
    mask_black_resized = resize_image(mask_black, main_frame)
    mask_white_resized = resize_image(mask_white, main_frame)

    # Resize design image to match main_frame dimensions
    design_resized = resize_image(design, main_frame)

    # Create 3-channel masks
    mask_black_3CH = np.stack((mask_black_resized,) * 3, axis=-1)
    mask_white_3CH = np.stack((mask_white_resized,) * 3, axis=-1)

    # Perform bitwise operations
    dst3 = cv2.bitwise_and(mask_black_3CH, main_frame)
    dst3_wh = cv2.bitwise_or(mask_white_3CH, dst3)

    design_mask_mixed = cv2.bitwise_or(mask_black_3CH, design_resized)
    final_image = cv2.bitwise_and(design_mask_mixed, dst3_wh)

    return final_image

# Main Streamlit UI function
def main():
    page = st.sidebar.selectbox(
        "Select a page",
        ["Home", "Try On","Trendzy"]
    )

# Home Page Function
def home_page():
    st.title("Welcome to Virtual Trial Room!")
    st.write("Upload your original image and choose a T-Shirt design to try on.")

    uploaded_main_image = st.file_uploader("Upload Original Image", type=["jpg", "jpeg", "png"])
    if uploaded_main_image is not None:
        original_image = np.array(Image.open(uploaded_main_image))
        st.image(original_image, caption='Original Image', use_column_width=True)

        uploaded_design_image = st.file_uploader("Upload T-Shirt Design", type=["jpg", "jpeg", "png"])
        if uploaded_design_image is not None:
            design_image = np.array(Image.open(uploaded_design_image))
            st.image(design_image, caption='T-Shirt Design', use_column_width=True)

            if st.button('Try on'):
                final_image = apply_mask(original_image, design_image)
                final_image_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
                st.image(final_image_rgb, caption='Final Image with T-Shirt Design', use_column_width=True)



if __name__ == "__main__":
    main()
