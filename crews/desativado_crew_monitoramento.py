import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

def run_monitoramento(clientes: str):
    """
    Configura e executa a crew para monitoramento de matérias jornalísticas
    publicadas nas últimas 24 horas que mencionem os clientes informados.

    Parâmetros:
        clientes (str): Lista de clientes separados por vírgula.

    Retorna:
        result: Saída da execução da crew com os resultados da pesquisa.
    """
    # Instanciando a ferramenta SerperDevTool configurada para ptbr e Fortaleza, CE.
    search_tool = SerperDevTool()
    
    # Definindo o agente com o papel de "Monitorador de Notícias"
    monitorador = Agent(
        role='Monitorador de Notícias',
        goal=(
            "Monitorar sites jornalísticos para identificar artigos publicados nas últimas 24 horas "
            "que mencionem os clientes da lista fornecida."
        ),
        verbose=True,
        memory=True,
        backstory=(
            "Você é um especialista em monitoramento de mídias e fontes jornalísticas. "
            "Sua experiência permite identificar rapidamente matérias recentes que mencionem os clientes, "
            "mesmo que a informação seja sutil."
        ),
        tools=[search_tool]
    )
    
    # Definindo a tarefa de monitoramento
    monitoramento_task = Task(
            description=(
                "Dada a lista de clientes {clientes}, formate uma query de busca com operadores OR entre os nomes "
                "para identificar artigos publicados nas últimas 24 horas que mencionem qualquer um dos clientes. "
                "Para cada artigo encontrado, colete as seguintes informações: título da matéria, DATA DE PUBLICAÇÃO, link do artigo "
                "e os clientes (da lista) mencionados na publicação. "
                "Seu relatório final deverá ser uma lista onde cada item seja um dicionário com as chaves 'título', 'data', 'link' "
                "e 'clientes mencionados'."
                "e pesquise nos sites jornalísticos. Exemplo: '\"Cliente A\" OR \"Cliente B\" OR \"Cliente C\"'. "
                "Colete matérias que mencionem QUALQUER um dos clientes individualmente."
                "Após coletar os resultados, verifique e remova matérias duplicadas usando o link como identificador único."
            ),
            expected_output=(
                "Uma lista de resultados, onde cada resultado é um dicionário contendo: "
                "'título' (string), 'data' (string no formato DD/MM/YYYY), 'link' (string) e 'clientes mencionados' (lista)."
            ),
        tools=[search_tool],
        agent=monitorador,
    )
    
    # Configurando a Crew com execução sequencial
    crew = Crew(
        agents=[monitorador],
        tasks=[monitoramento_task],
        process=Process.sequential
    )
    
    # Executando a crew com os inputs dos clientes
    result = crew.kickoff(inputs={'clientes': clientes})
    return result
