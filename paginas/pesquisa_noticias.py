# app/pages/pesquisa_links.py

import streamlit as st
from crews.pesquisa_caralho import executar_pesquisa

def render_pesquisa_page():
    st.title("🔎 Pesquisar notícias recentes sobre um cliente")
    st.write(
        """
        Insira o nome do cliente abaixo. O sistema irá pesquisar notícias publicadas nas últimas 24 horas que mencionem esse cliente.
        O resultado exibirá os links das matérias encontradas.
        """
    )

    cliente = st.text_input("Digite o nome do cliente:", value="Prefeitura de Fortaleza")

    if st.button("Pesquisar"):
        st.info("Pesquisando notícias, isso pode levar alguns segundos...")
        resultado = executar_pesquisa(cliente)

        st.success("🔗 Links encontrados:")
        st.text_area("Resumo via agentes:", resultado, height=300)
