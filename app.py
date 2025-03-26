import streamlit as st
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from util import set_background

set_background('./back.jpg')

# Azure credentials
endpoint = "https://ai-aihackthonhub282549186415.cognitiveservices.azure.com/"
key = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

# Initialize the client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Streamlit UI
st.title('Azure Medical Diagnosis')
st.write("Upload an image to analyze using Azure AI Vision API.")

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        # Read the image data
        image_data = uploaded_file.read()

        # Define visual features to analyze
        visual_features =[
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.READ,
            VisualFeatures.SMART_CROPS,
            VisualFeatures.PEOPLE,
        ]

        # Analyze the uploaded image
        result = client.analyze(
            image_data=image_data,
            visual_features=visual_features,
        )

        # Display results
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.write("### Image analysis results:")

        if result.caption:
            st.write(f"**Caption:** {result.caption.text} (Confidence: {result.caption.confidence:.4f})")

        if result.tags:
            st.write("**Tags:**")
            for tag in result.tags.list:
                st.write(f"• {tag.name} (Confidence: {tag.confidence:.4f})")

        if result.objects:
            st.write("**Objects:**")
            for obj in result.objects.list:
                st.write(f"• {obj.tags[0].name} (Confidence: {obj.tags[0].confidence:.4f})")

        if result.read:
            st.write("**Read (Text Detection):**")
            for line in result.read.blocks[0].lines:
                st.write(f"• {line.text}")

        if result.people:
            st.write("**People Detected:**")
            for person in result.people.list:
                st.write(f"• Confidence: {person.confidence:.4f}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image to proceed.")