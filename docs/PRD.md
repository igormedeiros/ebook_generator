# 📘 PRD – Ebook Generator 1.0

**Autor:** Igor Medeiros  
**Data:** Novembro/2025  
**Versão:** 1.0 (Revisada)

---

## 1. Visão Geral do Produto

O **Ebook Generator 1.0** é um sistema editorial automatizado baseado em agentes coordenados via LangChain 1.0 e nos modelos Gemini 2.5 (Flash para escrita e 2.5 padrão para pesquisa). Ele replica o fluxo profissional de uma editora — da concepção ao arquivo final — entregando ebooks coerentes, didáticos, bem estruturados e prontos para publicação na Amazon KDP.

---

## 2. Objetivo do Produto

Construir um pipeline totalmente automatizado capaz de:

- Receber **tema + público-alvo + objetivo instrucional**.
- Consolidar **ideia central** e **promessa de transformação**.
- Gerar **título/subtítulo otimizados** com base em bestsellers.
- Definir **estrutura editorial completa** com progressão didática.
- Executar **pesquisa real** (Google + Amazon + RAG Supabase).
- Escrever capítulos didáticos com exemplos de código, exercícios e explicações claras.
- Revisar o material com múltiplas perspectivas.
- Produzir arquivos finais em **Markdown + DOCX + EPUB**.
- Entregar **metadados KDP** prontos para publicação.

Tudo com mínima intervenção humana, preservando rigor técnico, didática clara e profundidade prática.

---

## 3. Público-Alvo

- Criadores independentes e infoprodutores de conteúdo técnico.
- Educadores e professores que desejam materializar seu método de ensino.
- Desenvolvedores e especialistas que produzem livros técnicos.
- Empresas que escalem conteúdo educativo em tecnologia.
- Consultores que transformam expertise em produtos digitais.

---

## 4. Escopo do Sistema

### 4.1 Inclui

- Pipeline editorial completo (ideação → publicação).
- Sistema multiagentes com funções especializadas.
- RAG via Supabase/pgvector integrando pesquisas externas.
- Conversão de arquivos e preparação de metadados KDP.
- Revisão multi-perspectiva (especialistas e leitores virtuais).
- Geração de capa com ferramenta de imagem.

### 4.2 Não inclui

- Backend FastAPI ou qualquer API pública.
- Docker ou estratégias de deploy.
- Interface visual interativa (CLI apenas).

---

## 5. Arquitetura Geral

Três camadas organizam o sistema:

```
Camada 1 – Orquestração
  → Superagente Editor-Chefe

Camada 2 – Produção Editorial
  → Agente da Ideia Central
  → Agente de Título/Subtítulo
  → Agente Estruturador
  → Agente Pesquisador (Google + RAG + Supabase)
  → Agente Escritor (didático, com exemplos)

Camada 3 – Qualidade Editorial
  → Superagente de Revisão (coordena 5 especialistas)
        ├ Revisor Técnico
        ├ Revisor Editorial
        ├ Copidesque
        ├ Agente de Governança
        └ Validador Ético
  → Superagente de Leitura Crítica (coordena 5 leitores virtuais)
  → Agente de Editoração
  → Agente Capista
  → Agente de Finalização
  → Agente KDP
```

---

## 6. Fluxo Operacional Completo

### 6.1 Etapa 1 — Entrada

O **Superagente Editor-Chefe** recebe tema, objetivo instrucional e público-alvo, gerando o **Book Requirements Document (BRD)** contendo ideia central, promessa de aprendizado, estilo didático e progressão de complexidade.

### 6.2 Etapa 2 — Ideação

O **Agente da Ideia Central** desdobra a transformação prometida, garante aderência didática ao público e define o tom técnico-acessível.

### 6.3 Etapa 3 — Título e Subtítulo

1. **Agente Pesquisador** coleta referências via Google e Amazon (bestsellers do tema).  
2. **Agente de Título/Subtítulo** aplica fórmulas observadas, gera variações e seleciona a melhor combinação com palavras-chave de SEO.

