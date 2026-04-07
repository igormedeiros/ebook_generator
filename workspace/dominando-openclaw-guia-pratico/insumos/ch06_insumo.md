# Insumo Capítulo 6: Memória Infinita (Daily Notes/Lessons)
**Fonte:** Pesquisa Web / NotebookLM ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0
**Data:** 2026-04-01

## Resumo Técnico
- **Camadas de Memória:**
  - **Daily Notes:** Registro do que aconteceu no dia.
  - **Lessons Learned:** Erros e acertos técnicos salvos para evitar repetição.
  - **Decisions:** Registro de decisões tomadas para manter a consistência.
- **Fim do Alzheimer:** Uso de RAG (Retrieval-Augmented Generation) para buscar contextos passados antes de responder.

## Novidades (Últimos 60 dias)
- **Memory Embeddings:** Expansão para suporte multilíngue, melhorando drasticamente a busca semântica em português.
- **SQLite Ledger:** A persistência de fluxos e decisões agora é garantida pelo banco de dados centralizado.

## Cicatrizes de Produção
- Muita memória irrelevante "polui" o contexto e faz o agente alucinar; é necessário um processo de limpeza periódica ou um agente (como a Clarice) para resumir memórias antigas.
- **Dica:** Use tags claras nas memórias (ex: #decision, #lesson) para facilitar a busca do agente.
