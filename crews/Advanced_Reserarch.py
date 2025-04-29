"""
Advanced_Reserarch Crew
======================

Este módulo define a crew Advanced_Reserarch, que automatiza a pesquisa de notícias recentes sobre um tema definido pelo usuário, utilizando múltiplos agentes para buscar, analisar e consolidar informações de sites relevantes.

Fluxo:
1. O usuário informa o tema da pesquisa e o número de agentes (enxame).
2. Um agente inicial busca sites confiáveis com notícias das últimas 24 horas sobre o tema.
3. Cada agente do enxame pesquisa detalhadamente um site.
4. Um agente agregador consolida os resultados em um arquivo Markdown.
5. O resultado é salvo e pode ser exibido em uma interface Streamlit.

Requisitos:
- crewai
- crewai_tools
- python-dotenv
- PyYAML

Entradas:
- topic (tema da pesquisa)
- enxame (número de agentes)

Saídas:
- output.md (resultado consolidado)
- partialX.md (resultados parciais por site)

"""

import yaml
import datetime
import locale
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import WebsiteSearchTool, SerperDevTool

# Configurar localização para datas em português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except locale.Error:
    pass  # fallback se não houver suporte

# Carregar variáveis de ambiente do .env
load_dotenv()

def run_advanced_research(topic: str, enxame: int = 5):
    """
    Executa a crew Advanced_Reserarch para pesquisar notícias recentes sobre um tema.
    Args:
        topic (str): Tema da pesquisa.
        enxame (int): Número de agentes do enxame.
    Returns:
        str: Caminho do arquivo Markdown consolidado.
        dict: Dados brutos dos sites encontrados.
    """
    # Ferramenta de busca geral
    search_tool = SerperDevTool()
    gpt_mini = 'gpt-4o-mini'

    # Data atual formatada
    data_atual = datetime.datetime.now()
    data_hoje = data_atual.strftime('%A, %d de %B de %Y')

    # Template YAML para sites
    template = """
site:
  - link: "url da notícia"
"""

    # Prompt do pesquisador: busca notícias das últimas 24h
    topic_full = f"{topic} (notícias das últimas 24 horas, atualizado para {data_hoje})"

    pesquisador_web = Agent(
        role='Pesquisador Web',
        goal=(
            f"Encontrar sites de notícias relevantes para o tema: {topic_full}. "
            "Produza uma saída YAML no seguinte template: {template}"
        ),
        backstory=(
            "Você é um especialista em encontrar fontes online confiáveis. "
            "Sua missão é fornecer uma lista de sites de notícias recentes sobre o tema especificado."
        ),
        tools=[search_tool],
        verbose=True,
        llm=gpt_mini
    )

    tarefa_encontrar_sites = Task(
        description=(
            f"Realize uma pesquisa na web para identificar e compilar uma lista de sites de notícias relevantes sobre: {topic_full}. "
            "A saída final deve ser formatada como YAML, seguindo o template fornecido. "
            "Retire quaisquer marcações como 'yaml' da saída."
        ),
        expected_output="Uma YAML de 5 a 10 sites relacionados ao tema.",
        agent=pesquisador_web
    )

    crew_inicial = Crew(
        agents=[pesquisador_web],
        tasks=[tarefa_encontrar_sites],
        process=Process.sequential
    )

    # Executar a crew inicial
    input_dict = {'topic': topic_full, 'template': template, 'sites': enxame}
    output = crew_inicial.kickoff(inputs=input_dict)
    yaml_string = output.raw.strip("'''yaml").strip("'''")
    data_dict = yaml.safe_load(yaml_string)
    sites_list = data_dict.get('site', [])

    agentes = []
    tarefas = []

    # Diretório temporário para arquivos parciais
    temp_dir = os.path.join('temp', 'advanced_research')
    os.makedirs(temp_dir, exist_ok=True)

    # Para cada site, criar um agente pesquisador
    for idx, site in enumerate(sites_list[:enxame]):
        try:
            busca = WebsiteSearchTool(website=site['link'])
            agente = Agent(
                role=f"Pesquisador Web {idx+1}",
                goal=f"Buscar notícias recentes sobre {topic_full} em {site['link']}",
                backstory=(
                    f"Especialista em recuperar informações detalhadas do site {site['link']} sobre {topic_full}."
                ),
                tools=[busca],
                verbose=True,
                memory=True,
                allow_delegation=False,
                llm=gpt_mini
            )
            tarefa = Task(
                description=(
                    f"Use o site {site['link']} para encontrar notícias detalhadas sobre {topic_full}. "
                    "Inclua o link de onde a informação foi encontrada."
                ),
                expected_output=f"Retornar informações sobre {topic_full} a partir do site {site['link']}.",
                agent=agente,
                output_file=os.path.join(temp_dir, f'partial{idx+1}.md')
            )
            agentes.append(agente)
            tarefas.append(tarefa)
        except Exception as e:
            print(f"Erro ao acessar site: {site.get('link', 'desconhecido')} - {e}")

    # Agente agregador
    agente_agregador = Agent(
        role='Agregador',
        goal='Consolidar informações dos agentes em um documento Markdown',
        backstory=(
            "Especialista em sintetizar informações de várias fontes em um formato coeso. "
            "Compila os insights coletados em um documento Markdown."
        ),
        verbose=True
    )
    tarefa_agregador = Task(
        description=(
            "Consolide os resultados dos agentes em um documento Markdown. "
            "Inclua todas as informações relevantes coletadas."
        ),
        expected_output="Um documento Markdown que resume as informações coletadas de todos os sites.",
        agent=agente_agregador,
        output_file=os.path.join(temp_dir, 'output.md')
    )
    agentes.append(agente_agregador)
    tarefas.append(tarefa_agregador)

    crew_assincrona = Crew(
        agents=agentes,
        tasks=tarefas,
        process=Process.sequential
    )
    result = crew_assincrona.kickoff(inputs={})

    # Limpeza dos arquivos temporários após execução
    for file in os.listdir(temp_dir):
        if file.startswith('partial') and file.endswith('.md'):
            try:
                os.remove(os.path.join(temp_dir, file))
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {file} - {e}")

    output_path = os.path.join(temp_dir, 'output.md')
    # Lê o conteúdo do output.md antes de apagar
    markdown_content = None
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        try:
            os.remove(output_path)
        except Exception as e:
            print(f"Erro ao remover output.md: {e}")

    return markdown_content, data_dict

# Exemplo de uso (remova ao importar como módulo):
# if __name__ == "__main__":
#     arquivo, dados = run_advanced_research("Preço de óculos de sol masculinos em sites do Brasil", enxame=5)
#     print(f"Arquivo gerado: {arquivo}")
#     print(dados)
