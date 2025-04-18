import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_TEMP = os.path.join(BASE_DIR, "temp")
PASTA_AUDIOS_DIVIDIDOS = os.path.join(PASTA_TEMP, "audios_divididos")
TEMP_DOWNLOADS = os.path.join(BASE_DIR, "temp_downloads")
TEMP_AUDIO = os.path.join(BASE_DIR, "temp_audio.mp3")

def limpar_pasta_temp(pasta_temp):
    if os.path.exists(pasta_temp):
        for arquivo in os.listdir(pasta_temp):
            caminho = os.path.join(pasta_temp, arquivo)
            try:
                if os.path.isfile(caminho) or os.path.islink(caminho):
                    os.unlink(caminho)
                elif os.path.isdir(caminho):
                    shutil.rmtree(caminho)
            except Exception as e:
                print(f'Erro ao deletar {caminho}: {e}')