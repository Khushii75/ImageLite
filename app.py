#for streamlitt. 
import streamlit as st
import cv2
import numpy as np
import os

st.set_page_config(page_title="ImageLite", page_icon="📸")

st.title("📉 ImageLite – Image Size Reducer")
st.write("Upload an image, resize it, and download a compressed version.")

uploaded_file = st.file_uploader(
    "Upload Image", 
    type=["jpg", "jpeg", "png", "bmp", "tiff"]
)

if uploaded_file is not None:
    scale_percentage = st.slider(
        "Resize Percentage",
        min_value=10,
        max_value=100,
        value=50
    )

    # Convert uploaded file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

    new_width = int(img.shape[1] * scale_percentage / 100)
    new_height = int(img.shape[0] * scale_percentage / 100)

    output = cv2.resize(img, (new_width, new_height))

    ext = uploaded_file.name.lower().split('.')[-1]

    params = []
    if ext in ["jpg", "jpeg"]:
        params = [cv2.IMWRITE_JPEG_QUALITY, 40]
        out_name = "compressed.jpg"
    elif ext == "png":
        params = [cv2.IMWRITE_PNG_COMPRESSION, 9]
        out_name = "compressed.png"
    else:
        out_name = f"compressed.{ext}"

    cv2.imwrite(out_name, output, params)

    st.image(output, caption="Compressed Image", use_column_width=True)

    with open(out_name, "rb") as f:
        st.download_button(
            label="⬇️ Download Image",
            data=f,
            file_name=out_name,
            mime="image/jpeg"
        )

    st.success("Image resized & compressed successfully 🎉")