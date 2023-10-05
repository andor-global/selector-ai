import streamlit as st
import numpy as np
import io
from PIL import Image
import style_look_description_generator as prompt_generator
import style_look_picture_generator as picture_generator

def get_pil_image(file):
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    pil_image = Image.open(io.BytesIO(file_bytes))
    return pil_image


# Title of the web app
st.title("Personality Style App")

# Input window for textual description of personality
personality_description = st.text_area("Enter Textual Description of Personality")

# Initialize a list to store information about each uploaded picture
uploaded_files_info = []

# Upload form for reference pictures (moodboard or clothes)
st.subheader("Upload Reference Pictures")
uploaded_files = st.file_uploader("Upload one or more reference pictures", accept_multiple_files=True)

# Create a list of options for picture type (moodboard or clothes)
picture_types = ["Moodboard", "Clothes"]

# Loop through uploaded pictures and create dropdowns for each
if uploaded_files:
    st.write("Specify the type for each uploaded picture:")
    for file in uploaded_files:
        # Display filename with larger font and highlighting
        pil_image = get_pil_image(file)
        st.markdown(f"**{file.name}**")
        picture_type = st.selectbox(f"Select type for {file.name}", picture_types)
        uploaded_files_info.append({"file": pil_image, "type": picture_type})

# Input form for style look goal
style_goal = st.text_area("Enter Style Look Goal")

# Process button to generate style look description and picture
if st.button("Generate"):
    st.spinner("Generating...")  # Display a spinner

    with st.spinner('Wait for it...'):
        # Generate style look description and picture
        style_look_description = prompt_generator.generate_style_look_description(personality_description, style_goal, uploaded_files_info)
        style_look_image = picture_generator.generate_style_look_picture(style_look_description)
    st.success('Generated!')

    # Display the generated picture
    st.write("Generated Style Look Picture:")
    st.image(style_look_image, use_column_width=True)

