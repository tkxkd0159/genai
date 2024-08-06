import os
import logging

from google.cloud import logging as cloud_logging
import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
import vertexai

# configure logging
logging.basicConfig(level=logging.INFO)

# ==== Need to get google cloud project id and region from environment variables ====

# attach a Cloud Logging handler to the root logger
log_client = cloud_logging.Client()
log_client.setup_logging()

PROJECT_ID = os.environ.get("PROJECT_ID")  # Your Cloud Project ID
LOCATION = os.environ.get("REGION")  # Your Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)


@st.cache_resource
def load_models():
    text_model_pro = GenerativeModel("gemini-pro")
    multimodal_model_pro = GenerativeModel("gemini-pro-vision")
    return text_model_pro, multimodal_model_pro


st.header("Vertex AI Gemini API", divider="rainbow")
text_model_pro, multimodal_model_pro = load_models()

# =====================================================================================

tab1, tab2, tab3, tab4 = st.tabs(
    ["Story", "Marketing Campaign", "Image Playground", "Video Playground"]
)

from story import render_story_tab

with tab1:
    render_story_tab()


from mktg_campaign import render_mktg_campaign_tab

with tab2:
    render_mktg_campaign_tab(text_model_pro)

from imganal import render_image_playground_tab

with tab3:
    render_image_playground_tab(multimodal_model_pro)

from videoe import render_video_playground_tab

with tab4:
    render_video_playground_tab(multimodal_model_pro)
