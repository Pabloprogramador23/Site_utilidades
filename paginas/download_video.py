import streamlit as st
from pathlib import Path
import os
import subprocess
from tqdm import tqdm
import time

class DownloadProgress:
    def __init__(self):
        self.pbar = None
        self.last_percent = 0

    def callback(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%')
            try:
                percent_float = float(percent.strip('%'))
                if self.pbar is None:
                    self.pbar = tqdm(total=100, desc='Baixando', 
                                   bar_format='{desc}: {percentage:3.1f}%|{bar}| {n_fmt}/{total_fmt}',
                                   position=0, leave=True)
                
                if percent_float > self.last_percent:
                    self.pbar.n = percent_float
                    self.pbar.refresh()
                    self.last_percent = percent_float
            except:
                pass
        elif d['status'] == 'finished' and self.pbar:
            self.pbar.close()

def baixar_com_ytdlp(link):
    try:
        temp_dir = Path(os.getcwd()) / "temp_downloads"
        temp_dir.mkdir(parents=True, exist_ok=True)

        saida = temp_dir / "%(title)s.%(ext)s"

        # Adicionando suporte a download segmentado
        comando = [
            "yt-dlp",
            "-f", "mp4",
            "--concurrent-fragments", "5",  # Define 5 fragmentos para download paralelo
            "-o", str(saida),
            link
        ]

        resultado = subprocess.run(comando, capture_output=True, text=True)

        if resultado.returncode != 0:
            raise Exception(f"Erro no download: {resultado.stderr}")

        arquivos_baixados = list(temp_dir.glob("*.mp4"))
        if not arquivos_baixados:
            raise Exception("Nenhum arquivo foi encontrado após o download.")

        return str(arquivos_baixados[0])

    except Exception as e:
        raise Exception(f"Erro ao baixar o vídeo: {str(e)}")

def render_download_page():
    st.title("Download de Vídeos")

    link = st.text_input("Insira o link do vídeo:")

    if st.button("Baixar"):
        if link:
            try:
                st.write("Iniciando o download...")
                with st.spinner("Baixando o vídeo, por favor aguarde..."):
                    caminho_arquivo = baixar_com_ytdlp(link)
                    time.sleep(1)  # Simula um pequeno atraso para feedback visual

                # Corrigir a definição de nome_arquivo
                nome_arquivo = os.path.basename(caminho_arquivo)

                # Gerar botão para download direto
                with open(caminho_arquivo, "rb") as file:
                    st.download_button(
                        label=f"Baixar {nome_arquivo}",
                        data=file,
                        file_name=nome_arquivo,
                        mime="video/mp4"
                    )

                # Remover o arquivo após o download
                os.remove(caminho_arquivo)

            except Exception as e:
                st.error(f"Erro: {str(e)}")
        else:
            st.warning("Por favor, insira um link válido.")