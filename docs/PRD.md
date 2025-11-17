# 📘 PRD – Ebook Generator 1.0

**Autor:** Igor Medeiros  
**Data:** Novembro/2025  
**Versão:** 1.0 (Revisada)

---

## 1. Visão Geral do Produto

O **Ebook Generator 1.0** é um sistema editorial automatizado baseado em agentes coordenados via LangChain 1.0 e nos modelos Gemini 2.5 (Flash para escrita e 2.5 padrão para pesquisa). Ele replica o fluxo profissional de uma editora — da concepção ao arquivo final — entregando ebooks coerentes, empáticos, bem estruturados e prontos para publicação na Amazon KDP.

---

## 2. Objetivo do Produto

Construir um pipeline totalmente automatizado capaz de:

- Receber **tema + problema + público-alvo**.
- Consolidar **ideia central** e **promessa de transformação**.
- Gerar **título/subtítulo otimizados** com base em bestsellers.
- Definir **estrutura editorial completa**.
- Executar **pesquisa real** (Google + Amazon + RAG Supabase).
- Escrever capítulos didáticos com exemplos, histórias e exercícios.
- Revisar o material com múltiplas perspectivas humanas simuladas.
- Produzir arquivos finais em **Markdown + DOCX + EPUB**.
- Entregar **metadados KDP** prontos para publicação.

Tudo com mínima intervenção humana, preservando profundidade técnica, empatia narrativa e rigor editorial.

---

## 3. Público-Alvo

- Criadores independentes e infoprodutores.
- Educadores e professores que desejam materializado seu método.
- Desenvolvedores e especialistas que produzem conteúdo técnico.
- Profissionais de saúde que buscam livros educativos.
- Equipes de marketing e conteúdo que precisam escalar publicações.

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
- Interface visual interativa (CLI apenas, por ora).

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
  → Agente Escritor

Camada 3 – Qualidade Editorial
  → Superagente de Revisão (coordena especialistas)
        ├ Revisor Técnico
        ├ Revisor Editorial
        ├ Copidesque
        ├ Agente de Governança
        └ Validador Ético
  → Superagente de Leitura Crítica (coordena 5 leitores virtuais)
        ├ Leitor Iniciante
        ├ Leitor Profissional
        ├ Leitor Acadêmico
        ├ Leitor Pragmático
        └ Leitor Cético
  → Agente de Editoração
  → Agente Capista
  → Agente de Finalização
  → Agente KDP
```

---

## 6. Fluxo Operacional Completo

### 6.1 Etapa 1 — Entrada

O **Superagente Editor-Chefe** recebe tema, problema e público-alvo e gera o **Documento de Especificação do Livro (DEL)** contendo ideia central, promessa, estilo, objetivos e direcionadores de conteúdo.

### 6.2 Etapa 2 — Ideação

O **Agente da Ideia Central** desdobra a transformação prometida, garante aderência ao público e define o tom geral.

### 6.3 Etapa 3 — Título e Subtítulo

1. **Agente Pesquisador** coleta referências via Google e Amazon (best-sellers do tema).  
2. **Agente de Título/Subtítulo** aplica fórmulas observadas, gera variações e seleciona a melhor combinação título/subtítulo.

### 6.4 Etapa 4 — Estrutura

O **Agente Estruturador** cria a arquitetura do livro: capítulos, seções, progressão didática, elementos especiais (cases, exercícios, checklists) e formato Markdown base.

### 6.5 Etapa 5 — Pesquisa Profunda (RAG)

O **Agente Pesquisador** executa para cada tópico:

1. Busca Google contextualizada.
2. Coleta de fontes oficiais/referências Amazon.
3. Registro em Supabase/pgvector com embeddings.
4. Disponibilização do contexto para o Agente Escritor.

### 6.6 Etapa 6 — Escrita

O **Agente Escritor** (Gemini 2.5 Flash) consulta RAG, integra histórias do autor, cria exemplos, exercícios e analogias, redigindo cada capítulo com coesão e empatia.

### 6.7 Etapa 7 — Revisão Especializada

O **Superagente de Revisão** coordena 5 especialistas:

- **Revisor Técnico**: precisão, código e frameworks.
- **Revisor Editorial**: clareza, fluxo e voz.
- **Copidesque**: estilo, padronização e consistência.
- **Governança**: conformidade, LGPD, versões e citações.
- **Ética**: vieses, segurança e disclaimers.

Três iterações sucessivas refinam o texto.

### 6.8 Etapa 8 — Leitura Crítica

O **Superagente de Leitura Crítica** simula cinco leitores com perfis distintos (iniciante, profissional, acadêmico, pragmático e cético). Cada um gera relatório crítico apontando lacunas, ritmo e compreensão. O ciclo roda por três iterações.

### 6.9 Etapa 9 — Editoração

O **Agente de Editoração** aplica padrões visuais: hierarquias de títulos, limites de parágrafo, blocos de código formatados, tabelas e chamadas.

### 6.10 Etapa 10 — Finalização

- **Agente Capista**: cria conceito e arte usando ferramenta de imagem com base no título/subtítulo.
- **Agente Finalizador**: gera sumário navegável, links internos e prepara conversões Markdown → HTML → DOCX/EPUB.

### 6.11 Etapa 11 — Metadados e KDP

O **Agente KDP** produz JSON completo com sinopse, tags, categorias, descrição marketing, créditos e público. Também consolida arquivos finais para submissão.

---

## 7. Agentes e Responsabilidades

Cada agente possui:

- **System prompt dedicado** descrevendo papel, foco e processo.
- **Ferramentas específicas** (Google Search, Supabase RAG, parsing Amazon, conversores, etc.).
- **Critérios de saída** claros (formato, estrutura, limites).

A listagem detalhada de prompts e instruções fica em `specs/agents.yaml` e é referenciada pelo pipeline (`specs/pipeline.yaml`).

---

## 8. Tecnologias

- **LLMs**: Gemini 2.5 Flash (escrita) e Gemini 2.5 (pesquisa/RAG).
- **Orquestração**: LangChain 1.0+ com agentes e tools dedicados.
- **RAG**: Supabase + pgvector para armazenar pesquisas e histórias.
- **Ferramentas principais**: Google Search, parsing Amazon, gerador de imagens, conversor Markdown → DOCX/EPUB.
- **Execução**: Python 3.11+, `uv` para dep/execução, Pandoc para conversões.

---

## 9. Critérios de Qualidade

- Clareza textual e aderência ao público-alvo.
- Progressão didática consistente em todos os capítulos.
- Coerência interna entre promessa, estrutura e entregáveis.
- Exemplos, exercícios e histórias integrados ao conteúdo técnico.
- Código e referências testados ou validados pelo Revisor Técnico.
- Zero vieses prejudiciais e conformidade LGPD/ética.
- Sumário navegável, metadados completos e formatação compatível com a Amazon KDP.

---

## 10. Métricas de Sucesso

- **Tempo de geração**: < 15 min para um ebook completo.
- **Aderência estrutural**: ≥ 99% conforme template editorial.
- **Qualidade revisões**: ≥ 90% de concordância entre especialistas e leitores virtuais.
- **Factualidade**: ≥ 95% graças à pesquisa + validação RAG.
- **Estabilidade de exportação**: 100% dos arquivos DOCX/EPUB gerados sem warnings.

---

Documento oficial atualizado conforme as novas diretrizes do Ebook Generator 1.0.