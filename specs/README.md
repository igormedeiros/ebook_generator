# 📋 Especificações (specs/) - Ebook Generator 1.0

Esta pasta contém todas as configurações e especificações parametrizáveis para o pipeline de geração de ebooks.

## 📁 Estrutura de Arquivos

```
specs/
├── pipeline.yaml          # Parâmetros dos 9 estágios do pipeline
├── config.yaml            # Strings em português e mensagens centralizadas
├── models.yaml            # Configuração de modelos IA (Gemini)
├── personas.yaml          # 10 personas de revisão + 5 leitores virtuais
├── tools.yaml             # Especificação de todas as tools (30+)
├── README.md              # Este arquivo
└── examples/              # Exemplos de configuração por tipo de ebook
    ├── academic_book.yaml
    ├── tech_guide.yaml
    ├── health_wellness.yaml
    └── business_book.yaml
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

## 📊 Exemplos de Configuração

Pasta `examples/` contém 4 templates pré-configurados:

### `academic_book.yaml`
- Foco: Pesquisa acadêmica e rigor
- Personas: Technical, Editorial, Research Validator
- Leitores: Technical Professional, Domain Specialist, Educator
- Formato: PDF + EPUB
- Word Count: 45.000

### `tech_guide.yaml`
- Foco: Tutorial prático com código
- Personas: Technical, Code Reviewer
- Leitores: Technical Professional, Curious Beginner, Educator
- Formato: EPUB + PDF + DOCX
- Word Count: 25.000

### `health_wellness.yaml`
- Foco: Bem-estar e saúde
- Personas: Editorial, Ethics, Author Stories
- Leitores: Curious Beginner, Reflective Reader
- Includes: Medical disclaimers, HIPAA compliance
- Word Count: 20.000

### `business_book.yaml`
- Foco: Empreendedorismo e negócios
- Personas: Technical, Editorial, Author Positioning
- Leitores: Technical Professional, Reflective Reader
- Includes: Case studies, frameworks, templates
- Word Count: 30.000

## 🚀 Como Usar

### Executar com configuração padrão:
```python
from src.main import run_ebook_pipeline
from specs import load_pipeline_config

config = load_pipeline_config("pipeline.yaml")
result = run_ebook_pipeline(
    topic="Python para Análise",
    audience="Cientistas de dados",
    word_count_target=config['stage_1']['word_count_target']
)
```

### Executar com exemplo pré-configurado:
```python
from src.main import run_ebook_pipeline
from specs import load_example_config

config = load_example_config("tech_guide")
result = run_ebook_pipeline(**config['input'])
```

### Personalizar configuração:
```python
from specs import load_pipeline_config, merge_overrides

base_config = load_pipeline_config("pipeline.yaml")
custom = {
    'stage_4b_chapter_writing': {
        'author_voice_weight': 0.8,
        'example_count': 5
    }
}
final_config = merge_overrides(base_config, custom)
```

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

### Adicionar novo persona:
```yaml
review_personas:
  meu_revisor:
    name: "Meu Revisor"
    expertise_areas: [...]
```

### Adicionar novo exemplo:
```bash
cp specs/examples/tech_guide.yaml specs/examples/meu_tipo_livro.yaml
# Editar conforme necessário
```

## ✅ Validação

Todos os arquivos YAML devem passar por validação:

```python
from specs import validate_config

errors = validate_config("pipeline.yaml")
if errors:
    print(f"Erros de validação: {errors}")
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
