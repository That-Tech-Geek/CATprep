import streamlit as st
import requests

# Direct API key inclusion (for demonstration purposes; not recommended for production)
api_key = "AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA"

# Headers for API call
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Function to call AI model to generate an essay based on prompt and word count
def generate_randomized_essay(word_count):
    prompt = f"Write an essay of approximately {word_count} words on a random thought-provoking topic."
    
    # Updated endpoint based on the provided URL
    response = requests.post(
        "https://catprep.streamlit.app/v1/generate",  # Correct endpoint
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
    
    # Count the number of words in the generated essay
    word_count_generated = len(essay_text.split())
    
    return essay_text, word_count_generated

# Function to call AI model to correct the essay and provide feedback
def generate_corrections_and_feedback(essay_text):
    correction_prompt = f"Provide grammatical corrections, improvements, and feedback on this essay:\n\n{essay_text}"
    
    # Updated endpoint based on the provided URL
    response = requests.post(
        "https://catprep.streamlit.app/v1/generate",  # Correct endpoint
        headers=headers,
        json={
            "prompt": correction_prompt,
            "max_tokens": 300  # Adjust token count as needed
        }
    )
    
    if response.status_code == 200:
        corrections_feedback = response.json().get("text", "Failed to generate feedback.")
    else:
        corrections_feedback = "Error: Could not connect to the AI model."
    
    return corrections_feedback

# Function to call AI model to generate a controversial topic
def generate_controversial_topic():
    prompt = "Generate a controversial topic for debate."
    
    # Updated endpoint based on the provided URL
    response = requests.post(
        "https://catprep.streamlit.app/v1/generate",  # Correct endpoint
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
            essay_text, word_count_generated = generate_randomized_essay(word_count)
        
        st.subheader("Essay")
        st.write(essay_text)
        
        st.subheader("Word Count")
        st.write(f"The generated essay contains **{word_count_generated}** words.")
        
        if st.button("Correct and Suggest Improvements"):
            with st.spinner("Analyzing essay for corrections and feedback..."):
                corrections_feedback = generate_corrections_and_feedback(essay_text)
                
            st.subheader("Corrections and Suggestions for Improvement")
            st.write(corrections_feedback)

elif option == "Controversial Topic Generator":
    st.header("Controversial Topic Generator")
    
    if st.button("Generate Topic"):
        topic = generate_controversial_topic()
        st.write(f"Controversial Topic: **{topic}**")
