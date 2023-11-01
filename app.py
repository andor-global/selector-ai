import io
import streamlit as st

from machine_learning import imgru, google_lenz_api

import requests
from PIL import Image
from io import BytesIO

from machine_learning.img2text import describe_image
from machine_learning.llava_model import get_style_look_description
from machine_learning.segmentation_model import get_clothes_images
from machine_learning.stable_diffusion_hf import generate_look


def get_image_bytes_from_url(url):
    try:
        response = requests.get(url)
        image_bytes = BytesIO(response.content)
        return image_bytes
    except Exception as e:
        print(f"An error occurred: {e}")

def get_bytes_image(file):
    file_bytes = bytearray(file.read())
    return file_bytes

st.markdown('<a href="https://genl.webflow.io/"><img src="https://i.imgur.com/8HFaK0v.jpg" width="700"></a>', unsafe_allow_html=True)

# Title of the web app
st.markdown('<h1 style="font-size: 24px;">Generate New Look</h1>', unsafe_allow_html=True)

# Gender
gender = st.selectbox("Select Gender", ["Female", "Male", "Non-binary"])

# Input form for age
age = st.selectbox(
    "Select Age Group",
    ["Child (5-12 yrs)", "Teen (13-19 yrs)", "Adult (20-39 yrs)", "Middle Age Adult (40-59 yrs)", "Senior Adult (60+)"],
)

# Input form for personality description in 3-5 words
personality_description_example = "Outgoing, Creative, Adventurous"
personality_description_input = st.text_input("Describe Your Personality (3-5 words)", placeholder =personality_description_example)
if personality_description_input == '':
    personality_description_input = personality_description_example

# Input form for hair color
hair_color_example = "Brown"
hair_color = st.text_input("Hair Color", placeholder =hair_color_example)
if hair_color == '':
    hair_color = hair_color_example

# Input form for any other extra information needed for style
extra_info_example = "Loves retro fashion, prefers bright colors"
extra_info = st.text_area("Any Other Extra Information for Your Style", placeholder =extra_info_example)
if extra_info == '':
    extra_info = extra_info_example

# Initialize variables to store the uploaded files
clothes_file = None
moodboard_file = None

# Upload form for clothes reference
st.subheader("Clothes")
clothes_file = st.file_uploader("Upload a clothes reference picture", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

# Process the uploaded files if they exist
if clothes_file is not None:
    bytes_image = get_bytes_image(clothes_file)
    image = Image.open(io.BytesIO(bytes_image))
    st.image(image, width=70)

# Upload form for moodboard
st.subheader("Moodboard")
moodboard_file = st.file_uploader("Upload a moodboard picture", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

# Process the uploaded files if they exist
if moodboard_file is not None:
    bytes_image = get_bytes_image(moodboard_file)
    image = Image.open(io.BytesIO(bytes_image))
    st.image(image, width=70)

# Input form for style look goal
style_goal_example = "Blind Date"
style_goal = st.text_area("Enter Style Look Goal", placeholder=style_goal_example)
if style_goal == '':
    style_goal = style_goal_example

# Process button to generate style look description and picture
if st.button("Generate"):
    with st.status("Downloading data."):

        st.write("Gathering all input info...")
        st.write("Observe moodboard...")
        moodboard_description = ''#describe_image(moodboard_file)
        print(moodboard_description)

        st.write("Analyzing provided info...")
        style_look_description = 'red dress with black shoes and blask wallet'#get_style_look_description(age, gender, personality_description_input,\
            #hair_color, extra_info, clothes_file, style_goal, moodboard_description)
        print("---------")
        print(style_look_description)

        if style_look_description == "":
            st.error("Please, generate again!")

        else:
            st.write("Generating style look....")
            style_look_image = generate_look(age, gender, hair_color, style_look_description)

            if style_look_image == None:
                st.error("Please, generate again!")
            else:
                st.success('Generated!')
                st.image(style_look_image, use_column_width=True)

                # Segment generated image
                cloth_images, cloth_classes = get_clothes_images(style_look_image)
                cloth_images_urls = [imgru.create_url(cloth_image) for cloth_image in cloth_images]

                for i, url in enumerate(cloth_images_urls):
                    st.write(cloth_classes[i])
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
