# pages/Transcricao.py

import os
import whisper
import shutil
import textwrap
import streamlit as st
from pydub import AudioSegment
from crews.crew_analyzer import analisar_parte

# ========== CONFIG ==========
DURACAO_BLOCOS_MINUTOS = 15
MODELO_WHISPER = "tiny"
PASTA_TEMP = "audios_divididos"
ARQUIVO_TRANSCRICAO = "transcricao_completa.txt"
TAMANHO_BLOCO_TEXTO = 2000


def transcrever_audio(mp3_path: str) -> str:
    st.info("🔪 Cortando o áudio em blocos...")

    audio = AudioSegment.from_mp3(mp3_path)
    duracao_total_ms = len(audio)
    bloco_ms = DURACAO_BLOCOS_MINUTOS * 60 * 1000
    total_blocos = (duracao_total_ms + bloco_ms - 1) // bloco_ms

    os.makedirs(PASTA_TEMP, exist_ok=True)
    arquivos_blocos = []

    for i in range(total_blocos):
        inicio = i * bloco_ms
        fim = min((i + 1) * bloco_ms, duracao_total_ms)
        trecho = audio[inicio:fim]
        nome_parte = os.path.join(PASTA_TEMP, f"parte_{i+1:02d}.mp3")
        trecho.export(nome_parte, format="mp3")
        arquivos_blocos.append(nome_parte)

    st.success(f"✅ Total de blocos criados: {len(arquivos_blocos)}")

    modelo = whisper.load_model(MODELO_WHISPER)
    transcricao_total = ""

    for i, caminho in enumerate(arquivos_blocos, 1):
        st.write(f"📝 Transcrevendo parte {i}/{len(arquivos_blocos)}...")
        resultado = modelo.transcribe(caminho)
        transcricao_total += f"\n\n=== Parte {i} ===\n{resultado['text']}"

    with open(ARQUIVO_TRANSCRICAO, "w", encoding="utf-8") as f:
        f.write(transcricao_total.strip())

    shutil.rmtree(PASTA_TEMP)

    return transcricao_total.strip()


# ========== PÁGINA PRINCIPAL ==========
def render_transcription_page():
    st.title("🎙️ Transcrição e Análise de Áudio Jornalístico")

    uploaded_file = st.file_uploader("📤 Envie seu arquivo .mp3", type=["mp3"], key="transcribe_mp3_uploader")

    if uploaded_file:
        with st.spinner("📥 Salvando o arquivo..."):
            mp3_path = "temp_audio.mp3"
            with open(mp3_path, "wb") as f:
                f.write(uploaded_file.read())

        with st.spinner("🧠 Transcrevendo o áudio..."):
            texto_transcrito = transcrever_audio(mp3_path)

        st.success("✅ Transcrição concluída.")
        st.subheader("📄 Transcrição Completa:")
        st.text_area("Texto Transcrito:", texto_transcrito, height=300)

        with open(ARQUIVO_TRANSCRICAO, "r", encoding="utf-8") as f:
            conteudo_txt = f.read()

        st.download_button(
            "📥 Baixar transcrição em .txt",
            data=conteudo_txt,
            file_name="transcricao_programa.txt",
            mime="text/plain"
        )

        # Limpeza dos arquivos temporários após o download
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        if os.path.exists(ARQUIVO_TRANSCRICAO):
            os.remove(ARQUIVO_TRANSCRICAO)

# ===== CHAMADA PRINCIPAL DA PÁGINA =====
render_transcription_page()
