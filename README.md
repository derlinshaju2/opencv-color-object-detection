# 🟡 OpenCV Color Object Detection

A web-based computer vision tool that identifies specific color ranges (Yellow) in a real-time video stream.

## 🚀 How it works
1. **WebRTC Stream:** Captures video via browser-side webcam.
2. **HSV Conversion:** Converts BGR frames to HSV (Hue, Saturation, Value) for more accurate color isolation.
3. **Morphological Operations:** Uses `OPEN` and `CLOSE` filters to remove background noise.
4. **Contour Detection:** Draws bounding boxes around detected clusters.

## 🛠️ Tech Stack
- **Python**
- **OpenCV** (Image Processing)
- **Streamlit** (UI)
- **Streamlit-WebRTC** (Real-time Streaming)
