<!-- instructions/INSTRUCTIONS-WORKFLOW.md -->
## 🚀 Workflow Principal: Criação de Ebook

Este workflow detalha as etapas sequenciais para a criação de um ebook, desde a concepção até a publicação. Cada etapa é projetada para ser iterativa e garantir a qualidade e alinhamento com as especificações.

1.  **Inicialização do Projeto:**
    *   **LEITURA OBRIGATÓRIA**: Primeiro, ler `@instructions/INSTRUCTIONS-ESCRITA.md` para entender os princípios de escrita e montagem do ebook.
    *   **CONSULTA AO CHECKLIST**: Verificar o arquivo `TODO.md` na raiz do projeto conforme definido em `@instructions/INSTRUCTIONS-CHECKLISTS.md`. Se não existir, criar com as tarefas iniciais.
    *   Criação do diretório `ebook/` vazio.
    *   **Cópia de `template/template.md` para `ebook/ebook.md`. ESTA CÓPIA É OBRIGATÓRIA e deve ser feita antes de qualquer edição do conteúdo do ebook.**
    *   **ATENÇÃO: O arquivo `ebook/ebook.md` deve SEMPRE ser inicializado a partir do template. NUNCA criar ou editar este arquivo sem antes ter copiado o template para lá.**

2.  **Definição e Validação do Tema e Público:**
    *   **Solicitar ao usuário a definição das especificações** (Tema, Público-Alvo, Tom de Voz, Propósito, Volume, etc.), conforme as orientações de `@instructions/INSTRUCTIONS-ESPECIFICACOES.md`.
    *   **Gravar os resultados em `@knowledge/RAG-ESPECIFICACOES.md`**, incluindo o volume do ebook (número de palavras - padrão 15.000).
    *   Leitura e análise de `@knowledge/RAG-ESPECIFICACOES.md` para tema e público-alvo.
    *   Pesquisa de mercado e validação da ideia (usando `web_fetch` e `google_web_search` se necessário).
    *   Refinamento do tema e público com base na pesquisa.

3.  **Estruturação do Ebook:**
    *   Geração da estrutura de capítulos e subtópicos com base em `INSTRUCTIONS-CAPITULOS.md` e `RAG-ESPECIFICACOES.md`.
    *   Criação de um sumário detalhado.

4.  **Definição da Persona de Escrita:**
    *   Definir a persona de escrita em `@instructions/INSTRUCTIONS-PERSONA.md` com base nas especificações em `@knowledge/RAG-ESPECIFICACOES.md`.
    *   Gravar as definições da persona em `@knowledge/RAG-PERSONA.md`.

