import streamlit as st
import requests
import time

# Direct API key inclusion (NOT RECOMMENDED for production)
api_key = "AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA"

# Headers for API call
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Function to call AI model to generate an essay based on prompt and word count
def generate_randomized_essay(word_count):
    prompt = f"Write an essay of approximately {word_count} words on a random thought-provoking topic."
    
    # Placeholder for API call (replace URL with the actual endpoint)
    response = requests.post(
        "https://api.genai.google.com/v1/generate",  # Adjust the endpoint as per Gemini API documentation
        headers=headers,
        json={
            "prompt": prompt,
            "max_tokens": word_count * 2  # Adjust token count as needed
        }
    )
    
    if response.status_code == 200:
        essay_text = response.json().get("text", "Failed to generate essay.")
    else:
        essay_text = "Error: Could not connect to the AI model."
    
    questions = [
        "What is the main argument presented in the essay?",
        "Identify any supporting points provided.",
        "Are there counterarguments mentioned?"
    ]
    return essay_text, questions

# Function to call AI model to generate a controversial topic
def generate_controversial_topic():
    prompt = "Generate a controversial topic for debate."
    
    # Placeholder for API call (replace URL with the actual endpoint)
    response = requests.post(
        "https://api.genai.google.com/v1/generate",  # Adjust the endpoint as per Gemini API documentation
        headers=headers,
        json={
            "prompt": prompt,
            "max_tokens": 50  # Short response for a single topic
        }
    )
    
    if response.status_code == 200:
        topic = response.json().get("text", "Failed to generate topic.")
    else:
        topic = "Error: Could not connect to the AI model."
    
    return topic

# Main Streamlit App
st.title("Essay Generator & Controversial Topic Tool")

# Dropdown to select functionality
option = st.selectbox("Choose a function:", ["Randomized Essay Writer", "Controversial Topic Generator"])

if option == "Randomized Essay Writer":
    st.header("Randomized Essay Writer")

    # Inputs for essay writer
    word_count = st.slider("Select word count for the essay:", min_value=100, max_value=1000, step=50)
    
    if st.button("Generate Essay"):
        with st.spinner("Generating essay..."):
            essay_text, questions = generate_randomized_essay(word_count)
            
        st.subheader("Essay")
        st.write(essay_text)
        
        st.subheader("Reflection Questions")
        for question in questions:
            st.write(f"- {question}")

elif option == "Controversial Topic Generator":
    st.header("Controversial Topic Generator")
    
    if st.button("Generate Topic"):
        topic = generate_controversial_topic()
        st.write(f"Controversial Topic: **{topic}**")
