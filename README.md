# 📚 Ebook Generator 1.0

Pipeline editorial multiagente em Python + LangChain que gera ebooks técnicos sobre LangChain aplicado à saúde clínica. O sistema lê um **Book Requirements Document (`specs/brd.yaml`)**, executa pesquisas temáticas e por capítulo com Gemini 2.5 Pro, redige capítulos completos com Gemini 2.5 Flash e entrega o material final em Markdown (`result/ebook.md`). Toda a experiência é guiada via Rich, com confirmações, tabelas e resumos visuais.

> Documentação complementar: [docs/PRD.md](docs/PRD.md) · [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## ✨ Principais capacidades

- **Fluxo em 3 fases** (`src/main.py`): pesquisa temática abrangente → pesquisa por capítulo → geração de conteúdo final.
- **Rastreabilidade total**: cada pesquisa é salva imediatamente em `kb/` (tanto por tópico quanto por capítulo) e reaproveitada em execuções futuras.
- **Configuração declarativa**: `specs/` concentra BRD, pipeline, agentes, tools, modelos, personas e mensagens em YAML.
- **UI rica**: `src/ui.py` oferece headers, tabelas, barras de progresso, prompts e resumos com Rich.
- **Multiagentes Gemini**: `src/agents.py` combina Gemini 2.5 Flash (escrita) e Gemini 2.5 Pro (research) com o inventário de tools em `src/tools.py`.
- **Exportações auxiliares**: ferramentas para DOCX/EPUB/PDF/JSON já existem (stubs) e podem ser orquestradas em automações futuras.

---

## 🗂️ Estrutura do repositório

```
├── docs/                 # PRD + Arquitetura atualizados a partir de src/
├── kb/                   # Pesquisas salvas (criado em tempo de execução)
├── result/               # Saída final em Markdown
├── specs/                # Configurações YAML (brd, pipeline, agents, tools, models, personas)
├── src/                  # Código-fonte (main, agents, tools, ui, config, input_validator)
├── templates/, template/ # Recursos auxiliares
├── tests/                # Testes automatizados (pytest)
├── pyproject.toml        # Dependências e metadados
└── README.md             # Este arquivo
```

---

## ⚙️ Pré-requisitos

- Python **3.11+**
- Conta Google com acesso ao **Gemini 2.5 Flash/Pro**
- `GOOGLE_API_KEY` definido no ambiente (`.env` suportado)
- macOS/Linux/WSL com acesso a terminal colorido (Rich)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/igormedeiros/ebook-generator.git
cd ebook-generator

# 2. Instale dependências (escolha uma opção)
uv sync              # recomendado
# ou
pip install -e .

# 3. Configure credenciais
export GOOGLE_API_KEY="sua-chave"
```

---

## 🧾 Preparando o BRD

1. Edite `specs/brd.yaml` para definir nome, descrição, público-alvo, `required_topics`, tom e características de escrita.
2. Ajuste parâmetros avançados em `specs/pipeline.yaml`, `specs/models.yaml`, `specs/tools.yaml` ou `specs/personas.yaml` conforme necessário.
3. Opcionalmente, rode `src/input_validator.py` para garantir que `specs/book.yaml` esteja completo antes da execução principal.

> Dica: mantenha pesquisas antigas em `kb/`. Na próxima execução o programa perguntará se deseja reutilizá-las ou gerar tudo do zero.

---

## ▶️ Executando o pipeline

```bash
uv run python -m src.main
# ou
python -m src.main
```

Durante a execução:

1. O sistema gera estrutura de capítulos e mostra prévia para aprovação.
2. Pesquisas temáticas são criadas (ou reutilizadas) e salvas imediatamente em `kb/thematic_*.md`.
3. Cada capítulo recebe pesquisa dedicada (`kb/research_*.md`).
4. Os capítulos finais são escritos em Markdown com base no research consolidado.
5. O ebook final é salvo em `result/ebook.md`, acompanhado de um resumo na TUI.

---

## 🔧 Tools e agentes

- `src/tools.py` agrupa mais de 30 ferramentas organizadas por estágio (ideação, títulos, estrutura, pesquisa, escrita, revisão, edição e publicação). Diversas funções já expõem TODOs para integrações reais com Supabase, Context7, ebooklib etc.
- `src/agents.py` registra `writer_agent`, `research_agent` e `thematic_research_agent` com prompts completos, garantindo consistência com o PRD.
- `src/config.py` carrega YAMLs e expõe `get_model()`, `get_research_model()` e helpers para mensagens, permitindo ajustes sem alterar código.

---

## 📄 Documentação complementar

- **Produto e requisitos**: [docs/PRD.md](docs/PRD.md)
- **Arquitetura técnica**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Specs avançadas**: veja arquivos em `specs/` (BRD, pipeline, agentes, tools, modelos, personas, prompts)

---

## ✅ Próximos passos sugeridos

- Conectar Supabase/pgvector nas funções `search_knowledge_base`, `retrieve_rag_context` e `store_in_rag_external`.
- Integrar Context7 MCP ao fluxo de pesquisa para enriquecer fontes externas.
- Ativar exportações DOCX/EPUB/PDF/JSON direto do pipeline principal.
- Automatizar validação de input (`SpecValidator`) antes de carregar o BRD.
- Criar testes de regressão para cada fase usando mocks de agentes.

Sinta-se à vontade para contribuir abrindo issues ou pull requests!
