# Site de Utilidades para Monitoramento de Mídia

Este projeto foi desenvolvido para automatizar e otimizar tarefas relacionadas ao monitoramento de mídia, economizando horas de trabalho manual. O site oferece uma interface intuitiva e diversas funcionalidades que facilitam o dia a dia de profissionais que lidam com grandes volumes de dados e informações.

## História

A ideia para este site surgiu da necessidade de poupar tempo e esforço no trabalho de monitoramento de mídia. Antes, era necessário realizar várias tarefas manualmente, como transcrever áudios, resumir PDFs, baixar vídeos e interpretar transcrições. Este site foi criado para centralizar e automatizar essas tarefas, permitindo que o foco seja direcionado para análises mais estratégicas e menos operacionais.

## Funcionalidades

- **Home**: Página inicial com informações gerais.
- **Post Agent**: Ferramenta para gerenciar e criar postagens.
- **Summary PDF**: Upload de arquivos PDF para gerar resumos automáticos.
- **Download Video**: Download de vídeos diretamente da plataforma.
- **Transcription**: Transcrição de áudios para texto.
- **Transcribe & Analyze**: Upload de arquivos MP3 para transcrição e análise detalhada.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- **app.py**: Arquivo principal que gerencia a interface do usuário e a navegação entre as páginas.
- **crews/**: Contém os módulos responsáveis por funcionalidades específicas, como transcrição e resumo de PDFs.
- **db/**: Banco de dados utilizado para armazenar informações e resultados processados.
- **images/**: Imagens utilizadas na interface do site.
- **paginas/**: Páginas individuais do site, como upload de PDF, download de vídeo e transcrição.
- **tools/**: Scripts e ferramentas auxiliares para processamento de dados, como transcrição de áudio.

## Como Executar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o servidor Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Acesse o site no navegador através do endereço exibido no terminal.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Streamlit**: Framework para criação de interfaces web interativas.
- **Pydantic**: Validação de dados.
- **PyDub**: Processamento de áudio.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias e novas funcionalidades.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).