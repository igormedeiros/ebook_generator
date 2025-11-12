# Arquitetura Técnica – Gerador Automatizado de eBook

**Ebook Generator 1.0 - Especificação Técnica da Arquitetura**

**Versão**: 1.0  
**Última Atualização**: 12 de Novembro de 2025  

---

## 1. Stack e Integrações

### Backend
- **Linguagem**: Python 3.11+
- **Orquestração IA**: LangChain 1.0+
- **Modelos IA**: 
  - Gemini 2.5 Flash (escrita rápida, temperatura 0.7)
  - Gemini 2.5 Pro (pesquisa profunda/RAG, temperatura 0.3)

### Armazenamento e Vetorização
- **Banco de Dados**: Supabase
- **Vetorização**: pgvector extension
- **Retriever**: LangChain Retriever

### Conversão e Exportação
- **Markdown → HTML/DOCX/EPUB**: Pandoc 3.0+
- **Geração de Capa**: Integração API (Banana ou similar)
- **Publicação**: Assistente para KDP (Kindle Direct Publishing)

---

## 2. Componentes Arquiteturais

### 2.1 Input Parser MD
```
Função: Interpretar e validar arquivo .md com especificações
Entrada: Arquivo .md com campos obrigatórios
  - numero_palavras: int
  - estilo_linguagem: str (empático, técnico, informal)
  - nome_autor: str
  - publico_alvo: str (opcional)
  - tom: str (opcional)
  - complexidade: str (opcional)
Saída: Configurações globais validadas
Responsabilidade: Propagar configurações para todo o pipeline
```

### 2.2 Agentes Principais (8)

#### 1. Agent: Ideia Central
- **Responsabilidade**: Gerar essência do livro conforme input/parâmetros
- **Entrada**: Tema, público-alvo, meta de palavras
- **Saída**: Ideia central, problema, promessa de transformação
- **Ferramentas**: Busca de conhecimento base, RAG context

#### 2. Agent: Título/Subtítulo
- **Responsabilidade**: Pesquisar best-sellers e sugerir título vencedor
- **Entrada**: Ideia central, público-alvo
- **Saída**: 3 opções de título + subtítulo otimizadas para Amazon
- **Ferramentas**: Pesquisa de mercado, validação SEO

#### 3. Agent: Estruturador
- **Responsabilidade**: Criar template do livro + capítulos/seções
- **Entrada**: Ideia central, título, meta de palavras
- **Saída**: Índice hierarchical com distribuição de palavras
- **Ferramentas**: Geração de outline, cálculo de palavras

#### 4. Agent: Redator
- **Responsabilidade**: Escrever capítulos com insumos sintéticos
- **Entrada**: Outline, ideia central, estilo especificado
- **Saída**: Capítulos didáticos com exemplos pessoais/autoriais
- **Ferramentas**: 
  - RAG externo (Gemini 2.5 Pro)
  - RAG autoral (histórias e opiniões)
  - Formatação Markdown
  - Validação de qualidade

#### 5. Agent: Revisão Múltipla
- **Responsabilidade**: Simular personas de revisão especializada (8 personas)
- **Personas**:
  - Editorial: Clareza, tom, fluxo
  - Técnica: Qualidade de código, precisão conceitual
  - Empatia: Acessibilidade, conexão emocional
  - Humor/Engajamento: Leveza, interesse
  - Compliance: LGPD, HIPAA, KDP
  - Histórias & Didática: Equilibra narrativas autorais com pedagogia
  - Posicionamento: Valida autoridade e posicionamento de mercado do autor
  - Visão & Opiniões: Revisa coerência com visão e opiniões do autor
- **Entrada**: Capítulos brutos
- **Saída**: Feedback estruturado por persona (8 perspectivas)
- **RAG Integration**:
  - RAG Histórias do Autor (para avaliação de equilíbrio narrativo)
  - RAG Posicionamento (para validação de autoridade)
  - RAG Visão & Opiniões (para coerência filosófica)
- **Loop**: Crítico de revisão baseado em público-alvo, estilo e identidade do autor

