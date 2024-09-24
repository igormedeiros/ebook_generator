
# -----------------------
# Configurações dos agentes
# configuração do groq
# configuração do RAG com supabase
# configuração do embeddings
# configuração dos agentes com as tools
# criação da tool RAG

# -----------------------
# Gera o ebook

from crew import Crew, Process
from agents import writer_agent
from tasks import (
    write_introduction_task,
    task_problema,
    task_identificacao,
    task_solucao,
    task_protecao,
    task_permissao,
    task_potencia
)

ebook_config_path = 'config/ebook_config.json'
ebook_template_path = '../templates/ebook_template.docx'


# Criando a crew com o agente e a task
crew = Crew(
    agents=[writer_agent],
    tasks=[
        write_introduction_task, 
        task_problema, 
        task_identificacao, 
        task_solucao,
        task_permissao,
        task_protecao,
        task_potencia
    ],
    process=Process.sequential  # Execução sequencial das tasks
)

# Executando o processo com o tema proposto
result = crew.kickoff(inputs={'topic': 'Autoconhecimento e Inteligência Emocional'})
print(result)

# 1) ler os valores de configuração do ebook
# 2) gera os capítulos do ebook
# 3) aplica os capítulos no template do ebook
# 4) gera os paragrafos iniciais de cada capítulo
# 5) aplica os paragrafos iniciais dos capítulos no template do ebook
# 6) gera os subcapítulos do ebook
# 7) aplica os subcapítulos no template do ebook
# 8) gera os paragrafos de cada subcapítulo
# 9) aplica os paragrafos dos subcapítulos no template do ebookx
