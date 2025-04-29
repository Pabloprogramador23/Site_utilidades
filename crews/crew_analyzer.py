# crew_analyzer.py

from crewai import Agent, Task, Crew, Process

def analisar_parte(texto: str, indice: int) -> str:
    agente = Agent(
        role="Curador Jornalístico",
        goal="Identificar todos os assuntos discutidos no trecho da transcrição.",
        backstory=(
            "Você é um jornalista experiente e analista de programas de rádio. "
            "Seu trabalho é extrair os temas discutidos em cada parte da transcrição, mantendo a sequência cronológica."
        ),
        verbose=False,
        allow_delegation=False
    )

    tarefa = Task(
        description=(
            f"Abaixo está um trecho da transcrição de um programa jornalístico.\n"
            f"Identifique os temas abordados neste trecho {indice}.\n\n"
            "Transcrição:\n{{transcricao}}"
        ),
        expected_output="Lista de assuntos discutidos nesta parte.",
        agent=agente
    )

    crew = Crew(agents=[agente], tasks=[tarefa], process=Process.sequential)

    resultado = crew.kickoff(inputs={"transcricao": texto})
    
    # ✅ Aqui pegamos o conteúdo da resposta
    return f"--- Parte {indice} ---\n{resultado.output.strip()}\n"