<!-- instructions/INSTRUCTIONS-CAPA.md -->
# instructions/INSTRUCTIONS-CAPA.md
# 🎨 CAPA.md
> Diretrizes para a Geração do Prompt da Capa do eBook

## 🎯 Objetivo
Definir um prompt detalhado e eficaz para a geração da capa do eBook utilizando o modelo de imagem do Gemini (Nano Banana), garantindo que a arte da capa esteja alinhada com o título, o tema e a visão do autor.

## ⚙️ Processo
A geração do prompt da capa ocorre **após** a definição do título final do eBook (conforme o processo em `@INSTRUCTIONS-TITULO.md`).

### Variáveis de Entrada
- **Título Final do eBook**: O título vencedor definido em `@INSTRUCTIONS-TITULO.md`.
- **Subtítulo Final do eBook**: O subtítulo definido em `@INSTRUCTIONS-TITULO.md`.
- **Tema Principal**: O tema definido em `@INSTRUCTIONS-ESPECIFICACOES.md`.
- **Palavras-chave**: As palavras-chave definidas em `@INSTRUCTIONS-TITULO.md`.
- **Visão do Autor**: A visão definida em `@INSTRUCTIONS-OPINIOES_VISAO_AUTOR.md`.

### Fórmula do Prompt (Estilo Nano Banana)

O prompt deve ser uma combinação dos seguintes elementos, em inglês, para melhor performance do modelo:

1.  **Estilo e Formato**: `photorealistic, book cover, professional, high quality, 4k`
2.  **Conceito Principal**: Uma representação visual do **título** e **tema**.
3.  **Elementos Simbólicos**: Ícones ou imagens que representem as **palavras-chave** (ex: cérebro para IA, corrente para LangChain, código para Python).
4.  **Paleta de Cores**: Cores que reflitam a **visão do autor** (ex: tons de azul e verde para saúde e tecnologia, tons quentes para humanismo).
5.  **Composição**: Descrição de como os elementos devem ser arranjados.
6.  **Texto**: O **título** e o **nome do autor** devem ser incluídos na imagem.

### Exemplo de Prompt

```
photorealistic book cover, professional, high quality, 4k. [DESCREVA O CONCEITO VISUAL PRINCIPAL DO SEU LIVRO]. O título "[TÍTULO FINAL DO EBOOK]" deve ser exibido de forma proeminente no topo, e o nome do autor "[NOME DO AUTOR]" na parte inferior. A paleta de cores é [PALETA DE CORES].
```

## ✅ Ação Final
Após a geração do prompt, ele deve ser inserido no arquivo `@ESPECIFICACOES.md`, na seção `Especificação da Capa`.