#### 6. Agent: Código
- **Responsabilidade**: Validar blocos Python do livro
- **Entrada**: Blocos de código extraídos dos capítulos
- **Saída**: Relatório de validação, sugestões de correção
- **Ferramentas**: Execução de código, linter, formatter

#### 7. Agent: Editor Estético
- **Responsabilidade**: Refinar estilos, headings, links, template Markdown
- **Entrada**: Capítulos revisados
- **Saída**: Documento com formatação padronizada
- **Validações**: Hierarchia de headings, consistência, accessibility

#### 8. Agent: Sumário/Capa
- **Responsabilidade**: Gerar sumário dinâmico e criar capa
- **Entrada**: Capítulos finais, tema, público-alvo
- **Saída**: 
  - Sumário atualizado
  - Capa gerada via API
  - Capa inserida no documento
- **Ferramentas**: Geração de capa, API de design

---

## 3. RAG Pipeline (Arquitetura)

### 3.1 RAG Externo
```
Fluxo: Redator → Gemini 2.5 Pro → Query Supabase → Retriever
- Gemini 2.5 Pro faz pesquisa profunda para cada capítulo
- Resultados vetorizados e armazenados em Supabase
- LangChain Retriever busca top-k documentos relevantes
- Resultados alimentam contexto da escrita
```

### 3.2 RAG Autoral - Author Knowledge Integration (Histórias, Posicionamento, Visão)
```
Fluxo: Input Autoral → Ingestão → Vetorização → Supabase (3 categorias) → Retriever
- Ingestão de 3 tipos de conhecimento autoral:
  1. Histórias Pessoais (narrativas, experiências, memórias do autor)
  2. Posicionamento de Mercado (autoridade, nicho, diferenciação)
  3. Visão & Opiniões (valores, filosofia, worldview do autor)
- Vetorização de cada categoria com metadata de contexto
- Armazenamento em tabelas separadas em Supabase (rag_author_stories, rag_author_positioning, rag_author_vision)
- Retriever integrado em:
  - Redator: Para incorporar narrativas autorais de forma orgânica
  - Autor Stories Reviewer: Para validar equilíbrio narrativo
  - Autor Positioning Reviewer: Para validar clareza de posicionamento
  - Autor Vision Reviewer: Para validar coerência filosófica
- Garantia de rastreabilidade: Cada insumo RAG autoral é marcado no documento final
```

### 3.3 RAG Externo
```
Fluxo: Input Autoral → Ingestão → Vetorização → Supabase → Retriever
- Ingestão de histórias pessoais do autor
- Vetorização de opiniões (especialmente sobre IA em saúde)
- Armazenamento em tabela separada em Supabase
- Retriever integrado no Redator para uso recorrente
- Garantia de rastreabilidade no documento final
```

### 3.4 Configuração Supabase
```sql
-- Tabela: rag_external
CREATE TABLE rag_external (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(1536),
  source VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela: rag_author_stories
CREATE TABLE rag_author_stories (
  id BIGSERIAL PRIMARY KEY,
  story TEXT NOT NULL,
  embedding vector(1536),
  category VARCHAR(100),
  tags TEXT[],
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela: rag_author_positioning
CREATE TABLE rag_author_positioning (
  id BIGSERIAL PRIMARY KEY,
  positioning_statement TEXT NOT NULL,
  embedding vector(1536),
  aspect VARCHAR(100),
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela: rag_author_vision
CREATE TABLE rag_author_vision (
  id BIGSERIAL PRIMARY KEY,
  vision_or_opinion TEXT NOT NULL,
  embedding vector(1536),
  category VARCHAR(100),
  principle VARCHAR(255),
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para busca vetorial
CREATE INDEX ON rag_external USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON rag_author_stories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON rag_author_positioning USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON rag_author_vision USING ivfflat (embedding vector_cosine_ops);
```

---

## 4. Sequência de Execução (Flowchart)

