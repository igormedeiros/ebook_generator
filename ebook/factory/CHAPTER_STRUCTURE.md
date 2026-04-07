# Estrutura Padrão de Capítulo (CHAPTER_STRUCTURE.md)

Este documento define a anatomia interna obrigatória para cada um dos 10 capítulos técnicos dos e-books gerados.

## 1. Componentes do Capítulo
Cada capítulo deve seguir esta sequência lógica:

1. **Título do Capítulo:** Claro, direto e focado no benefício/aprendizado.
2. **Introdução e Contexto:** O "porquê" deste tópico. Qual problema estamos resolvendo?
3. **Desenvolvimento Técnico (A Tríade de Código):**
    - **Contexto:** Desenho do problema técnico/clínico.
    - **Código:** Bloco limpo, com Type Hints e comentários em inglês.
    - **Dissecação:** Explicação linha a linha focada em "cicatrizes de produção" (o que pode dar errado).
4. **Storytelling/Vivência:** Breve inserção de experiências reais baseadas no `STORIES.md`.
5. **Resumo do Aprendizado:** O que o leitor deve ter fixado.

## 2. Seção de Exercícios (Obrigatória)
Todo capítulo **DEVE** terminar com as seguintes atividades para fixação:

### 2.1. Desafios de Múltipla Escolha
Devem ser apresentados **5 exercícios**, cada um com exatamente **4 opções (A, B, C, D)**.

**Exemplo de Formatação:**
1. [Pergunta do exercício]?
   A) Opção 1
   B) Opção 2
   C) Opção 3
   D) Opção 4

### 2.2. Gabarito dos Desafios
As respostas corretas devem vir logo após o último exercício de múltipla escolha, de forma concisa.

**Exemplo de Formatação:**
> **Gabarito:** 1-A, 2-C, 3-B, 4-D, 5-A.

### 2.3. Exercício de Aplicação Prática (Sem Resolução)
Um exercício aberto, focado em "mão na massa" ou reflexão crítica, contendo apenas o enunciado. O objetivo é que o leitor tente implementar por conta própria sem consultar uma resposta pronta.

**Exemplo de Formatação:**
> **Desafio Extra:** Implemente uma função que valide o fluxo de autenticação descrito na seção 3.2, garantindo que o log de erro não exponha o token do usuário.

## 3. Diretrizes de Escrita
- **Tom de Voz:** Mantenha a Tríade Editorial (2ª pessoa para engajar, "Nós" para o código, 1ª pessoa para histórias).
- **Complexidade Progressiva:** Garanta que os exercícios reflitam o conteúdo abordado no capítulo.
