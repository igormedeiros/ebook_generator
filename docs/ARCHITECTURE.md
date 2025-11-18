# 🏗️ Arquitetura Técnica – Ebook Generator 1.0

**Versão:** 1.1 (alinhada ao estado atual de `src/`)  \
**Atualização:** Novembro/2025  \
**Stack principal:** Python 3.11 · LangChain 1.0 · Gemini 2.5 Flash/Pro · Rich

---

## 1. Visão Técnica

O projeto implementa uma **pipeline editorial multiagente** que lê um BRD em YAML, dispara agentes especializados (pesquisa temática, pesquisa por capítulo e escrita) e salva cada entrega em disco. O fluxo completo está em `src/main.py` e é dirigido por configurações declarativas em `specs/`. A arquitetura privilegia transparência (UI Rich), rastreabilidade (arquivos em `kb/` e `result/`) e fácil evolução para integrações externas como Supabase ou Context7.

---

## 2. Componentes Principais

| Componente | Local | Responsabilidade |
|------------|-------|------------------|
| **Config Loader** | `src/config.py` | Carrega `specs/*.yaml`, inicializa console Rich, expõe logger, provê helpers para mensagens, agentes e modelos. |
| **Input Validator** | `src/input_validator.py` | Valida `specs/book.yaml` (ou merge futuro de `input/book_input.yaml`), solicita campos obrigatórios e garante ranges/formatos. |
| **UI Layer** | `src/ui.py` | Centraliza painéis, tabelas, barras de progresso e prompts Rich usados em toda a execução. |
| **Agents** | `src/agents.py` | Cria `writer_agent`, `research_agent` e `thematic_research_agent` com LangChain `create_agent`, modelos Gemini e tools adequadas. |
| **Tools** | `src/tools.py` | Define funções `@tool` para ideação, títulos, outlines, pesquisa (incluindo stubs Supabase/Context7), escrita, revisão e exportação. |
| **Orquestrador** | `src/main.py` | Carrega BRD, gera estrutura, conduz pesquisas, escreve capítulos, salva arquivos e controla UX. |
| **Supabase/Docs Assets** | `kb/`, `result/`, `docs/` | Armazenam pesquisas, saídas finais e documentação estratégica (PRD/Architecture). |

---

## 3. Fluxo de Dados

1. **Entrada**: `specs/brd.yaml` descreve projeto (nome, descrição, público, tópicos, estilo, parâmetros).
2. **Estrutura**: `generate_chapter_structure()` chama `writer_agent` para montar capítulos (`name`, `purpose`, `elements`).
3. **Pesquisa Temática**:
   - `check_existing_thematic_research()` detecta arquivos pré-existentes em `kb/`.
   - `generate_thematic_research()` usa `thematic_research_agent` para cada `required_topic` e salva imediatamente com `save_thematic_research_immediately()`.
4. **Pesquisa por Capítulo**:
   - `generate_chapter_research()` usa `research_agent` e grava `kb/research_<cap>.md` via `save_research_to_kb()`.
5. **Geração de Capítulos**:
   - `build_chapter_queries_with_research()` combina estrutura + research + estilo.
   - `writer_agent` gera Markdown final, armazenado em `ebook['chapters']`.
6. **Persistência**:
   - `save_ebook()` compila título, descrição e capítulos em `result/ebook.md`.
   - UI resume progresso e resultados usando `print_*` helpers.

O diretório `kb/` passa a ser o RAG local — arquivos podem ser reaproveitados em execuções futuras e migrar para Supabase quando as funções stub forem conectadas.

---

## 4. Design dos Agentes

- **thematic_research_agent** (`gemini-2.5-pro` + `get_research_tools()`): produz dossiês de 3000+ palavras com glossário, tabelas, exemplos e diretrizes de compliance.
- **research_agent** (`gemini-2.5-pro` + `get_research_tools()`): cria pesquisas focadas em capítulos com estrutura Contexto→Problema→Solução→Aplicação→Ética e referências numeradas.
- **writer_agent** (`gemini-2.5-flash` + `get_all_tools()`): redige capítulos seguindo tom, abordagem e características definidos no BRD.

Os prompts de sistema residem diretamente em `src/agents.py` para garantir alinhamento com os requisitos atuais. Tools especializadas (busca, validação, exportação) são registradas via funções `get_*_tools()` para facilitar testes e reuso.

---

## 5. Camadas de Interface e Experiência

- **Rich Console**: Painéis para cabeçalhos, tabelas de capítulos, prompts de confirmação e resumos de conclusão.
- **Barras de Progresso**: `create_progress_bar()` e logs incrementalmente informam andamento das pesquisas e geração.
- **Mensagens Centralizadas**: `config.yaml` fornece textos em português, permitindo localizar mensagens e reutilizá-las em futuras interfaces.

---

## 6. Persistência e Arquivos

```
kb/
├── thematic_<topic>.md   # Pesquisas temáticas (salvas imediatamente)
├── research_<chapter>.md # Pesquisas por capítulo (Contexto→Aplicação)
result/
└── ebook.md              # Conteúdo final em Markdown
specs/
├── brd.yaml              # Documento mestre usado pelo pipeline
├── pipeline.yaml         # Parametrização dos estágios
├── agents|tools|models   # Configurações declarativas
```

As tools de exportação (`export_to_docx`, `export_to_epub`, `export_to_pdf`, `export_to_json`) criam arquivos adicionais quando acionadas manualmente ou por automações futuras.

---

## 7. Considerações Futuras

- **Supabase/pgvector**: `store_in_rag_external()` e `search_knowledge_base()` possuem TODOs prontos para conectar credenciais e persistir embeddings.
- **Context7 MCP**: `query_context7_mcp()` já expõe assinatura e mensagens de retorno para instrumentação futura.
- **Input Dinâmico**: `SpecValidator` pode ser integrado ao CLI para montar `specs/book.yaml` antes de carregar o BRD.
- **Testes Automatizados**: A separação entre agentes, tools e UI viabiliza mocks e testes unitários/integração com pytest.

Esta arquitetura descreve exatamente o que está implementado hoje, servindo como base para as evoluções descritas no PRD.