```
InputMD 
  ↓
ParserMD (validação e propagação de config)
  ↓
IdeiaCentral (essência + promessa)
  ↓
TituloSubtitulo (pesquisa + 3 opções)
  ↓
Estruturador (outline + distribuição de palavras)
  ↓
Redator (capítulos com RAG)
  ├→ RAGExterno (Gemini 2.5 Pro)
  ├→ RAGHistoriasAutorais (histórias pessoais)
  ├→ RAGOpinioesAutorais (opiniões do autor)
  └→ Redator (síntese de insumos)
  ↓
RevisaoMultipla (8 personas)
  ├→ Editorial
  ├→ Técnica
  ├→ Empatia
  ├→ Engajamento
  ├→ Compliance
  ├→ Histórias & Didática (RAG Histórias)
  ├→ Posicionamento (RAG Posicionamento)
  └→ Visão & Opiniões (RAG Visão)
  ↓
CodigoAgente (validação de blocos Python)
  ↓
EditorEstetico (formatação Markdown)
  ↓
SumarioCapa (dinâmico + API design)
  ↓
ConversorFinalizador (export formatos)
  ├→ HTML
  ├→ DOCX
  ├→ EPUB
  └→ JSON (metadados)
  ↓
AgentPublicacao (compilação KDP)
  ├→ Metadados
  ├→ Sinopse
  ├→ Ficha catalográfica
  └→ Arquivos finais
  ↓
OUTPUT (eBook pronto para KDP)
```

---

## 5. Papéis dos Modelos Gemini

### Gemini 2.5 Flash (Escrita Rápida)
- **Temperatura**: 0.7 (criatividade balanceada)
- **Uso Primário**:
  - Escrita de capítulos
  - Revisões (todas as 5 personas)
  - Geração de sumário
  - Prompts curtos e rápidos
- **Características**: Rápido, criativo, balanceado

### Gemini 2.5 Pro (Pesquisa Profunda)
- **Temperatura**: 0.3 (foco em precisão)
- **Uso Primário**:
  - Pesquisas externas (RAG externo)
  - Ingestão de histórias/opiniões do autor
  - Vetorização de conteúdo autoral
  - Validação factual
- **Características**: Preciso, profundo, contextual

---

## 6. Fluxo de Tokens e Otimização

### Estratégia de Minimização de Tokens
1. **Caching de Queries**: Resultados de RAG cacheados localmente
2. **Deduplicação**: Mesma query = mesmo resultado armazenado
3. **Resumos**: Uso de resumos ao invés de conteúdo completo
4. **Top-k Reduzido**: top_k=3 ao invés de 10 para RAG
5. **Prompts Otimizados**: Prompts concisos sem informações desnecessárias

### Estimativa de Uso
- **Por Capítulo**: 500-1000 tokens
- **Revisão Multi-Persona**: 300-500 tokens
- **RAG Externo**: 200-400 tokens
- **Pipeline Completo (10 capítulos)**: 10,000-20,000 tokens

---

## 7. Observações Críticas

### Rastreabilidade
- Todo insumo utilizado é rastreável no documento final
- Marcação clara de fonte: externa (RAG), autoral (histórias/opiniões), ou gerada
- Footnotes/citações automáticas para cada insumo RAG

### Personalização Radical
- Garantir que conteúdo do autor se mescle com resultado editorial universal
- Histórias e opiniões do autor aparecem de forma orgânica
- Balance entre voz do autor e qualidade editorial

### Adaptações Futuras
- Estruturas internas permitem adicionar novos tipos de input
- Canal extensível para novos assets (imagens, vídeos, etc.)
- Novos canais de pesquisa integráveis sem refatoração

---

## 8. Dependências de Externos

### APIs Requeridas
- **Google Gemini API**: Para LLMs (Flash + Pro)
- **Supabase API**: Para armazenamento e vetorização
- **Banana API** (ou similar): Para geração de capa IA
- **Pandoc**: Para conversão de formatos (local)

### Configuração de Ambiente
```bash
export GOOGLE_API_KEY="your-key"
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-key"
export BANANA_API_KEY="your-key"  # opcional para capa
```

---

## 9. Segurança e Conformidade

