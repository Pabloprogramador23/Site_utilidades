from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os

# Modelo de entrada já definido
class AudioTranscriptionInput(BaseModel):
    file_path: str = Field(..., description="Caminho para o arquivo MP3 de áudio a ser transcrito")

# Em sua classe, adicione a anotação de tipo:
class AudioTranscriptionTool(BaseTool):
    name: str = "AudioTranscriptionTool"
    description: str = "Transcreve o áudio de um arquivo MP3 para texto usando reconhecimento de voz"
    #args_schema: Type[BaseModel] = AudioTranscriptionInput

    
    def _run(self, file_path: str) -> str:
        try:
            from pydub import AudioSegment
        except ImportError:
            return "Erro: Biblioteca pydub não instalada. Execute 'pip install pydub'."
        try:
            import whisper
        except ImportError:
            return "Erro: Biblioteca Whisper não instalada. Execute 'pip install openai-whisper'."

        # Converter MP3 para WAV
        try:
            audio = AudioSegment.from_mp3(file_path)
            wav_path = os.path.splitext(file_path)[0] + ".wav"
            audio.export(wav_path, format='wav')
        except Exception as e:
            return f"Erro na conversão: {e}"

        # Dividir o áudio em pedaços menores (30 segundos cada)
        chunk_length_ms = 30 * 1000  # 30 segundos
        audio_chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

        # Carregar o modelo Whisper
        model = whisper.load_model("base")

        # Transcrever cada pedaço e concatenar os resultados
        transcription = ""
        for i, chunk in enumerate(audio_chunks):
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            try:
                result = model.transcribe(chunk_path, language="pt")
                transcription += result["text"] + " "
            except Exception as e:
                return f"Erro durante a transcrição do pedaço {i}: {e}"
            finally:
                os.remove(chunk_path)

        try:
            os.remove(wav_path)
        except Exception:
            pass

        return transcription.strip()
