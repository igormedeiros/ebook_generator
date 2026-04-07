# Insumo Capítulo 5: O Cérebro Híbrido (APIs vs Ollama)
**Fonte:** Pesquisa Web / NotebookLM ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0
**Data:** 2026-04-01

## Resumo Técnico
- **Estratégia Híbrida:**
  - **Orquestrador (Cloud):** Anthropic Claude (Opus/Sonnet) ou Gemini 1.5 Pro para raciocínio complexo.
  - **Executores (Local):** Ollama com Qwen 3.5 (Coder/72B) para tarefas repetitivas, leitura de arquivos e execução de código.
- **Token Economy:** Economia de até 90% enviando tarefas de "braço" para o local e reservando o cloud para o "cérebro".

## Novidades (Últimos 60 dias)
- **Ollama Onboarding:** Redesenhado para suportar Ollama nativamente com sugestões automáticas de modelos para codificação.
- **Claude via Vertex AI:** Suporte nativo para rotear chamadas da Anthropic via Google Cloud Vertex AI com autenticação GCP.
- **Qwen 3.5:** Confirmado como o modelo favorito para "local arms" devido ao excelente tool-calling.

## Cicatrizes de Produção
- Tentar rodar modelos 70B em hardware sem VRAM suficiente causa lentidão extrema; é melhor usar um 7B/14B rápido (como Qwen 2.5/3.5) do que um grande lento.
- **Mudança de API:** O caminho `openclaw/extension-api` foi removido; deve-se usar `openclaw/plugin-sdk/*`.
