# Ebook Generator 1.0 - Execution Guide

**Updated**: November 13, 2025

## Quick Start

```bash
# Run the complete pipeline
uv run python -m src

# Run with timeout (useful for testing with API quota limits)
timeout 120 uv run python -m src

# Run functional tests (mocked, no API calls)
uv run python test_functional_pipeline.py

# Run integration tests (real API calls)
timeout 60 uv run python test_integration_pipeline.py
```

## What's New in v1.0 - Verbose Logging & Progress Tracking

### 🚀 Progress Bar
The pipeline now displays a progress bar showing:
- **Overall progress**: 9-stage pipeline completion percentage
- **Stage indicators**: 1️⃣ 2️⃣ 3️⃣ 4️⃣A 4️⃣B 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ emojis
- **Real-time updates**: Bar advances after each stage completes

```
📚 Pipeline [████████████████░░░░░░░░░░░░░] 56%
```

### 🤖 Agent Transparency - "Pensamento Alto" (Chain of Thought)

Each agent now logs its thinking process:

**Stage 1: Ideation**
```
🤖 Criando agente de ideação...
✅ Agente criado: CompiledStateGraph
🔧 Montando prompt...
✅ Prompt (4250 chars)
🤖 Executando agente (Gemini 2.5 Flash)...
⏳ Processando com IA...
✅ Ideação concluída
📤 Saída: [first 150 chars...]
```

The flow shows:
1. Agent creation and initialization
2. Prompt template loading and construction
3. Prompt size verification
4. Model selection (Flash or Pro)
5. Execution with spinner feedback
6. Completion status
7. Output excerpt

### 📚 RAG (Retrieval-Augmented Generation) Visibility

When tools access knowledge bases:

```
🔎 [RAG] Buscando na knowledge base: 'Python healthcare applications...'
📊 Gerando embedding para query...
✅ Embedding gerado - buscando similaridade no pgvector...
✅ [RAG] Encontrados 5 documentos relevantes
```

Shows:
- Tool activation with 🔎 emoji
- Embedding generation progress
- Supabase pgvector similarity search
- Result count

### 👥 Review Personas Transparency

Stage 5 (Specialized Review) with 10 personas:

```
🤖 Criando coordenador de revisões...
👥 Construindo 10 personas especializadas...
✅ Personas criadas: Technical Reviewer, Editorial Reviewer, ...
📋 Persona: Technical Reviewer...
✅ Technical Reviewer - Revisão concluída
📋 Persona: Editorial Reviewer...
[Progress bar for 10 personas]
✅ Revisão concluído com 10 personas
📤 Feedback recebido de: 10 personas
```

### 👁️  Virtual Readers Transparency

Stage 6 (Critical Reading) with 5 virtual reader personas:

```
🤖 Criando coordenador de leitura crítica...
👁️  Construindo 5 leitores virtuais...
✅ Leitores criados: Curious Beginner, Technical Professional, ...
🤖 Executando 3 ciclos de leitura crítica...
📖 Perspectivas: Curiosidade, Profundidade, Didática, Especialização, Reflexão
✅ Leitura crítica concluída
📤 Feedback de 5 leitores virtuais
```

## Complete Pipeline Flow with New Logging

```
[0/9] 🎯 Inicialização: Carregando modelos Gemini...
✅ Modelo de escrita: ChatGoogleGenerativeAI
✅ Modelo de pesquisa: ChatGoogleGenerativeAI

[1/9] 🎯 Ideação: Gerando ideia central...
=====================================
ESTÁGIO 1: IDEAÇÃO
=====================================
🤖 Criando agente de ideação...
✅ Agente criado: CompiledStateGraph
📋 Carregando templates de prompts...
✅ Templates carregados
🔧 Montando prompt...
✅ Prompt (4250 chars)
🤖 Executando agente (Gemini 2.5 Flash)...
⏳ Processando com IA...
✅ Ideação concluída
📤 Saída: [excerpt...]
✅ ESTÁGIO 1 CONCLUÍDO

[2/9] 🎯 Geração de Títulos: Pesquisando bestsellers...
[... continues for all 9 stages ...]
```

## Verbose Mode Features

### ✅ No More Frozen UI

Previous issue: During API calls, the pipeline appeared frozen with no feedback.

**Solution**: Added visual spinner during `execute_agent()` execution:

```python
with console.status("[bold cyan]⏳ Processando com IA...[/bold cyan]", spinner="dots"):
    response = agent.invoke(...)
```

### 🔎 Tool Usage Visibility

All tool invocations are now logged:

```
🔎 [RAG] Buscando na knowledge base...
📚 [RAG] Recuperando contexto...
📦 Gerando embedding para query...
📊 [RAG] Encontrados N documentos relevantes
```

### 🎯 Stage Numbering

Each log message now includes stage number:

```
[1/9] 🎯 Stage: Action
[2/9] 🎯 Stage: Action
[3/9] 🎯 Stage: Action
```

## API Integration Points

### Stage 4A: Deep Research (Context7 MCP)
```
🤖 Executando agente (Gemini 2.5 Pro - RAG enabled)...
📚 [RAG] Será utilizado para Context7 MCP e Supabase pgvector
```

### Stage 5: Specialized Review (10 Personas)
```
📝 Persona: Technical Reviewer
📝 Persona: Editorial Reviewer  
📝 Persona: Content Stylist
[10 specialized perspectives]
```

### Stage 6: Critical Reading (5 Virtual Readers, 3 Cycles)
```
📖 Perspectivas: Curiosidade, Profundidade, Didática, Especialização, Reflexão
🤖 Executando 3 ciclos de leitura crítica...
```

## Performance Notes

- **Stage 1-3**: ~5-10 seconds each (writing model)
- **Stage 4A**: ~15-20 seconds (research model + RAG queries)
- **Stage 4B**: ~10-15 seconds (chapter writing)
- **Stage 5**: ~30-60 seconds (10 personas * ~3-6 seconds each)
- **Stage 6**: ~45-90 seconds (5 readers * 3 cycles)
- **Stage 7-9**: ~5-10 seconds each (editing/finalization/publication)

**Total**: 2-5 minutes depending on API response times

## Troubleshooting

### "Processando com IA..." spinner stays forever

**Cause**: API rate limiting or network issue  
**Solution**: Press Ctrl+C and retry. Check `GOOGLE_API_KEY` environment variable.

### Missing emojis in output

**Cause**: Terminal doesn't support unicode  
**Solution**: Ensure terminal is set to UTF-8: `export LANG=en_US.UTF-8`

### No verbose output

**Cause**: Logger level is too high  
**Check**: Verify `DEBUG_LEVEL` in `src/config.py` is set appropriately

## API Quota Management

Free tier Gemini limits:
- **Rate**: 10 requests/minute
- **Daily**: 1500 requests/day

**Each pipeline run uses ~30-40 API calls** (9 stages + reviews/readers)

For full testing, consider:
1. Running functional tests first (mocked, no quota used)
2. Staggering integration test runs
3. Using paid tier for consistent testing

## Next Steps

To see advanced features, check:
- **Context7 MCP**: Search capability in stage 4A
- **Supabase RAG**: Vector storage in stage 4A  
- **Author Knowledge Base**: RAG Autoral integration in reviews
- **KDP Publication**: Export in stage 9

## Questions?

See `/docs/ARCHITECTURE.md` and `/docs/PRD.md` for detailed specifications.
