[x] Popular tabelas do Supabase com histórias, posicionamentos e visão do autor
[x] Reimplementar store_in_rag_external com inserts reais no Supabase
[x] Substituir revisão de exercícios por execução real de código Python em sandbox
[x] Remover todas as dependências CrewAI do projeto
[x] Migrar para LangChain 1.0+ puro com agent.invoke()
[x] Remover tasks.py e reposicionar config em conceitos LangChain 1.0
[x] Refatorar __main__.py para carregar BRD diretamente
[x] Usar Gemini 2.5 Flash como modelo principal
[x] Testar pipeline end-to-end com BRD real
[x] Refatorar estrutura src - mover main/* para src/ e remover __init__.py
[x] Renomear files para padrão final: agents_write.py, tools.py
[x] Implementar 33 tools baseado em specs/tools.yaml
[x] Atualizar copilot-instructions.md com padrões finais
[x] Implement real Supabase RAG tools in src/tools.py
[x] Add progress bars and ETA to src/main.py
[x] Fix generation logic when skipping deep research
[x] Integrate template/template.md into save_ebook
[x] Implement Review, Critical Reading, and Editing phases in generate_ebook
[x] Fix output parsing for Python list strings
[x] Initialize ebook.md immediately after confirmation using template
[x] Add progress bar to thematic research phase
[x] Fix NameError: name 'brd' is not defined in save_ebook
[x] Implement incremental saving of chapters to ebook.md
[x] Update get_confirmation to support skip_prompt parameter
[x] Fix JSON parsing errors in chapter structure generation using json_repair
[x] Test EPUB generation end-to-end with --test mode
[x] git add -A && git commit -m "feat: implement EPUB generation from markdown"
[x] Fix persistent JSON output in markdown by handling AIMessage objects in pipeline_helpers and agents
[x] Atualizar pipeline para reutilizar capítulos aprovados do BRD
[x] Implementar fluxo de aprovação de títulos de capítulos com persistência no BRD
[x] Garantir uso obrigatório de RAG na geração de capítulos
[x] git add -A && git commit -m "feat: habilitar aprovação de títulos e forçar RAG"
[x] Corrigir bloqueio do prompt de aprovação de títulos ao pausar a barra de progresso
[ ] git add -A && git commit -m "fix: pausar barra antes de aprovar títulos"
