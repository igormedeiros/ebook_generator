# E-book Bibliographer (Skill)

Esta skill é responsável por consolidar e formatar todas as referências bibliográficas utilizadas durante a criação do e-book.

## Como usar

1.  **Varrer Insumos**: A skill deve ler todos os arquivos em `workspace/<slug>/insumos/` e o arquivo `workspace/process/04B-DEEP_RESEARCH.md`.
2.  **Extrair Fontes**: Identificar URLs, IDs de notebooks do NotebookLM, nomes de livros e documentações oficiais mencionadas.
3.  **Formatar**: Organizar as fontes em ordem alfabética e categorizá-las (ex: "Web e Notícias", "Bases de Conhecimento", "Documentação Técnica").
4.  **Gerar Checkpoint**: Salvar o resultado em `workspace/process/07C-BIBLIOGRAPHY.md`.

## Padrões de Qualidade

- **Verificação de Links**: Sempre que possível, validar se as URLs citadas ainda são acessíveis.
- **Citação NotebookLM**: Incluir o Título e o ID do notebook utilizado.
- **Data de Acesso**: Registrar a data em que a pesquisa foi realizada para fontes web.

## Estrutura do Arquivo Final
- Cabeçalho: # Referências Bibliográficas
- Seções por Categoria.
- Nota de Rodapé sobre a Soberania dos Dados.
