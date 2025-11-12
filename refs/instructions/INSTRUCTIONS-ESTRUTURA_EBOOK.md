<!-- instructions/INSTRUCTIONS-ESTRUTURA_EBOOK.md -->
# instructions/INSTRUCTIONS-ESTRUTURA_EBOOK.md
# 📖 ESTRUTURA_EBOOK.md
> Define a sequência e a organização padrão de todos os eBooks gerados por este framework, com base nas diretrizes do autor.

Este documento é a referência-mestra para a montagem do arquivo final do eBook, garantindo que todas as seções apareçam na ordem correta e com a formatação adequada.

---

## 🏗️ Estrutura Completa do eBook (Ordem de Montagem)

### Parte 1: Seções Iniciais (Front Matter)

1.  **Capa**: (Artefato externo para KDP, não incluído no manuscrito).
2.  **Folha de Rosto**:
    - Título do Livro
    - Subtítulo
    - Nome do Autor: [NOME DO AUTOR]
3.  **Aviso Legal**:
    - Conteúdo de `@INSTRUCTIONS-AVISO_LEGAL.md`.
4.  **Página de Copyright**:
    - Conteúdo de `@INSTRUCTIONS-COPYRIGHT.md`.
5.  **Dedicatória**:
    - Conteúdo de `@INSTRUCTIONS-DEDICATORIA.md`.
6.  **Agradecimentos**:
    - Seção para agradecer nomes específicos, conforme solicitado.
7.  **Prefácio**:
    - Uma introdução mais pessoal e filosófica, conectando o tema ao propósito do autor.
8.  **Sumário (Índice)**:
    - Lista detalhada de capítulos e seções principais com links.

### Parte 2: Corpo Principal do Livro

8.  **Introdução**:
    - Apresenta o tema do livro, sua relevância, o que o leitor vai aprender, para quem se destina e como aproveitá-lo ao máximo.
9.  **Capítulos Técnicos**:
    - O conteúdo principal, gerado conforme `@INSTRUCTIONS-CAPITULOS.md`.
    - Cada capítulo deve seguir a estrutura detalhada na próxima seção.

### Parte 3: Seções Finais (Back Matter)

10. **Conclusão**:
    - Recapitula os principais aprendizados do livro.
    - Oferece uma visão para o futuro e sugere próximos passos para o leitor.
11. **Glossário de Termos**:
    - Definições dos termos técnicos mais importantes usados no livro.
12. **Apêndice**:
    - (Opcional) Seção com conteúdo extra, como guias de instalação, dicas e truques.
13. **Download do Código Fonte**:
    - Link para o repositório GitHub: `[LINK PARA O REPOSITÓRIO DO CÓDIGO FONTE]`.
14. **Referências Bibliográficas**:
    - Lista de livros, artigos e recursos online citados.
15. **Sobre o Autor**:
    - Biografia completa do autor, vinda de `@INSTRUCTIONS-AUTOR.md`.
16. **Chamada para Ação (Call to Action)**:
    - Convite para o leitor deixar uma avaliação na Amazon.
    - Links para contato e mais informações: `[WEBSITE DO AUTOR]`.

---

## 🏛️ Estrutura Interna de um Capítulo

Cada capítulo técnico deve ser autocontido e seguir rigorosamente esta estrutura interna:

1.  **Título do Capítulo**
2.  **Objetivos de Aprendizado**:
    - Lista clara do que o leitor será capaz de fazer ao final do capítulo.
3.  **Conteúdo Principal**:
    - Explicações técnicas detalhadas e passo a passo.
    - **Exemplos de Código**: Comentados, seguindo PEP 8, com nome do arquivo no comentário (`# capitulo_XX/nome_exemplo.py`) e instruções de execução.
    - **Storytelling e Filosofia**: Conexões com histórias pessoais (`@HISTORIAS_AUTOR.md`), curiosidades e a filosofia do autor para tornar o conteúdo mais envolvente.
    - **Recursos Visuais**: Tabelas e descrições de diagramas para ilustrar conceitos.
    - **Notas Marginais**: Dicas rápidas ou alertas sobre erros comuns.
4.  **Estudo de Caso**:
    - Um cenário prático que aplica os conceitos do capítulo.
5.  **Resumo do Capítulo**:
    - Principais pontos abordados em formato de lista (*bullet points*).
6.  **Checklist Prático**:
    - Passos acionáveis para o leitor aplicar o que aprendeu.
7.  **Exercícios de Fixação**:
    - Cinco perguntas de múltipla escolha com quatro opções cada.
    - Respostas comentadas ao final da seção para reforçar o aprendizado.

---

## 🔄 Fluxo de Montagem

O agente orquestrador final é responsável por coletar o conteúdo de todos os arquivos `.md` e montá-los nesta ordem exata para gerar o manuscrito final.