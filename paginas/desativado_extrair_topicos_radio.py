# arquivo: pages/extrair_topicos_radio.py

import streamlit as st

from crews.radio_topic_extractor import extrair_topicos


def render_extrair_topicos_radio():
    st.title("📻 Extração de Tópicos de Programa de Rádio")

    st.markdown("Cole a transcrição completa abaixo:")

    transcricao = st.text_area("Transcrição do Programa", height=400)

    if st.button("Extrair Tópicos"):
        if not transcricao.strip():
            st.warning("Por favor, cole uma transcrição válida.")
        else:
            with st.spinner("Analisando tópicos..."):
                resultado = extrair_topicos(transcricao)
            st.success("Tópicos extraídos com sucesso!")
            st.markdown("### 📝 Tópicos:")
            st.markdown(resultado)