### LGPD (Lei Geral de Proteção de Dados)
- Dados pessoais do autor criptografados
- Conformidade validada em Agent: Compliance
- Política de retenção: 6 meses (customizável)

### HIPAA (Saúde)
- Validação automática de disclaimers médicos
- Alertas para conteúdo sensível em saúde
- Review qualificado para conteúdo médico

### KDP Compliance
- Validação automática de formatos
- Metadata conforme requisitos Amazon
- Teste de publicabilidade antes de export

---

## 10. Próximas Evoluções

### v1.1 (Q1 2025)
- [ ] Loop de revisão completo (3 iterações)
- [ ] Dashboard simples para monitoramento
- [ ] Logging detalhado de execução

### v1.2 (Q2 2025)
- [ ] REST API para execução remota
- [ ] Publicação automática no KDP
- [ ] Analytics de qualidade por capítulo

### v2.0 (Q3 2025)
- [ ] LangGraph para orquestração avançada
- [ ] Web UI completa
- [ ] Batch processing para múltiplos eBooks
- [ ] Multi-idioma

---

## 11. Diagrama de Componentes

```
┌─────────────────────────────────────────────────────┐
│        EBOOK GENERATOR 1.0 - ARQUITETURA             │
└─────────────────────────────────────────────────────┘

INPUT LAYER
├── InputMD Parser
└── Config Validator

AGENT LAYER (8 Agentes)
├── Ideia Central
├── Título/Subtítulo
├── Estruturador
├── Redator
├── Revisão Múltipla (8 personas especializadas)
├── Código
├── Editor Estético
└── Sumário/Capa

RAG LAYER
├── RAG Externo (Gemini 2.5 Pro)
├── RAG Autoral - 3 Conhecimentos:
│   ├── Histórias Pessoais (rag_author_stories)
│   ├── Posicionamento Marketing (rag_author_positioning)
│   └── Visão & Opiniões (rag_author_vision)
├── Supabase Storage (4 tabelas vetorizadas)
└── LangChain Retriever

EXPORT LAYER
├── Conversor HTML
├── Conversor DOCX
├── Conversor EPUB
└── JSON Metadata

PUBLICATION LAYER
└── KDP Assistant

LLM LAYER
├── Gemini 2.5 Flash (escrita)
└── Gemini 2.5 Pro (pesquisa)
```

---

**Documento Versão**: 1.0  
**Última Atualização**: 12 de Novembro de 2025  
**Proprietário**: Igor Medeiros  
**Status**: Ativo

```
USER INPUT (topic, audience, word_count)
    ↓
┌─ ORCHESTRATOR (run_ebook_pipeline)
│
├─→ STAGE 1: IDEATION AGENT
│   └─ Define central idea, problem, audience, promise
│
├─→ STAGE 2: TITLE AGENT
│   └─ Generate 3 Amazon-optimized title options
│
├─→ STAGE 3: STRUCTURE AGENT
│   └─ Create hierarchical outline
│
├─→ STAGE 4: CHAPTER AGENT
│   └─ Write didactic content with RAG
│
├─→ STAGE 5: REVIEW (8 SPECIALIZED PERSONAS)
│   ├─→ TECHNICAL REVIEWER (code quality, versions)
│   ├─→ EDITORIAL REVIEWER (clarity, tone, flow)
│   ├─→ CONTENT STYLIST (formatting, structure)
│   ├─→ GOVERNANCE QA (compliance, metadata)
│   ├─→ ETHICS VALIDATOR (bias, disclaimers)
│   ├─→ AUTHOR STORIES & DIDACTICS (narrative balance, RAG Stories)
│   ├─→ AUTHOR POSITIONING (marketing authority, RAG Positioning)
│   └─→ AUTHOR VISION & OPINIONS (values alignment, RAG Vision)
│       └─ Aggregated feedback dict (8 perspectives)
│
├─→ STAGE 6: EDITING AGENT
│   └─ Final formatting and validation
│
├─→ STAGE 7: FINALIZATION AGENT
│   └─ Cover generation and metadata
│
└─→ STAGE 8: PUBLICATION AGENT
    └─ DOCX, EPUB, PDF, JSON exports

OUTPUT (results dictionary with all stage outputs)
```

