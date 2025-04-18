import os
import streamlit as st
from crews.crew_monitoramento import run_monitoramento

def render_monitoramento_page():
    st.title("Monitoramento de Notícias com CrewAI")
    st.write(
        """
        Insira a lista de clientes (separados por vírgula) abaixo. O sistema monitorará os sites jornalísticos,
        buscando por matérias publicadas nas últimas 24 horas que mencionem esses clientes. O resultado exibirá,
        para cada artigo, o título, o link e os clientes mencionados.
        """
    )

    clientes_input = st.text_input("Lista de Clientes")

    if st.button("Executar Monitoramento"):
        with st.spinner("Executando monitoramento..."):
            try:
                resultados = run_monitoramento(clientes_input)
                
                if resultados and isinstance(resultados, list):
                    st.success("Monitoramento concluído! Resultados encontrados:")
                    
                    for i, artigo in enumerate(resultados, 1):
                        with st.expander(f"Matéria {i}: {artigo.get('título', 'Sem título')}"):
                            st.markdown(f"""
                            **Data de Publicação:** {artigo.get('data', 'Data não disponível')}
                            
                            **Clientes Mencionados:** {', '.join(artigo.get('clientes mencionados', []))}
                            
                            **Link:** [{artigo.get('link', 'Sem link')}]({artigo.get('link', '')})
                            """)
                        st.divider()
                else:
                    st.info("Nenhuma matéria encontrada nas últimas 24 horas.")
                    
            except Exception as e:
                st.error(f"Erro na execução: {str(e)}")

# Para uso standalone
if __name__ == "__main__":
    render_monitoramento_page()
