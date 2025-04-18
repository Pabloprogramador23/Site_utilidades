import streamlit as st
from streamlit_option_menu import option_menu
from crews.transcribe_and_analyze_app import transcrever_audio
from images._my_images import Image
from paginas.welcome import render_welcome
from paginas.post import render_post_page
from paginas.upload_pdf import render_upload_page
from paginas.download_video import render_download_page
from paginas.transcription_page import render_transcription_page
from paginas.extrair_topicos_radio import render_extrair_topicos_radio
from paginas.pesquisa_noticias import render_pesquisa_page



st.sidebar.image(
    Image.LOGO,
    use_container_width=True,
    width=200
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Agentic Platform",  # Título do menu
        options=["Home", "Post Agent", "Summary PDF", "Download Video", "Transcription", "Transcribe & Analyze", "Extract Radio Topics", "Pesquisa Caralho"],  # Adicionada nova opção
        icons=['house','file-earmark-text','cloud-upload','download','file-text'],
        menu_icon='robot',
        default_index=0,
        orientation="vertical" #teste com "horizontal"
    )

st.sidebar.image(
    Image.POWERED, 
    use_container_width=True,
    width=200
)


# Conteúdo baseado na opção selecionada
if selected == "Home":
    render_welcome()

elif selected == "Post Agent":
    render_post_page()

elif selected == "Summary PDF":
    render_upload_page()

elif selected == "Download Video":
    render_download_page()

elif selected == "Transcription":
    render_transcription_page()

elif selected == "Transcribe & Analyze":
    render_transcription_page

elif selected == "Extract Radio Topics":
    render_extrair_topicos_radio()

elif selected == "Pesquisa Caralho":
    render_pesquisa_page()

