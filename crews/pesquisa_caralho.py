# app/crew/pesquisa_crew.py

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

load_dotenv()

search_tool = SerperDevTool()
search_tool.n_results = 20
search_tool.location = "Fortaleza, state of Ceará, Brazil"

# Agente pesquisador padrão
def criar_pesquisador():
    return Agent(
        role='Pesquisador de Notícias Recentes',
        goal='Encontrar notícias publicadas nas últimas 24 horas sobre o cliente atribuído',
        backstory='Você é um jornalista digital dedicado a encontrar o que saiu de mais recente sobre {cliente}.',
        tools=[search_tool],
        verbose=False,
        memory=True
    )

# Agente orquestrador que formata os dados
orquestrador = Agent(
    role='Orquestrador de Inteligência',
    goal='Coletar as respostas dos pesquisadores e montar um relatório organizado por cliente',
    backstory='Você é o coordenador da equipe de inteligência e é responsável por juntar os dados e formatar a entrega.',
    verbose=True,
    memory=True
)

# Função para gerar data de busca
def _data_query():
    ontem = datetime.now() - timedelta(days=1)
    return ontem.strftime("%Y-%m-%d")

# Função principal que roda a crew multi-clientes
def executar_em_lote(lista_clientes: list[str]) -> str:
    data_query = _data_query()
    tasks = []
    pesquisadores = []

    # Criar uma task por cliente
    for cliente in lista_clientes:
        pesquisador = criar_pesquisador()
        pesquisadores.append(pesquisador)

        task = Task(
            description=(
                f"Pesquise notícias publicadas desde {data_query} sobre o cliente: {cliente}. "
                f"Use o termo de busca '{cliente} after:{data_query}'. "
                f"Para cada resultado, extraia o **título da matéria** seguido do link. "
                f"Formate assim: \n\nTítulo da Matéria\nlink\n\nTítulo da Matéria\nlink\n...\n\n"
            f"Não escreva mais nada além disso."
            ),
            expected_output="Uma lista contendo o título de cada matéria seguido do link, um bloco por linha.",
            agent=pesquisador
        )

        tasks.append(task)

    # Task final: orquestrador que junta tudo
    final_task = Task(
        description=(
            "Você vai receber as respostas de diversos pesquisadores. "
            "Formate um relatório assim:\n\n"
            "Cliente: <NOME>\n\n"
            "Título da matéria\nlink\n\n"
            "Título da matéria\nlink\n\n"
            "/////////////////////////\n\n"
            "Faça isso para cada cliente recebido."
        ),
        expected_output="Relatório organizado com títulos e links, separados por cliente.",
        agent=orquestrador
    )

    tasks.append(final_task)

    crew = Crew(
        agents=pesquisadores + [orquestrador],
        tasks=tasks,
        process=Process.sequential
    )

    resultado = crew.kickoff()
    return resultado
