import os
from crewai import Agent, Task, Crew, Process
from tools.audio_transcription_tool import AudioTranscriptionTool
from dotenv import load_dotenv

load_dotenv()

class CrewTranscriptionAndInterpretation:
    """
    Esta classe define uma crew da CrewAI que executa, de forma sequencial,
    as seguintes tarefas:
      1. Transcrever um arquivo de áudio (MP3) para texto.
      2. A partir do texto transcrito, extrair e listar todas as matérias faladas
         no programa de rádio, indicando o minuto de início (ou null, caso não exista).
    """

    def __init__(self):
        # Inicializa a ferramenta de transcrição
        self.transcription_tool = AudioTranscriptionTool()
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Define o agente responsável pela transcrição de áudio
        transcription_agent = Agent(
            role="Transcritor de Áudio",
            goal="Transcrever o programa de rádio a partir de um arquivo MP3 para texto.",
            backstory="Você é um especialista em reconhecimento de voz, capaz de transformar áudios em texto com alta precisão.",
            tools=[self.transcription_tool],
            verbose=True
        )

        # Define o agente responsável por extrair os segmentos/matérias da transcrição
        segmentation_agent = Agent(
            role="Segmentador de Matérias",
            goal=(
                "Dado o texto transcrito do programa de rádio, extraia uma lista ordenada com todas as matérias faladas, "
                "indicando o minuto de início de cada uma. Se o minuto não estiver explícito, retorne null. "
                
            ),
            backstory=(
                "Você é um especialista em análise de transcrições jornalísticas e sabe identificar os diferentes segmentos do programa. "
                "Utilize o texto transcrito fornecido como contexto para extrair e organizar as matérias junto com os respectivos horários de início."
            ),
            verbose=True
        )

        # Define a Tarefa 1: Transcrever o áudio
        transcription_task = Task(
            description="Transcreva o áudio presente no arquivo {file_path}.",
            expected_output="Texto completo contendo a transcrição do programa de rádio.",
            agent=transcription_agent,
            
        )

        # Define a Tarefa 2: Extrair os segmentos a partir da transcrição
        segmentation_task = Task(
            description=(
                "Utilize o texto de transcrição para identificar e extrair uma lista ordenada das matérias do jornal, "
                "incluindo o minuto de início de cada matéria. Se não houver um minuto específico, use null.\n"
                "Texto da transcrição"
            ),
            expected_output=(
                "Uma lista em formato JSON com os segmentos extraídos e os respectivos minutos, por exemplo:\n"
                '[{"segmento": "Título da matéria", "minuto": "MM:SS"}, ...]'
            ),
            agent=segmentation_agent,
            context=[transcription_task]
        )

        # Cria a crew, definindo o processo de execução sequencial e permitindo logs detalhados
        return Crew(
            agents=[transcription_agent, segmentation_agent],
            tasks=[transcription_task, segmentation_task],
            process=Process.sequential,
            verbose=True
        )

    def kickoff(self, inputs):
        # Executa a crew passando os inputs (por exemplo, o caminho do arquivo MP3)
        resposta = self.crew.kickoff(inputs=inputs)
        return resposta.raw

# Exemplo de uso:
if __name__ == "__main__":
    # Substitua pelo caminho real do seu arquivo MP3
    inputs = {"file_path": "caminho/para/seu/programa_radio.mp3"}
    crew_instance = CrewTranscriptionAndInterpretation()
    result = crew_instance.kickoff(inputs=inputs)
    print("Resultado Final das Tarefas:")
    print(result)