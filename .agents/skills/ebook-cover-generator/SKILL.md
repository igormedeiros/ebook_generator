---
name: ebook-cover-generator
description: Gera capas de e-books no padrão "O'Reilly Mitológico" usando nanana (Gemini Imagen). Substitui animais por Deuses Gregos, mantém o autor Igor Medeiros e utiliza um template visual fixo em templates/covers/.
---

# E-book Cover Generator (O'Reilly Mythological Edition)

Este skill automatiza a criação de capas seguindo a icônica estética da O'Reilly (estilo woodcut/gravura, fundo branco, molduras clássicas), mas utiliza Deuses da Mitologia Grega relacionados ao tema do livro em vez de animais.

## Regras de Design Inegociáveis

1.  **Autor**: O nome "Igor Medeiros" deve constar obrigatoriamente em todas as capas.
2.  **Estética**: Estilo "O'Reilly" (traços de gravura em preto e branco ou sépia, alto contraste, fundo limpo).
3.  **Elemento Central**: Um Deus ou figura da Mitologia Grega que simbolize o tema (ex: Hermes para comunicação/bots, Atena para estratégia/IA, Hefesto para automação/ferramentas).
4.  **Template**: Utilizar sempre o modelo base localizado em `templates/covers/master_template.png` (ou similar) se disponível para composição.

## Fluxo de Trabalho

1.  **Mapeamento Divino**: Analisar o tema do e-book e sugerir o Deus Grego correspondente.
    - *Exemplo*: Para "O Agente Invisível" -> **Hermes** (O mensageiro, deus dos viajantes e da comunicação rápida).
2.  **Geração de Prompt**:
    ```text
    "Uma gravura em estilo woodcut de [DEUS GREGO], traços detalhados em preto e branco, fundo branco minimalista, estilo capa de livro técnico clássico O'Reilly."
    ```
3.  **Execução do Nanana**:
    ```bash
    nanana "[PROMPT]" --title "[TITULO_DO_LIVRO]" --author "Igor Medeiros" -o workspace/[NOME_DO_EBOOK]/assets/cover.png
    ```
4.  **Injeção no E-book**: O skill deve garantir que a imagem gerada seja a primeira página do arquivo HTML/EPUB.

## Localização de Recursos

- **Template de Referência**: `templates/covers/`
- **Output de Imagem**: `workspace/[NOME_DO_EBOOK]/assets/cover.png`

## Segurança

- A `GEMINI_API_KEY` deve ser lida do arquivo `.env` na raiz do projeto.
