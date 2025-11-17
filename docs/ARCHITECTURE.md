# Arquitetura Técnica – Ebook Generator 1.0

**Documento:** Especificação Arquitetural Oficial  
**Versão:** 1.0 (Revisada)  
**Atualização:** Novembro/2025  
**Foco:** LangChain 1.0 para Iniciantes em Desenvolvimento de Aplicações com LLMs

---

## 1. Visão Técnica Geral

O Ebook Generator 1.0 opera como uma **plataforma editorial multiagente**. O Superagente Editor-Chefe coordena agentes especializados em ideação, pesquisa, escrita didática, revisão e publicação, replicando o workflow de uma editora profissional. Toda a execução é dirigida por parâmetros YAML e pelo dual-model Gemini 2.5 (Flash para escrita; 2.5 padrão para pesquisa), garantindo rapidez criativa e rigor factual.

Este sistema foi redesenhado para produzir ebooks técnico-educativos com foco em clareza didática, exemplos práticos de código e progressão do básico ao avançado.

---

## 2. Stack e Integrações

### Backend e Orquestração
- **Linguagem:** Python 3.11+
- **Gerenciador/Runner:** `uv` (instalação, sincronização e execução)
- **Framework:** LangChain 1.0+ (agents + tools + Runnables)
- **CLI/TUI:** Rich + typer (sem FastAPI/Docker)

### Modelos e LLMs
- **Gemini 2.5 Flash** – Escrita criativa e didática, revisão textual, iterações (temp. 0.7)
- **Gemini 2.5** – Pesquisa profunda, RAG e análise factual (temp. 0.3)

