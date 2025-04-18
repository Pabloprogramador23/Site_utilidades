# app/crew/pesquisa_crew.py

import os
from datetime import datetime, timedelta
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
load_dotenv()

def executar_pesquisa(cliente: str) -> str:
    # Data das últimas 24h
    ontem = datetime.now() - timedelta(days=1)
    data_query = ontem.strftime("%Y-%m-%d")

    # Ferramenta
    search_tool = SerperDevTool()

    # Agente
    researcher = Agent(
        role='Pesquisador de Notícias Recentes',
        goal='Encontrar notícias publicadas nas últimas 24 horas sobre o cliente especificado',
        backstory=(
            "Você é um jornalista digital especializado em encontrar tudo que sai sobre um cliente em tempo real. "
            "Com um olhar afiado para relevância, você rastreia as manchetes mais recentes para manter o time sempre informado."
        ),
        tools=[search_tool],
        verbose=False,
        memory=True
    )

    # Tarefa
    task = Task(
        description=(
            f"Utilize ferramentas de busca para encontrar notícias publicadas desde {data_query} "
            f"sobre o cliente: {cliente}. Use 'after:{data_query}' na pesquisa para filtrar. "
            f"Retorne apenas os links mais relevantes."
        ),
        expected_output="Uma lista com os links diretos das matérias encontradas nas últimas 24h sobre o cliente.",
        agent=researcher
    )

    # Crew
    crew = Crew(
        agents=[researcher],
        tasks=[task],
        process=Process.sequential
    )

    resultado = crew.kickoff(inputs={"cliente": f"{cliente} after:{data_query}"})
    return resultado  # Já é string