---

## 🎯 The 8 Main Pipeline Stages

### 1️⃣ **Stage 1: Ideation Agent**
- **Purpose:** Transform raw input into coherent business idea
- **Responsibility:** Define transformation promise, core problem, target audience
- **Tools:** 
  - `search_knowledge_base()` - Find relevant information
  - `retrieve_rag_context()` - RAG integration point
- **Output:** Central idea framework with:
  - Transformation promise
  - Problem definition
  - Target audience profile
  - Value proposition

### 2️⃣ **Stage 2: Title Agent**
- **Purpose:** Generate market-optimized titles for Amazon visibility
- **Responsibility:** Create 3 title + subtitle combinations optimized for SEO and market appeal
- **Tools:**
  - `generate_amazon_optimized_title()` - Market analysis
  - `validate_title_seo()` - SEO scoring
- **Output:** 3 Amazon-optimized options with:
  - Title + subtitle combinations
  - SEO keyword alignment
  - Market appeal rating

### 3️⃣ **Stage 3: Structure Agent**
- **Purpose:** Create content hierarchy dimensioned to target word count
- **Responsibility:** Generate hierarchical outline with section weights
- **Tools:**
  - `generate_outline()` - Creates structured outline
  - `count_words()` - Validates word counts
- **Output:** Table of contents in Markdown with:
  - Chapter structure
  - Estimated word counts per section
  - Didactic flow

### 4️⃣ **Stage 4: Chapter Writing Agent**
- **Purpose:** Write didactic, high-quality content chapters
- **Responsibility:** Produce engaging technical content with RAG context
- **Tools:**
  - `retrieve_rag_context()` - Knowledge retrieval
  - `format_markdown()` - Markdown formatting
  - `validate_content_quality()` - Quality metrics
- **Output:** Didactic chapters with:
  - Technical accuracy
  - Clear explanations
  - RAG citations
  - Proper formatting

### 5️⃣ **Stage 5: Specialized Review (5 Personas)**
- **Purpose:** Comprehensive multi-perspective quality assurance
- **Responsibility:** Execute 5 specialized reviewers for thorough validation
- **Review Personas:**

#### **Technical Reviewer Agent**
- **Focus:** Code quality, framework versions, technical accuracy
- **Checks:**
  - Python code syntax and best practices
  - LangChain 1.0+ API compatibility
  - AI/ML concept accuracy
  - Example code execution validation
- **Output:** Technical feedback with quality metrics

#### **Editorial Reviewer Agent**
- **Focus:** Writing quality, clarity, flow, audience alignment
- **Checks:**
  - Readability and clarity
  - Tone consistency
  - Paragraph flow and transitions
  - Grammar and spelling accuracy
- **Output:** Editorial suggestions and improvements

#### **Content Stylist Agent**
- **Focus:** Formatting consistency, visual hierarchy, structure
- **Checks:**
  - Heading hierarchy (H1, H2, H3)
  - Code block formatting
  - List consistency
  - Table of contents accuracy
- **Output:** Formatting recommendations

#### **Governance QA Agent**
- **Focus:** Compliance, metadata, security, standards
- **Checks:**
  - Framework version compliance
  - Security and data protection
  - LGPD compliance (Brazilian regulation)
  - Metadata completeness
- **Output:** Compliance validation report

#### **Ethics Validator Agent**
- **Focus:** Bias detection, medical disclaimers, AI ethics principles
- **Checks:**
  - Language bias detection
  - Medical disclaimer requirements
  - AI ethics principles
  - HIPAA/LGPD compliance
- **Output:** Ethics validation and recommendations

#### **Author Stories & Didactics Reviewer Agent** (NEW)
- **Focus:** Balance between author's personal narratives and pedagogical clarity
- **Responsibility:** Ensure author stories enhance (not overshadow) learning objectives
- **Checks:**
  - Story relevance to chapter topic
  - Narrative weight vs. content balance
  - Educational value and didactic flow
  - Avoid excessive personal details or off-topic anecdotes
  - Stories serve as teaching tools or relatable examples