### Persistência e RAG
- **Supabase + Postgres** – Base operacional
- **pgvector** – Armazena embeddings (`rag_external` e recursos didáticos)
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
├── pipeline.yaml      # Estágios e agentes da pipeline (11 estágios)
├── agents.yaml        # Agentes independentes (produção + revisão + leitura crítica)
├── personas.yaml      # Perfis de revisores e leitores virtuais
├── tools.yaml         # Definição das 30+ ferramentas
├── models.yaml        # Configuração do dual-model Gemini
├── config.yaml        # Mensagens em português
├── book.yaml          # Gerado após validação (gitignored)
└── README.md          # Documentação
```

**Parâmetros principais para didática:**
- `reading_level`: beginner (para público-alvo iniciante)
- `example_count`: Número de exemplos de código por seção
- `include_exercises`: Ativar exercícios práticos
- `outline_depth`: Profundidade da estrutura hierárquica

### 3.2 Núcleo de Execução (`src/`)

```
src/
├── main.py             # Orquestração dos 11 estágios
├── agents.py           # Factories create_agent() + prompts sistêmicos
├── tools.py            # Implementação @tool (RAG, pesquisa, formatação)
├── config.py           # Carregamento YAML, logging Rich, modelos Gemini
├── input_validator.py  # Validação de input → specs/book.yaml
├── llm_fallback.py     # Estratégia de fallback/resiliência
└── __init__.py         # API pública
```

### 3.3 Validador de Entrada
- Lê `input/book_input.yaml`.
- Checa campos essenciais (tema, público, objetivos).
- Solicita dados faltantes via prompts Rich.
- Gera `specs/book.yaml` com metadata + parâmetros didáticos.

### 3.4 Logging e Saída
- Todo output usa `logging` + Rich (`print_panel`, `print_table`).
- `get_logger()` centraliza formato e níveis.
- `print()` é proibido para manter padrão visual.

---

## 4. Pipeline Multiagente (11 Estágios)

### 4.1 Camada de Orquestração
- **Superagente Editor-Chefe**: Consolida tema/público/objetivo, gera DEL e dispara cada estágio.

### 4.2 Camada de Produção Editorial

1. **Agente da Ideia Central** – Refina a promessa de aprendizado e direcionadores de tom didático.
2. **Agente de Título/Subtítulo** – Pesquisa bestsellers, gera títulos otimizados com SEO.
3. **Agente Estruturador** – Outline com progressão didática, distribuição de palavras e elementos (exemplos, exercícios).
4. **Agente Pesquisador** – Google Search + Context7 + Supabase RAG para cada tópico.
5. **Agente Escritor** – Usa Gemini Flash, consulta RAG, cria explicações didáticas com código comentado.

### 4.3 Camada de Qualidade Editorial

6. **Superagente de Revisão** – Coordena 5 especialistas (técnico, editorial, copidesque, governança, ética). Três iterações.
7. **Superagente de Leitura Crítica** – Simula 5 leitores virtuais em 3 ciclos de feedback.
8. **Agente de Editoração** – Aplica padrões Markdown (ATX, 100 colunas, GFM).
9. **Agente Capista** – Gera visual para capa.
10. **Agente de Finalização** – Sumário navegável, links internos, conversões Pandoc.
11. **Agente KDP** – JSON de metadados + exportação final.

---

## 5. RAG e Pesquisa

### 5.1 Bases Vetoriais Reorganizadas

```sql
CREATE TABLE rag_external (
  id BIGSERIAL PRIMARY KEY,
  source TEXT,
  content TEXT NOT NULL,
  type VARCHAR(50),
  embedding VECTOR(1536),
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Tipos de conteúdo:**
- `documentation`: Documentação oficial (LangChain, LLM APIs)
- `tutorial`: Tutoriais e guias práticos
- `code_example`: Exemplos de código reais
- `best_practice`: Boas práticas e padrões
- `case_study`: Estudos de caso

### 5.2 Fluxo de Pesquisa Didática

1. Estruturador define tópicos com progressão de complexidade.
2. Pesquisador busca recursos documentados e exemplo de código.
3. Escritor consome RAG segmentado, incluindo código nos exemplos.
4. Revisor Técnico valida precisão e clareza.

---

## 6. Agentes, Ferramentas e Prompts

- **agents.py** expõe `create_*_agent()` seguindo LangChain `create_agent(model, tools, system_prompt)`.
- Cada agente possui **System Prompt** com papel didático, foco, processo e formato de saída.
- **Ferramentas** (`tools.py`) usam `@tool`, com docstrings em inglês.
- Agrupamento por estágio permite reuse e testes unitários.

**Exemplo de ferramenta didática:**

```python
@tool
def extract_code_snippet(topic: str, language: str = "python") -> dict:
    """
    Extract a practical, commented code example for a topic.
    Used by the Escritor agent to provide executable examples.
    
    Args:
        topic: The LangChain or Python concept to exemplify
        language: Programming language (default: python)
    
    Returns:
        dict with 'code', 'explanation', 'expected_output'
    """
```

---

## 7. Personas Especialistas e Leitores Virtuais

### 7.1 Revisão Especializada (5 perfis)
- **Técnico**: Precisão, código, boas práticas LangChain.
- **Editorial**: Clareza, progressão didática, voz.
- **Copidesque**: Estilo, padronização.
- **Governança**: Conformidade, versões, citações.
- **Ética**: Vieses, disclaimers sobre limitações de LLMs.

### 7.2 Leitores Virtuais (5 perfis)
- **Curioso Iniciante**: Busca fundamentação clara.
- **Profissional Técnico**: Busca depth e boas práticas.
- **Educador Didático**: Avalia eficácia da pedagogia.
- **Especialista de Domínio**: Valida aplicações práticas.
- **Leitor Reflexivo**: Conecta com relevância maior.

---

## 8. Padrões Operacionais

- **Execução**: `uv run src/main.py`. Nenhum uso direto de `python`.
- **Dependências**: `uv sync` para instalar; `uv add` para novas libs.
- **Logs**: `logger.info|warning|error|debug`, sem `print()`.
- **Internacionalização**: Código em inglês; strings em português via `get_message()`.
- **Conformidade**: Sem FastAPI/Docker; foco em CLI offline.

---

## 9. Dependências Externas

- **Google Gemini API** – Modelos Flash e 2.5.
- **Supabase** – Banco Postgres e vetores.
- **Context7 MCP** – Pesquisa semântica externa.
- **Ferramenta de Imagem** – Geração de capa.
- **Pandoc** – Conversões para DOCX/EPUB/PDF.

---

Este documento reflete a arquitetura técnica redesenhada para Ebook Generator 1.0 com foco em didática e LangChain para iniciantes.
