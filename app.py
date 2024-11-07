import streamlit as st
import requests
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyBzP_urPbe1zBnZwgjhSlVl-MWtUQMEqQA")

# Function to generate content
def generate_content(topic):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Write a detailed essay for my CAT Preparation. The topic is '{topic}'.")
    return response.text if response else "Failed to generate essay."

# Function to call AI model to correct the essay and provide feedback
def generate_corrections_and_feedback(essay_text, summary):
    correction_prompt = f"Evaluate the summary of this essay, '{essay_text}', and propose where I could have done better. Also grade my summary in terms of accuracy of thought: '{summary}'"
    headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}  # Add appropriate headers
    response = requests.post(
        "https://catprep.streamlit.app/v1/generate",
        headers=headers,
        json={"prompt": correction_prompt, "max_tokens": 300}
    )
    if response.status_code == 200:
        return response.json().get("text", "Failed to generate feedback.")
    else:
        return "Error: Could not connect to the AI model."

# Function to call AI model to generate a controversial topic
def generate_controversial_topic():
    prompt = "Generate a controversial topic for debate."
    headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}  # Add appropriate headers
    response = requests.post(
        "https://catprep.streamlit.app/v1/generate",
        headers=headers,
        json={"prompt": prompt, "max_tokens": 50}
    )
    if response.status_code == 200:
        return response.json().get("text", "Failed to generate topic.")
    else:
        return "Error: Could not connect to the AI model."

# Main Streamlit App
st.title("Essay Generator & Controversial Topic Tool")

# Dropdown to select functionality
option = st.selectbox("Choose a function:", ["Randomized Essay Writer", "Controversial Topic Generator"])

if option == "Randomized Essay Writer":
    st.header("Randomized Essay Writer")
    
    # Topic selection dropdown
    topic = st.selectbox("Choose a topic:", ["Philosophy", "Business and Economics", "Ethics", "Current Affairs"])
    
    if st.button("Generate Essay"):
        with st.spinner("Generating essay..."):
            essay_text = generate_content(topic)
        
        st.subheader("Essay")
        st.write(essay_text)
        
        st.subheader("Word Count")
        word_count_generated = len(essay_text.split())
        st.write(f"The generated essay contains **{word_count_generated}** words.")
        
        # Summary input for correction
        summary = st.text_area("Enter the summary of the essay for correction and feedback")
        
        if st.button("Correct and Suggest Improvements"):
            with st.spinner("Analyzing essay for corrections and feedback..."):
                corrections_feedback = generate_corrections_and_feedback(essay_text, summary)
                
            st.subheader("Corrections and Suggestions for Improvement")
            st.write(corrections_feedback)

elif option == "Controversial Topic Generator":
    st.header("Controversial Topic Generator")
    
    if st.button("Generate Topic"):
        topic = generate_controversial_topic()
        st.write(f"Controversial Topic: **{topic}**")
