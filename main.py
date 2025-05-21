import streamlit as st
import requests
import json
from PIL import Image
import io

# Set up Azure Cognitive Services credentials
AZURE_ENDPOINT = "https://ai-aihackthonhub282549186415.cognitiveservices.azure.com/"
AZURE_API_KEY =  "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"
AZURE_API_URL = f"{AZURE_ENDPOINT}vision/v3.2/analyze"

# Define parameters for Azure Vision API
PARAMS = {
    "visualFeatures": "Tags,Description,Objects",
    "details": "",
    "language": "en",
}

# Streamlit UI
st.title("🩺 AI-Powered Medical Diagnosis Assistant")
st.write("Upload an X-ray or MRI scan for AI-based anomaly detection.")

# Upload Medical Image
uploaded_file = st.file_uploader("Upload a Medical Scan (X-ray, MRI, CT)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display Image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Medical Scan", use_column_width=True)

    # Convert image to binary format for API request
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_data = image_bytes.getvalue()

    # Send image to Azure API
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
        "Content-Type": "application/octet-stream",
    }

    #Hi this is just a testing for git

    try:
        response = requests.post(AZURE_API_URL, headers=headers, params=PARAMS, data=image_data)
        response.raise_for_status()
        result = response.json()
        st.write(result)

        # Display AI Results
        st.write("### AI Diagnosis Results:")

        # Image Description (if available)
        if "description" in result and "captions" in result["description"]:
            caption = result["description"]["captions"][0]
            st.write(f"**Diagnosis:** {caption['text']} (Confidence: {caption['confidence']:.4f})")

        # Detected Tags (Possible Conditions)
        if "tags" in result:
            st.write("**Detected Anomalies:**")
            for tag in result["tags"]:
                st.write(f"• {tag['name']} (Confidence: {tag['confidence']:.4f})")

        # Detected Objects (If relevant to fractures/tumors)
        if "objects" in result:
            st.write("**Detected Medical Objects:**")
            for obj in result["objects"]:
                st.write(f"• {obj['object']} (Confidence: {obj['confidence']:.4f})")

        # Medical Condition Assessment
        condition = caption['text'].lower()
        if "pneumonia" in condition:
            st.warning("⚠️ Possible signs of pneumonia detected. Consult a radiologist.")
        elif "fracture" in condition:
            st.warning("🦴 Fracture detected. Immediate medical attention is recommended.")
        elif "tumor" in condition:
            st.error("🔬 Suspicious tumor detected. Please consult a specialist.")
        else:
            st.success("✅ No major abnormalities detected. However, always consult a doctor.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Azure API: {e}")

else:
    st.info("Please upload a medical scan to proceed.")
