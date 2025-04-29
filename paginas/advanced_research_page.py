"""
Página Streamlit para a crew Advanced_Reserarch
------------------------------------------------
Permite ao usuário definir o tema e o número de agentes, executar a crew e visualizar/salvar o resultado.
"""

import streamlit as st
from crews.Advanced_Reserarch import run_advanced_research

def render_advanced_research_page():
    """
    Renderiza a interface Streamlit para a crew Advanced_Reserarch.
    Permite ao usuário definir o tema e o número de agentes, executar a crew e visualizar/salvar o resultado.
    """
    st.title('Advanced Research - CrewAI')
    st.write('Automatize pesquisas de notícias recentes sobre qualquer tema usando múltiplos agentes.')

    tema = st.text_input('Tema da pesquisa', value='Preço de óculos de sol masculinos em sites do Brasil')
    enxame = st.number_input('Número de agentes (enxame)', min_value=1, max_value=10, value=5, step=1)

    if st.button('Executar pesquisa'):
        with st.spinner('Executando pesquisa avançada...'):
            markdown_content, sites_data = run_advanced_research(tema, enxame)
            st.success('Pesquisa concluída!')
            st.subheader('Sites encontrados:')
            for site in sites_data.get('site', []):
                st.write(f"- {site.get('link', '')}")
            st.subheader('Resultado consolidado (Markdown):')
            if markdown_content:
                st.markdown(markdown_content)
                st.download_button('Baixar resultado Markdown', markdown_content, file_name='output.md')
            else:
                st.warning('Nenhum resultado Markdown gerado.')
    else:
        st.info('Preencha o tema e o número de agentes, depois clique em "Executar pesquisa".')
