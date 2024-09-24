import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key
import os


genai.configure(api_key= api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_prompt = '''
As a highly skilled medical practitioner speciallizing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.
Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Finding Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured form.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: 'Consult with a Doctor before making any decisions.'
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide me an output response with these four headings Detailes analysis,Detailed Analysis,Finding Report,Recommendations and Next Steps,Treatment Suggestions.
'''


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-exp-0827",
    generation_config=generation_config
)


st.set_page_config(page_title='VitalImage Analytics', page_icon='robot')

st.image('logo.png', width=150)
st.title('Vital Image Analytics')
st.subheader('An Application that can help users to identify medical images')

uploaded_file = st.file_uploader('Upload the medical image for analysis', type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, width =250,caption = 'Uploaded Medical Image')
submit_button = st.button('Generate The Analysis')

if submit_button and uploaded_file is not None:
    image_data = uploaded_file.getvalue()
    image_parts = [
        {
            "mime_type": "image/jpeg",  
            "data": image_data
        }
    ]
    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]

    st.title('Here is the analysis based on your image')
    try:
        response = model.generate_content(prompt_parts)
        st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    if not uploaded_file:
        st.warning("Please upload a medical image before proceeding.")
