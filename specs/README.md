# 📋 Especificações (specs/) - Ebook Generator 1.0

Esta pasta contém todas as configurações e especificações parametrizáveis para o pipeline de geração de ebooks.

## 📁 Estrutura de Arquivos

```
specs/
├── pipeline.yaml          # Parâmetros dos 9 estágios (padrões + constraints)
├── config.yaml            # Strings em português e mensagens centralizadas
├── models.yaml            # Configuração de modelos Gemini
├── personas.yaml          # 10 personas de revisão + 5 leitores virtuais
├── tools.yaml             # Especificação de todas as tools (30+)
├── book.yaml              # GERADO: Merged config from input validation
└── README.md              # Este arquivo

input/
└── book_input.yaml        # USUÁRIO: Preenche com especificações do livro
```

## 🎯 Arquivos de Configuração

### 1. `pipeline.yaml`
Define os 9 estágios do pipeline com todos os parâmetros configuráveis:

- **Stage 1 - Ideação**: topic, audience, word_count_target
- **Stage 2 - Títulos**: title_count, seo_keywords, amazon_compliance
- **Stage 3 - Estrutura**: outline_depth, chapter_count, didactic_progression
- **Stage 4A - Pesquisa Profunda**: query_types, research_depth, source_limit
- **Stage 4B - Escrita**: chapter_template, rag_context_limit, author_voice_weight
- **Stage 5 - Revisão**: active_personas, feedback_aggregation, threshold_score
- **Stage 6 - Leitura Crítica**: iteration_cycles, active_virtual_readers, refinement_threshold
- **Stage 7 - Edição**: markdown_standard, line_length_max, heading_style
- **Stage 8 - Finalização**: cover_style, include_glossary, metadata_template
- **Stage 9 - Publicação**: export_formats, kdp_compliance_strict

### 2. `config.yaml`
Centraliza todas as strings em português:

- **messages**: 100+ mensagens do pipeline (estágios, agentes, operações)
- **labels**: Labels para UI e relatórios
- **prompts**: System prompts base para agents
- **tables**: Títulos de tabelas de saída
- **Icons**: Ícones para output formatado com Rich

### 3. `models.yaml`
Configuração dos modelos de IA:

- **write_model**: Gemini 2.5 Flash (0.7 temperatura)
- **research_model**: Gemini 2.5 Pro (0.3 temperatura)
- **embeddings**: Modelo para vetorização
- **API Configuration**: Credenciais e URLs
- **RAG Settings**: Configuração pgvector e Supabase
- **Token Limits**: Limites por estágio e pipeline

### 4. `personas.yaml`
Especificação completa de personas e leitores:

- **10 Review Personas**: Technical, Editorial, Stylist, Governance, Ethics, Author Stories, Author Positioning, Author Vision, Code Reviewer, Research Validator
- **5 Virtual Readers**: Curious Beginner, Technical Professional, Didactic Educator, Domain Specialist, Reflective Reader
- **Feedback Aggregation**: Estratégias de consolidação
- **Iteration Settings**: Configuração de ciclos de iteração

### 5. `tools.yaml`
Inventário completo de ferramentas:

- **tool_categories**: 9 categorias por estágio
- **tools**: 30+ tools com parâmetros detalhados
- **defaults**: Configurações padrão (rag_top_k, timeout, retries)

## 🎯 Fluxo de Entrada

### 1. Usuário preenche `input/book_input.yaml`

```yaml
topic: "Python para Análise de Dados"
target_audience: "Cientistas de dados iniciantes"
word_count_target: 25000
transformation_promise: "Dominar análise de dados com Python"
reading_level: "intermediary"

# stage_overrides: (opcional)
#   stage_5_review:
#     threshold_score: 0.85
```

### 2. Input Validator processa

```
1. Carrega input/book_input.yaml
2. Valida campos obrigatórios
3. Valida tipos e ranges
4. Prompta usuário se algum campo falta/inválido
5. Gera specs/book.yaml (merged config)
6. Retorna validado para pipeline
```

### 3. Pipeline executa com `specs/book.yaml`

```python
from src.input_validator import validate_book_input
from src.main import run_ebook_pipeline

config = validate_book_input()  # Carrega e valida
result = run_ebook_pipeline(**config['input'])
```

## 📋 Campos de Entrada (input/book_input.yaml)

## 📝 Logging e Output

A partir da integração com Rich:

```python
from src.logger import get_logger

logger = get_logger("ebook_generator")
logger.info("Iniciando pipeline")  # ✓ Com formatação
logger.error("Erro na execução")   # ✗ Com formatação
logger.debug("Detalhes técnicos")  # Em modo debug
```

Output com Rich:

```
📝 Estágio 1: Gerando ideia central...
✓ Ideia central gerada com sucesso

📚 Estágio 2: Gerando títulos otimizados...
[████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 35%
✓ Títulos gerados com sucesso
```

## 🔧 Personalização

Cada arquivo YAML pode ser estendido:

### Adicionar novo parâmetro ao pipeline:
```yaml
stage_4b_chapter_writing:
  novo_parametro:
    type: string
    required: false
    default: "valor"
    description: "Descrição"
```

### Customizar input do livro:
```yaml
# input/book_input.yaml
topic: "Seu tópico"
target_audience: "Seu público"
word_count_target: 30000
stage_overrides:
  stage_5_review:
    threshold_score: 0.9  # Mais rigoroso
```

## ✅ Validação

Input Validator valida `input/book_input.yaml` automaticamente:

```python
from src.input_validator import validate_book_input

try:
    config = validate_book_input()
    print(f"✓ Configuração válida")
except ValueError as e:
    print(f"✗ Erro: {e}")
    # Usuário será prompts interativamente para corrigir
```

## 📖 Documentação Relacionada

- [PRD.md](../docs/PRD.md) - Requisitos de produto
- [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - Arquitetura técnica
- [copilot-instructions.md](../.github/copilot-instructions.md) - Padrões de código

## 🔐 Segurança

- Credenciais: Use variáveis de ambiente (não hardcode)
- Dados Sensíveis: LGPD e HIPAA compliance validados
- Versões: Manter atualizado com releases de APIs

## 📈 Evolução

Os arquivos de specs devem ser versionados com o projeto:

```bash
git tag v1.0-specs  # Marcar versão junto com release
```

---

**Última atualização**: 12 de novembro, 2025  
**Versão**: 1.0  
**Status**: Production Ready
