import os
from pydub import AudioSegment
import whisper

def transcrever_audio_em_blocos(file_path, output_dir="temp", duracao_blocos_minutos=15, modelo_whisper="tiny"):
    """
    Transcreve um arquivo de áudio em blocos e salva a transcrição em um arquivo .txt.

    Args:
        file_path (str): Caminho para o arquivo de áudio.
        output_dir (str): Diretório onde o arquivo .txt será salvo.
        duracao_blocos_minutos (int): Duração de cada bloco em minutos.
        modelo_whisper (str): Modelo Whisper a ser usado (e.g., "tiny", "base").

    Returns:
        str: Caminho para o arquivo .txt gerado.
    """
    # Garantir que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)

    # Carregar o áudio
    audio = AudioSegment.from_mp3(file_path)
    duracao_total_ms = len(audio)
    bloco_ms = duracao_blocos_minutos * 60 * 1000
    total_blocos = (duracao_total_ms + bloco_ms - 1) // bloco_ms

    # Criar pasta para os pedaços
    pasta_blocos = os.path.join(output_dir, "audios_divididos")
    os.makedirs(pasta_blocos, exist_ok=True)

    arquivos_blocos = []

    for i in range(total_blocos):
        inicio = i * bloco_ms
        fim = min((i + 1) * bloco_ms, duracao_total_ms)
        trecho = audio[inicio:fim]
        nome_parte = os.path.join(pasta_blocos, f"parte_{i+1:02d}.mp3")
        trecho.export(nome_parte, format="mp3")
        arquivos_blocos.append(nome_parte)

    # Carregar o modelo Whisper
    modelo = whisper.load_model(modelo_whisper)

    # Transcrever cada bloco e concatenar os resultados
    transcricao_total = ""

    for i, caminho in enumerate(arquivos_blocos, 1):
        resultado = modelo.transcribe(caminho)
        transcricao_total += f"\n\n=== Parte {i} ===\n{resultado['text']}"

    # Salvar a transcrição em um arquivo .txt
    saida_txt = os.path.join(output_dir, os.path.basename(file_path).replace(".mp3", "_transcricao.txt"))
    with open(saida_txt, "w", encoding="utf-8") as f:
        f.write(transcricao_total.strip())

    return saida_txt

# Exemplo de uso
if __name__ == "__main__":
    input_audio = "temp/Hi - Fi Internet Stream (5).mp3"
    output_txt = transcrever_audio_em_blocos(input_audio)
    print(f"Transcrição salva em: {output_txt}")