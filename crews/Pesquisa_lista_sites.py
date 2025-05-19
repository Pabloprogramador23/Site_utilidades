import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool

# Carrega lista fixa de sites (você pode substituir pelo caminho absoluto se quiser)
SITE_PATH = "sites.txt"

def carregar_sites():
    with open(SITE_PATH, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]

# AGENTES

coordenador = Agent(
    role="Coordenador de Monitoramento",
    goal="Distribuir os sites para análise e garantir que cada site seja investigado",
    backstory="Você coordena uma equipe de investigadores que monitoram sites jornalísticos.",
    verbose=True
)

def criar_investigador(site_url):
    return Agent(
        role="Investigador Jornalístico",
        goal=f"Analisar o site {site_url} e encontrar menções recentes",
        backstory=(
            f"Você vasculha conteúdos de {site_url} em busca de nomes ou organizações mencionadas recentemente."
        ),
        tools=[ScrapeWebsiteTool(website_url=site_url)],
        verbose=True
    )

analista = Agent(
    role="Analista Consolidado",
    goal="Organizar e apresentar os resultados das investigações",
    backstory="Você resume todas as menções encontradas em um relatório estruturado.",
    verbose=True
)

# FUNÇÃO PRINCIPAL
def executar_crew(palavras_chave: list) -> str:
    sites = carregar_sites()

    tarefas_investigacao = []
    investigadores = []

    hoje = datetime.now().strftime('%d/%m/%Y')
    palavras_str = ', '.join(palavras_chave)

    for site in sites:
        investigador = criar_investigador(site)
        investigadores.append(investigador)

        tarefa = Task(
            description=(
                f"Acesse o site {site} e analise todo o conteúdo possível. "
                f"Busque por matérias ou postagens publicadas nas últimas 24 horas (até {hoje}) "
                f"que mencionem as palavras-chave: {palavras_str}. "
                "Use scraping para acessar e analisar o conteúdo textual do site."
            ),
            expected_output="Lista de menções com título e link da matéria.",
            tools=investigador.tools,
            agent=investigador
        )
        tarefas_investigacao.append(tarefa)

    tarefa_final = Task(
        description=(
            "Reúna os resultados de todas as investigações e crie um relatório organizado com: "
            "data da análise, site e links das matérias encontradas que citam as palavras-chave."
        ),
        expected_output="Relatório consolidado com data, site e links relevantes.",
        agent=analista
    )

    crew = Crew(
        agents=[coordenador] + investigadores + [analista],
        tasks=tarefas_investigacao + [tarefa_final],
        process=Process.sequential

    )

    resultado = crew.kickoff()
    return resultado