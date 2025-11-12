<!-- instructions/INSTRUCTIONS-CRIAR-PROJETO.md -->
# ⚙️ INSTRUCTIONS-CRIAR-PROJETO.md

## Objetivo
Este arquivo define o passo a passo para a criação de um novo projeto de ebook, desde a configuração inicial do diretório até a definição do título.

## Processo

1.  **Criação do Diretório de Trabalho `ebook/`:**
    -   Ao iniciar um novo projeto, o primeiro passo é criar um diretório vazio chamado `ebook/`. Este diretório conterá o manuscrito e os artefatos gerados para o novo ebook.
    -   **Importante:** Os diretórios `@instructions/` e `@knowledge/` servem como a base de conhecimento e as diretrizes para a criação do ebook. Eles devem ser **referenciados** durante o processo, mas **não devem ser copiados** para dentro da pasta `ebook/`.

2.  **Criação do Manuscrito Inicial:**
    -   Copie o arquivo `template/template.md` para dentro do diretório `ebook/` e renomeie-o para `ebook.md`. Este arquivo servirá como o manuscrito inicial do livro.

3.  **Definição da Ideia Central:**
    -   Utilize o arquivo `ebook/INSTRUCTIONS-IDEIACENTRAL.md` para capturar e refinar a ideia principal do livro. O resultado deste processo deve ser armazenado no arquivo `ebook/INSTRUCTIONS-ESPECIFICACOES.md`.

4.  **Definição do Título:**
    -   Com a ideia central definida, o próximo passo é gerar o título do ebook. Utilize o arquivo `ebook/INSTRUCTIONS-TITULO.md` para gerar 10 opções de títulos, selecionar 3 finalistas e, por fim, escolher o título vencedor.

5.  **Renomeação do Diretório e do Manuscrito:**
    -   Após a definição do título, o diretório `ebook/` deve ser renomeado para `ebook-[TÍTULO_SLUG]/`, onde `[TÍTULO_SLUG]` é a versão "slugificada" do título do livro (letras minúsculas, sem espaços ou caracteres especiais, com palavras separadas por hífen).
    -   O arquivo do manuscrito, `ebook.md`, também deve ser renomeado para `[TÍTULO_SLUG].md` e movido para dentro do novo diretório `ebook-[TÍTULO_SLUG]/`.