- **RAG Integration:** Consults RAG Author Stories knowledge base
- **Output:** Balance feedback and narrative optimization suggestions

#### **Author Positioning Reviewer Agent** (NEW)
- **Focus:** Author's market positioning and subject matter authority
- **Responsibility:** Validate clear positioning in target industry/theme and expertise prominence
- **Checks:**
  - Author's authority and credibility are evident
  - Positioning in target market/industry is clear
  - Niche expertise and specialization shine through
  - Marketing positioning is authentic and compelling
  - Author's unique perspective/angle is distinctive
- **RAG Integration:** Consults RAG Author Positioning knowledge base
- **Output:** Positioning clarity and authority validation

#### **Author Vision & Opinions Reviewer Agent** (NEW)
- **Focus:** Author's worldview, core values, and thematic opinions
- **Responsibility:** Ensure content aligns with author's philosophy and authentic voice
- **Checks:**
  - Content reflects author's stated values and principles
  - Opinions are authentic and consistent
  - Philosophical stance is clear and coherent
  - Author's vision for impact permeates the work
  - No contradictions with stated worldview
- **RAG Integration:** Consults RAG Author Vision & Opinions knowledge base
- **Output:** Vision consistency and authenticity feedback

- **Output:** Aggregated feedback from 5 perspectives:
  ```python
  {
    "technical": "Code quality feedback...",
    "editorial": "Writing quality feedback...",
    "stylist": "Formatting feedback...",
    "governance": "Compliance feedback...",
    "ethics": "Ethics and bias feedback..."
  }
  ```

### 6️⃣ **Stage 6: Editing Agent**
- **Purpose:** Final formatting validation and consistency check
- **Responsibility:** Ensure document meets publishing standards
- **Tools:**
  - `review_logical_flow()` - Flow validation
  - `validate_markdown_format()` - Format validation
- **Output:** Publication-ready formatted document

### 7️⃣ **Stage 7: Finalization Agent**
- **Purpose:** Generate cover and validate all metadata
- **Responsibility:** Create cover concept and complete metadata
- **Tools:**
  - `generate_cover()` - AI cover design
  - `generate_kdp_metadata()` - Metadata generation
### 8️⃣ **Stage 8: Publication Agent**
- **Purpose:** Export to multiple formats for KDP
- **Responsibility:** Generate publication-ready packages
- **Tools:**
  - `export_to_docx()` - Word format export
  - `export_to_epub()` - EPUB format export
  - `export_to_pdf()` - PDF format export
  - Export to JSON for metadata
- **Output:** Complete KDP package with:
  - DOCX file (for editing)
  - EPUB file (for distribution)
  - PDF file (for preview)
  - JSON metadata

---

## 📁 File Organization

```
src/
├── main.py           # Pipeline orchestration (8 stages)
├── agents.py         # 8 agents + 1 coordinator + 5 specialized reviewers
├── tools.py          # 30+ specialized tools
├── config.py         # Model initialization and config
└── __init__.py       # Package initialization
```

---

## 🚀 Performance Summary

| Component | Time | Notes |
|-----------|------|-------|
| Full Pipeline | 2-5 min | API latency dependent |
| Single Agent | 15-30 sec | Average per stage |
| 5 Review Personas | 60-90 sec | Sequential execution |
| Total Tokens | 5K-10K | Gemini API usage |

---

## 🔐 Security & Compliance

- ✅ LGPD (Brazilian Data Protection) - Validated in Governance QA
- ✅ HIPAA (Healthcare) - Checked in Ethics Validator
- ✅ No credentials in code - Environment-based configuration
- ✅ Type hints and docstrings - Full documentation
- ✅ Error handling - Layered approach across all levels

---

## ✅ Implementation Status

