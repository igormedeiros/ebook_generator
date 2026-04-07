# Insumo Capítulo 5: O Cérebro Híbrido (APIs de Elite vs Executores de Baixo Custo)
**Fonte:** NotebookLM / Pesquisa de Mercado (v2026.3.31)
**Data:** 2026-04-01

## Estratégia "Brain vs Arms" (Cérebro vs Braços)
- **O Cérebro (Chief of Staff):** Deve rodar em modelos de altíssimo nível (ex: Claude 3.5 Opus ou GPT-4o). Ele é responsável pela estratégia, delegação e orquestração da equipe.
- **Os Braços (Executores):** Agentes que acordam a cada 15 min (Heartbeats) para tarefas rotineiras devem usar modelos baratos (ex: Gemini 1.5 Flash, Grok ou Qwen 3.5 via Alibaba Cloud).
- **Otimização:** Pedir verbalmente ao agente principal: "Altere a IA de background do agente Pedro para Gemini para economizar tokens".

## Alternativas de Baixo Custo
- **Alibaba Cloud (Model Studio):** Recomendado para modelos Qwen 3.5 pela alta velocidade e custo reduzido.
- **Ollama (Execução Local):** A estratégia definitiva para "Braços" que realizam tarefas simples (resumo, tradução, formatação), com custo zero de token após o investimento em hardware.

---

# Insumo Capítulo 6: Memória Infinita (Adeus Alzheimer Reset)
**Fonte:** NotebookLM / Estrutura v2026.3.31
**Data:** 2026-04-01

## Camadas de Memória no OpenClaw
1. **Memória de Trabalho (`working.md`):** Documenta a tarefa atual e o status. Lida por todo sub-agente ao "acordar".
2. **Notas Diárias (`daily_notes/`):** Compactação automática de tudo o que ocorreu no dia (executada à meia-noite).
3. **Lições Aprendidas (`lessons_learned.md`):** Arquivo persistente para salvar correções de erros. Se o robô errou e você corrigiu, mande: "Salve esta lição aprendida".
4. **Decisões (`decisions.md`):** Registro de todas as escolhas importantes feitas pelo dono e pela IA.

## Regras Invioláveis de Compactação
- Configurar a compactação ao atingir 80% da janela de tokens (ex: 160k de 200k).
- **Obrigatório:** Antes de compactar, a IA DEVE extrair Lessons, Decisions, People e Projects.

## Cicatrizes de Produção
- Repreensões no chat não sobrevivem ao reinício. Se você não mandar salvar a lição em um arquivo, a IA cometerá o mesmo erro amanhã.
- Curadoria Periódica: A cada 15 dias, a IA deve reler as notas diárias para "pescar" o que foi esquecido na compactação automática.