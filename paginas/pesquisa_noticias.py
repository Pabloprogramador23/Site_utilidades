# app/pages/pesquisa_links.py

import streamlit as st
from crews.pesquisa_caralho import executar_em_lote
import tempfile
import os

def render_pesquisa_page():
    st.title("🔎 Buscar notícias para múltiplos clientes")

    input_clientes = st.text_area(
        "Cole aqui os nomes dos clientes (um por linha):",
        height=200,
        placeholder="Ex:\nPrefeitura de Fortaleza\niFood\nNubank"
    )

    if st.button("Pesquisar todos"):
        lista = [c.strip() for c in input_clientes.split("\n") if c.strip()]
        
        if not lista:
            st.warning("Por favor, informe pelo menos um cliente.")
        else:
            st.info(f"Iniciando busca para {len(lista)} clientes...")
            resultado_geral = executar_em_lote(lista)

            st.success("🔗 Resultados por cliente:")
            st.text_area("Resultado", resultado_geral, height=600)

            # Cria arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as f:
                f.write(resultado_geral)
                temp_file_name = f.name

            # Botão de download
            with open(temp_file_name, "rb") as file:
                st.download_button(
                    label="📥 Baixar relatório em .txt",
                    data=file,
                    file_name="relatorio_clientes.txt",
                    mime="text/plain"
                )

            # Apaga o arquivo temporário após o botão (pode ajustar o tempo com threading, se quiser)
            os.remove(temp_file_name)