| Component | Status | Details |
|-----------|--------|---------|
| 8 Main Agents | ✅ Complete | All stages implemented |
| 5 Review Personas | ✅ Complete | Specialized expertise agents |
| 30+ Tools | ✅ Complete | Organized by stage |
| LangChain 1.0+ | ✅ Integrated | Using create_agent() pattern |
| Gemini 2.5 Flash | ✅ Configured | Model initialized |
| RAG Integration Points | ✅ Ready | TODO implementations marked |
| Code Standards | ✅ Documented | .github/copilot-instructions.md |
| Documentation | ✅ Complete | README.md, ARCHITECTURE.md |

### 🎯 **Superagente Coordenador**
- **Responsabilidade:** Orquestra todo o pipeline de 8 etapas
- **Ferramentas:** Todas as ferramentas disponíveis
- **Output:** E-book completo publicável

---

## 🛠️ Ferramentas Disponíveis

### Pesquisa e Busca
- `pesquisar()` - Busca informações contextualizadas
- `calcular()` - Expressões matemáticas
- `consultar_rag()` - Banco de dados vetorial

### Criação e Formatação
- `gerar_outline()` - Estrutura de conteúdo
- `gerar_titulo_amazon()` - Títulos otimizados KDP
- `formatar_markdown()` - Formatação padrão
- `gerar_capa_ia()` - Capa visual
- `gerar_metadados_kdp()` - Arquivo JSON metadados

### Validação e Revisão
- `revisar_humor()` - Tone e engajamento
- `revisar_empatia()` - Clareza e acessibilidade
- `revisar_gramatica()` - Ortografia e gramática
- `revisar_coerencia()` - Fluxo lógico
- `revisar_codigo()` - Exemplos técnicos
- `validar_conteudo()` - Qualidade geral

### Exportação
- `exportar_docx()` - Microsoft Word
- `exportar_epub()` - E-book format
- `contar_palavras()` - Word counter final

---

## 📁 Estrutura de Arquivos

```
src/
├── main.py           # Pipeline editorial principal (8 etapas)
├── agents.py         # Definição dos 8 agentes especializados
├── tools.py          # Ferramentas disponíveis (30+ tools)
├── config.py         # Configuração do modelo Gemini 2.5 Flash
└── __pycache__/
```

---

## 🚀 Como Executar

```bash
# Configurar variável de ambiente
export GOOGLE_API_KEY='sua_api_key'

# Executar pipeline
uv run python src/main.py
```

### Customizar Tema e Meta

Editar em `src/main.py`, função `main()`:

```python
tema = "Seu Tema"
publico_alvo = "Seu Público"
meta_palavras = 15000  # ou outro valor
pipeline_ebook(tema, publico_alvo, meta_palavras)
```

---

## 📊 Fluxo do Pipeline

```
INPUT (tema, público, meta)
         ↓
    IDEAÇÃO (Agent 1)
         ↓
    TÍTULO (Agent 2)
         ↓
    ESTRUTURA (Agent 3)
         ↓
    CAPÍTULOS (Agent 4) → RAG
         ↓
    REVISÃO (Agent 5) → 3 loops
         ↓
    EDITORAÇÃO (Agent 6)
         ↓
    FINALIZAÇÃO (Agent 7) → Capa
         ↓
    KDP (Agent 8) → DOCX + EPUB + JSON
         ↓
OUTPUT (E-book pronto para publicação)
```

---

## ✨ Características

- ✅ **Modular:** Cada agente tem responsabilidade única
- ✅ **Escalável:** Fácil adicionar novos agentes/ferramentas
- ✅ **RAG-Ready:** Integrado com banco vetorial (Supabase pgvector)
- ✅ **MCP-Compatible:** Interface para ferramentas externas
- ✅ **KDP-Compliant:** Saída pronta para Amazon Kindle
- ✅ **Multi-language:** Strings em português, código em inglês

---

## 🎯 Próximas Iterações (Roadmap)

- [ ] **v1.1:** Loop de revisão completo (3 iterações)
- [ ] **v1.2:** Integração MCP com ferramentas externas
- [ ] **v2.0:** LangGraph + Interface Web
- [ ] **v2.1:** Publicação automática no KDP

---

**Desenvolvido por:** Igor Medeiros  
**Data:** Novembro de 2025  
**Versão:** 1.0 (MVP)
