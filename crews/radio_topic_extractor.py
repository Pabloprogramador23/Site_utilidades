# arquivo: radio_topic_extractor.py

from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv
load_dotenv()



# Agente 1: Analista de Conversa
conversation_analyst = Agent(
    role="Analista de Conversa de Rádio",
    goal="Compreender o fluxo da conversa e dividir a transcrição em blocos temáticos.",
    backstory=(
        "Você é um linguista especializado em transcrições de programas de rádio. "
        "Com um ouvido treinado para mudanças de tópico e nuances de discurso, sua missão é "
        "entender a estrutura da conversa e ajudar a identificar os assuntos abordados."
    ),
    verbose=True,
    allow_delegation=False
)

# Agente 2: Organizador de Tópicos
topic_organizer = Agent(
    role="Detector e Organizador de Tópicos",
    goal="Identificar e organizar os tópicos discutidos na transcrição em ordem cronológica.",
    backstory=(
        "Você trabalha como editor de programas de podcast, especialista em resumir episódios longos "
        "em listas de tópicos. Sua função é destacar claramente cada assunto discutido, seguindo a ordem do diálogo."
    ),
    verbose=True
)

# Função principal
def extrair_topicos(transcricao: str) -> str:
    # Tarefa
    analyze_transcript_task = Task(
        description=(
            "Leia a seguinte transcrição de um programa de rádio e identifique todos os assuntos abordados. "
            "Organize esses tópicos em uma lista na ordem cronológica em que aparecem. "
            "Evite interpretações subjetivas e use frases curtas e objetivas para descrever cada tópico.\n\n"
            "Transcrição:\n{transcricao}"
        ),
        expected_output=(
            "Uma lista com os tópicos abordados, na ordem cronológica. Exemplo:\n"
            "1. Introdução do programa e apresentação dos participantes\n"
            "2. Discussão sobre política internacional\n..."
        ),
        agent=topic_organizer
    )

    crew = Crew(
        agents=[conversation_analyst, topic_organizer],
        tasks=[analyze_transcript_task],
        process=Process.sequential
    )

    resultado = crew.kickoff(inputs={"transcricao": transcricao})
    return resultado
