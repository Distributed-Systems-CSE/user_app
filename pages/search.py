import streamlit as st
import requests
from tqdm import tqdm
import json

from utils.download import *
from utils.fileData import * 


with open('/Users/sanduninduwara/Desktop/Sem 8/Distributed/project/stremlit/pages/styles.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

all_files=getAllFileData()

with st.form('chat_input_form'):
    # Create two columns; adjust the ratio to your liking
    col1, col2 = st.columns([5,1]) 
    # Use the first column for text input
    with col1:
        prompt = st.text_input(label="adfaf", label_visibility='collapsed')
    # Use the second column for the submit button
    with col2:
        submitted = st.form_submit_button('Search')
    if submitted:
        # Do something with the inputted text here
        if prompt:
            st.write(f"You said: {prompt}")
            all_files=getSearchFile(prompt)
        else:
            all_files=getAllFileData()



with st.container():
        for key,val in all_files.items():
            c1, c2 = st.columns([5,1]) 
            with c1:
                st.markdown(f'<div class="item"><div class="file-name">File name: {val}</div></div>', unsafe_allow_html=True)
            # Use the second column for the submit button
            with c2:
                down_submitted = st.button(label="Download", key=f"button_{key}" )

            if down_submitted:
                st.write(f"You clicked download for file {key}")
                merkel_tree,chunk_map=getFileBlockData(key)
                download_file_with_progress("downloaded_file.zip", "1", chunk_map)



# col1, col2, col3 = st.columns(3)
# col1.write('cool column box 1')
# col2.write('cool column box 2')
# col3.write('cool column box 3')

