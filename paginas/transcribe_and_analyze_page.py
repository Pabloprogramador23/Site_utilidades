import streamlit as st
import sys
import os

# Adiciona o diretório 'crews' ao sys.path para importar o app de transcrição
sys.path.append(os.path.join(os.path.dirname(__file__), '../crews'))

from crews import transcribe_and_analyze_app

def render_transcribe_and_analyze_page():
    # Executa o app de transcrição e análise diretamente
    transcribe_and_analyze_app  # O código já executa ao importar