5.  **Geração do Conteúdo (Escrita Iterativa):**
    *   Escrita de cada capítulo, utilizando os módulos importados (RAG-AUTOR.md, RAG-HISTORIAS_AUTOR.0md, etc.) como base de conhecimento.
    *   **Ao encontrar qualquer referência a @instructions/***, a persona definida em `@knowledge/RAG-PERSONA.md` deve ser acionada para gerar o conteúdo correspondente.
    *   Aplicação dos princípios de escrita definidos em `INSTRUCTIONS-ESCRITA.md`.
    *   Revisão contínua e auto-correção.

6.  **Revisão Multi-Persona:**
    *   Após a conclusão do conteúdo, inicia-se o processo de revisão multiperspectiva.
    *   Acionamento do pipeline de revisão (`*revisar`) com as personas definidas em `INSTRUCTIONS-REVISORES.md`.
    *   Cada persona revisora deve ler e analisar o ebook completo de ponta a ponta, aplicando sua lente específica de revisão a todo o conteúdo. O processo segue a sequência recomendada definida em `INSTRUCTIONS-REVISORES.md`, onde cada revisor contribui com sua perspectiva única (técnicas, ética, filosófica, emocional e estética).
    *   Análise e incorporação do feedback dos revisores.

7.  **Formatação para KDP:**
    *   Aplicação das diretrizes de formatação da Amazon KDP, conforme `RAG-GUIA_KDP.md`.
    *   Geração da capa do ebook com base no prompt em `RAG-ESPECIFICACOES.md`.
    *   Criação do arquivo final em formato ePub.

8.  **Avaliação de Volume:**
    *   Utilizar a ferramenta Python `@tools/word_count.py` para contar as palavras do arquivo `.md` gerado.
    *   Comparar o número de palavras com o volume definido em `@knowledge/RAG-ESPECIFICACOES.md`.
    *   Se o número de palavras for inferior ao definido, o agente deve expandir o texto das seções dos capítulos até atingir o volume desejado, seguindo as diretrizes de conteúdo definidas em `@knowledge/RAG-ESPECIFICACOES.md`.

9.  **Finalização e Publicação:**
    *   Revisão final de todos os elementos (aviso legal, dedicatória, sobre o autor, etc.).
    *   Preparação para upload na plataforma KDP.

10. **Geração de Arquivos Finais:**
    *   Utilizar as ferramentas descritas em `@tools/TOOL-EBOOK-GENERATOR.md` para converter o ebook em formatos adequados (ePub, HTML).
    *   Verificar qualidade e formatação dos arquivos gerados.
    *   Testar os arquivos em diferentes leitores para garantir compatibilidade.

---

## 🚦 Ponto de Partida Obrigatório

**A primeira ação em qualquer interação deve ser a leitura do arquivo `@instructions/INSTRUCTIONS-ESCRITA.md` para garantir o alinhamento com o fluxo de trabalho de planejamento e execução de tarefas.**

**Em seguida, deve-se consultar o arquivo `TODO.md` na raiz do projeto conforme definido em `@instructions/INSTRUCTIONS-CHECKLISTS.md`. Se o arquivo não existir, ele deve ser criado com as tarefas iniciais do workflow.**

**Depois, é essencial verificar se o arquivo `ebook/ebook.md` existe e foi corretamente inicializado a partir do `template/template.md`.**

---

## 📂 Estrutura de Arquivos e Fluxo de Trabalho

O projeto utiliza uma estrutura de diretórios dinâmica para organizar cada ebook.

- **`instructions/`**: Contém os modelos de instrução (`INSTRUCTIONS-*.md`). **Este diretório é somente leitura.**

- **`knowledge/`**: Contém a base de conhecimento para o RAG (Retrieval-Augmented Generation), como histórias do autor e visões sobre os temas. **Este diretório é somente leitura e não deve ser editado a menos que explicitamente solicitado.**

- **`ebook/` (Inicial)**: Ao iniciar um novo projeto, um diretório `ebook/` é criado. O arquivo `template/template.md` é copiado para `ebook/ebook.md`, que servirá como o manuscrito inicial. Todo o trabalho inicial é feito aqui. Os diretórios `instructions/` e `knowledge/` são referenciados, não copiados.

- **`ebook-[TÍTULO_SLUG]/` (Final)**: Após a definição do título do livro (Etapa 4 do Pipeline), o diretório `ebook/` é renomeado para `ebook-[TÍTULO_SLUG]/`. O arquivo do manuscrito `ebook/ebook.md` é renomeado para `[TÍTULO_SLUG].md` dentro deste novo diretório. Todas as etapas subsequentes de escrita e revisão ocorrem nesta pasta final.

---

## 🗂️ Módulos Importados

| Tipo                      | Arquivo                                                 |


| 🚀 Workflow Principal     | `@instructions/INSTRUCTIONS-WORKFLOW.md`        |



| 🎯 Especificações         | `@knowledge/RAG-ESPECIFICACOES.md`          |
| 💡 Ideia Central          | `@instructions/INSTRUCTIONS-IDEIACENTRAL.md`            |
| 🛠️ Preferências Técnicas  | `@knowledge/RAG-PREFERENCIAS_AUTOR.md`      |
| 📍 Posicionamento         | `@knowledge/RAG-POSICIONAMENTO.md`                          |
| 🙏 Dedicatória            | `@instructions/INSTRUCTIONS-DEDICATORIA.md`             |
| 💡 Título                 | `@instructions/INSTRUCTIONS-TITULO.md`                  |

| 📚 Fontes e livros       | `@instructions/INSTRUCTIONS-LIVROS_BASE.md`             |
| ⚖️ Aviso Legal           | `@knowledge/RAG-AVISO_LEGAL.md`             |
| 🧠 Filosofia              | `@knowledge/RAG-OPINIOES_VISAO_AUTOR.md`                    |
| 📖 Narrativa pessoal      | `@knowledge/RAG-HISTORIAS_AUTOR.md`                         |
| 🏗️ Estrutura de capítulos | `@instructions/INSTRUCTIONS-CAPITULOS.md`                               |
| 🌐 Histórias da Internet  | `@instructions/INSTRUCTIONS-HISTORIAS-DE-INTERNET.md`   |
| 🧍 Sobre o autor          | `@knowledge/RAG-AUTOR.md`                                   |
| 📝 Exercícios             | `@instructions/INSTRUCTIONS-EXERCICIOS.md`              |
| 📌 Estudos de caso        | `@instructions/INSTRUCTIONS-ESTUDOS_DE_CASO.md`         |
| ✅ Checklists             | `@instructions/INSTRUCTIONS-CHECKLISTS.md`              |
| 🧪 Revisores              | `@instructions/INSTRUCTIONS-REVISORES.md`               |
| 📘 Especificações Amazon  | `@knowledge/RAG-GUIA_KDP.md`                   |
| ✍️ Escrita                | `@instructions/INSTRUCTIONS-ESCRITA.md`                 |
| 📖 Glossário              | `@knowledge/RAG-GLOSSARIO.md`               |
| 🛠️ Geração de Ebook       | `@tools/TOOL-EBOOK-GENERATOR.md`              |
| 🧍 Persona de Escrita      | `@instructions/INSTRUCTIONS-PERSONA.md`       |
| 🧠 RAG da Persona          | `@knowledge/RAG-PERSONA.md`                   |
| 📊 Contador de Palavras    | `@tools/word_count.py`                        |