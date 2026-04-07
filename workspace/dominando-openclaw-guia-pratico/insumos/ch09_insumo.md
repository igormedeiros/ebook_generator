# Insumo Capítulo 9: Exército (Multi-agentes)
**Fonte:** Pesquisa Web / NotebookLM ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0
**Data:** 2026-04-01

## Resumo Técnico
- **Esquadrão de Especialistas:**
  - **Pedro (YouTube):** Monitora canais, baixa transcrições e faz a curadoria de conteúdo em vídeo.
  - **Clarice (Redatora):** Transforma dados brutos em posts de LinkedIn, newsletters e artigos, mantendo o estilo do autor.
- **Delegar vs Executar:** O agente principal atua como o Gerente (PM) que distribui tarefas para os sub-agentes.

## Novidades (Últimos 60 dias)
- **SQLite Task Tracking:** Melhor acompanhamento de tarefas delegadas a sub-agentes, permitindo que o agente principal saiba o status de cada "soldado".
- **NemoClaw:** Lançamento da NVIDIA (março/2026) que fornece uma camada enterprise para governar esquadrões de agentes.

## Cicatrizes de Produção
- Agentes que falam entre si sem supervisão podem entrar em loops de concordância infinita ("O que você acha?", "Eu concordo, e você?"); é necessário definir um limite de turnos para a colaboração.
- **Cicatriz:** Transcrições do Pedro que falham por mudanças na API do YouTube (yt-dlp precisa de atualização constante).
