import io
from PIL import Image
import streamlit as st
import machine_learning.style_look_description_generator as prompt_generator
import machine_learning.style_look_picture_generator as picture_generator
from machine_learning import imgru, google_lenz_api


def get_bytes_image(file):
    file_bytes = bytearray(file.read())
    return file_bytes

st.markdown('<a href="https://selector-ai.onrender.com/"><img src="https://i.imgur.com/2ewASpg.jpg" width="700"></a>', unsafe_allow_html=True)

# Title of the web app
st.markdown('<h1 style="font-size: 24px;">Generate New Look With Selector AI</h1>', unsafe_allow_html=True)

# Gender
gender = st.selectbox("Select Gender", ["Male", "Female", "Non-binary"])

# Input form for age
age = st.selectbox(
    "Select Age Group",
    ["Infant (0-1 year)", "Toddler (2-4 yrs)", "Child (5-12 yrs)", "Teen (13-19 yrs)", "Adult (20-39 yrs)", "Middle Age Adult (40-59 yrs)", "Senior Adult (60+)"],
)

# Input form for personality description in 3-5 words
personality_description_example = "Outgoing, Creative, Adventurous"
personality_description_input = st.text_input("Describe Your Personality (3-5 words)", placeholder =personality_description_example)

# Input form for hair color
hair_color_example = "Brown"
hair_color = st.text_input("Hair Color", placeholder =hair_color_example)

# Input form for eye color
eye_color_example = "Blue"
eye_color = st.text_input("Eye Color", placeholder =eye_color_example)

# Input form for any other extra information needed for style
extra_info_example = "Loves retro fashion, prefers bright colors"
extra_info = st.text_area("Any Other Extra Information for Your Style", placeholder =extra_info_example)

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
        bytes_image = get_bytes_image(file)
        image = Image.open(io.BytesIO(bytes_image))
        st.image(image, width=70)
        st.markdown(f"**{file.name}**")
        picture_type = st.selectbox(f"Select type for {file.name}", picture_types)
        uploaded_files_info.append({"file": bytes_image, "type": picture_type})

# Input form for style look goal
style_goal_example = "Blind Date"
style_goal = st.text_area("Enter Style Look Goal", placeholder=style_goal_example)

# Process button to generate style look description and picture
if st.button("Generate"):
    #st.spinner("Generating...")  # Display a spinner

    #with st.spinner("Generating new look for you..."):
    with st.status("Downloading data..."):

        st.write("Gathering all input data...")
        references_descriptions = prompt_generator.generate_reference_images_description(uploaded_files_info)
        st.write("Gathering style look...")
        style_look_description = prompt_generator.generate_style_look_description(age, gender, personality_description_input, eye_color,\
            hair_color, extra_info, style_goal, references_descriptions)
        st.write("Generating final picture...")
        style_look_image = picture_generator.generate_style_look_picture(style_look_description)

        if style_look_image == None or style_look_description == "":
            st.error("Please, generate again!")
        else:
            st.success('Generated!')

            # Display the generated picture
            st.write("Generated Style Look Picture:")
            st.image(style_look_image, use_column_width=True)

            url = imgru.create_url(style_look_image)
            shopping_df = google_lenz_api.query(url)

            st.data_editor(
                shopping_df,
                column_config={
                    "pic": st.column_config.ImageColumn(
                        "Preview Image",
                    ),
                    "link": st.column_config.LinkColumn(
                        "Shops",
                    ),
                    "price": st.column_config.NumberColumn(
                        "Price (in USD)",
                        help="The price of the product in USD",
                        format="%d",
                    ),
                    "title": st.column_config.TextColumn(
                        "Title",
                    ),
                    "currency": st.column_config.TextColumn(
                        "Currency"
                    )
                },
                hide_index=True,
            )

