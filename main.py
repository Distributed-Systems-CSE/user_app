import streamlit as st

def main():
    st.title("Welcome to SecureFileShare")
    st.write(
        "SecureFileShare is a secure and trusted distributed file storage system "
        "that allows you to store, manage, and retrieve your files with ease."
    )

    st.subheader("Features:")
    st.write(
        "- Securely store files on a distributed cluster of nodes\n"
        "- Retrieve files as a single entity regardless of chunk distribution\n"
        "- Validate file integrity using Merkle Tree or other techniques\n"
        "- User-friendly interface for managing files\n"
        "- Ability to list, search, view metadata, verify integrity, and download files"
    )

    st.subheader("Get Started:")
    st.write(
        "1. Upload your files to SecureFileShare\n"
        "2. View and manage your files in the dashboard\n"
        "3. Download files as needed\n"
        "4. Verify file integrity to ensure trustworthiness"
    )



    st.subheader("About Us:")
    st.write(
        "SecureFileShare is developed by the Department of CSE at the University of Moratuwa. "
        "For any inquiries or assistance, please contact XXXXXX"
    )

if __name__ == "__main__":
    main()
