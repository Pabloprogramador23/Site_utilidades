import os
from crewai import Agent, Task, Crew, Process
from tools import audio_transcription_tool
from dotenv import load_dotenv

load_dotenv()

class CrewTranscriptionAndInterpretation:

    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Agente de transcrição
        transcriber = Agent(
            role='Transcriber',
            goal='Transcrever o conteúdo do arquivo de áudio.',
            verbose=True,
            memory=True,
            backstory='Você é um especialista em transcrever áudios com precisão.',
            tools=[audio_transcription_tool]
        )

        # Agente de interpretação
        interpreter = Agent(
            role='Interpreter',
            goal='Interpretar a transcrição e listar todas as matérias jornalísticas mencionadas.',
            verbose=True,
            memory=True,
            backstory='Você é um analista especializado em identificar tópicos jornalísticos em transcrições.',
        )

        # Tarefa de transcrição
        transcription_task = Task(
            description='Transcreva o conteúdo do arquivo de áudio.',
            expected_output='Uma transcrição completa do áudio.',
            agent=transcriber
        )

        # Tarefa de interpretação
        interpretation_task = Task(
            description='Analise a transcrição e liste todas as matérias jornalísticas mencionadas.',
            expected_output='Uma lista de matérias jornalísticas.',
            agent=interpreter,
            context=[transcription_task]
        )

        # Criando o Crew
        return Crew(
            agents=[transcriber, interpreter],
            tasks=[transcription_task, interpretation_task],
            process=Process.sequential
        )

    def kickoff(self):
        # Executa o Crew com o caminho do áudio como entrada
        resposta = self.crew.kickoff(inputs={"audio_path": self.audio_path})
        return resposta.raw

class CrewTranscriptionInterpretation:
    """
    Esta crew realiza a interpretação de um arquivo de transcrição gerado previamente
    e organiza o resultado em um arquivo Markdown (.md).
    """

    def __init__(self):
        # Agente para interpretar o conteúdo do arquivo .txt
        interpretation_agent = Agent(
            role="Interprete de Transcrição",
            goal="Interpretar o conteúdo do arquivo de transcrição e gerar um resumo estruturado.",
            backstory="Você é um especialista em análise de transcrições e sabe identificar informações importantes.",
            verbose=True
        )

        # Agente para revisar e organizar o conteúdo em um arquivo Markdown
        revision_agent = Agent(
            role="Revisor e Organizador",
            goal="Revisar o conteúdo interpretado e organizá-lo em um arquivo Markdown (.md).",
            backstory="Você é um especialista em formatação e organização de conteúdo para exibição clara e profissional.",
            verbose=True
        )

        # Tarefa 1: Interpretar o conteúdo do arquivo .txt
        interpretation_task = Task(
            description="Leia o conteúdo do arquivo {file_path} e interprete as informações importantes.",
            expected_output="Um resumo estruturado das informações interpretadas.",
            agent=interpretation_agent
        )

        # Tarefa 2: Revisar e organizar o conteúdo em Markdown
        revision_task = Task(
            description="Revisar o conteúdo interpretado e organizá-lo em um arquivo Markdown.",
            expected_output="Um arquivo .md contendo o conteúdo revisado e formatado.",
            agent=revision_agent,
            context={"interpreted_content": interpretation_task.output}
        )

        # Criar a crew
        self.crew = Crew(
            agents=[interpretation_agent, revision_agent],
            tasks=[interpretation_task, revision_task],
            process=Process.sequential,
            verbose=True
        )

    def kickoff(self, inputs):
        """
        Executa a crew com os inputs fornecidos.

        Args:
            inputs (dict): Dicionário contendo o caminho do arquivo .txt (e.g., {"file_path": "caminho/para/arquivo.txt"}).

        Returns:
            dict: Resultado bruto da execução da crew.
        """
        return self.crew.kickoff(inputs=inputs).raw