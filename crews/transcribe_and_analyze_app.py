# transcribe_and_analyze_app.py

import os
import whisper
import streamlit as st
from pydub import AudioSegment
from crewai import Agent, Task, Crew, Process

# ========= CONFIGURAÇÕES ==========
DURACAO_BLOCOS_MINUTOS = 15       # Cada parte do áudio terá no máximo 15 minutos
MODELO_WHISPER = "tiny"           # Modelo Whisper usado ("tiny" = mais leve e rápido)
PASTA_TEMP = "audios_divididos"   # Onde os blocos temporários do áudio serão salvos


# ========= ETAPA 1: TRANSCRIÇÃO DO ÁUDIO ==========
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

    return transcricao_total.strip()


# ========= ETAPA 2: AGENTE + CREWAI ==========
def analisar_temas(texto_transcricao: str) -> str:
    agente = Agent(
        role="Curador Jornalístico",
        goal="Ler a transcrição de um programa de rádio e identificar todos os assuntos discutidos",
        backstory=(
            "Você é um jornalista experiente e analista de programas de rádio. "
            "Seu trabalho é extrair os principais temas discutidos, apresentando-os em uma lista clara e objetiva."
        ),
        verbose=True,
        allow_delegation=False
    )

    tarefa = Task(
        description=(
            "Abaixo está a transcrição de um programa de rádio jornalístico.\n"
            "Liste todos os assuntos e temas abordados no episódio.\n"
            "Use uma lista clara, separada por tópicos.\n\n"
            "Transcrição completa:\n{transcricao}"
        ),
        expected_output="Lista de todos os temas discutidos no programa de rádio.",
        agent=agente
    )

    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        process=Process.sequential
    )

    # 👇 Passando o texto via input e não embedado na description
    resultado = crew.kickoff(inputs={"transcricao": texto_transcricao})
    return resultado.strip()


# ========= ETAPA 3: APP STREAMLIT ==========
st.set_page_config(page_title="Analisador de Áudio Jornalístico", layout="centered")
st.title("🎙️ Análise de Programas de Rádio com IA")

uploaded_file = st.file_uploader("Faça upload de um arquivo .mp3", type=["mp3"])

if uploaded_file:
    with st.spinner("📥 Salvando o arquivo..."):
        mp3_path = os.path.join("temp_audio.mp3")
        with open(mp3_path, "wb") as f:
            f.write(uploaded_file.read())

    with st.spinner("🧠 Transcrevendo o áudio..."):
        texto_transcrito = transcrever_audio(mp3_path)

    with st.spinner("🤖 Analisando os temas do programa..."):
        temas = analisar_temas(texto_transcrito)

    # Mostrar e baixar resultado
    st.subheader("📋 Temas Identificados no Programa:")
    st.text_area("Resultado:", temas, height=400)

    st.download_button(
        "📥 Baixar resultado em .txt",
        data=temas,
        file_name="temas_programa.txt",
        mime="text/plain"
    )
