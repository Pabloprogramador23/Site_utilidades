# transcribe_and_analyze_app.py

import os
import whisper
import streamlit as st
from pydub import AudioSegment
from crewai import Agent, Task, Crew, Process
import shutil
import textwrap

# ========= CONFIGURAÇÕES ==========
DURACAO_BLOCOS_MINUTOS = 15
MODELO_WHISPER = "tiny"
PASTA_TEMP = "audios_divididos"
ARQUIVO_TRANSCRICAO = "transcricao_completa.txt"
TAMANHO_BLOCO_TEXTO = 2000  # Número de caracteres por parte na análise


# ========= ETAPA 1: TRANSCRIÇÃO ==========
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

    # Salvar em .txt
    with open(ARQUIVO_TRANSCRICAO, "w", encoding="utf-8") as f:
        f.write(transcricao_total.strip())

    # Limpar arquivos temporários
    shutil.rmtree(PASTA_TEMP)

    return transcricao_total.strip()


# ========= ETAPA 2: ANALISAR UMA PARTE ==========
def analisar_parte(texto: str, indice: int) -> str:
    agente = Agent(
        role="Curador Jornalístico",
        goal="Identificar todos os assuntos discutidos no trecho da transcrição.",
        backstory=(
            "Você é um jornalista experiente e analista de programas de rádio. "
            "Seu trabalho é extrair os temas discutidos em cada parte da transcrição, mantendo a sequência cronológica."
        ),
        verbose=False,
        allow_delegation=False
    )

    tarefa = Task(
        description=(
            f"Abaixo está um trecho da transcrição de um programa jornalístico.\n"
            f"Identifique os temas abordados neste trecho {indice}.\n\n"
            "Transcrição:\n{transcricao}"
        ),
        expected_output="Lista de assuntos discutidos nesta parte.",
        agent=agente
    )

    crew = Crew(agents=[agente], tasks=[tarefa], process=Process.sequential)
    resultado = crew.kickoff(inputs={"transcricao": texto})
    return f"--- Parte {indice} ---\n{resultado.strip()}\n"


# ========= ETAPA 3: APP STREAMLIT ==========
#st.set_page_config(page_title="Analisador de Áudio Jornalístico", layout="centered")
st.title("🎙️ Análise de Programas de Rádio com IA")

uploaded_file = st.file_uploader("Faça upload de um arquivo .mp3", type=["mp3"])

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

    if st.button("🤖 Analisar Temas com IA"):
        st.info("🔍 Dividindo a transcrição para análise...")

        blocos = textwrap.wrap(conteudo_txt, TAMANHO_BLOCO_TEXTO)
        resultados = []

        for i, bloco in enumerate(blocos, 1):
            with st.spinner(f"Analisando parte {i}/{len(blocos)}..."):
                resultado = analisar_parte(bloco, i)
                resultados.append(resultado)

        resultado_final = "\n".join(resultados)

        st.subheader("📋 Temas Identificados em Ordem Cronológica:")
        st.text_area("Resultado da Análise:", resultado_final, height=500)

        st.download_button(
            "📥 Baixar análise em .txt",
            data=resultado_final,
            file_name="temas_identificados.txt",
            mime="text/plain"
        )