### 6.4 Etapa 4 — Estrutura

O **Agente Estruturador** cria a arquitetura do livro: capítulos, seções com progressão do básico ao avançado, elementos didáticos (exemplos, exercícios, casos) e formato Markdown base.

### 6.5 Etapa 5 — Pesquisa Profunda (RAG)

O **Agente Pesquisador** executa para cada tópico:

1. Busca Google contextualizada.
2. Coleta de fontes oficiais e referências de documentação.
3. Registro em Supabase/pgvector com embeddings.
4. Disponibilização do contexto para o Agente Escritor.

### 6.6 Etapa 6 — Escrita

O **Agente Escritor** (Gemini 2.5 Flash) consulta RAG, cria explicações didáticas com exemplos de código comentados, exercícios práticos e progressão clara, redigindo cada capítulo com clareza e acessibilidade.

### 6.7 Etapa 7 — Revisão Especializada

O **Superagente de Revisão** coordena 5 especialistas com foco em:

- **Revisor Técnico**: precisão, código e boas práticas.
- **Revisor Editorial**: clareza, fluxo didático e voz.
- **Copidesque**: estilo, padronização e consistência.
- **Governança**: conformidade, versões e citações.
- **Ética**: vieses e disclaimers sobre limitações.

Três iterações sucessivas refinam o texto.

### 6.8 Etapa 8 — Leitura Crítica

O **Superagente de Leitura Crítica** simula cinco leitores com perfis distintos. Cada um gera relatório crítico apontando lacunas, ritmo de aprendizado e compreensão. O ciclo roda por três iterações.

### 6.9 Etapa 9 — Editoração

O **Agente de Editoração** aplica padrões visuais: hierarquias de títulos, blocos de código formatados, tabelas, chamadas e boxes didáticos.

### 6.10 Etapa 10 — Finalização

- **Agente Capista**: cria conceito visual baseado no título/subtítulo.
- **Agente Finalizador**: gera sumário navegável, links internos e prepara conversões Markdown → DOCX/EPUB.

### 6.11 Etapa 11 — Metadados e KDP

O **Agente KDP** produz JSON com sinopse, tags, categorias, descrição marketing e público. Consolida arquivos finais para submissão.

---

## 7. Agentes e Responsabilidades

Cada agente possui:

- **System prompt dedicado** descrevendo papel, foco didático e processo.
- **Ferramentas específicas** (Google Search, Supabase RAG, parsing Amazon, etc.).
- **Critérios de saída** claros e validação de qualidade.

---

## 8. Tecnologias

- **LLMs**: Gemini 2.5 Flash (escrita) e Gemini 2.5 (pesquisa/RAG).
- **Orquestração**: LangChain 1.0+ com agentes e tools.
- **RAG**: Supabase + pgvector.
- **Execução**: Python 3.11+, `uv` para gerenciamento, Pandoc para conversões.

---

## 9. Critérios de Qualidade

- Clareza textual com linguagem acessível para iniciantes.
- Progressão didática consistente e bem estruturada.
- Exemplos de código reais, comentados e práticos.
- Exercícios que consolidam aprendizado.
- Referências úteis e links para aprofundamento.
- Zero vieses prejudiciais.
- Sumário navegável e metadados completos KDP.

---

## 10. Métricas de Sucesso

- **Tempo de geração**: < 15 min para um ebook completo.
- **Aderência estrutural**: ≥ 99% conforme template editorial.
- **Qualidade revisões**: ≥ 90% de concordância entre especialistas.
- **Factualidade**: ≥ 95% graças à pesquisa + validação RAG.
- **Estabilidade de exportação**: 100% dos arquivos DOCX/EPUB gerados sem warnings.

---

Documento oficial atualizado para Ebook Generator 1.0 com foco em LangChain para iniciantes.