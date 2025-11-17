# Arquitetura Técnica – Ebook Generator 1.0

**Documento:** Especificação Arquitetural Oficial  
**Versão:** 1.0 (Revisada)  
**Atualização:** Novembro/2025  

## Documentos Relacionados

- **[PRD.md](./PRD.md)** – Diretrizes de produto, escopo e métricas.
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** – (este arquivo) visão técnica completa.
- **[.github/copilot-instructions.md](../.github/copilot-instructions.md)** – Padrões de engenharia e governança.

---

## 1. Visão Técnica Geral

O Ebook Generator 1.0 opera como uma **plataforma editorial multiagente**. O Superagente Editor-Chefe coordena agentes especializados em ideação, pesquisa, escrita, revisão e publicação, replicando o workflow de uma editora profissional. Toda a execução é dirigida por parâmetros YAML e pelo dual-model Gemini 2.5 (Flash para escrita; 2.5 padrão para pesquisa), garantindo rapidez criativa e rigor factual.

---

## 2. Stack e Integrações

### Backend e Orquestração
- **Linguagem:** Python 3.11+
- **Gerenciador/Runner:** `uv` (instalação, sincronização e execução)
- **Framework:** LangChain 1.0+ (agents + tools + Runnables)
- **CLI/TUI:** Rich + typer (sem FastAPI/Docker)

### Modelos e LLMs
- **Gemini 2.5 Flash** – Escrita criativa, revisão textual, iterações (temp. 0.7)
- **Gemini 2.5** – Pesquisa profunda, RAG e análise factual (temp. 0.3)

### Persistência e RAG
- **Supabase + Postgres** – Base operacional
- **pgvector** – Armazena embeddings (`rag_author_*`, `rag_external`)
- **Retriever LangChain** – Consulta dos vetores para os agentes

### Conversão e Publicação
- **Pandoc 3.0+** – Markdown → HTML/DOCX/EPUB
- **Ferramenta de imagem (Banana/NanoBanana)** – Geração de capa
- **Saída KDP** – JSON com metadados, DOCX/EPUB finais

---

## 3. Componentes Arquiteturais

### 3.1 Configuração Parametrizada (`specs/`)

Todos os parâmetros ficam fora do código:

```
specs/
├── pipeline.yaml      # Estágios e agentes do pipeline editoral
├── agents.yaml        # 25 agentes independentes (principais + revisores + leitores)
├── personas.yaml      # Perfis detalhados dos revisores e leitores
├── tools.yaml         # Definição das 30+ ferramentas
├── models.yaml        # Configuração do dual-model Gemini
├── config.yaml        # Mensagens em português para a TUI/logs
├── book.yaml          # Gerado após validação de entrada (gitignored)
└── README.md          # Documentação das especificações
```

**Princípios-chave**:
- Agentes são declarados em `agents.yaml` e reutilizados por múltiplos estágios.
- `pipeline.yaml` apenas referencia IDs de agentes e parâmetros (ideação → publicação).
- Strings em português ficam centralizadas em `config.yaml`.
- `book.yaml` combina input do usuário com defaults validados.

### 3.2 Núcleo de Execução (`src/`)

```
src/
├── main.py             # Orquestração dos 11 passos editoriais
├── agents.py           # Factories create_agent() + prompts sistêmicos
├── tools.py            # Implementação @tool (RAG, pesquisa, formatação)
├── config.py           # Carregamento YAML, logging Rich, modelos Gemini
├── input_validator.py  # Validação de input/book_input.yaml → specs/book.yaml
├── llm_fallback.py     # Estratégia de fallback/resiliência de modelos
└── __init__.py         # API pública do pacote
```

### 3.3 Validador de Entrada
- Lê `input/book_input.yaml`.
- Checa campos essenciais (tema, público, word count, promessa).
- Solicita dados faltantes via prompts interativos Rich.
- Gera `specs/book.yaml` com metadata + parâmetros prontos para a pipeline.

### 3.4 Logging e Saída
- Todo output usa `logging` + Rich (`print_panel`, `print_table`).
- `get_logger()` centraliza formato, níveis e contexto.
- `print()` é proibido para manter padrão visual e rastreabilidade.

---

## 4. Pipeline Multiagente

### 4.1 Camada de Orquestração
- **Superagente Editor-Chefe**: Consolida tema/problema/público, gera Documento de Especificação do Livro (DEL) e dispara cada estágio.

### 4.2 Camada de Produção Editorial
1. **Agente da Ideia Central** – Refinamento da promessa e direcionadores de tom.
2. **Agente de Título/Subtítulo** – Baseado em pesquisa Amazon/Google dos best-sellers.
3. **Agente Estruturador** – Outline completo, distribuição de palavras e elementos didáticos.
4. **Agente Pesquisador** – Google Search + Context7 + Supabase (armazenamento vetorial).
5. **Agente Escritor** – Usa Gemini Flash, consulta RAG e aplica voz do autor.

