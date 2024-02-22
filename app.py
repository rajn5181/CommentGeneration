import os
import openai
import streamlit as st
import base64
from io import BytesIO

# OpenAI API key
open_api_key = "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"
openai.api_key = open_api_key
os.environ["OPENAI_API_KEY"] = open_api_key

def getChatGPTresponse(input_code, custom_prompt):
    # Generate the response from ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert assistant with expertise in commenting on code"},
            {"role": "user", "content": f'Can you add comments to this class and return the class with comments make sure you generated the provided code?:\n TEXT: {input_code}'},
            {"role": "user", "content": custom_prompt}
        ],
        max_tokens=3000,
        temperature=0.01,
    )

    text = response['choices'][0]['message']['content'].strip()
    return text

# Function to save generated comments to a file
def save_to_file(response_text, file_name):
    with open(file_name, 'w') as file:   
        file.write(response_text)

st.set_page_config(page_title="Generate Code Comments",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Code Comments 🤖")
custom_prompt = st.text_area("Enter custom prompt","", height=50)

# Option to choose input method
input_method = st.selectbox("Choose Input Method:", ["Upload File", "Input Text"])

if input_method == "Upload File":
    # File upload
    uploaded_files = st.file_uploader("Upload code files", type=["cs", "py", "cpp", "java", "html", "js"], accept_multiple_files=True)

    if st.button("Generate"):
        for uploaded_file in uploaded_files:
            # Extract code from the uploaded file
            code_text = uploaded_file.read()
            file_extension = uploaded_file.name.split(".")[-1]

            if code_text.strip() != "":
                generated_response = getChatGPTresponse(code_text, custom_prompt)
                st.write(f"Generated Comments for {uploaded_file.name}:")
                st.code(generated_response, language='text')

                # Save generated comments to a file
                output_file_name = f"generated_comments.{file_extension}"
                save_to_file(generated_response, output_file_name)
                st.success(f"Generated comments saved to {output_file_name}")

                # Provide download link for the generated file
                st.markdown(f'<a href="data:application/octet-stream;base64,{base64.b64encode(generated_response.encode()).decode()}" download="{uploaded_file.name.replace(".", "_generated.")}">Download Generated Comments</a>', unsafe_allow_html=True)

else:
    # Input text area for code
    code_text = st.text_area("Enter Your code here", "", height=300)
    file_extension = "txt"

    if st.button("Generate") and code_text.strip() != "":
        generated_response = getChatGPTresponse(code_text, custom_prompt)
        st.write("Generated Comments:")
        # st.code(generated_response, language='text')
        st.text_area(generated_response,height=200)

        # Save generated comments to a file
        output_file_name = f"generated_comments.{file_extension}"
        save_to_file(generated_response, output_file_name)
        st.success(f"Generated comments saved to {output_file_name}")

        # Provide download link for the generated file
        st.markdown(f'<a href="data:application/octet-stream;base64,{base64.b64encode(generated_response.encode()).decode()}" download="generated_comments.{file_extension}">Download Generated Comments</a>', unsafe_allow_html=True)
