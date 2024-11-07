import streamlit as st
import requests
import google.generativeai as genai
# Configure Google Generative AI
genai.configure(api_key="AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA")

# Function to generate content
def generate_content(topic):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Write a detailed essay for my CAT Preparation.")
    return response.text
    st.text("Enter the summary of this passage in the textbox below")
    answer = st.textbox("Summary")
# Function to call AI model to correct the essay and provide feedback
def generate_corrections_and_feedback(essay_text):
    correction_prompt = f"Evaluate the summary of this essay, '{response.text}', and propose where I could have done better. Also grade my summary in terms of accuracyof thought: '{answer}'"
    
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
    
    if st.button("Generate Essay"):
        with st.spinner("Generating essay..."):
            generate_content(topic)
        
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
