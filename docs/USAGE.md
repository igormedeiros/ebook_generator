# Ebook Generator 1.0 - Guia de Uso

## Visão Geral

O Ebook Generator é um pipeline de 9 estágios que transforma um tópico em um ebook pronto para publicação. O sistema carrega especificações do arquivo `input/book_input.yaml` e prompts interativamente por dados faltantes.

## Formas de Uso

### 1. Modo Interativo (Recomendado)

O modo mais simples - o sistema carrega `input/book_input.yaml` e prompta qualquer campo faltante:

```bash
uv run python -m src
```

**Fluxo:**
1. Sistema verifica `input/book_input.yaml`
2. Se campos obrigatórios estiverem vazios, prompta no terminal
3. Executa os 9 estágios do pipeline
4. Gera output em `specs/book.yaml`

### 2. Modo Pré-Configurado

Preencha `input/book_input.yaml` com suas especificações:

```yaml
topic: "Seu Tópico"
target_audience: "Seu Público-alvo"
word_count_target: 15000
transformation_promise: "Transformação para o leitor"
reading_level: "intermediate"
```

Depois execute:

```bash
uv run python -m src
```

### 3. Uso Programático

Integre o pipeline em seu código Python:

```python
from src.input_validator import InputValidator
from src.main import run_ebook_pipeline

# Validar e carregar especificações
validator = InputValidator()
config = validator.validate()

# Extrair dados
metadata = config.get("metadata", {})
parameters = config.get("parameters", {})

# Executar pipeline
results = run_ebook_pipeline(
    topic=metadata["topic"],
    target_audience=metadata["target_audience"],
    word_count_target=parameters["word_count_target"],
    transformation_promise=parameters.get("transformation_promise", ""),
    reading_level=parameters.get("reading_level", "intermediate"),
    run_all_stages=True
)
```

## Arquivos de Especificação

### `input/book_input.yaml` (Principal)

Seu arquivo de configuração. Campos:

**Obrigatórios:**
- `topic`: O tema do ebook
- `target_audience`: Para quem é o ebook
- `word_count_target`: Meta de palavras (5000-100000)

**Opcionais:**
- `transformation_promise`: O que o leitor vai aprender/conseguir
- `reading_level`: beginner, intermediate, advanced (padrão: intermediate)
- `author_name`: Seu nome
- `author_bio`: Suas credenciais
- `publication_year`: Ano de publicação
- `stage_overrides`: Customizações por estágio

### `input/book_input.example-*.yaml`

Exemplos pré-configurados para diferentes tipos de ebooks:

- `book_input.example-empty.yaml` - Template vazio para começar do zero
- `book_input.example-langchain.yaml` - Exemplo completo (LangChain)
- `book_input.yaml` - Configuração padrão atual

**Para usar um exemplo:**

```bash
cp input/book_input.example-langchain.yaml input/book_input.yaml
uv run python -m src
```

## Campos Interativos

Se qualquer campo obrigatório estiver vazio em `input/book_input.yaml`, o sistema prompta:

```
[cyan]Qual é o tópico principal do ebook?[/cyan] Python para Análise
[cyan]Qual é o público-alvo?[/cyan] Data Scientists iniciantes
[cyan]Qual é a contagem de palavras alvo?[/cyan] 15000
```

## Output do Pipeline

Após execução bem-sucedida, o sistema gera:

1. **`specs/book.yaml`** - Configuração consolidada do ebook (metadata + parameters + stages)
2. **`results/stage_1_ideation.json`** - Saída do estágio 1 (ideia, problema, promessa)
3. **`results/stage_2_title.json`** - 3 título opções otimizadas
4. **`results/stage_3_structure.json`** - Índice hierárquico
5. **`results/stage_4a_deep_research.json`** - Pesquisa profunda + vetorização
6. **`results/stage_4b_chapter_writing.json`** - Conteúdo dos capítulos
7. **`results/stage_5_review.json`** - Feedback de 10 personas especializadas
8. **`results/stage_6_critical_reading.json`** - Iteração crítica (3 ciclos)
9. **`results/stage_7_editing.json`** - Edição final
10. **`results/stage_8_finalization.json`** - Capa + metadados
11. **`results/stage_9_publication.json`** - Exportações (DOCX, EPUB, PDF, JSON)

## Variáveis de Ambiente

Configure sua chave de API do Google:

```bash
export GOOGLE_API_KEY="sua-chave-aqui"
```

Ou adicione ao `.env`:

```
GOOGLE_API_KEY=sua-chave-aqui
```

## Troubleshooting

### "Campo obrigatório não pode estar vazio"

Preencha o campo em `input/book_input.yaml` ou responda no prompt interativo.

### "Erro ao processar YAML"

Verifique a sintaxe de `input/book_input.yaml`. Certifique-se que:
- Strings com espaços estão entre aspas
- Indentação está correta (2 espaços)
- Sem tabs

### Pipeline não executa

Verifique:
- `export GOOGLE_API_KEY="..."`
- `uv sync` executado
- Todos os campos obrigatórios preenchidos

## Configuração Avançada

### Stage Overrides

Para customizar comportamento de estágios específicos:

```yaml
stage_overrides:
  stage_1_ideation:
    reading_level: "beginner"
  stage_2_title:
    title_count: 5
  stage_4b_chapter_writing:
    author_voice_weight: 0.8
    example_count: 4
```

### Modelo de Temperatura

Por padrão:
- **Escrita/Criação**: Gemini 2.5 Flash (temperatura 0.7)
- **Pesquisa/RAG**: Gemini 2.5 Pro (temperatura 0.3)

Para modificar, edite `specs/models.yaml` e recarregue.

## Próximos Passos

1. Crie seu `input/book_input.yaml`
2. Execute `uv run python -m src`
3. Acompanhe o pipeline no terminal (output colorido em português)
4. Verifique os resultados em `results/`
