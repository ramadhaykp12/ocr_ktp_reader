import easyocr
from PIL import Image
import re
import warnings
import pandas as pd
import streamlit as st
import numpy as np

warnings.filterwarnings("ignore")

# Buat reader bahasa Indonesia
reader = easyocr.Reader(['id'])

image_path = st.file_uploader("Unggah gambar KTP", type=["png", "jpg", "jpeg"])

if image_path is not None:
    img = Image.open(image_path)
    results = reader.readtext(np.array(img), detail=0)  # konversi ke array
    text = "\n".join(results)

# Jalankan OCR
def extract_field(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else "Tidak ditemukan"

nik = extract_field(r'NIK[:\s]*([0-9]{16})', text)
nama = extract_field(r'Nama[:\s]*(.+)', text)
alamat = extract_field(r'Alamat[:\s]*(.+)', text)
tanggal_lahir = extract_field(r'Tempat/Tgl Lahir[:\s]*(.+)', text)

st.title("Ekstraksi Data KTP dengan OCR")

if image_path is not None:
    st.image(img, caption="KTP yang diupload", use_container_width=True)
    st.subheader("Hasil Ekstraksi:")
    st.write(f"NIK: {nik}")
    st.write(f"Nama: {nama}")
    st.write(f"Alamat: {alamat}")
    st.write(f"Tempat/Tgl Lahir: {tanggal_lahir}")