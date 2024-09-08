import cv2
import mediapipe as mp
import os
import numpy as np
import streamlit as st
from PIL import Image

def virtual_try_on():
    # Initialize MediaPipe pose detection
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Load shirt images from the folder
    shirtFolderPath = "Resources/Dress"
    listShirts = os.listdir(shirtFolderPath)

    # Default scaling factor
    default_scaling_factor = 1.6

    # Specific scaling factor for certain shirts
    special_scaling_factor = 3

    # Offset to move the shirt up
    offset_factor = 1

    # Function to load and resize the selected shirt image while maintaining aspect ratio
    def load_and_scale_shirt(image_number, shoulder_width, torso_height):
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[image_number]), cv2.IMREAD_UNCHANGED)
        
        # Determine the scaling factor to use
        shirt_filename = listShirts[image_number]
        if shirt_filename in ["4.png", "7.png", "8.png"]:
            scaling_factor = special_scaling_factor
        else:
            scaling_factor = default_scaling_factor

        # Calculate the aspect ratio of the shirt
        shirt_aspect_ratio = imgShirt.shape[0] / imgShirt.shape[1]

        # Resize the shirt based on shoulder width, maintaining the aspect ratio
        new_shirt_width = int(shoulder_width * scaling_factor)
        new_shirt_height = int(new_shirt_width * shirt_aspect_ratio)

        # If the shirt height exceeds torso height, scale down to fit torso
        if new_shirt_height > torso_height:
            new_shirt_height = int(torso_height * scaling_factor)
            new_shirt_width = int(new_shirt_height / shirt_aspect_ratio)

        # Resize the shirt image
        resized_shirt = cv2.resize(imgShirt, (new_shirt_width, new_shirt_height))

        return resized_shirt

    # Streamlit app
    st.title('Virtual Try-On')

    # Initialize session state
    if 'webcam_running' not in st.session_state:
        st.session_state.webcam_running = False
    if 'selected_shirt' not in st.session_state:
        st.session_state.selected_shirt = 0

    # Define the width for the images
    image_width = 150
    row_spacing = 20  # Space between rows

    # Display all shirts for selection
    num_shirts = len(listShirts)
    num_columns = min(num_shirts, 4)  # Display shirts in up to 4 columns
    cols = st.columns(num_columns)

    for row in range(0, num_shirts, num_columns):
        for i in range(row, min(row + num_columns, num_shirts)):
            shirt = listShirts[i]
            img = Image.open(os.path.join(shirtFolderPath, shirt)).resize((image_width, int(image_width * 1.5)))  # Resize images to avoid large display
            with cols[i % num_columns]:  # Display in columns
                if st.button(f'Try me!', key=f'dress_{i}'):
                    st.session_state.selected_shirt = i
                    st.session_state.webcam_running = True
                st.image(img, caption=f'Dress {i+1}')
        st.write("")  # Add space between rows

    # Handle webcam stream
    if st.session_state.webcam_running:
        cap = cv2.VideoCapture(0)

        # Display webcam feed
        stframe = st.empty()

       

        # Desired frame width (you can change this based on how small or large you want the webcam feed)
        desired_width = 300
        desired_height = 300

        while st.session_state.webcam_running:
            ret, frame = cap.read()
            if not ret:
                st.session_state.webcam_running = False
                cap.release()
                cv2.destroyAllWindows()
                st.write("Webcam feed stopped.")
                break

            frame = cv2.resize(frame, (desired_width, desired_height))

            # Flip the frame horizontally for a more natural selfie view
            frame = cv2.flip(frame, 1)

            # Convert the frame to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform pose estimation
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                # Get landmark positions for shoulders (11, 12) and hips (23, 24)
                landmarks = results.pose_landmarks.landmark
                lm11 = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                lm12 = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                lm23 = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                lm24 = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

                # Calculate shoulder width and torso height
                shoulder_width = int(((lm11.x - lm12.x) ** 2 + (lm11.y - lm12.y) ** 2) ** 0.5 * frame.shape[1])
                torso_height = int(((lm11.y - lm23.y) ** 2 + (lm12.y - lm24.y) ** 2) ** 0.5 * frame.shape[1] / 2)

                # Load and scale the selected shirt based on the body dimensions
                imgShirt = load_and_scale_shirt(st.session_state.selected_shirt, shoulder_width, torso_height)

                # Calculate the midpoint for positioning the shirt
                midpoint_x = int((lm11.x + lm12.x) * frame.shape[1] / 2)
                y_offset = int(min(lm11.y, lm12.y) * frame.shape[1]) - int(shoulder_width * offset_factor)  # Move the shirt up

                # Overlay the shirt image at the calculated position
                try:
                    for i in range(imgShirt.shape[0]):
                        for j in range(imgShirt.shape[1]):
                            if imgShirt[i, j, 3] != 0:  # Check if the pixel is not transparent
                                frame[y_offset + i, midpoint_x - imgShirt.shape[1] // 2 + j] = imgShirt[i, j, :3]
                except:
                    pass

            # Convert the result frame to display in Streamlit
            result_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            stframe.image(result_image, caption='Virtual Try-On Result', use_column_width=True)

        # Add a button to stop webcam stream
        if st.button('Stop Webcam', key='stop_webcam'):
            st.session_state.webcam_running = False
            cap.release()
            cv2.destroyAllWindows()

