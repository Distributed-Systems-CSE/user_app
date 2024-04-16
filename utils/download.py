import os.path

import streamlit as st
import requests
from tqdm import tqdm
import json
from retrying import retry


def download_file_with_progress(file_name, chunk_map):
    current_chunk = 0
    total_chunks_count = len(chunk_map)
    progress_text = f"Operation in progress. {current_chunk}/{total_chunks_count}"
    my_bar = st.progress(0, text=progress_text)

    with open(os.path.join("downloads", file_name), 'wb') as f:
        for ch in chunk_map:
            url = f"http://{ch['node']}:5001/getChunk?hash={ch['hash']}"
            chunk_file = os.path.join("downloads", file_name, f"chunk_{ch['index']}")

            current_chunk += 1
            progress_text = f"Operation in progress. {current_chunk}/{total_chunks_count}"
            my_bar.progress(0, text=progress_text)

            # Send a GET request to the server to download the file with retry
            @retry(stop_max_attempt_number=3, wait_fixed=2000)
            def get_request_with_retry():
                response = requests.get(url, stream=True)
                return response

            response = None
            try:
                response = get_request_with_retry()
            except Exception as e:
                st.error(f"Failed to download chunk {ch['index']}. Error: {str(e)}")

            if response is not None:
                # Check if the request was successful
                if response.status_code == 200:
                    # Get the total file size in bytes
                    file_size = int(response.headers.get('content-length', 0))
                    # Initialize tqdm progress bar with total file size
                    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
                    # Open the local file in binary write mode

                    for chunk in response.iter_content(chunk_size=16*1024):
                        # Write the chunk to the file
                        f.write(chunk)
                        # Update the progress bar with the size of the downloaded chunk
                        progress_bar.update(len(chunk))
                        # Update the Streamlit progress bar
                        my_bar.progress(progress_bar.n / file_size, text=progress_text)
                    # Close the progress bar
                    # progress_bar.close()
                    # my_bar.empty()
                    my_bar.progress(100, text="complete ✅")
                else:
                    st.error(f"Failed to download chunk {ch['index']}. Status code: {response.status_code}")


# if __name__ == "__main__":
#     st.title("File Downloader")

#     x = '{ "1":"5000", "2":"5001", "3":"5002"}'
#     chunk_map = json.loads(x)
#     # Button to start download
#     if st.button("Download File"):
#         download_file_with_progress("downloaded_file.zip", "1", chunk_map)
