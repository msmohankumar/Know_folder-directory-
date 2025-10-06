# app.py
import os
import json
import streamlit as st

def folder_to_dict(path):
    """Recursively create a dictionary representing folder structure."""
    folder_dict = {"name": os.path.basename(path), "type": "folder", "children": []}
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                folder_dict["children"].append(folder_to_dict(item_path))
            else:
                folder_dict["children"].append({"name": item, "type": "file"})
    except PermissionError:
        pass  # Skip folders/files you cannot access
    return folder_dict

# --- Streamlit UI ---
st.title("Folder to JSON Generator 📁➡️📄")

folder_path = st.text_input("Enter folder path to scan:")

if st.button("Generate JSON"):
    if not folder_path:
        st.error("Please enter a folder path!")
    elif not os.path.exists(folder_path):
        st.error("The path does not exist!")
    else:
        st.info("Scanning folder... this may take a few seconds.")

        folder_structure = folder_to_dict(folder_path)

        # Convert to JSON string
        json_data = json.dumps(folder_structure, indent=4)

        # Provide download button
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="folder_structure.json",
            mime="application/json"
        )

        st.success("JSON ready! Click the button above to download.")
