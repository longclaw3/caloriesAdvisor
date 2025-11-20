import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini AI response
def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content([input_prompt, image])
        return response.text
    except Exception as e:
        return f"⚠️ Error while generating response: {e}"

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError("No image uploaded")

# Streamlit Page Configuration
st.set_page_config(page_title="Calories Advisor App", page_icon="🍎")
st.title("🍎 Calories Advisor App")
st.write("Upload a food image and get AI-based calorie and nutrition analysis.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Nutritionist prompt
input_prompt = """
You are an expert nutritionist. Analyze the food items from the image, 
calculate the total calories, and provide a breakdown as follows:

1. Item 1 - No of calories
2. Item 2 - No of calories
---
Finally, indicate whether the food is healthy or not. 
Also, provide a percentage split of carbohydrates, fats, fibers, sugar, and other essential nutrients.
"""

# Submit button
if st.button("🔍 Analyze Image"):
    if uploaded_file:
        with st.spinner("Analyzing image... Please wait ⏳"):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data)
                st.success("✅ Analysis Complete!")
                st.subheader("AI Nutrition Report")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please upload an image first.")
