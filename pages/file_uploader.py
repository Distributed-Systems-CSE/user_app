import streamlit as st
import requests
import os

def upload_file_to_server(file, upload_url):
    # Send a POST request to the server to upload the file
    with open(os.path.join("downloads", file.name), 'wb') as f:
        f.write(file.getbuffer())

    with open(os.path.join("downloads", file.name), 'rb') as f:
        files = {'file': f}
        response = requests.post(upload_url, files=files)
        if response.status_code == 200:
            st.success("File uploaded successfully")
        else:
            st.error(f"Failed to upload file. Status code: {response.status_code}")
    os.remove(os.path.join("downloads", file.name))


st.title("File Uploader")

# Display a file uploader widget
uploaded_file = st.file_uploader("Choose a file")

# URL to upload the file to
upload_url = "http://127.0.0.1:5001/upload"

# Button to upload the file
if st.button("Upload File") and uploaded_file is not None:
    upload_file_to_server(uploaded_file, upload_url)