### 4.3 Camada de Qualidade Editorial
6. **Superagente de Revisão** – Coordena 5 especialistas: Técnico, Editorial, Copidesque, Governança e Ética. Executa três iterações obrigatórias.
7. **Superagente de Leitura Crítica** – Emula 5 leitores virtuais (iniciante, profissional, acadêmico, pragmático, cético) em três rodadas com foco diferente (clareza, precisão, engajamento).
8. **Agente de Editoração** – Aplica padrões Markdown (ATX, 100 colunas, GFM) e organiza blocos de código, tabelas e chamadas.
9. **Agente Capista** – Gera briefing visual e solicita arte à tool de imagem.
10. **Agente de Finalização** – Monta sumário navegável, links internos e prepara conversões Pandoc.
11. **Agente KDP** – Exporta arquivos (DOCX/EPUB/Markdown) e monta JSON de metadados, tags e descrições de marketing.

---

## 5. RAG e Pesquisa

### 5.1 Bases Vetoriais
- **`rag_author_stories`** – Histórias e narrativas pessoais.
- **`rag_author_positioning`** – Diferenciais e autoridade do autor.
- **`rag_author_vision`** – Valores, ética e visão estratégica.
- **`rag_external`** – Pesquisas coletadas pelo Agente Pesquisador (Google, papers, Amazon, guias).

### 5.2 Fluxo de Pesquisa
1. Agente Estruturador define capítulos/seções.
2. Agente Pesquisador cria consultas (tipos: research, best_practices, case_studies, expert_perspectives).
3. Resultados são normalizados, vectorizados (modelo `text-embedding-3-small`) e enviados para Supabase.
4. Agente Escritor consome RAG segmentado por capítulo, respeitando `rag_context_limit`.
5. Revisores Técnico e de Referências validam credibilidade (`credibility_threshold`).

### 5.3 Esquema Supabase Simplificado

```sql
CREATE TABLE rag_external (
  id BIGSERIAL PRIMARY KEY,
  chapter_id VARCHAR(64),
  topic TEXT,
  source TEXT,
  content TEXT NOT NULL,
  embedding VECTOR(1536),
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 6. Agentes, Ferramentas e Prompts

- **agents.py** expõe `create_*_agent()` seguindo o padrão LangChain `create_agent(model, tools, system_prompt)`.
- Cada agente possui **System Prompt** com papel, foco, processo e formato de saída (vide PRD).
- **Ferramentas** (`tools.py`) usam `@tool`, com docstrings em inglês e strings de interface em português (quando expostas ao usuário).
- Agrupamento de ferramentas por estágio (ideação, título, estrutura, pesquisa, escrita, revisão, finalização) permite reuse e testes unitários segmentados.

---

## 7. Personas Especialistas e Leitores Virtuais

### 7.1 Revisão Especializada (5 principais nesta versão)
1. **Revisor Técnico** – Analisa código, frameworks e precisão factual.
2. **Revisor Editorial** – Avalia clareza narrativa e adequação ao público.
3. **Copidesque** – Padroniza estilo, gramática e consistência terminológica.
4. **Governança** – Garante conformidade legal, LGPD, versões e citações.
5. **Ética** – Monitora vieses, segurança e necessidade de disclaimers.

*(Os demais perfis herdados do PRD continuam definidos em `personas.yaml` para expansão futura.)*

### 7.2 Leitores Virtuais (5)
- **Curioso Iniciante**, **Profissional Técnico**, **Educador Didático**, **Especialista de Domínio**, **Leitor Reflexivo** – cada um gera relatórios focados em clareza, profundidade, didática, aplicação prática e impacto emocional.

---

## 8. Padrões Operacionais

- **Execução**: `uv run src/main.py` (ou módulos específicos). Nenhum uso direto de `python`.
- **Dependências**: `uv sync` para instalar; `uv add` para novas libs.
- **Logs**: `logger.info|warning|error|debug`, sem `print()`.
- **Internacionalização**: Código e docstrings em inglês; strings exibidas em português via `get_message()`.
- **Conformidade**: Sem FastAPI/Docker; foco em CLI offline.

---

## 9. Dependências Externas

- **Google Gemini API** – Modelos Flash e 2.5 (pesquisa, escrita, embeddings quando necessário).
- **Supabase** – Banco Postgres, autenticação e vetores.
- **Context7 MCP** – Pesquisa semântica externa.
- **Ferramenta de Imagem** – Geração de capa a partir de prompt estruturado.
- **Pandoc** – Conversões para DOCX/EPUB/PDF.

---

Este documento reflete a arquitetura técnica alinhada ao PRD revisado, servindo como blueprint direto para implementação e auditorias futuras.