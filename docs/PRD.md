# 📘 Product Requirements Document – Ebook Generator 1.0

**Autor:** Igor Medeiros  \
**Versão:** 1.1 (Atualizada a partir do código em `src/`)  \
**Data:** Novembro/2025

---

## 1. Visão Geral do Produto

O **Ebook Generator 1.0** é um pipeline editorial automatizado em Python 3.11+ que utiliza LangChain 1.0, modelos Gemini 2.5 (Flash para escrita e Pro para pesquisa) e uma interface rica em terminal para produzir ebooks técnicos prontos para publicação. O sistema parte de um **Book Requirements Document (`specs/brd.yaml`)** com tema, público, tópicos obrigatórios e estilo, gera pesquisas temáticas, conduz pesquisa capítulo a capítulo, armazena tudo em `kb/` e finalmente redige o ebook completo em Markdown (`result/ebook.md`).

---

## 2. Objetivos do Produto

1. **Automatizar o fluxo editorial** da estruturação até a redação final de ebooks técnicos sobre LangChain na saúde clínica.
2. **Garantir rastreabilidade de pesquisa** salvando cada entrega em `kb/` e permitindo reuso em execuções futuras.
3. **Aplicar dois modelos especializados** (Gemini Flash e Gemini Pro) para equilibrar criatividade na escrita e rigor na pesquisa.
4. **Oferecer experiência guiada** via TUI Rich, com confirmações e transparência de cada etapa.
5. **Preparar terreno para RAG/Supabase** armazenando pesquisas localmente e exibindo opção de envio futuro.

---

## 3. Público-Alvo

- Criadores independentes que produzem ebooks técnicos.
- Educadores e equipes de enablement que precisam de material consistente e atualizado.
- Times de produto/IA interessados em documentar soluções baseadas em LangChain.
- Profissionais de saúde digital que desejam guias aplicados a contextos clínicos com compliance.

---

## 4. Escopo do Sistema

### 4.1 Inclui

- Carregamento de requisitos a partir de `specs/brd.yaml` e validações adicionais via `src/input_validator.py`.
- Orquestração completa em `src/main.py` com três fases principais:
  1. **Pesquisa Temática Abrangente** (por tópico obrigatório) salva imediatamente.
  2. **Pesquisa por Capítulo** (Contexto → Problema → Solução → Aplicação → Ética) com registro em `kb/`.
  3. **Geração de Conteúdo** em Markdown por capítulo usando o contexto pesquisado.
- Sistema multiagente (`src/agents.py`) com modelos Gemini e ferramentas definidas em `src/tools.py`.
- UI baseada em Rich (`src/ui.py`) para cabeçalhos, tabelas, barras de progresso e confirmações do usuário.
- Exportação principal para Markdown (`result/ebook.md`) e utilitários de publicação (DOCX/EPUB/PDF/JSON) expostos via tools.

### 4.2 Não inclui

- API pública ou interface web; execução é exclusivamente via CLI/TUI.
- Persistência efetiva em Supabase/pgvector (placeholders documentados nas tools).
- Integração ativa com Context7 MCP ou geração de capa real (funções stub retornam mensagens simuladas).
- Automação de submissão para KDP/Amazon além da geração dos conteúdos.

---

## 5. Requisitos Funcionais

1. **RF-01 – Preparação**: Carregar `specs/brd.yaml`, exibir resumo do livro e pré-visualização dos capítulos antes da execução.
2. **RF-02 – Confirmação**: Solicitar aprovação do usuário via Rich antes de prosseguir.
3. **RF-03 – Pesquisa Temática**: Para cada `required_topic` no BRD, gerar documento de ~3000 palavras, 7+ fontes e salvar imediatamente em `kb/thematic_*.md`.
4. **RF-04 – Pesquisa por Capítulo**: Para cada capítulo sugerido pelo agente escritor, gerar pesquisa mínima de 2000 palavras com 5+ fontes e salvar em `kb/research_*.md`.
5. **RF-05 – Geração de Capítulos**: Usar `writer_agent` com contexto pesquisado para criar capítulos (~word_count_target ÷ n capítulos) e anexá-los ao ebook.
6. **RF-06 – Persistência**: Salvar o ebook consolidado em `result/ebook.md`, criando a pasta caso não exista.
7. **RF-07 – UX Transparente**: Mostrar fases, progresso e resumos (sucesso/erro) usando componentes Rich definidos em `src/ui.py`.
8. **RF-08 – Configurabilidade**: Permitir ajustes em `specs/` (`pipeline.yaml`, `config.yaml`, `models.yaml`, `tools.yaml`, `personas.yaml`) sem alterar código.

---

## 6. Requisitos Não Funcionais

- **RNF-01 – Plataforma**: Python 3.11+ com dependências gerenciadas via `uv` ou `pip` (ver `pyproject.toml`).
- **RNF-02 – Segurança**: Exigir `GOOGLE_API_KEY` em variáveis de ambiente, sem armazenamento em repositório.
- **RNF-03 – Observabilidade**: Toda saída deve usar logging Rich/UI; `print` simples é desencorajado.
- **RNF-04 – Estruturação**: Conteúdo final e pesquisas usam Markdown GFM com headings hierárquicos.
- **RNF-05 – Testabilidade**: Ferramentas ficam isoladas em `src/tools.py` para facilitar testes unitários.

---

## 7. Dependências & Integrações

- **Gemini 2.5 Flash / Pro**: Principais modelos via `langchain-google-genai`.
- **LangChain 1.0**: Criação de agentes, ferramentas e execução de chamadas LLM.
- **Rich**: UI e feedback do pipeline.
- **python-docx / futuro ebooklib/reportlab**: Suporte a exportações adicionais.
- **Supabase / Context7**: Integrações planejadas com métodos stub já definidos nas tools.

---

## 8. Métricas de Sucesso

- Gerar ebooks completos (>10k palavras) sem intervenção manual após confirmação inicial.
- Garantir que cada capítulo possua um arquivo de pesquisa correspondente em `kb/`.
- Permitir reexecução incremental reutilizando pesquisas temáticas existentes, reduzindo tempo em execuções repetidas.
- Manter consistência estilística definida no BRD (tom, abordagem, características) em todos os capítulos.

---

## 9. Roadmap e Próximos Passos

1. **Integrações externas**: ativar Supabase/pgvector, Context7 MCP e armazenamento remoto real para RAG.
2. **Formatos finais adicionais**: completar exportações EPUB/PDF/JSON e automatizar metadados KDP.
3. **Validações ampliadas**: conectar `src/input_validator.py` diretamente ao fluxo principal para preencher BRDs dinamicamente.
4. **Testes automatizados**: cobrir fases do pipeline com mocks de agentes para validar UX e persistência.
5. **Capa e assets visuais**: conectar ferramentas de imagem reais e anexar arquivos gerados ao pacote final.

---

Este PRD reflete o comportamento atual implementado em `src/` e serve de referência única para evolução futura do Ebook Generator 1.0.
