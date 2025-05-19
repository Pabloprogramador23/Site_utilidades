import streamlit as st
from crews.Pesquisa_lista_sites import executar_crew

def render_pesquisa_lista_sites_page():
    st.title("🔎 Pesquisa de Menções em Sites Jornalísticos")
    st.markdown("""
Insira nomes, termos ou organizações para buscar menções recentes em diversos sites jornalísticos. 
A busca será realizada por agentes autônomos, que analisam conteúdos publicados nas últimas 24 horas.

- A lista de sites é definida no arquivo `sites.txt`.
- Separe múltiplos termos por vírgula.
""")

    palavras = st.text_area("Nomes, termos ou organizações (separe por vírgula)", "exemplo1, exemplo2")

    if st.button("Executar pesquisa"):
        palavras_chave = [p.strip() for p in palavras.split(",") if p.strip()]
        with st.spinner("Executando CrewAI e pesquisando nos sites..."):
            try:
                resultado = executar_crew(palavras_chave)
                st.success("Pesquisa concluída!")
                st.text_area("Resultado consolidado", resultado, height=600)
            except Exception as e:
                st.error(f"Erro ao executar a pesquisa: {e}")
