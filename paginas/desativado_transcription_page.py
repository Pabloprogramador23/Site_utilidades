import os
import time
import streamlit as st
import crews.escuta_radio_crew as escuta_radio_crew
import subprocess
from tools.audio_transcription_script import transcrever_audio_em_blocos as transcrever_audio


# Configuração do diretório temporário
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def render_transcription_page():
    st.title("Transcrição e Interpretação de Áudio")
    st.write("Faça upload de um arquivo MP3 para transcrever e interpretar o conteúdo.")

    uploaded_file = st.file_uploader("Escolha um arquivo MP3", type="mp3")

    if uploaded_file is not None:
        try:
            # Salvando o arquivo no diretório temporário
            temp_file_path = os.path.join(TEMP_DIR, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Upload realizado com sucesso: {uploaded_file.name}")
            st.info("Processando o áudio com agentes CrewAI")

            # Loader durante a execução da tarefa
            with st.spinner('Executando tarefas do Crew...'):
                # Chamar o script de transcrição para gerar o arquivo .txt
                try:
                    txt_path = transcrever_audio(temp_file_path)
                    st.success(f"Transcrição salva em: {txt_path}")

                    # Chamar a crew para interpretar o arquivo .txt
                    st.info("Interpretando o arquivo de transcrição...")
                    crew_instance = escuta_radio_crew.CrewTranscriptionAndInterpretation()
                    inputs = {"file_path": txt_path}
                    resultado = crew_instance.kickoff(inputs=inputs)

                    # Exibir o resultado da interpretação
                    st.text_area("Resultado da interpretação:", str(resultado), height=300)

                except Exception as e:
                    st.error(f"Erro durante a transcrição ou interpretação: {e}")

            # Opcional: remover o arquivo temporário após o processamento
            try:
                os.remove(temp_file_path)
            except Exception as e:
                st.warning(f"Não foi possível remover o arquivo temporário: {e}")

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")

