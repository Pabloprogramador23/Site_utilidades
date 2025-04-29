import streamlit as st

def render_welcome():
    st.title("🤖 Bem-vindo Agentic Platform do Pablo!")
    st.write("""
Esta plataforma reúne diversas utilidades para automação e análise de dados jornalísticos e de mídia, utilizando **Streamlit** e **CrewAI**. Explore as funcionalidades disponíveis no menu lateral:

- **Post Agent:** Crie e gerencie postagens automaticamente com agentes de IA.
- **Summary PDF:** Faça upload de arquivos PDF para obter um resumo gerado por IA.
- **Download Video:** Baixe vídeos a partir de links fornecidos.
- **Transcription:** Transcreva e interprete áudios em MP3 usando agentes especializados.
- **Transcribe & Analyze:** Faça upload de um áudio MP3 para transcrição e análise automática dos temas abordados.
- **Extract Radio Topics:** Extraia tópicos principais a partir da transcrição de programas de rádio.
- **Pesquisa Caralho:** Busque notícias em massa para múltiplos clientes e gere relatórios.

Sinta-se à vontade para explorar cada utilidade!
""")
    st.markdown("""
---
Desenvolvido por [Pablo Magalhães](https://github.com/pablopromgramador23).
""")
