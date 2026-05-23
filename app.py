import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# --- Logic from utils.py ---
def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    hue = hsvC[0][0][0]

    lower_limit = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8)
    upper_limit = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8)

    return lower_limit, upper_limit

# --- Video Processing Class ---
class ColorProcessor(VideoTransformerBase):
    def __init__(self):
        self.target_color = [0, 255, 255] # Yellow in BGR

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Flip image for a mirror effect
        img = cv2.flip(img, 1)

        # Get limits
        lower_limit, upper_limit = get_limits(self.target_color)

        # Convert to HSV and create mask
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_limit, upper_limit)

        # Remove noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(img, "Yellow Object", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return img

# --- Streamlit UI ---
st.set_page_config(page_title="Color Object Detection")
st.title("🟡 Real-time Yellow Object Detection")
st.write("This app uses your webcam to detect yellow objects using OpenCV.")

webrtc_streamer(key="color-detection", video_transformer_factory=ColorProcessor)
