import hashlib
import os.path

import streamlit as st
import requests
from tqdm import tqdm
import json
from retrying import retry


def download_file_with_progress(file_name, file_info):
    chunk_map = file_info.get('chunks-info')
    current_chunk = 0
    total_chunks_count = len(chunk_map)
    progress_text = f"Operation in progress. {current_chunk}/{total_chunks_count}"
    my_bar = st.progress(0, text=progress_text)

    byte_stream = b""
    for ch in chunk_map:
        url = f"http://{ch['node']}:5001/getChunk?hash={ch['hash']}"

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

                chunk = response.content
                # filling chunk with zeros to make it 16KB
                chunk = chunk.ljust(16 * 1024, b'\0')
                # if chunk is greater than 16KB, truncate it
                chunk = chunk[:16 * 1024]
                byte_stream += chunk
                # Update the Streamlit progress bar
                my_bar.progress(current_chunk/total_chunks_count, text=progress_text)
                my_bar.progress(100, text="complete ✅")
            else:
                st.error(f"Failed to download chunk {ch['index']}. Status code: {response.status_code}")

    (mutated, mutated_chunk_ids) = verify_content(byte_stream, file_info.get('merkel-tree'))
    if mutated:
        st.error(f"Chunk files: {', '.join(mutated_chunk_ids)} is/are mutated")
    else:
        padding = file_info.get('padding-length')
        with open(os.path.join('downloads', file_name), 'wb') as f:
            f.write(byte_stream[:-padding])
        st.success("File downloaded successfully")


def verify_content(byte_stream, merkel_tree):
    """
    :param byte_stream:
    :param merkel_tree:
    :return: tuple(mutated, mutated_chunk_id)
    """
    if merkel_tree.get('root') == hashlib.sha256(byte_stream).hexdigest():
        return False, []
    elif merkel_tree.get('left_child') is None and merkel_tree.get('right_child') is None:
        if merkel_tree.get('root') != hashlib.sha256(byte_stream).hexdigest():
            return True, [merkel_tree.get('root')]
        else:
            return False, []
    else:
        mid = len(byte_stream) // 2
        left = verify_content(byte_stream[:mid], merkel_tree.get('left_child'))
        right = verify_content(byte_stream[mid:], merkel_tree.get('right_child'))
        return left[0] or right[0], [*left[1], *right[1]]

# if __name__ == "__main__":
#     st.title("File Downloader")

#     x = '{ "1":"5000", "2":"5001", "3":"5002"}'
#     chunk_map = json.loads(x)
#     # Button to start download
#     if st.button("Download File"):
#         download_file_with_progress("downloaded_file.zip", "1", chunk_map)
